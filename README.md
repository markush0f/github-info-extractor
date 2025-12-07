# User Info Bot – Local Installation Guide

This project is an advanced chatbot capable of responding with **real information about the user**, combining web scraping via **HeadlessX**, GitHub repository analysis, vector-based semantic search, and a RAG (Retrieval-Augmented Generation) architecture using the OpenAI API.

Below is a complete guide to running the project **locally**, including Docker for the database, environment variables, and backend startup.

---

## 1. Requirements

* Python 3.11+
* Docker & Docker Compose
* Git
* An OpenAI API Key

---

## 2. Clone the Repository

```bash
git clone https://github.com/markush0f/user-info-bot.git
cd user-info-bot
```

---

## 3. Install and Configure HeadlessX

This project requires **HeadlessX** to enable advanced dynamic web scraping.

📌 **HeadlessX repository & documentation:**
[https://headlessx.saify.me/#api](https://headlessx.saify.me/#api)

Follow the instructions in their documentation to set up the service and generate your API keys.

---

## 4. Environment Variables

Create a `.env` file in the project root with the following structure:

```env
# OPENAI
OPENAI_API_KEY=

# DATABASE
USER_DB=
PASSWORD_DB=
DATABASE=
HOST=
PORT=
# REQUIRED if you use PSYCOPG2,
# SSL=require

# GITHUB
GITHUB_TOKEN=

# HEADLESSX
# Or use: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
HEADLESSX_AUTH_TOKEN=
HEADLESSX_API=
```

---

## 5. Start the Database with Docker

Run PostgreSQL using Docker Compose:

```bash
docker compose up -d
```

---

## 6. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 7. Run the Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

📌 **Important:**
All database tables are automatically created on startup using SQLModel — no migrations are required.

Your server will be available at:

```
http://localhost:8000
```

Interactive API docs:

```
http://localhost:8000/docs
```

---

## 8. Summary

With this guide, you can run the project locally with:

* PostgreSQL using Docker
* FastAPI backend fully configured
* Automatic table creation using SQLModel
* Complete environment variables for development or production
* HeadlessX integrated for dynamic web scraping

If you would like a section for VPS deployment, full Dockerization of the backend, or a diagram explaining the system architecture, I can add it.
