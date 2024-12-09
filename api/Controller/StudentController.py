import os
import requests

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
        response = requests.get(url)
        
        if response.status_code != 200:
            return "Data not Found!"
        
        mahasiswa_list = response.json().get("mahasiswa", [])
        if not mahasiswa_list:
            return "Data not Found!"
        
        result = "\n ---- LIST MAHASISWA ----\n"
        for mahasiswa in mahasiswa_list:
            result += (
                f"Detail: /{mahasiswa.get('id', 'N/A')}\n"
                f"Name: {mahasiswa.get('nama', 'N/A')}\n"
                f"NIM: {mahasiswa.get('nim', 'N/A')}\n"
                f"College: {mahasiswa.get('nama_pt', 'N/A')}\n"
                f"Study Program: {mahasiswa.get('nama_prodi', 'N/A')}\n\n"
            )
        return result

    @staticmethod
    def _get_student_detail(student_id):
        url = f'{DATA_API}detail_student/{student_id}'
        response = requests.get(url)
        
        if response.status_code != 200:
            return "Data not Found!"
        
        data = response.json()
        dataumum = data.get("dataumum", {})
        datastatuskuliah = data.get("datastatuskuliah", [])
        datastudi = data.get("datastudi", [])

        result = (
            f" ----------- DATA UMUM -----------\n"
            f"Name: {dataumum.get('nm_pd', 'N/A')}\n"
            f"Gender: {dataumum.get('jk', 'N/A')}\n"
            f"nipd: {dataumum.get('nipd', 'N/A')}\n"
            f"Degree: {dataumum.get('namajenjang', 'N/A')}\n"
            f"Study Program: {dataumum.get('namaprodi', 'N/A')}\n"
            f"College Name: {dataumum.get('namapt', 'N/A')}\n"
            f"Sign Up Type: {dataumum.get('nm_jns_daftar', 'N/A')}\n"
            f"reg_pd: {dataumum.get('reg_pd', 'N/A')}\n"
            f"From College Name: {dataumum.get('nm_pt_asal', 'N/A')}\n"
            f"From SP Name: {dataumum.get('nm_prodi_asal', 'N/A')}\n"
            f"Desc Out: {dataumum.get('ket_keluar', 'N/A')}\n"
            f"Date Out: {dataumum.get('tgl_keluar', 'N/A')}\n"
            f"Serial Number Ijazah: {dataumum.get('no_seri_ijazah', 'N/A')}\n"
            f"Prof: {dataumum.get('sert_prof', 'N/A')}\n"
            f"Start: {dataumum.get('mulai_smt', 'N/A')}\n"
        )

        if datastatuskuliah:
            result += "\n ---- DATA STATUS KULIAH ----\n"
            for status in datastatuskuliah:
                result += (
                    f"\nID SMT : {status['id_smt']}\n"
                    f"SKS    : {status['sks_smt']}\n"
                    f"Status : {status['nm_stat_mhs']}\n"
                )

        if datastudi:
            result += "\n -------- DATA STUDY --------\n"
            for study in datastudi:
                result += (
                    f"\nCode MK: {study['kode_mk']}\n"
                    f"Name MK: {study['nm_mk']}\n"
                    f"SKS: {study['sks_mk']}\n"
                    f"ID SMT: {study['id_smt']}\n"
                    f"Grade: {study['nilai_huruf']}\n"
                )

        return result


class Message:

    @staticmethod
    def message_parser(message):
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
        payload = {'chat_id': chat_id, 'text': f'```{text}```', 'parse_mode': 'Markdown'}
        response = requests.post(url, json=payload)
        return response