import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
import logging
import uuid
import datetime

logging.basicConfig(level=logging.DEBUG)

# Laden der Umgebungsvariablen aus einer .env-Datei
load_dotenv()

class MongoDB:
    def __init__(self, mongo_db_login):
        self.client = self.connect_mongodb(mongo_db_login)
        self.db = self.client['text_generator_project']
        self.api_request_collection = self.db['api_request']
        self.ai_feedback_collection = self.db['ai_feedback']
        self.text_example_collection = self.db['text_example']

    def connect_mongodb(self, mongo_db_login):
        
        try:

            # Verbindung zu MongoDB herstellen
            self.client = pymongo.MongoClient(mongo_db_login)
            
            # Überprüfen, ob die Verbindung erfolgreich ist
            self.client.admin.command('ping')
            logging.debug("Verbindung zu MongoDB erfolgreich")

            return self.client
        
        except ConnectionFailure as e:
            logging.error(f"Fehler bei der Verbindung zu MongoDB: {e}")
        except Exception as e:
            logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    # insert
    def insert_api_request_collection(self, payload, keywords):
        try:
            # Überprüfen, ob die erforderlichen Felder vorhanden sind
            if not payload or not keywords:
                raise ValueError("Payload und Keywords sind erforderlich")
            
            # Automatisch eine generation_id generieren
            generation_id = str(uuid.uuid4())

            self.api_request_document = {
                "payload":payload,
                "keywords": keywords,
                "generation_id": generation_id,
                "timestamp": str(datetime.datetime.now())
                }

            # Daten in die Collection "api_request" einfügen
            result = self.api_request_collection.insert_one(self.api_request_document)
            logging.debug(f'Dokument in api_request eingefügt mit ID: {result.inserted_id}')
            return generation_id
        
        except OperationFailure as e:
            logging.error(f"Fehler bei der Operation in MongoDB: {e}")
        except Exception as e:
            logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    def insert_ai_feedback_collection(self, ai_feedback_data, token_usage, generation_id):
        try:
             if not ai_feedback_data or not token_usage or not generation_id:
                raise ValueError("ai_feedback_data, token_usage und generation_id sind erforderlich")
             
             self.ai_feedback_document = {
                "ai_feedback_data":ai_feedback_data,
                "token_usage":token_usage,
                "generation_id":generation_id
                }

            # Daten in die "ai_feedback" Collection einfügen
             result = self.ai_feedback_collection.insert_one(self.ai_feedback_document)
             logging.debug(f'Dokument in ai_feedback eingefügt mit ID: {result.inserted_id}')
        except OperationFailure as e:
            logging.error(f"Fehler bei der Operation in MongoDB: {e}")
        except Exception as e:
            logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    
    def insert_text_example_collection(self, prompt_content, generation_id):
        try:
            if not prompt_content or not generation_id:
                raise ValueError("text_example und generation_id sind erforderlich")
            
            text_example_document = {
                "prompt_content": prompt_content,
                "generation_id": generation_id
            }

            # Daten in die "text_example" Collection einfügen
            result = self.text_example_collection.insert_one(text_example_document)
        
            logging.debug(f'Dokument in text_example eingefügt mit ID: {result.inserted_id}')
        except OperationFailure as e:
            logging.error(f"Fehler bei der Operation in MongoDB: {e}")
        except Exception as e:
            logging.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


    def close(self):
        if self.client:
            self.client.close()
            logging.debug("Verbindung zu MongoDB geschlossen")