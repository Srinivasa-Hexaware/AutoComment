# AutoComment: AI-Powered Code Comment Generator
![image](https://github.com/user-attachments/assets/2b1cc8d7-311d-44a8-9d2f-b2d65bd5039d)


## Project Overview
AutoComment is a web-based application that uses AI to generate descriptive and informative comments for code snippets. The AI can handle multiple programming languages and provides accurate comments to enhance code readability and maintainability.

## Project Structure

/project-root
│
├── app.py # Main Flask server script
├──prompt_logic # Logic to handle the send and receive response from model
├── requirements.txt # Dependencies file
│
├── templates # Folder for HTML files
│ └── index.html # Main HTML file
│
├── static # Folder for static files (CSS, JS, images)
│ ├── css
│ │ └── styles.css # CSS file
│ │
│ ├── js
│ │ └── scripts.js # JavaScript file
│ │
│ └── img
│ └── user-icon.png # User icon image
│
├── Chats # Folder to store chat history as JSON files
│ └── example_chat.json # Example JSON file for chat history
│
└── README.md # Project description and instructions


## Setup Instructions

1. Clone the repository:
git clone https://github.com/Srinivasa-Hexaware/autocomment.git
cd autocomment

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate


3. Install the dependencies:
pip install -r requirements.txt


4. Set up your OpenAI API key:
Replace `endpoint`, `apikey`, `api_version` & `deployment_name` in `config.py` with your actual AzureOpenAI API details.

5. Run the Flask application:
python app.py


6. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the AutoComment application.


## Usage

- **New Chat:** Click the "New Chat" button to start a new chat session.
- **Prompt Area:** Type your code snippet in the prompt area and press the "Send" button to generate comments.
- **Search Bar:** Use the search bar to search within the chat or application.


## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI Model:** AzureOpenAI API
- **Development Environment:** VS Code
