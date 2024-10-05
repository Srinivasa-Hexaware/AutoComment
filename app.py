from flask import Flask, request, jsonify, render_template
import re
import os
import json
import markdown
import prompt_logic
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send_prompt', methods=['POST'])
def generate_comment_api():
    data = request.json
    prompt_content = data.get('prompt_content')
        
    # # Check if the prompt_content is code
    # if is_code_snippet(prompt_content):
    #     prompt_content = f"Identify the language of the following code snippet and provide both in-code comments along with the code and a detailed explanation. Make sure the in-code comments are included directly within the code.:\n{prompt_content}"
    # else:
    #     prompt_content = prompt_content

    # Advanced regular expression to detect code snippets
    # code_regex = re.compile(
    #     r'(?:(?:def|class|function|return|if|else|for|while|try|catch|finally|switch|case|break|continue|new|delete|throw|import|from|export|public|private|protected|static|void|const|let|var|int|float|double|string|char|boolean|bool|enum|struct|typedef|namespace|using|template|typename|this|self|super|extends|implements|interface|package|lambda|yield|async|await|print|println|main|args)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*(?:\(|{|\:|=))|'
    #     r'(?://|/\*|#|<!--|<!---|-->|--->|//|/\*|\*/|#|--|%|\bprint\b|\bprintln\b|\bfunction\b|\bdef\b|\bclass\b|\breturn\b|\bif\b|\belse\b|\bfor\b|\bwhile\b|\btry\b|\bcatch\b|\bfinally\b|\bswitch\b|\bcase\b|\bbreak\b|\bcontinue\b|\bnew\b|\bdelete\b|\bthrow\b|\bimport\b|\bfrom\b|\bexport\b|\bpublic\b|\bprivate\b|\bprotected\b|\bstatic\b|\bvoid\b|\bconst\b|\blet\b|\bvar\b|\bint\b|\bfloat\b|\bdouble\b|\bstring\b|\bchar\b|\bboolean\b|\bbool\b|\benum\b|\bstruct\b|\btypedef\b|\bnamespace\b|\busing\b|\btemplate\b|\btypename\b|\bthis\b|\bself\b|\bsuper\b|\bextends\b|\bimplements\b|\binterface\b|\bpackage\b|\blambda\b|\byield\b|\basync\b|\bawait\b|\bprint\b|\bprintln\b|\bmain\b|\bargs\b)'
    # )
    # # Check if the prompt_content is code
    # if code_regex.search(prompt_content):
    #     prompt_content = f"Identify the language of code snippet and provide both in-code comments along with code and detailed explanation as html.\n{prompt_content}"
    # else:
    #     prompt_content = f"Notify the user that the code provided is not valid and ask them to provide a valid code snippet, because you are a model specified to generate the comments for code snippets."
    
    print(prompt_content)   
    if not prompt_content:
        return jsonify({'error': 'Prompt content is required🫣'}), 400

    try:
        comment = prompt_logic.run_prompt_logic(prompt_content)
        # with open('output.txt', 'w') as file:
        #     json.dump(comment, file, indent=4)
        comment = markdown.markdown(comment, extensions=['extra', 'codehilite', 'toc', 'meta', 'sane_lists', 'fenced_code', 'attr_list', 'footnotes', 'tables', 'admonition', 'def_list', 'smarty', 'nl2br', 'abbr'])
        # Get the Pygments CSS for code highlighting
        pygments_style = HtmlFormatter().get_style_defs('.codehilite')
        comment = f"<style>{pygments_style}</style>\n{comment}"
        comment = re.sub(r'\n+', '\n', comment)
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
