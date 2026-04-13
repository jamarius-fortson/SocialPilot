# SocialPilot — Autonomous Social Media Agent

SocialPilot is a Python-based autonomous social media workflow built around a stateful graph and specialist AI agents. It is designed to run brand-safe campaigns, generate platform-native copy, execute approvals, and schedule content with minimal manual coordination.

## What this repository is

- A FastAPI backend for `client/profile`, `run`, and approval workflows.
- A LangGraph state machine that routes tasks through trend, content, guardrails, scheduling, engagement, and analytics nodes.
- A mock-friendly mode for offline testing and product demo cycles.
- A lightweight browser dashboard launcher in `run_dashboard.py`.

## Why it matters

- Enables rapid prototyping of an autonomous marketing engine.
- Separates decision orchestration from execution logic.
- Includes human-in-the-loop approval for sensitive content.
- Supports multi-stage campaigns and specialized engagement or analytics flows.

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

2. Copy the environment template:

```bash
copy .env.example .env
```

3. Toggle mock mode for local testing:

```bash
setx MOCK_MODE true
```

4. Start the API server:

```bash
py -m uvicorn app.main:app --reload
```

5. Open the local dashboard:

```bash
py run_dashboard.py
```

## Repository layout

- `app/main.py` — FastAPI service and workflow entrypoints
- `app/graphs/orchestrator.py` — State graph configuration and routing
- `app/graphs/nodes.py` — Workflow nodes for each automation stage
- `app/agents/factory.py` — Agent factory and prompt integration
- `app/schemas/state.py` — Shared state models and validation
- `app/tools/social_tools.py` — Integration tools for agent tasks
- `social_media_prompts.py` — Specialist prompt templates

## API reference

### Create or update a client profile

`POST /client/profile`

Request body:

```json
{
  "brand_name": "Acme Co",
  "brand_voice": "conversational",
  "target_audience": "young professionals",
  "content_pillars": ["product education", "thought leadership"],
  "banned_topics": ["politics", "religion"],
  "active_platforms": ["x", "linkedin", "instagram"],
  "posting_frequency": 3,
  "primary_goal": "engagement",
  "competitor_accounts": ["@competitor"]
}
```

`client_id` is passed as a query parameter.

### Run a workflow

`POST /run`

Request body:

```json
{
  "client_id": "client-123",
  "task_type": "campaign"
}
```

Supported `task_type` values:
- `campaign`
- `content`
- `engagement`
- `analytics`
- `scheduling`

### Approve flagged content

`POST /approve/{approval_id}`

This resumes the workflow after guardrails flag content for manual review.

### Reject flagged content

`POST /reject/{approval_id}`

Use this endpoint to reject content and return a feedback message.

## Improvements applied

- Fixed workflow agent creation in `app/graphs/nodes.py` for content generation and campaign scheduling.
- Strengthened `README.md` with installation, architecture, and API usage.

## Notes for GitHub upload

- Keep `.env` private and do not commit secrets.
- Use the existing `.gitignore` to exclude logs, virtual environments, and environment files.
- If you want, I can also help prepare a commit message and a polished GitHub description for your repo.
