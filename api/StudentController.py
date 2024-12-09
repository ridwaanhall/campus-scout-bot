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
        
        if message == "/start":
            return Answer._start_message()
        elif message.startswith("/"):
            return Answer._get_student_detail(message[1:])
        else:
            return Answer._search_students(message)

    @staticmethod
    def _start_message():
        return (
            "Welcome to the Student Information Bot!\n"
            "You can search for students by sending a message with their name or NIM.\n"
            "To get details of a specific student, send a message with their ID in the format /ID.\n"
            "For example, to get details of a student with ID 123, send /123."
        )

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
        
        result = "---- LIST MAHASISWA ----\n"
        for mahasiswa in mahasiswa_list:
            result += (
                # f"ID: {mahasiswa.get('id', 'N/A')}\n"
                f"NIM: {mahasiswa.get('nim', 'N/A')}\n"
                f"Name: {mahasiswa.get('nama', 'N/A')}\n"
                f"Study Program: {mahasiswa.get('nama_prodi', 'N/A')}\n"
                f"College: {mahasiswa.get('nama_pt', 'N/A')} ({mahasiswa.get('sinkatan_pt', 'N/A')})\n\n"
                # f"College Abbreviation: \n"
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
        
        # Truncate the message before adding HTML tags
        if len(text) > 4096:
            text = text[:4096]
        
        response = requests.post(url, json=payload)
        response_data = response.json()
        print("Response from Telegram: ", response_data)
        
        if not response_data.get('ok'):
            if response_data.get('error_code') == 400 and 'message is too long' in response_data.get('description', ''):
                # Truncate the message again if necessary
                text = text[:4096]
                payload['text'] = text
                response = requests.post(url, json=payload)
                print("Response from Telegram after truncation: ", response.json())
        
        return response.json()
