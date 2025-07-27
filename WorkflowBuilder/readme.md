# LLM-Enhanced DETEXA Workflow Builder (Alpha Version)

This project provides an interactive interface and backend engine for configuring **semantic enrichment workflows** using DETEXA and **LLMs**. It enables users to combine traditional SQL-based text processing with targeted LLM-based enhancement through UDFs.

## 🔍 Key Features

- 🧱 **Modular Workflow Design**: Build semantic enrichment pipelines using configurable blocks.
- ✍️ **LLM Integration**: Add LLM-based UDFs for classification, link extraction, and semantic analysis.
- ⚙️ **Backend Automation**: Automatically generates Python UDFs and SQL queries based on user-defined parameters.
- 🧪 **Hybrid Execution**: Mix efficient SQL filters with python UDFs and LLM-based precision on selected text segments.

## 🧰 Components

- **Web Interface**: GUI to define patterns, normalization steps, prompt templates, and classification logic.
- **Backend Generator**: Converts UI configuration to executable SQL + UDF workflows.
- **Execution Engine**: Runs workflows on compatible databases (e.g., PostgreSQL, DuckDB, SQLite).

## 🎥 Demo

Watch a short video demo of the workflow builder in action:

👉 [Click here to view the demo](https://doi.org/10.5281/zenodo.16450765
)

## ⚡ Example Use Case

Extract and normalize Data Availability Statements (DAS) from research publications:
1. Pre-filter sections with SQL.
2. Normalize and tokenize text.
3. Configure a pattern based classification algorithm for DAS.
4. Use LLM to extract data availability labels when the pattern based classification fails.
5. Return enriched outputs into tabular format.

