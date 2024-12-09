import os
import requests
from dotenv import load_dotenv

load_dotenv()

DATA_API = os.getenv('DATA_API')
TELE_BOT_TOKEN = os.getenv('TELE_BOT_TOKEN')

class Answer:

    @staticmethod
    def generate_answer(message):
        if not message:
            return "Empty message."
        
        if message.startswith("/"):
            return Answer._get_student_detail(message[1:])
        else:
            return Answer._search_students(message)

    @staticmethod
    def _search_students(query):
        url = f'{DATA_API}search/all/{query}'
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"An error occurred: {e}"
        
        mahasiswa_list = response.json().get("mahasiswa", [])
        if not mahasiswa_list:
            return "Data not Found!"
        
        result = "\n ---- LIST MAHASISWA ----\n"
        for mahasiswa in mahasiswa_list:
            result += (
                f"Detail: <code>/{mahasiswa.get('id', 'N/A')}</code>\n"
                f"Name: {mahasiswa.get('nama', 'N/A')}\n"
                f"NIM: {mahasiswa.get('nim', 'N/A')}\n"
                f"College: {mahasiswa.get('nama_pt', 'N/A')}\n"
                f"Study Program: {mahasiswa.get('nama_prodi', 'N/A')}\n\n"
            )
        return result

    @staticmethod
    def _get_student_detail(student_id):
        pass

class Message:

    @staticmethod
    def process_message(message):
        chat_id = message['message']['chat']['id']
        text = message['message'].get('text', None)
        
        if text:
            print("Chat ID: ", chat_id)
            print("Message: ", text)
            return chat_id, text
        else:
            print("Chat ID: ", chat_id)
            print("Message does not contain text.")
            return chat_id, None

    @staticmethod
    def send_message_telegram(chat_id, text):
        url = f'https://api.telegram.org/bot{TELE_BOT_TOKEN}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        response = requests.post(url, json=payload)
        response_data = response.json()
        print("Response from Telegram: ", response_data)
        
        if not response_data.get('ok'):
            if response_data.get('error_code') == 400 and 'message is too long' in response_data.get('description', ''):
                text = text[:4096]  # Truncate the message to the maximum allowed length
                payload['text'] = text
                response = requests.post(url, json=payload)
                print("Response from Telegram after truncation: ", response.json())
        
        return response.json()
