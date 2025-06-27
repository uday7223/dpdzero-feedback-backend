# 🚀 DPDzero Feedback System - Backend

A secure, lightweight, and production-ready backend built using **FastAPI** and **PostgreSQL**, designed to handle structured feedback within teams.  
Developed as part of the **DPDzero Fullstack Developer Internship Assignment**, this backend powers role-based feedback flows, JWT authentication, and secure data access — all fully containerized using Docker.

---

## 📦 Tech Stack

- **FastAPI** – Modern, high-performance Python web framework
- **PostgreSQL** – Reliable, scalable relational database
- **SQLAlchemy** – ORM for database interaction
- **Pydantic** – Data validation for request/response models
- **Docker & Docker Compose** – Seamless containerization
- **Passlib + bcrypt** – Password hashing for secure authentication
- **JWT (JSON Web Tokens)** – Secure token-based login system

---

## ✅ Features Implemented :

### 🔐 Secure Authentication & Role Management

- **JWT-based login system** with secure access tokens
- **Password hashing with bcrypt** at registration and login
- Role-based access control:
  - **Managers** see and manage feedback for only their team
  - **Employees** access only their own feedback
- Protected routes with full token-based authorization

### 💬 Feedback Functionality

- Managers can submit structured feedback including:
  - **Strengths**
  - **Areas to Improve**
  - **Overall Sentiment**: Positive / Neutral / Negative
- Feedback history available to both managers and employees
- Employees can **acknowledge** feedback they've read
- Managers can **edit/update** previously given feedback

### 📊 Dashboard-Ready API Endpoints

- **Manager view**: Aggregated team feedback stats and sentiment tracking
- **Employee view**: Chronological timeline of feedback received

---

## 🐳 Run with Docker

### 🔧 Prerequisites

- Docker
- Docker Compose

### 🛠️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/<your-username>/dpdzero-feedback-backend.git
cd dpdzero-feedback-backend

# Build and run the containers
docker-compose up --build

API Docs (Swagger): http://localhost:8000/docs

## Project Structure
dpdzero-feedback-backend/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── models.py          # SQLAlchemy models (User, Feedback, etc.)
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # PostgreSQL DB connection setup
│   ├── auth.py            # JWT token creation and validation
│   ├── utils.py           # Password hashing, role utils
│   └── routers/           # Route handlers organized by feature
│       ├── users.py       # User registration & authentication
│       ├── feedback.py    # Feedback CRUD endpoints
│       └── dashboard.py   # Manager/Employee dashboard endpoints
├── Dockerfile             # Backend Docker configuration
├── docker-compose.yml     # Backend + PostgreSQL services
├── requirements.txt       # Python dependencies
└── README.md              # You're reading it!

🧠 Design Decisions
🔐 JWT with bcrypt: Ensures secure login, session management

🧱 Clean, scalable architecture: Follows separation of concerns

🐳 Docker-first development: Easily portable, ideal for deployment

⚡ FastAPI built-in docs: Streamlined API testing and debugging

👨‍💻 Author
Uday Kumar N
🔧 Fullstack Developer — Internship Assignment Submission
📁 GitHub: @udaykumar223
🌐 LinkedIn: linkedin.com/in/udaykumarn