from langchain_ollama import ChatOllama
from langchain import hub
from langchain_community.tools import QuerySQLDataBaseTool
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from state import State, QueryOutput
from db_connector import DatabaseConnection
from config import load_config

class QueryPipeline:
    def __init__(self, db: DatabaseConnection, model_config: dict):
        self.db = db
        self.model = ChatOllama(
            model=model_config.get("name", "qwen2.5:7b"),
            temperature=model_config.get("temperature", 0.7)
        )
        self.query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
        self.setup_pipeline()

    def write_query(self, state: State):
        prompt = self.query_prompt_template.invoke({
            "dialect": self.db.get_dialect(),
            "table_info": self.db.get_table_info(),
            "input": state["question"],
            "top_k": 10
        })
        structured_llm = self.model.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}

    def execute_query(self, state: State):
        execute_query_tool = QuerySQLDataBaseTool(db=self.db.db)
        return {"result": execute_query_tool.invoke(state["query"])}

    def generate_answer(self, state: State):
        prompt = (
            "Given the following user question, corresponding SQL query, and the result, answer the user question.\n\n"
            f"Question:{state['question']}\n"
            f"SQL Query:{state['query']}\n"
            f"SQL result:{state['result']}"
        )
        response = self.model.invoke(prompt)
        return {"answer": response.content}

    def setup_pipeline(self):
        self.graph_builder = StateGraph(State).add_sequence([
            self.write_query,
            self.execute_query,
            self.generate_answer
        ])
        self.graph_builder.add_edge(START, "write_query")
        self.memory = MemorySaver()
        self.graph = self.graph_builder.compile(
            checkpointer=self.memory,
            interrupt_before=["execute_query"]
        )

    def process_question(self, question, config: dict = None, continue_execution=False):
        if config is None:
            config = {"configurable": {"thread_id": 1}}

        results = []

        if continue_execution:
            # Continue from the last checkpoint
            for step in self.graph.stream(
                None,  # No new input needed
                config,
                stream_mode="updates"
            ):
                results.append(step)
        else:
            # Start new execution
            for step in self.graph.stream(
                {"question": question},
                config,
                stream_mode="updates"
            ):
                results.append(step)

        return results[-1] if results else None

# config = load_config()
# db = DatabaseConnection(config)
# db.get_tables()

# qp = QueryPipeline(db, config["model"])
# # bla = qp.write_query({"question": "What is the total number of employees?"})
# # print(bla)
# # qp.execute_query({"query": bla["query"]})

# # memory = MemorySaver()
# # graph = qp.graph_builder.compile(checkpointer=memory, interrupt_before=["execute_query"])
# config = {"configurable": {"thread_id": 1}}
# # for step in qp.graph.stream(
# #     {"question": "What is the total number of employees?"},
# #     config=config,
# #     stream_mode="updates"
# # ):
# #     print(step)


# qp.process_question("What is the total number of employees?", config=config)
