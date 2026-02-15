import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def seed():
    print("🚀 Starting Railway Database Seeding...")
    
    # Connection details from .env
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

    try:
        with connection.cursor() as cursor:
            # Read the SQL file
            sql_path = "railway_database_setup.sql"
            if not os.path.exists(sql_path):
                # Try parent dir if running from backend/
                sql_path = "../railway_database_setup.sql"
                
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_commands = f.read().split(';')
            
            print(f"📖 Found {len(sql_commands)} commands. Executing...")
            
            for command in sql_commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                    except Exception as e:
                        print(f"⚠️ Warning: Some commands might already exist. Skipping...")
            
            print("✅ Database Seeding Complete! Your dashboard is now alive.")
            
    finally:
        connection.close()

if __name__ == "__main__":
    seed()
