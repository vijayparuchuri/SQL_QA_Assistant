import logging
from db_connector import DatabaseConnection
from query_pipeline import QueryPipeline
from config import load_config

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()

    try:
        # Load configuration
        config = load_config()
        # logger.info("Configuration loaded successfully")

        # Initialize database connection
        db = DatabaseConnection(config["database"])
        # logger.info("Database connection established")

        # Initialize pipeline
        pipeline = QueryPipeline(db, config["model"])
        # logger.info("Query pipeline initialized")

        while True:
                question = input("\nEnter your question (or 'quit' to exit): ")
                if question.lower() == 'quit':
                    break

                # logger.info(f"Processing question: {question}")

                # First call to generate query
                config = {"configurable": {"thread_id": 1}}
                result = pipeline.process_question(question, config=config)
                if result:
                    print("Query has been generated!")
                    # print("\nQuery generated:", result.get("write_query", ""))
                    user_approval = input("\nDo you want to execute the query? (Y/N): ")

                    if user_approval.lower() == 'y':
                        # Continue execution from checkpoint with the same config
                        final_result = pipeline.process_question(
                            None,
                            config=config,
                            continue_execution=True
                        )
                        if final_result:
                            print("\nAnswer:", final_result.get("generate_answer", "Query not parsed")["answer"])
                    else:
                        print("Query execution cancelled")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
