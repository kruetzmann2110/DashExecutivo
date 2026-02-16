# DashExecutivo

Dashboard Executivo para Power BI com consolidação de dados Oracle.

## 📁 Arquivos

- **`consolidacao_oracle.py`** - Script de consolidação de dados das tabelas B2C_COE
- **`README_CONSOLIDACAO.md`** - Documentação completa do processo de consolidação

## 🚀 Quick Start

```bash
# Instalar dependências
pip install oracledb

# Executar consolidação
python consolidacao_oracle.py
```

## 📊 Sobre

Este projeto consolida dados de 6 tabelas históricas Oracle (B2C_COE_HIST_M1 a M5 + MES_ATUAL) em uma única tabela otimizada para análise no Power BI, garantindo unicidade por COD_TT e melhor performance para grandes volumes de dados.

Para mais detalhes, consulte [README_CONSOLIDACAO.md](README_CONSOLIDACAO.md).
