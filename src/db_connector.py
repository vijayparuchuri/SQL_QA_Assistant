from langchain_community.utilities import SQLDatabase
from typing import List
import os
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self, config: dict):
        load_dotenv()
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 3306)
        self.database = config.get("name", "Chinook")
        self.connection_string = f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.db = SQLDatabase.from_uri(self.connection_string)

    def get_dialect(self):
        return self.db.dialect

    def get_tables(self) -> List[str]:
        return self.db.get_usable_table_names()

    def get_table_info(self) -> str:
        return self.db.get_table_info()

    def execute_query(self, query: str) -> str:
        return self.db.run(query)
