"""
===================================================================================
CONSOLIDAÇÃO ORACLE - B2C_COE
===================================================================================
Script otimizado para execução automática via Agendador de Tarefas do Windows.

Otimizações aplicadas:
  - Todo processamento acontece DENTRO do Oracle (sem FOR em Python)
  - Logging em arquivo para monitoramento pós-execução
  - Lock file para evitar execução duplicada pelo Task Scheduler
  - Retry automático com reconexão em caso de falha
  - Drop/Recreate de índices para carga rápida
  - NOLOGGING + APPEND para máxima performance de INSERT
  - Ping de conexão para detectar quedas antes de operar
  - Exit codes para o Task Scheduler interpretar sucesso/falha

Uso:
  python consolidacao_oracle.py
  python consolidacao_oracle.py --metodo incremental
  python consolidacao_oracle.py --metodo direto
===================================================================================
"""

import os
import sys
import oracledb
from datetime import datetime
import time
import logging
import argparse

# ========================== CONFIGURAÇÃO ORACLE ==========================
CLIENT_DIR = r"C:\oracle\instantclient_23_8"
if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(CLIENT_DIR)
oracledb.init_oracle_client(lib_dir=CLIENT_DIR)

ORACLE_HOST = "vipscancrs015.gvt.net.br"
ORACLE_PORT = "1521"
ORACLE_SERVICE = "IPTBM"
ORACLE_USER = "cicadmin"
ORACLE_PASS = "An4lyt1c$"
ORACLE_DSN = f"{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

# ======================== CONFIGURAÇÃO DE TABELAS ========================
ORACLE_TABLE_NAME = "B2C_COE_CONSOLIDADO"
TABELAS_ORIGEM = [
    "B2C_COE_HIST_M1",
    "B2C_COE_HIST_M2",
    "B2C_COE_HIST_M3",
    "B2C_COE_HIST_M4",
    "B2C_COE_HIST_M5",
    "B2C_COE_MES_ATUAL",
]

# ======================== CONFIGURAÇÃO DE EXECUÇÃO ========================
# "auto" = tenta direto, fallback incremental  | "direto" | "incremental"
METODO_CONSOLIDACAO = "auto"

# Número máximo de tentativas em caso de falha de conexão/timeout
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 30

# Índices para Power BI (serão dropados antes da carga e recriados depois)
INDICES = [
    ("IDX_CONSOLIDADO_DT_CRIACAO", "DT_CRIACAO"),
    ("IDX_CONSOLIDADO_STATUS",     "STATUS_REASON"),
    ("IDX_CONSOLIDADO_REGIONAL",   "REGIONAL, NCLUSTER"),
    ("IDX_CONSOLIDADO_TIPO",       "TIPO_RECLAMACAO"),
]

# ========================= CONFIGURAÇÃO DE LOG ===========================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
LOCK_FILE = os.path.join(SCRIPT_DIR, ".consolidacao.lock")

# Colunas da tabela consolidada
COLUNAS = [
    "COD_TT", "DT_CRIACAO", "DT_DISPONIBILIDADE", "DT_FECHAMENTO",
    "DATA_EXECUCAO", "BDFLOW", "TABULADOR", "TRANSF_CRM", "INTEGRA",
    "TIPO_RECLAMACAO", "ABERTO", "NOM_GRUPOIRT_BRUTO",
    "NOM_DESCREGRA_IRT_BRUTO", "STATUS_REASON", "NOTDONEREASON",
    "CANCELAMENTO", "NCLUSTER", "CERT_REGIONAIS", "BACKLOG_URA",
    "INTEGRA_RETESTE", "MASSIVA", "AURA", "WHATSAPP_RPA",
    "TIPO_TRATAMENTO", "REPETIDO_15", "REPETIU_7",
    "DAT_INICIOEXEC_HIST", "REGIONAL", "TABELA_ORIGEM",
]


# ==========================================================================
#  LOGGING
# ==========================================================================
def configurar_logging():
    """Configura logging duplo: tela + arquivo (para Task Scheduler)"""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(
        LOG_DIR,
        f"consolidacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler de arquivo
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Handler de console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger = logging.getLogger("consolidacao")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger, log_file


# ==========================================================================
#  LOCK FILE (evita execução duplicada pelo Task Scheduler)
# ==========================================================================
def adquirir_lock(log):
    """Cria lock file para evitar execução simultânea"""
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                info = f.read().strip()
            log.error(f"Execução já em andamento! Lock: {info}")
            log.error(f"Se travou, delete: {LOCK_FILE}")
        except Exception:
            log.error("Execução já em andamento (lock file presente)")
        return False

    try:
        with open(LOCK_FILE, "w") as f:
            f.write(f"PID={os.getpid()} | Inicio={datetime.now().isoformat()}")
        return True
    except Exception as e:
        log.error(f"Erro ao criar lock file: {e}")
        return False


def liberar_lock(log):
    """Remove lock file"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except Exception as e:
        log.warning(f"Erro ao remover lock file: {e}")


# ==========================================================================
#  CONEXÃO ORACLE
# ==========================================================================
def conectar_oracle(log, tentativa=1):
    """Conecta ao Oracle com configurações de performance e timeout"""
    try:
        log.info(f"Conectando ao Oracle ({tentativa}/{MAX_RETRIES})...")
        conn = oracledb.connect(
            user=ORACLE_USER,
            password=ORACLE_PASS,
            dsn=ORACLE_DSN,
            tcp_connect_timeout=60,
        )
        conn.call_timeout = 0  # Sem timeout nas chamadas (queries longas)

        cursor = conn.cursor()
        _exec_safe(cursor, "ALTER SESSION SET DDL_LOCK_TIMEOUT = 600", log)
        _exec_safe(cursor, "ALTER SESSION SET OPTIMIZER_MODE = ALL_ROWS", log)
        _exec_safe(cursor, "ALTER SESSION SET SORT_AREA_SIZE = 104857600", log)
        _exec_safe(cursor, "ALTER SESSION SET HASH_AREA_SIZE = 104857600", log)
        cursor.close()

        log.info("Conectado ao Oracle com sucesso")
        return conn
    except Exception as e:
        log.error(f"Erro ao conectar: {e}")
        if tentativa < MAX_RETRIES:
            log.info(f"Aguardando {RETRY_DELAY_SECONDS}s para nova tentativa...")
            time.sleep(RETRY_DELAY_SECONDS)
            return conectar_oracle(log, tentativa + 1)
        raise


def verificar_conexao(conn, log):
    """Verifica se a conexão está viva; reconecta se necessário"""
    try:
        conn.ping()
        return conn
    except Exception:
        log.warning("Conexão perdida. Reconectando...")
        try:
            conn.close()
        except Exception:
            pass
        return conectar_oracle(log)


def _exec_safe(cursor, sql, log):
    """Executa SQL ignorando erros de permissão"""
    try:
        cursor.execute(sql)
    except oracledb.DatabaseError as e:
        log.debug(f"Ignorando erro em '{sql[:60]}': {e}")


# ==========================================================================
#  ESTRUTURA DA TABELA
# ==========================================================================
def criar_tabela_consolidada(conn, log):
    """Cria a tabela consolidada se não existir"""
    ddl = f"""
    CREATE TABLE {ORACLE_TABLE_NAME} (
        COD_TT                  VARCHAR2(15) PRIMARY KEY,
        DT_CRIACAO              DATE,
        DT_DISPONIBILIDADE      DATE,
        DT_FECHAMENTO           DATE,
        DATA_EXECUCAO           DATE,
        BDFLOW                  NUMBER(22),
        TABULADOR               NUMBER(22),
        TRANSF_CRM              NUMBER(22),
        INTEGRA                 NUMBER(22),
        TIPO_RECLAMACAO         VARCHAR2(200),
        ABERTO                  VARCHAR2(4),
        NOM_GRUPOIRT_BRUTO      VARCHAR2(25),
        NOM_DESCREGRA_IRT_BRUTO VARCHAR2(100),
        STATUS_REASON           VARCHAR2(255),
        NOTDONEREASON           VARCHAR2(255),
        CANCELAMENTO            NUMBER(22),
        NCLUSTER                VARCHAR2(100),
        CERT_REGIONAIS          NUMBER(22),
        BACKLOG_URA             NUMBER(22),
        INTEGRA_RETESTE         NUMBER(22),
        MASSIVA                 NUMBER(22),
        AURA                    NUMBER(22),
        WHATSAPP_RPA            NUMBER(22),
        TIPO_TRATAMENTO         VARCHAR2(20),
        REPETIDO_15             NUMBER(22),
        REPETIU_7               NUMBER(22),
        DAT_INICIOEXEC_HIST     DATE,
        REGIONAL                VARCHAR2(100),
        DATA_CARGA              TIMESTAMP DEFAULT SYSTIMESTAMP,
        TABELA_ORIGEM           VARCHAR2(30)
    )
    """
    cursor = conn.cursor()
    try:
        cursor.execute(ddl)
        conn.commit()
        log.info(f"Tabela {ORACLE_TABLE_NAME} criada")
    except oracledb.DatabaseError as e:
        if e.args[0].code == 955:
            log.info(f"Tabela {ORACLE_TABLE_NAME} já existe")
        else:
            raise
    finally:
        cursor.close()


# ==========================================================================
#  GERENCIAMENTO DE ÍNDICES (drop antes = carga muito mais rápida)
# ==========================================================================
def dropar_indices(conn, log):
    """Remove índices antes da carga para acelerar INSERT"""
    cursor = conn.cursor()
    for nome, _ in INDICES:
        try:
            cursor.execute(f"DROP INDEX {nome}")
            log.info(f"  Índice {nome} removido")
        except oracledb.DatabaseError as e:
            if e.args[0].code == 1418:
                log.debug(f"  Índice {nome} não existia")
            else:
                log.warning(f"  Erro ao dropar {nome}: {e}")
    conn.commit()
    cursor.close()


def criar_indices(conn, log):
    """Recria índices após carga + coleta estatísticas"""
    cursor = conn.cursor()
    for nome, colunas in INDICES:
        try:
            cursor.execute(
                f"CREATE INDEX {nome} ON {ORACLE_TABLE_NAME}({colunas}) NOLOGGING PARALLEL 4"
            )
            log.info(f"  Índice {nome} criado")
        except oracledb.DatabaseError as e:
            if e.args[0].code == 955:
                log.info(f"  Índice {nome} já existe")
            else:
                log.warning(f"  Erro ao criar {nome}: {e}")

    # Voltar indices para NOPARALLEL/LOGGING (produção)
    for nome, _ in INDICES:
        _exec_safe(cursor, f"ALTER INDEX {nome} NOPARALLEL LOGGING", log)

    # Coletar estatísticas
    log.info("Coletando estatísticas da tabela...")
    try:
        cursor.execute(f"""
            BEGIN
                DBMS_STATS.GATHER_TABLE_STATS(
                    ownname          => USER,
                    tabname          => '{ORACLE_TABLE_NAME}',
                    estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
                    method_opt       => 'FOR ALL COLUMNS SIZE AUTO',
                    degree           => 4
                );
            END;
        """)
        log.info("Estatísticas coletadas")
    except Exception as e:
        log.warning(f"Erro ao coletar estatísticas: {e}")

    conn.commit()
    cursor.close()


# ==========================================================================
#  PREPARAÇÃO DA TABELA PARA CARGA
# ==========================================================================
def preparar_tabela_para_carga(conn, log):
    """Coloca a tabela em NOLOGGING para carga rápida"""
    cursor = conn.cursor()
    _exec_safe(cursor, f"ALTER TABLE {ORACLE_TABLE_NAME} NOLOGGING", log)
    log.info("Tabela em modo NOLOGGING")
    cursor.close()


def finalizar_tabela_pos_carga(conn, log):
    """Restaura tabela para modo normal"""
    cursor = conn.cursor()
    _exec_safe(cursor, f"ALTER TABLE {ORACLE_TABLE_NAME} LOGGING", log)
    log.info("Tabela restaurada para LOGGING")
    cursor.close()


# ==========================================================================
#  TRUNCATE
# ==========================================================================
def truncar_tabela(conn, log):
    """Limpa a tabela consolidada"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"TRUNCATE TABLE {ORACLE_TABLE_NAME}")
        log.info(f"Tabela {ORACLE_TABLE_NAME} truncada")
    except Exception as e:
        log.error(f"Erro ao truncar: {e}")
        raise
    finally:
        cursor.close()


# ==========================================================================
#  QUERIES DE CONSOLIDAÇÃO
# ==========================================================================
def _select_colunas():
    """Retorna colunas para SELECT (sem TABELA_ORIGEM)"""
    cols = [c for c in COLUNAS if c != "TABELA_ORIGEM"]
    return ",\n        ".join(cols)


def _select_de_tabela(tabela):
    """Gera SELECT de uma tabela com marcação de origem e ROW_NUMBER"""
    cols = _select_colunas()
    return f"""
        SELECT 
            {cols},
            '{tabela}' AS TABELA_ORIGEM,
            ROW_NUMBER() OVER (PARTITION BY COD_TT ORDER BY DT_CRIACAO DESC NULLS LAST) AS rn
        FROM {tabela}
    """


def _query_consolidacao_completa():
    """Query que une todas as tabelas e mantém apenas o COD_TT mais recente"""
    subqueries = [_select_de_tabela(t) for t in TABELAS_ORIGEM]
    colunas_final = ",\n        ".join(COLUNAS)

    return f"""
    SELECT /*+ PARALLEL(4) */
        {colunas_final}
    FROM (
        {" UNION ALL ".join(subqueries)}
    )
    WHERE rn = 1
    """


# ==========================================================================
#  MÉTODO 1: INSERT DIRETO (tudo no Oracle, sem FOR em Python)
# ==========================================================================
def consolidar_direto(conn, log):
    """
    INSERT /*+ APPEND NOLOGGING PARALLEL */ INTO ... SELECT ...
    
    TODA a operação roda dentro do Oracle.
    Python apenas dispara o comando e espera o resultado.
    Elimina completamente o loop FOR que travava.
    """
    log.info("=" * 60)
    log.info("MÉTODO DIRETO: INSERT INTO ... SELECT (tudo no Oracle)")
    log.info("=" * 60)

    cursor = conn.cursor()
    inicio = time.time()

    colunas_str = ",\n         ".join(COLUNAS)
    query = _query_consolidacao_completa()

    insert_sql = f"""
    INSERT /*+ APPEND NOLOGGING PARALLEL(4) */ INTO {ORACLE_TABLE_NAME}
    ({colunas_str})
    {query}
    """

    log.info(f"Executando INSERT direto de {len(TABELAS_ORIGEM)} tabelas...")
    log.info("Aguardando Oracle processar (pode levar vários minutos)...")

    cursor.execute(insert_sql)
    total = cursor.rowcount
    conn.commit()

    tempo = time.time() - inicio
    vel = total / tempo if tempo > 0 else 0
    log.info(f"Inseridos: {total:,} registros em {tempo:.1f}s ({vel:,.0f} reg/s)")

    cursor.close()
    return total


# ==========================================================================
#  MÉTODO 2: INCREMENTAL (tabela por tabela, mais estável)
# ==========================================================================
def consolidar_incremental(conn, log):
    """
    Processa uma tabela de cada vez com MERGE.
    Mais lento, mas não sobrecarrega o Oracle.
    Reconecta automaticamente se perder conexão entre tabelas.
    """
    log.info("=" * 60)
    log.info("MÉTODO INCREMENTAL: MERGE tabela por tabela")
    log.info("=" * 60)

    total_geral = 0
    inicio_geral = time.time()

    for idx, tabela in enumerate(TABELAS_ORIGEM, 1):
        log.info(f"\n[{idx}/{len(TABELAS_ORIGEM)}] Processando {tabela}...")
        inicio_tab = time.time()

        # Verificar/reconectar antes de cada tabela
        conn = verificar_conexao(conn, log)
        cursor = conn.cursor()

        cols_sem_origem = _select_colunas()
        colunas_str = ", ".join(COLUNAS)

        if idx == 1:
            # Primeira tabela: INSERT simples (tabela está vazia após TRUNCATE)
            sql = f"""
            INSERT /*+ APPEND NOLOGGING PARALLEL(4) */ INTO {ORACLE_TABLE_NAME}
            ({colunas_str})
            SELECT 
                {cols_sem_origem},
                '{tabela}' AS TABELA_ORIGEM
            FROM {tabela}
            """
        else:
            # Demais tabelas: MERGE (mantém COD_TT mais recente por DT_CRIACAO)
            cols_update = [c for c in COLUNAS if c not in ("COD_TT", "TABELA_ORIGEM")]
            update_set = ",\n                    ".join(
                [f"dest.{c} = src.{c}" for c in cols_update]
            )
            update_set += ",\n                    dest.TABELA_ORIGEM = src.TABELA_ORIGEM"

            insert_vals = ", ".join([f"src.{c}" for c in COLUNAS])

            sql = f"""
            MERGE /*+ PARALLEL(4) */ INTO {ORACLE_TABLE_NAME} dest
            USING (
                SELECT 
                    {cols_sem_origem},
                    '{tabela}' AS TABELA_ORIGEM
                FROM {tabela}
            ) src
            ON (dest.COD_TT = src.COD_TT)
            WHEN MATCHED THEN
                UPDATE SET
                    {update_set}
                WHERE src.DT_CRIACAO > dest.DT_CRIACAO
                   OR dest.DT_CRIACAO IS NULL
            WHEN NOT MATCHED THEN
                INSERT ({colunas_str})
                VALUES ({insert_vals})
            """

        try:
            cursor.execute(sql)
            registros = cursor.rowcount
            conn.commit()

            tempo_tab = time.time() - inicio_tab
            vel = registros / tempo_tab if tempo_tab > 0 else 0
            log.info(f"  {registros:,} registros | {tempo_tab:.1f}s | {vel:,.0f} reg/s")
            total_geral += registros

        except Exception as e:
            log.error(f"  Erro ao processar {tabela}: {e}")
            try:
                conn.rollback()
            except Exception:
                pass
            raise
        finally:
            cursor.close()

    tempo_total = time.time() - inicio_geral
    vel_media = total_geral / tempo_total if tempo_total > 0 else 0
    log.info(f"\nTotal: {total_geral:,} registros em {tempo_total:.1f}s ({vel_media:,.0f} reg/s)")

    return total_geral


# ==========================================================================
#  CONSOLIDAÇÃO (com auto-fallback)
# ==========================================================================
def consolidar_dados(conn, log, metodo):
    """Executa consolidação pelo método escolhido, com fallback automático"""
    if metodo == "direto":
        return consolidar_direto(conn, log)

    elif metodo == "incremental":
        return consolidar_incremental(conn, log)

    else:  # "auto"
        log.info("Modo AUTO: tentando INSERT direto primeiro...")
        try:
            return consolidar_direto(conn, log)
        except Exception as e:
            log.warning(f"INSERT direto falhou: {e}")
            log.info("Alternando para método incremental...")
            truncar_tabela(conn, log)
            return consolidar_incremental(conn, log)


# ==========================================================================
#  VALIDAÇÃO
# ==========================================================================
def validar_consolidacao(conn, log):
    """Validação rápida da consolidação"""
    log.info("-" * 60)
    log.info("VALIDAÇÃO")
    log.info("-" * 60)

    cursor = conn.cursor()

    # Total
    cursor.execute(f"SELECT COUNT(*) FROM {ORACLE_TABLE_NAME}")
    total = cursor.fetchone()[0]
    log.info(f"Total de registros: {total:,}")

    # Por tabela de origem
    cursor.execute(f"""
        SELECT TABELA_ORIGEM, COUNT(*) AS QTDE
        FROM {ORACLE_TABLE_NAME}
        GROUP BY TABELA_ORIGEM
        ORDER BY TABELA_ORIGEM
    """)
    log.info("Distribuição por origem:")
    for row in cursor:
        log.info(f"  {row[0]}: {row[1]:,}")

    # Duplicatas (query otimizada - não traz todos, só conta)
    cursor.execute(f"""
        SELECT COUNT(*) FROM (
            SELECT COD_TT FROM {ORACLE_TABLE_NAME}
            GROUP BY COD_TT HAVING COUNT(*) > 1
        )
    """)
    dups = cursor.fetchone()[0]
    if dups > 0:
        log.warning(f"ATENÇÃO: {dups:,} COD_TT duplicados!")
    else:
        log.info("Unicidade OK: sem duplicatas")

    # Nulos
    cursor.execute(f"SELECT COUNT(*) FROM {ORACLE_TABLE_NAME} WHERE COD_TT IS NULL")
    nulos = cursor.fetchone()[0]
    if nulos > 0:
        log.warning(f"{nulos:,} registros com COD_TT nulo")
    else:
        log.info("Integridade OK: sem COD_TT nulo")

    cursor.close()
    return total


# ==========================================================================
#  MAIN
# ==========================================================================
def main():
    # === Argumentos de linha de comando ===
    parser = argparse.ArgumentParser(description="Consolidação Oracle B2C_COE")
    parser.add_argument(
        "--metodo",
        choices=["auto", "direto", "incremental"],
        default=METODO_CONSOLIDACAO,
        help="Método de consolidação (default: auto)",
    )
    args = parser.parse_args()

    # === Logging ===
    log, log_file = configurar_logging()

    log.info("=" * 70)
    log.info("  CONSOLIDAÇÃO ORACLE: B2C_COE")
    log.info("=" * 70)
    log.info(f"Tabelas origem : {', '.join(TABELAS_ORIGEM)}")
    log.info(f"Tabela destino : {ORACLE_TABLE_NAME}")
    log.info(f"Método         : {args.metodo}")
    log.info(f"Log            : {log_file}")
    log.info(f"Início         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # === Lock file ===
    if not adquirir_lock(log):
        sys.exit(2)  # Exit code 2 = já em execução

    inicio = datetime.now()
    conn = None
    exit_code = 0

    try:
        # 1) Conectar
        conn = conectar_oracle(log)

        # 2) Criar tabela (se não existir)
        criar_tabela_consolidada(conn, log)

        # 3) Dropar índices (carga fica muito mais rápida sem eles)
        log.info("-" * 60)
        log.info("PREPARAÇÃO")
        log.info("-" * 60)
        dropar_indices(conn, log)

        # 4) Configurar tabela para carga rápida (NOLOGGING)
        preparar_tabela_para_carga(conn, log)

        # 5) Truncar dados antigos
        truncar_tabela(conn, log)

        # 6) Consolidar
        log.info("-" * 60)
        total = consolidar_dados(conn, log, args.metodo)

        # 7) Recriar índices + estatísticas
        log.info("-" * 60)
        log.info("PÓS-CARGA")
        log.info("-" * 60)
        finalizar_tabela_pos_carga(conn, log)
        criar_indices(conn, log)

        # 8) Validar
        validar_consolidacao(conn, log)

        # Resumo final
        fim = datetime.now()
        duracao = fim - inicio
        minutos = int(duracao.total_seconds() // 60)
        segundos = int(duracao.total_seconds() % 60)

        log.info("=" * 70)
        log.info("  CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO")
        log.info(f"  Registros : {total:,}")
        log.info(f"  Duração   : {minutos}min {segundos}s")
        log.info(f"  Término   : {fim.strftime('%Y-%m-%d %H:%M:%S')}")
        log.info("=" * 70)

    except Exception as e:
        exit_code = 1
        log.error("=" * 70)
        log.error(f"  ERRO NA CONSOLIDAÇÃO: {e}")
        log.error("=" * 70, exc_info=True)

        if conn:
            try:
                conn.rollback()
                log.info("Rollback executado")
            except Exception:
                pass

    finally:
        if conn:
            try:
                conn.close()
                log.info("Conexão Oracle fechada")
            except Exception:
                pass

        liberar_lock(log)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
