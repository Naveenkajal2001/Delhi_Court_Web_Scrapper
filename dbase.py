import mysql.connector
import mysql.connector
from mysql.connector import errorcode
import json
from datetime import datetime

class database:

    def __init__(self):
        db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'kajalnaveen'
        }
        database_name = 'Queries'

        try:
            # Connect to MySQL server
            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor()

            # Create database if not exists
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"✅ Database '{database_name}' ensured.")

            # Use the created/existing database
            self.cursor.execute(f"USE {database_name}")

            # Create table if not exists
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS case_queries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    case_type VARCHAR(50),
                    case_number VARCHAR(50),
                    case_year VARCHAR(10),
                    raw_result json,
                    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    
                )
            """)
            print("✅ Table ensured.")
        except mysql.connector.Error as err:
            print(f"❌ Error: {err}")


    def insert_case_query(self,case_type, case_number, case_year,raw_result):
        if isinstance(raw_result, (dict, list)):
            raw_result = json.dumps(raw_result)

        search_time = datetime.now()

        insert_query = """
            INSERT INTO case_queries (case_type, case_number, case_year,raw_result,search_time)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (case_type, case_number, case_year,raw_result,search_time)

        self.cursor.execute(insert_query, values)
        self.conn.commit()

        print("✅ Case query inserted.")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("🛑 Database connection closed.")


# a=database()
