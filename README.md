# Dashboard Executivo para Power BI

Um dashboard executivo abrangente projetado para Power BI, fornecendo insights de negócios chave e KPIs para tomada de decisões estratégicas.

---

## 📊 Visão Geral

Este projeto fornece uma solução completa de dashboard executivo para Power BI, incluindo:

- **Modelo de Dados Dimensional**: Schema star com dimensões e tabelas de fatos
- **Medidas DAX**: Métricas pré-construídas e cálculos KPI
- **Dados de Exemplo**: Gerador de dados de amostra para teste
- **Especificações de Design**: Design detalhado e diretrizes visuais
- **Guia de Implantação**: Instruções passo a passo para implementação

---

## 🎯 Funcionalidades Principais

### Páginas do Dashboard:

1. **Visão Geral Executiva**
   - KPIs principais (Vendas, Lucro, Margem, Crescimento)
   - Tendências de vendas vs ano anterior
   - Vendas por departamento e região
   - Top 10 produtos

2. **Desempenho Financeiro**
   - Análise Orçamento vs Real
   - Análise de lucro e margens
   - Tendência de margem de lucro
   - KPIs financeiros por departamento

3. **Análise de Vendas**
   - Vendas por categoria e segmento
   - Decomposição detalhada de vendas
   - Matriz de desempenho de produtos
   - Análise de tendências

4. **Insights de Clientes**
   - Métricas de clientes (total, novos, retenção)
   - Distribuição por região e segmento
   - Top 20 clientes
   - Funil de retenção

5. **Dashboard de KPIs**
   - Scorecard de KPIs por departamento
   - Gráficos de medidor de realização
   - Análise de tendências de KPI
   - Mapa de calor de KPIs

---

## 📁 Estrutura do Projeto

```
DashExecutivo/
├── DataModel/
│   └── schema.sql              # Schema do banco de dados (dimensões e fatos)
├── DAX/
│   └── measures.dax            # Medidas e cálculos DAX
├── SampleData/
│   └── generate_sample_data.py # Script Python para gerar dados de teste
├── Documentation/
│   ├── dashboard_design.md     # Especificações de design do dashboard
│   └── deployment_guide.md     # Guia de implantação e configuração
└── README.md                   # Este arquivo
```

---

## 🚀 Início Rápido

### Pré-requisitos:

- Power BI Desktop (versão mais recente)
- Python 3.x (para gerar dados de exemplo)
- Banco de dados SQL Server ou Azure SQL (para produção)

### Passos:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/kruetzmann2110/DashExecutivo.git
   cd DashExecutivo
   ```

2. **Gere dados de exemplo** (para teste):
   ```bash
   cd SampleData
   python generate_sample_data.py
   ```

3. **Configure o banco de dados**:
   - Execute `DataModel/schema.sql` em seu banco de dados
   - Ou importe os arquivos CSV gerados diretamente no Power BI

4. **Crie o Dashboard no Power BI**:
   - Abra o Power BI Desktop
   - Conecte-se à fonte de dados
   - Configure relacionamentos do modelo de dados
   - Adicione medidas DAX de `DAX/measures.dax`
   - Crie visualizações seguindo `Documentation/dashboard_design.md`

5. **Publique no Power BI Service**:
   - Clique em "Publicar" no Power BI Desktop
   - Configure agendamento de atualização
   - Configure segurança em nível de linha (RLS)
   - Compartilhe com usuários

---

## 📚 Documentação

### Guias Disponíveis:

- **[Dashboard Design](Documentation/dashboard_design.md)**: Especificações detalhadas de design, esquema de cores, tipografia e layouts de página
- **[Deployment Guide](Documentation/deployment_guide.md)**: Instruções passo a passo para implantação, configuração e manutenção

### Modelo de Dados:

O dashboard usa um **schema star** com:

**Dimensões**:
- `DimTime`: Dimensão de tempo (datas, anos, meses, semanas)
- `DimDepartment`: Departamentos organizacionais
- `DimProduct`: Catálogo de produtos
- `DimCustomer`: Informações de clientes

**Fatos**:
- `FactSales`: Transações de vendas
- `FactBudget`: Orçamentos por departamento
- `FactKPI`: Indicadores de desempenho chave

---

## 📊 Principais Medidas DAX

### Vendas:
- Total Sales (Vendas Totais)
- Sales Growth % (Crescimento de Vendas %)
- Sales YTD (Vendas Acumuladas no Ano)
- Average Transaction Value (Valor Médio de Transação)

### Lucro:
- Total Profit (Lucro Total)
- Profit Margin % (Margem de Lucro %)
- Profit Growth % (Crescimento de Lucro %)

### Orçamento:
- Total Budget (Orçamento Total)
- Budget vs Actual (Orçamento vs Real)
- Budget Achievement % (Realização do Orçamento %)

### KPIs:
- KPI Current Value (Valor Atual do KPI)
- KPI Achievement % (Realização do KPI %)
- KPI Status (Status do KPI)

### Clientes:
- Total Customers (Total de Clientes)
- Customer Retention Rate (Taxa de Retenção)
- New Customers (Novos Clientes)

---

## 🎨 Design e Estilo

### Esquema de Cores:
- **Azul Primário**: #1F4E78 (cabeçalhos, elementos principais)
- **Azul Secundário**: #4472C4 (gráficos, visuais)
- **Verde**: #70AD47 (indicadores positivos)
- **Vermelho**: #FF6B6B (indicadores negativos, alertas)
- **Laranja**: #FFA500 (avisos, próximo à meta)

### Fontes:
- **Principal**: Segoe UI
- **Cabeçalhos**: 16-20pt, Negrito
- **Corpo**: 10-12pt, Regular
- **Valores KPI**: 24-32pt, Negrito

---

## 🔒 Segurança

### Row-Level Security (RLS):

O dashboard suporta segurança em nível de linha com as seguintes funções:

- **Gerentes de Departamento**: Veem apenas dados de seu departamento
- **Gerentes Regionais**: Veem apenas dados de sua região
- **Executivos**: Veem todos os dados

---

## 🔄 Atualização de Dados

### Configuração Recomendada:
- **Frequência**: Diariamente às 6h
- **Atualização Incremental**: Últimos 2 anos
- **Notificações**: Email em caso de falha

---

## 🛠️ Tecnologias Utilizadas

- **Power BI Desktop**: Desenvolvimento de dashboard
- **Power BI Service**: Publicação e compartilhamento
- **DAX**: Linguagem de expressões de dados
- **SQL**: Modelagem de dados
- **Python**: Geração de dados de exemplo

---

## 📈 Otimização de Desempenho

- Uso de agregações para consultas mais rápidas
- Modelo de dados otimizado (schema star)
- Medidas em vez de colunas calculadas
- Atualização incremental configurada
- Indexação adequada de tabelas

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é de código aberto e está disponível para uso.

---

## 📧 Suporte

Para dúvidas, problemas ou sugestões:

- Abra uma issue no GitHub
- Consulte a [documentação do Power BI](https://docs.microsoft.com/power-bi/)
- Visite a [comunidade Power BI](https://community.powerbi.com/)

---

## 🎓 Recursos Adicionais

- **DAX Guide**: https://dax.guide/
- **Power BI Blog**: https://powerbi.microsoft.com/blog/
- **SQLBI**: https://www.sqlbi.com/

---

**Desenvolvido com ❤️ para análise de negócios e inteligência executiva**
