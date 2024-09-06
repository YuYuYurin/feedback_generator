import unittest
from pymongo import MongoClient
import os
import sys 
from pathlib import Path
from dotenv import load_dotenv
import logging
import pandas as pd


# Aktuellen Pfad und das Hauptverzeichnis zum sys.path hinzufügen
sys.path.append(str(Path(__file__).resolve().parent.parent))
from mongodb import MongoDB

logging.basicConfig(level=logging.DEBUG)


class Test_MongoDB(unittest.TestCase):
    def setUp(self):
        self.db = MongoDB(mongo_db_login=os.getenv("MONGO_DB_LOGIN"))

    def tearDown(self):
        self.db.close()

# test indert_api_request

    def test_insert_api_request_collection(self):
        payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant for Japanese teachers of kids. Always respond friendly"
            },
            {
                "role": "user",
                "content": "prompt_content_version_1"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
        }

        keywords = {
        "授業態度": "集中力",
        "感情": "",
        "褒めたい事柄": "",
        "授業テーマ": "植物の育ち方",
        "文章に入れたいエピソードなど": ""
        }
        generation_id = self.db.insert_api_request_collection(payload, keywords)
        self.assertIsNotNone(generation_id, "Generation ID sollte nicht None sein")
        
        # test_insert_ai_feedback_collection
        token_usage = { 
            "prompt_tokens": 13,
            "completion_tokens": 7,
            "total_tokens": 20
        }
    
        ai_feedback_data = {
        "content":"test content"
        }
        self.db.insert_ai_feedback_collection(ai_feedback_data, token_usage, generation_id)

        # test_insert_text_example_collection
        df = pd.read_excel('/home/yuri/Dokumente/Weiterbildung_2023/KI_Python/TOIRO-Projekt/例文集.xlsx')

        text_example = {
        df.to_string()

        }
        self.db.insert_text_example_collection(text_example, generation_id)


# test fetch_api_request
if __name__ == '__main__':
    unittest.main()