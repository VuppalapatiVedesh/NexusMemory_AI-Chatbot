# NexusMemory AI Chatbot

NexusMemory AI is a clean, modern, and production-quality chatbot application built with a Python (Flask) backend and a highly polished Glassmorphic dark-theme frontend using HTML, CSS, and Vanilla JavaScript. 

It integrates the latest **OpenAI Python SDK** configured to connect directly with the **Groq API** (e.g. `llama-3.3-70b-versatile` model) to deliver near-instantaneous responses. A key feature is its **long-term session memory** which stores the complete conversation history on the server-side, enabling context-aware discussions without hitches.

---

## Key Features

1. **Long-Term Session Memory**: Avoids client-side browser cookie limits (4KB) by holding the message history in server memory mapped to unique browser session UUIDs.
2. **Context-Aware Responses**: Always passes the complete chat session history to the LLM so the AI can track preferences, reference earlier topics, and respond like a real human assistant.
3. **Markdown Rendering**: Formats AI responses using `marked.js` to render lists, bold texts, and paragraphs.
4. **Code Syntax Highlighting**: Leverages `highlight.js` with the Tokyo Night Dark theme to display source code beautifully inside message bubbles.
5. **Glassmorphic Dark Theme**: Premium UI designed with responsive CSS, pulsing background gradients, dynamic status states, bounce-dots typing indicators, and micro-animations.
6. **Error Handling**: Graceful error UI that highlights problems such as missing API keys or backend connectivity issues.
7. **Clean Structure**: Beginner-friendly architecture separating backend routes, memory stores, and AI generation logic.

---

## Project Structure

```text
AI-ChatBot/
│
├── app.py              # Main Flask application and API route mapping
├── chatbot.py          # Groq API interaction via the OpenAI Python SDK
├── memory.py           # In-memory session tracking and history store
├── requirements.txt    # Python dependencies list
├── .env.example        # Environment variable configuration template
├── README.md           # Documentation and guides (this file)
├── .gitignore          # Version control file exclusions
│
├── templates/
│   └── index.html      # Glassmorphic user interface structure
│
└── static/
    ├── style.css       # Complete layout styling, colors, and keyframe animations
    └── script.js       # Dynamic AJAX logic, Markdown processing, and DOM updates
```

---

## Requirements

Ensure you have the following installed on your system:
- Python 3.8 or higher
- A Groq API Key (obtainable from the [Groq Console](https://console.groq.com/))

---

## Installation & Setup

Follow these steps to run the chatbot application locally:

### 1. Clone or Download the Project
```bash
git clone https://github.com/your-username/AI-ChatBot.git
cd AI-ChatBot
```

### 2. Set Up a Virtual Environment (Recommended)
Creating a virtual environment ensures that the project's dependencies do not conflict with other Python installations on your machine.

**On Windows (Command Prompt / PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all package requirements listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
1. Copy the template `.env.example` file to create your local `.env` configuration:
   ```bash
   cp .env.example .env
   ```
   *(On Windows Command Prompt, run: `copy .env.example .env`)*

2. Open the `.env` file and replace the placeholders:
   ```env
   # Secure random key for cookie sessions (change this in production)
   FLASK_SECRET_KEY=generate_a_random_key_here
   
   # Add your actual Groq API key
   GROQ_API_KEY=gsk_your_actual_groq_api_key_goes_here
   ```

---

## How to Run

1. Make sure your virtual environment is active.
2. Launch the Flask application:
   ```bash
   python app.py
   ```
3. The server starts running locally at `http://127.0.0.1:5000`.
4. Open your web browser and navigate to `http://127.0.0.1:5000` to start chatting!

---

## Screenshots Placeholder

Once running, the application features:
- **Desktop Sidebar view**: Showing information, tech stack, and clear button.
- **Responsive Layout**: Hides the sidebar on mobile devices for optimized focus on messaging.
- **Glassmorphic Theme**: Dark gradient background with subtle neon ambient lights.

*(Add screenshots here when deploying to GitHub)*

---

## Future Improvements

For further iterations, consider adding:
1. **Persistent Databases**: Replace the in-memory server dictionary in `memory.py` with a Redis cache or a SQL database (like SQLite/PostgreSQL) to persist history across server restarts.
2. **Multiple Chat Rooms**: Allow users to save, switch, and delete multiple historical threads in the sidebar.
3. **Voice Input/Output**: Integrate Web Audio APIs for text-to-speech and speech-to-text.
4. **Export Formats**: Allow users to download chat logs as TXT, JSON, or Markdown documents.

---

## License

This project is open-source and available under the [MIT License](LICENSE). Feel free to use, modify, and distribute it for learning or college submissions.
