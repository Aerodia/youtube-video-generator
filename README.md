**YouTube Video Content Generator**

This application helps content creators quickly generate catchy YouTube video titles and detailed, SEO-optimized video descriptions based on a provided script or summary. It consists of a React frontend and a Flask backend that leverages the Google Gemini API for powerful text generation.

#Features:
1.Frontend (React): A user-friendly interface to input video scripts/summaries and display generated titles and descriptions.
2.Backend (Flask): A lightweight API that handles requests from the frontend, communicates with the Google Gemini API, and processes the AI-generated responses.
3.AI-Powered Generation: Utilizes state-of-the-art Large Language Models (LLMs) from Google Gemini to create relevant and engaging content.


#Technologies Used
Frontend: React.js, HTML, CSS
Backend: Flask, Python 3.9+, requests, python-dotenv, google-generativeai, gunicorn
AI Model: Google Gemini API (models/gemini-1.5-flash-latest or similar)

#Prerequisites
Before you begin, ensure you have the following installed on your machine:

Node.js & npm: https://nodejs.org/en/download/ (npm is included with Node.js)
Python 3.9+: https://www.python.org/downloads/
pip: Python's package installer (usually comes with Python)
Git: https://git-scm.com/downloads
Google AI Studio API Key:
  Go to https://ai.google.dev/
  Sign in with your Google account.
  Click on "Get API key" in the left sidebar.
  Click "Create API key in new project".
  Copy the generated API key immediately and keep it safe.


#Setup & Local Development
Follow these steps to get the application running on your local machine.

1. Clone the Repository
git clone https://github.com/your-username/youtube-video-generator.git # Replace with your repo URL if you fork it
cd youtube-video-generator

2. Backend Setup (Flask API)
Navigate into the backend directory, create a virtual environment, install dependencies, and configure your API key.

cd backend

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
  On macOS/Linux:
    source venv/bin/activate
  On Windows (Command Prompt/PowerShell):
    .\venv\Scripts\activate
  On Windows (Git Bash/MinGW):
    source venv/Scripts/activate
# Install Python dependencies
pip install -r requirements.txt

Create .env file: In the youtube-video-generator root directory (one level up from backend), create a file named .env.

# Go to the root directory
cd ..

# Create the .env file
touch .env # On Windows, you might need to use `notepad .env` or similar
Configure .env: Open the newly created .env file and add your Google API key and the desired Gemini model.

GOOGLE_API_KEY="YOUR_API_KEY_FROM_GOOGLE_AI_STUDIO"
GOOGLE_GEMINI_MODEL="models/gemini-1.5-flash-latest" # Recommended for this project

Important: Replace "YOUR_API_KEY_FROM_GOOGLE_AI_STUDIO" with the actual API key you obtained from Google AI Studio.

3. Frontend Setup (React App)
Navigate into the frontend directory and install JavaScript dependencies.

cd frontend

# Install Node.js dependencies
npm install

4. Run the Backend
Make sure your virtual environment is active in the backend directory.

cd ~/youtube-video-generator/backend # Ensure you are in the backend directory

# (venv)
python app.py

You should see output indicating the Flask app is running, typically on http://127.0.0.1:5000. Keep this terminal open.

5. Run the Frontend
In a new terminal window, navigate into the frontend directory and start the React development server.

cd ~/youtube-video-generator/frontend # Ensure you are in the frontend directory
npm start

This will open the React app in your web browser, usually at http://localhost:3000/.

Now you can interact with the application locally! Input your video script or summary and generate content.
