# Consolidação Oracle - B2C_COE

## 📋 Descrição
Script Python para consolidação de dados de múltiplas tabelas Oracle históricas em uma única tabela consolidada, com garantia de unicidade por `COD_TT`.

## ✨ Funcionalidades

- **Consolidação de 6 tabelas** (B2C_COE_HIST_M1 a M5 + MES_ATUAL)
- **Garantia de unicidade** por COD_TT (mantém registro mais recente)
- **3 métodos de consolidação** (direto, incremental, automático)
- **Otimização para grandes volumes** (> 100M registros)
- **Validação automática** de duplicatas e integridade
- **Criação de índices** otimizados para Power BI
- **Estatísticas de performance** detalhadas

## 🚀 Otimizações para Grandes Volumes

### Problema Identificado
Em bases muito grandes, o script original parava no loop FOR devido a:
- Transferência de dados Oracle → Python → Oracle (lento)
- Processamento linha por linha em Python
- Timeout de conexão em queries longas
- Uso excessivo de memória

### Solução Implementada

#### **Método 1: INSERT Direto (Padrão)**
```sql
INSERT INTO destino SELECT ... FROM origens
```
- ✅ **Mais rápido** (até 10x mais rápido)
- ✅ Dados nunca saem do Oracle
- ✅ Usa hint `APPEND` para carga rápida
- ✅ Ideal para bases até 100M registros
- ⚠️ Pode falhar em bases muito grandes por timeout

#### **Método 2: Incremental (Fallback)**
```sql
MERGE INTO destino ... (tabela por tabela)
```
- ✅ **Mais estável** para grandes volumes
- ✅ Processa uma tabela por vez
- ✅ Usa MERGE para garantir unicidade durante processo
- ✅ Ideal para bases > 100M registros
- ⚠️ Mais lento que o método direto

#### **Método 3: Automático (Recomendado)**
- Tenta método direto primeiro
- Se falhar, usa método incremental automaticamente
- Melhor dos dois mundos

## ⚙️ Configuração

No arquivo `consolidacao_oracle.py`, configure:

```python
# Escolha o método de consolidação:
METODO_CONSOLIDACAO = "auto"  # Opções: "auto", "direto", "incremental"
```

### Quando usar cada método?

| Volume de Dados | Método Recomendado | Tempo Estimado |
|-----------------|-------------------|----------------|
| < 50M registros | `"direto"` | 5-15 min |
| 50M - 100M | `"auto"` | 10-30 min |
| > 100M registros | `"incremental"` | 30-90 min |

## 📊 Estrutura da Tabela Consolidada

```sql
B2C_COE_CONSOLIDADO (
    COD_TT              VARCHAR2(15) PRIMARY KEY
    DT_CRIACAO          DATE
    DT_DISPONIBILIDADE  DATE
    DT_FECHAMENTO       DATE
    REGIONAL            VARCHAR2(100)
    STATUS_REASON       VARCHAR2(255)
    TIPO_RECLAMACAO     VARCHAR2(200)
    ...
    TABELA_ORIGEM       VARCHAR2(30)
    DATA_CARGA          TIMESTAMP
)
```

## 🔧 Requisitos

```bash
pip install oracledb
```

**Oracle Instant Client**: 
- Windows: `C:\oracle\instantclient_23_8`
- Configure o caminho no script se necessário

## 📝 Uso

```bash
python consolidacao_oracle.py
```

## 📈 Otimizações Aplicadas

### 1. **Configurações de Sessão Oracle**
```sql
ALTER SESSION SET DDL_LOCK_TIMEOUT = 600        -- Timeout de 10min
ALTER SESSION SET OPTIMIZER_MODE = ALL_ROWS     -- Otimiza para grandes volumes
ALTER SESSION SET SORT_AREA_SIZE = 104857600    -- 100MB para sorts
ALTER SESSION SET HASH_AREA_SIZE = 104857600    -- 100MB para hash joins
```

### 2. **Hints de Performance**
```sql
/*+ PARALLEL(4) */    -- Processamento paralelo
/*+ APPEND */         -- Carga rápida sem log
```

### 3. **Índices Criados**
- `IDX_CONSOLIDADO_DT_CRIACAO` (DT_CRIACAO)
- `IDX_CONSOLIDADO_STATUS` (STATUS_REASON)
- `IDX_CONSOLIDADO_REGIONAL` (REGIONAL, NCLUSTER)
- `IDX_CONSOLIDADO_TIPO` (TIPO_RECLAMACAO)

### 4. **Estatísticas Oracle**
- Coleta automática de estatísticas após consolidação
- Melhora performance de consultas do Power BI

## 🐛 Troubleshooting

### Timeout em bases muito grandes
```python
METODO_CONSOLIDACAO = "incremental"
```

### Erro de memória
- Reduza `BATCH_SIZE` e `ARRAY_SIZE`
- Use método `"incremental"`

### Duplicatas na tabela
- O script usa ROW_NUMBER() para garantir unicidade
- Mantém sempre o registro com DT_CRIACAO mais recente

## 📊 Monitoramento

Durante a execução, o script exibe:
- ✓ Status de cada etapa
- ℹ Progresso em tempo real
- ⏱️ Velocidade de processamento (registros/segundo)
- 📈 Distribuição por tabela de origem
- ✅ Validações de unicidade e integridade

## 🔐 Segurança

⚠️ **IMPORTANTE**: As credenciais estão expostas no código.
- Para produção, use variáveis de ambiente ou vault
- Nunca commite credenciais em repositórios públicos

```python
# Exemplo usando variáveis de ambiente:
import os
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASS = os.getenv("ORACLE_PASS")
```

## 📅 Manutenção

- Execute diariamente/semanalmente conforme necessidade
- Monitore crescimento das tabelas origem
- Ajuste método de consolidação se necessário
- Acompanhe tempo de execução

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique os logs de execução
2. Teste com método `"incremental"` se houver timeout
3. Valide conectividade com o Oracle
4. Confirme credenciais e permissões
