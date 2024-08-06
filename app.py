from flask import Flask, request, jsonify, render_template
import os
import json
from pygments import lexers, util
import prompt_logic

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send_prompt', methods=['POST'])
def generate_comment_api():
    data = request.json
    prompt_content = data.get('prompt_content')

    # Function to check if the content is code using Pygments
    def is_code_snippet(content):
        try:
            lexer = lexers.guess_lexer(content)
            return True
        except util.ClassNotFound:
            return False
        
    # Check if the prompt_content is code
    if is_code_snippet(prompt_content):
        prompt_content = f"Identify the language of the following code snippet and provide both in-code comments along with the code and a detailed explanation. Make sure the in-code comments are included directly within the code.:\n{prompt_content}"
    else:
        prompt_content = prompt_content
    print(prompt_content)   
    if not prompt_content:
        return jsonify({'error': 'Prompt content is required🫣'}), 400

    try:
        comment = prompt_logic.run_prompt_logic(prompt_content)
        return jsonify({'comment': comment})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chats_history/')
def list_chats():
    chats_dir = os.path.join(os.getcwd(), 'chats_history')
    chat_files = os.listdir(chats_dir)
    chat_ids = [os.path.splitext(filename)[0] for filename in chat_files if filename.endswith('.json')]
    return jsonify(chat_ids)

@app.route('/chats_history/<chat_id>.json')
def get_chat_history(chat_id):
    try:
        with open(os.path.join(os.getcwd(), 'chats_history', f'{chat_id}.json')) as f:
            history = json.load(f)
            return jsonify(history)
    except FileNotFoundError:
        return jsonify({'history': []})

@app.route('/api/new_chat', methods=['POST'])
def create_chat():
    data = request.json
    chat_id = data.get('chat_id')
    if not chat_id:
        return jsonify({'error': 'Chat ID is required🫠'}), 400

    chat_file = os.path.join(os.getcwd(), 'chats_history', f'{chat_id}.json')
    if os.path.exists(chat_file):
        return jsonify({'error': 'Chat ID already exists😥'}), 400

    with open(chat_file, 'w') as f:
        json.dump({'history': []}, f)

    return jsonify({'message': f'Chat "{chat_id}" created successfully🥳✌️'})

@app.route('/api/save_chat', methods=['POST'])
def save_chat():
    data = request.json
    chat_id = data.get('chat_id')
    history = data.get('history')

    if not chat_id:
        return jsonify({'error': 'Chat ID is required'}), 400

    chat_file = os.path.join(os.getcwd(), 'chats_history', f'{chat_id}.json')
    with open(chat_file, 'w') as f:
        json.dump({'history': history.split('<br>')}, f)

    return jsonify({'message': f'Chat "{chat_id}" saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)
