# LLM-Enhanced DETEXA Workflow Builder

This project provides a prototype of an interactive interface and backend engine for configuring **semantic enrichment workflows** using [DETEXA] and **LLMs**. It allows users to combine SQL-based text processing with targeted LLM-based enrichment through UDFs.

> ⚠️ **Alpha version** — currently supports **YeSQL's** integration with **SQLite**. More engines and features coming soon!

## 🔍 Key Features

- 🧱 **Modular Workflow Design**: Define workflows using pattern matching, normalization, prompt templates, and classification logic.
- ✍️ **LLM Integration**: Integrate LLM-based UDFs for link extraction, semantic labeling, and classification.
- ⚙️ **Just in Time Code Generation**: Generates Python UDFs and SQL pipelines from GUI configurations.
- 🧪 **Hybrid Execution**: Combine efficient SQL filtering with precise LLM post-processing.
- 📝 **Built-in Code Editor**: Edit and preview Python UDFs and SQL queries directly in the interface, with syntax highlighting, and real-time error feedback.
- 🐞 **Live Debugging of UDFs**: Inspect and test UDF logic on the fly with sample inputs. Errors are shown **inline in the code editor**, with annotated highlights on the exact lines.

## 🧰 Components

- **Web Interface**: Interactive UI to configure workflows step by step.
- **Backend Generator**: Translates configuration into executable SQL + UDF code.
- **Execution Layer**: Runs workflows on **YeSQL** compatible databases. 

## 🎥 Demo

Watch a short video demo of the workflow builder in action:

👉 [Click here to view the demo](https://doi.org/10.5281/zenodo.16450765
)



