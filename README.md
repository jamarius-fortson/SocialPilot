# OmniViral AI

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Supported-orange.svg)](https://python.langchain.com/docs/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**OmniViral AI** is an enterprise-grade autonomous social media orchestration engine. Built with a multi-agent architecture (using LangGraph and CrewAI), it automates content generation, trend analysis, safety compliance, and scheduling across multiple platforms.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
  - [Starting the API Server](#starting-the-api-server)
  - [Launching the Dashboard](#launching-the-dashboard)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

Managing social media presence at scale requires bridging the gap between proactive strategy and reactive execution. OmniViral AI solves this by deploying specialized AI agents that act synchronously. From recognizing emerging cultural trends to generating safe, brand-aligned content, the platform orchestrates the entire lifecycle while keeping a Human-In-The-Loop (HITL) for critical approvals.

## ✨ Key Features

- **Multi-Agent Orchestration:** Utilizes LangGraph to coordinate specialized cognitive agents (TrendAnalyzer, ContentGenerator, SafetyOfficer, Accountant).
- **Asynchronous Execution:** Built on FastAPI with `BackgroundTasks` to handle non-blocking, long-running agent workflows seamlessly.
- **Brand Guardrails:** Enforces brand ethics and safety guidelines automatically, flagging high-risk content for manual human review.
- **Zero-Trust Security:** API endpoints are secured using API Key headers (`X-OmniViral-Key`).
- **Interactive Dashboard:** Includes a modern Glassmorphism frontend to monitor agents, view active trends, and approve/reject pending content.

---

## 🏗️ Architecture

The system operates on an event-driven state graph.

1. **Input:** Client provides Brand Profile (tonality, audience, banned topics).
2. **Analysis:** The `TrendAnalyzer` scans for relevant market data.
3. **Generation:** The `ContentGenerator` crafts platform-specific copy.
4. **Validation:** The `SafetyOfficer` scores the content against brand safety rules.
5. **Approval:** If safety scores mandate review, the process pauses (Awaiting Approval). Human operators approve/reject via the API/Dashboard.
6. **Execution:** Once approved, the content is queued for scheduling.

---

## ⚙️ Prerequisites

- **Python:** 3.9 or higher
- **Package Manager:** `pip`
- **Environment:** Windows, macOS, or Linux
- **API Keys:** OpenAI API Key or Anthropic API Key (depending on chosen models)

---

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/OmniViral-AI.git
   cd OmniViral-AI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Configuration

OmniViral AI relies on environment variables for sensitive configurations. 

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and configure your keys:
   ```env
   OPENAI_API_KEY=sk-your-openai-api-key
   ANTHROPIC_API_KEY=sk-your-anthropic-api-key
   MOCK_MODE=false
   ```
   *(Note: Set `MOCK_MODE=true` for local development to bypass LLM billing costs).*

---

## 🚀 Usage

### Starting the API Server

Launch the FastAPI backend server. This handles all state management and LLM orchestration.

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.*

### Launching the Dashboard

In a new terminal instance, start the administrative dashboard:

```bash
python run_dashboard.py
```
*The dashboard will securely connect to the API server to display running agents and pending content approvals.*

---

## 📡 API Reference

Authentication requires the custom header: `X-OmniViral-Key` (Default for dev: `ov_live_sk_example_123`).

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Returns the health and status of the OmniViral engine. |
| `POST` | `/client/profile` | Synchronizes a brand profile dictionary into system memory. |
| `POST` | `/run` | Dispatches an asynchronous campaign graph executing background tasks. |
| `GET` | `/task/{task_id}` | Polls the real-time status of a dispatched campaign graph. |
| `POST` | `/approve/{id}` | Grants human authorization for flagged content to proceed. |
| `POST` | `/reject/{id}` | Rejects flagged content, halting the execution graph. |

---

## 📂 Project Structure

```text
OmniViral-AI/
├── app/
│   ├── agents/          # Individual CrewAI Agent definitions
│   ├── graphs/          # LangGraph state orchestration logic
│   ├── schemas/         # Pydantic models and state dictionaries
│   ├── main.py          # FastAPI application entry point
│   └── utils.py         # Shared utility functions
├── .env.example         # Template for environment variables
├── index.html           # Frontend Dashboard markup
├── requirements.txt     # Python package dependencies
├── run_dashboard.py     # Script to launch the localhost dashboard
└── social_media_prompts.py # Central prompt repository
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve OmniViral AI, please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please ensure that tests pass and the code adheres to the project's style guidelines before submitting a PR.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
