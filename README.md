# SQL QA Assistant

A natural language to SQL query assistant that allows users to interact with databases using conversational language. The application leverages LLMs to translate natural language questions into SQL queries and provide human-readable answers.

## Features

- Natural language to SQL query conversion
- Interactive query execution approval
- Support for MySQL databases
- Configurable LLM model settings
- Safe query execution with user confirmation
- Detailed logging system

## Architecture

The project consists of several key components:

- `db_connector.py`: Handles database connections and query execution
- `query_pipeline.py`: Manages the LLM pipeline for query generation and answer synthesis
- `state.py`: Defines state management types
- `config.py`: Handles configuration loading
- `main.py`: Entry point with interactive CLI

## Prerequisites

- Python 3.8+
- MySQL database
- Ollama (for running local LLMs)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sql-qa-assistant.git
cd sql-qa-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your database credentials:
```env
DB_USER=your_username
DB_PASSWORD=your_password
```

## Configuration

Update `config/config.yaml` with your settings:

```yaml
database:
  host: localhost
  port: 3306
  name: YourDatabaseName

model:
  name: "qwen2.5:7b"
  temperature: 0.7
```

## Usage

Run the application:
```bash
python src/main.py
```

Example interaction:
```
Enter your question (or 'quit' to exit): How many employees are there in total?
Query has been generated!

Do you want to execute the query? (Y/N): Y

Answer: There are 8 employees in total.
```
