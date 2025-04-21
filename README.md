# 🧠 Mental Health Support Agent 🤗

![Mental Health Support](https://img.shields.io/badge/Mental%20Health-Support-brightgreen)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Next.js](https://img.shields.io/badge/Frontend-Next.js-000000)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20GPT--4o-74aa9c)

## 📋 Overview

A compassionate AI-powered mental health assistant designed to provide support, empathy, and guidance to individuals navigating life's challenges. This application combines a **FastAPI** backend with a **Next.js** frontend to create a responsive and empathetic conversational experience.

## ✨ Features

| 🌟 Feature | 📝 Description |
|------------|---------------|
| 💬 Empathetic Conversations | The agent actively listens and responds with compassion and understanding |
| 🛠️ Tool Integration | Provides real-time information through integrated tools |
| 🔒 Safety Guardrails | Ensures conversations stay within mental health support boundaries |
| 📱 Responsive Interface | Clean user interface for easy interaction on any device |
| 📊 Message History | Keeps track of conversation context for meaningful exchanges |

## 🚀 Project Structure

```
Mental-Health-Support-Agent/
├── 📂 backend/               # FastAPI server
│   ├── 📂 src/
│   │   ├── 📂 models/        # Pydantic models
│   │   ├── 📂 routes/        # API endpoints
│   │   ├── 📂 tools/         # Agent tools
│   │   └── 📂 utils/         # Helper functions
│   └── 📄 run.py            # Entry point
└── 📂 frontend/              # Next.js client
    ├── 📂 public/           # Static assets
    └── 📂 src/
        ├── 📂 app/          # Next.js pages
        └── 📂 components/   # React components
```

## 🔧 Upcoming Enhancements

- 📚 **Reading Help**: Resources and recommendations for mental health literature
- 🧘 **Meditation Help**: Guided meditation exercises and mindfulness techniques
- 💾 **Database Integration**: Persistent storage for user conversations and preferences
- 🤖 **Telegram Bot**: Extended reach through Telegram messaging platform

## 🛠️ Technical Implementation

The agent is powered by OpenAI's **GPT-4o** model, enhanced with custom tools and guardrails:

### Backend

- **FastAPI** framework for high-performance API endpoints
- Custom tool integrations for enhanced capabilities
- Safety guardrails to ensure appropriate conversation topics

### Frontend

- **Next.js** with **React** for a responsive user interface
- Real-time streaming responses for natural conversation flow
- Markdown support for formatted responses

## 💻 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key

### Installation

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the server
python run.py
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your settings

# Run the development server
npm run dev
# or
pnpm dev
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to help improve the Mental Health Support Agent.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

Created with ❤️ by [Raj Kapadia](https://github.com/RajKKapadia)