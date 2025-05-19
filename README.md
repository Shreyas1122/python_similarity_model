# 🔍 Skill Recommender API with Flask & Cosine Similarity

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📘 Overview

This is a **Skill Recommendation API** developed using **Python Flask**. The purpose of this API is to recommend the most relevant skill to a user based on what they want to learn, using **cosine similarity** for comparing skill names.

For example:

> If a user named Aditya wants to learn **Digital Marketing**, the API will analyze this input, compare it with a database of existing skills, and return the best-matched skill like **Digital Marketing** itself or similar skills such as **SEO** or **Social Media Marketing**.

---

## 🧠 How It Works

1. The user submits a skill they are interested in learning.
2. The input is processed and compared with the existing skills in the database.
3. Cosine similarity is applied to measure the closeness between the input and each skill.
4. The API returns the most similar skill as the recommendation.

---

## ⚙️ Tech Stack

- **Python** - Core language
- **Flask** - Web framework for API development
- **Scikit-learn** - Used for cosine similarity and text vectorization
- **Pandas** - For working with datasets
- **JSON** - Input and output format for the API

---

## 🖼️ Project Preview

### 🔁 Database example

![Recommendation Flow](images/recommendation-flow.png)

### 📩 Sample API Request and Response

![API Example](images/api-example.png)

---

## 📂 Project Structure

