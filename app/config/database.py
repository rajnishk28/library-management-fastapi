from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

try:
    client = MongoClient(MONGO_URL)

    # check connection
    client.admin.command("ping")

    db = client[DATABASE_NAME]

    print("MongoDB Connected Successfully")

except Exception as e:
    print("MongoDB Connection Failed")
    print("Error:", e)
