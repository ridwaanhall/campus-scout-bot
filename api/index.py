from flask import Flask, Response, request, jsonify
from api.StudentController import Answer, Message

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            msg = request.get_json()
            if not msg:
                return jsonify({'error': 'Invalid input'}), 400

            chat_id, incoming_question = Message.process_message(msg)
            answer = Answer.generate_answer(incoming_question)
            Message.send_message_telegram(chat_id, answer)
            return Response('ok', status=200)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return "<h1>You're lost</h1>"
