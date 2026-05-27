# AI Interview Copilot

AI Interview Copilot is a fullstack interview practice platform built with FastAPI, PostgreSQL, JavaScript and JWT authentication.

The application simulates technical interview sessions, scores answers, generates AI-style feedback, tracks user performance history and displays analytics dashboards with charts and leaderboards.

---

# Features

- User registration & login
- JWT authentication
- Technical interview simulation
- Dynamic interview questions
- AI-style feedback generation
- Interview scoring system
- User-specific interview history
- Leaderboard & ranking system
- PDF interview reports
- Analytics dashboard
- Chart.js visualizations
- PostgreSQL database
- Fullstack deployment

---

# Tech Stack

## Backend
- Python
- FastAPI
- PostgreSQL
- psycopg2
- JWT Authentication
- bcrypt

## Frontend
- HTML
- CSS
- JavaScript
- Chart.js

## Deployment
- Render (backend)
- Vercel (frontend)

---

# Architecture

Frontend (Vercel)
↓
FastAPI Backend (Render)
↓
PostgreSQL Database

---

# Authentication

The application uses JWT-based authentication:

- User registration
- Secure password hashing with bcrypt
- Login token generation
- Protected API endpoints
- User-specific dashboard data

---

# AI Feedback System

The project includes a lightweight AI-style feedback engine that:

- analyzes interview answers
- scores technical responses
- generates coaching feedback
- simulates interviewer behavior

This implementation does not require paid AI APIs.

---

# Dashboard Features

Users can:

- track interview scores
- visualize progress history
- compare leaderboard rankings
- download PDF reports

---

# API Endpoints

## Authentication

### Register
POST /register

### Login
POST /login

---

## Interview

### Get Question
GET /question

### Submit Answer
POST /score

---

## Analytics

### User History
GET /history

### Leaderboard
GET /leaderboard

---

# Local Installation

## Clone repository

```bash
git clone https://github.com/nataliakloc96-ui/AI-Interview-Copilot.git
cd AI-Interview-Copilot