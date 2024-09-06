from dotenv import load_dotenv
import os
#import sys
import pandas as pd
import requests
from flask import Flask, render_template, request, jsonify
import logging
#from pathlib import Path
# Aktuellen Pfad und das Hauptverzeichnis zum sys.path hinzufügen
#sys.path.append(str(Path(__file__).resolve().parent.parent))
from mongodb import MongoDB

logging.basicConfig(level=logging.DEBUG)

# MongoDB Instance
db = MongoDB(mongo_db_login=os.getenv("MONGO_DB_LOGIN"))

# Load environment variables from .env file
load_dotenv()

# Fetch the API key
api_key = os.getenv("OPENAI_API_KEY")

# Ensure the API key is correctly fetched
if not api_key:
    raise ValueError("API key is not set. Please check your environment variables.")


# Load the Excel file (only 1st sheet)
df = pd.read_excel('/home/yuri/Dokumente/Weiterbildung_2023/KI_Python/TOIRO-Projekt/例文集.xlsx')

# Extract the relevant data as a string
text_data = df.to_string()
#logging.debug(f"text_data: {text_data}")

app = Flask(__name__)

def generate_feedback(keywords):
    logging.debug(f"input keywords: {keywords}")
    # Prepare the prompt content using the keywords and the data from the Excel file
    prompt_content = f"""
    The following is feedback template data:
    {text_data}

    Based on this data and the following keywords, generate a positive feedback message for a Japanese teacher. Include references to the student's language skills and attitude.

    Keywords:
    {keywords}
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are a Japanese teachers of kids. Always respond friendly."
            },
            {
                "role": "user",
                "content": prompt_content
            }
        ],
        "temperature": 0.9,
        "max_tokens": 300
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # Exception handling bei HTTP-Fehlern. raise_for_status() wirft eine HTTPError-Exception, falls ein Fehler auftritt
        response_data = response.json()

        token_usage = response_data['usage']
        logging.info(f"Token usage: {token_usage}")
        
        ai_feedback_data = response_data['choices'][0]['message']['content']
        
        # Speichern der API-Anfrage und der Feedback-Daten in der Datenbank
        generation_id =db.insert_api_request_collection(payload, keywords)
        db.insert_ai_feedback_collection(ai_feedback_data,token_usage, generation_id)
        db.insert_text_example_collection(prompt_content, generation_id)

        return ai_feedback_data
    
    except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None
    except Exception as e:
            logging.error(f"An error occurred during database operations: {e}")
            return None
    
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_feedback', methods=['POST'])
def generate_feedback_route():
    try:
        data = request.json
        keywords = data.get('keywords', {})
        keywords_str = ""
        for item in keywords:
            for key, values in item.items():
                if isinstance(values, list):
                    values_str = ", ".join(values)
                    logging.debug(f"values_str: {values_str}")
                else:
                    values_str = values
                keywords_str += f"{key}: {values_str}\n"
        feedback = generate_feedback(keywords_str)
        return jsonify({'feedback': feedback})
    except Exception as e:
        logging.error(f"An error occurred in generate_feedback_route(): {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
