@echo off
REM ==========================================================================
REM  CONSOLIDAÇÃO ORACLE - B2C_COE
REM  Script .bat para Agendador de Tarefas do Windows
REM ==========================================================================
REM
REM  Configurar no Agendador de Tarefas:
REM    Programa/script: C:\caminho\para\executar_consolidacao.bat
REM    Iniciar em:      C:\caminho\para\DashExecutivo
REM
REM  O script gera logs na pasta "logs\" automaticamente
REM  Exit codes: 0 = sucesso, 1 = erro, 2 = já em execução
REM ==========================================================================

cd /d "%~dp0"

echo [%date% %time%] Iniciando consolidacao Oracle...

REM === Ajuste o caminho do Python se necessário ===
python consolidacao_oracle.py --metodo auto

set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE%==0 (
    echo [%date% %time%] Consolidacao concluida com SUCESSO
) else if %EXIT_CODE%==2 (
    echo [%date% %time%] IGNORADO - Execucao anterior ainda em andamento
) else (
    echo [%date% %time%] ERRO na consolidacao (codigo: %EXIT_CODE%)
)

exit /b %EXIT_CODE%
