import os
import psycopg2
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Migrations")

# Usually DB_CONNECTION_STRING is for sqlalchemy like postgresql://...
# psycopg2 can accept a DSN or URI.
DB_DSN = os.getenv("DB_CONNECTION_STRING", "postgresql://sribash:56789@localhost:5432/world_sim")

def run_migrations():
    logger.info("Connecting to Database...")
    try:
        conn = psycopg2.connect(DB_DSN)
        conn.autocommit = True
        cur = conn.cursor()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        for file in ["init_schema.sql", "phase2_schema.sql"]:
            filepath = os.path.join(script_dir, file)
            if os.path.exists(filepath):
                logger.info(f"Running {file}...")
                with open(filepath, 'r') as f:
                    sql = f.read()
                    cur.execute(sql)
                logger.info(f"Successfully applied {file}.")
            else:
                logger.warning(f"File {file} not found.")
                
        cur.close()
        conn.close()
        logger.info("All migrations applied successfully.")
    except Exception as e:
        logger.error(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migrations()
