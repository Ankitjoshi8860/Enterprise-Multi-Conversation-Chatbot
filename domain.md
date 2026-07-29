# Domain Specification – MediAssist AI

## Project Name

MediAssist AI

---

## Overview

MediAssist AI is an AI-powered healthcare assistant built using FastAPI, GroqCloud with `llama-3.3-70b-versatile`, SQLite, and a modern web interface.

The assistant helps users understand common medical topics in simple language while maintaining conversation history across multiple chat sessions.

This project is intended for educational and portfolio purposes only and does not provide medical diagnosis or emergency healthcare advice.

---

## Disclaimer

MediAssist AI is intended for educational and informational purposes only.

It does not provide medical diagnosis, emergency assistance, or personalized treatment recommendations. Users should consult qualified healthcare professionals for medical advice.


## Primary Goal

Build a production-style AI chatbot that demonstrates:

- FastAPI backend
- GroqCloud API integration using `llama-3.3-70b-versatile`
- SQLite persistence
- Multi-conversation memory
- Modern chat interface
- REST API architecture

---

## Core Features

### Health Questions

Users can ask general healthcare questions.

Examples:

- What is diabetes?
- What causes high blood pressure?
- What are the symptoms of dengue?

---

### Disease Explanations

Explain diseases using simple, non-technical language.

Example:

Explain hypertension like I'm a beginner.

---

### Medicine Information

Provide general educational information about medicines.

Examples:

- What is Paracetamol used for?
- What are common side effects of Ibuprofen?

The assistant must not prescribe medicines.

---

### Healthy Lifestyle Advice

Provide general wellness recommendations.

Examples:

- How can I sleep better?
- Tips to reduce stress
- Healthy eating habits
- Exercise recommendations

---

### Conversation Memory

Each conversation remembers previous messages.

Users can create multiple independent conversations.

Each conversation maintains its own context.

---

## Future Enhancements

The following features are intentionally excluded from Version 1 but may be added later:

- Medical report summarization (PDF upload)
- OCR for laboratory reports
- Retrieval-Augmented Generation (RAG)
- Doctor recommendation system
- Appointment scheduling
- Voice conversation
- Image analysis
- Authentication
- Cloud deployment

---

## Safety Requirements

The assistant must:

- Never claim to be a doctor.
- Never provide emergency medical advice.
- Encourage users to consult qualified healthcare professionals for diagnosis or treatment.
- Clearly state that responses are informational only.

---

## Example User Questions

- What is diabetes?
- Explain hypertension in simple words.
- What are the symptoms of dengue?
- What causes anemia?
- How can I improve my sleep?
- What are the benefits of walking every day?
- Explain Vitamin D deficiency.

---

## Technology Stack

Backend:
- FastAPI

Database:
- SQLite

AI Model:
- GroqCloud API (`llama-3.3-70b-versatile`)

Frontend:
- HTML
- CSS
- JavaScript

Version:
- Portfolio Version 1
