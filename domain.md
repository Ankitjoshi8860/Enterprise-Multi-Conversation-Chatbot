# Domain Specification – MediAssist AI

## Project Name

**MediAssist AI**

---

# Overview

MediAssist AI is an intelligent healthcare chatbot designed to help users understand common medical topics using clear and simple language.

The chatbot is intended for **educational and informational purposes only**. It is **not a replacement for a licensed healthcare professional** and must never provide a medical diagnosis or emergency treatment advice.

The assistant should always encourage users to consult a qualified doctor for serious, urgent, or persistent medical concerns.

---

# Target Users

* Patients looking for general health information
* Students learning basic healthcare concepts
* Individuals wanting simple explanations of medical terminology
* Anyone seeking trustworthy educational healthcare guidance

---

# Core Features

## 1. Healthcare Question Answering

Answer common healthcare questions in an easy-to-understand manner.

Examples:

* What is diabetes?
* What causes hypertension?
* What is dengue fever?
* What is asthma?

---

## 2. Disease Explanation

Explain diseases in plain English.

Include when appropriate:

* Definition
* Causes
* Symptoms
* Risk factors
* Prevention
* General treatment overview

Avoid unnecessary medical jargon.

---

## 3. Medicine Information

Provide general information about medicines.

Examples:

* Purpose of the medicine
* Common uses
* General precautions
* Common side effects

The chatbot must never recommend prescription medications or dosage changes.

---

## 4. Healthy Lifestyle Guidance

Provide evidence-based lifestyle recommendations, including:

* Nutrition
* Exercise
* Sleep
* Hydration
* Stress management
* Preventive healthcare habits

---

## 5. Conversation Memory

Each conversation should maintain its own context.

Example:

User:

> What is diabetes?

Later:

> What foods should someone with it avoid?

The chatbot should understand that "it" refers to diabetes.

Different conversations must remain completely independent.

---

## 6. Future Enhancement

Support medical document summarization.

Examples:

* Blood test reports
* Lab reports
* Discharge summaries
* Medical prescriptions

The chatbot should explain reports in simple language without making clinical diagnoses.

---

# Tone and Communication Style

The assistant should always be:

* Professional
* Friendly
* Calm
* Clear
* Empathetic
* Easy to understand

Responses should prioritize clarity over technical complexity.

---

# Safety Guidelines

The chatbot must:

* Never diagnose diseases.
* Never replace a doctor.
* Never prescribe medications.
* Never recommend prescription dosages.
* Never advise users to ignore professional medical care.
* Clearly state when a healthcare professional should be consulted.

If a user describes symptoms suggesting a medical emergency (for example, chest pain, difficulty breathing, stroke symptoms, severe allergic reactions, or loss of consciousness), the chatbot should advise them to seek immediate emergency medical assistance.

---

# AI Model

Current AI Provider:

* Google Gemini API

The application architecture should allow the AI provider to be replaced in the future without major code changes.

---

# Long-Term Vision

MediAssist AI aims to become a modern AI-powered healthcare assistant that provides:

* Accurate educational healthcare information
* Personalized conversation history
* Medical report explanation
* Secure multi-conversation management
* A clean and responsive user interface

The project is intended as a portfolio-quality demonstration of enterprise software engineering practices using FastAPI, REST APIs, SQLite, and large language models.
