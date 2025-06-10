# Structured-Data-Extraction-from-NCERT
# 📘 Structured Data Extraction from NCERT Class 6 Textbooks

This project focuses on converting unstructured educational content from NCERT Class 6 Science and Mathematics textbooks into a structured, machine-readable format. It enables downstream applications like semantic search, educational chatbots, and curriculum mapping through hierarchical content extraction using AI models.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Sample Output](#sample-output)
- [Applications](#applications)
- [Contributors](#contributors)

---

## 🧠 Overview

Educational content is typically locked in unstructured formats like PDFs. This project leverages open-source LLMs and prompt engineering to extract:
- Chapters
- Topics
- Sub-topics
- Definitions
- Question-Answer pairs
- Formulae

All data is exported in structured formats (Excel/JSON) for ease of access and integration.

---

## 🎯 Objectives

- Extract chapter-wise structured data from NCERT Class 6 Science and Math books.
- Automate the identification of pedagogical elements: Q&A, definitions, and formulas.
- Build a dataset that supports curriculum-aligned educational applications.

---

## 🛠️ Tech Stack

| Tool/Library     | Purpose                            |
|------------------|------------------------------------|
| Python           | Core scripting                     |
| Pandas           | Data transformation and export     |
| PyMuPDF / pdfplumber | PDF text extraction         |
| Ollama + Mistral/LLaMA3 | Local LLM inference         |
| OpenAI-compatible prompts | Prompt engineering       |
| Excel/JSON       | Output formats                     |

---

## 🧱 Architecture


---

## ⚙️ How It Works

1. **Text Extraction**: Uses `pdfplumber` or `PyMuPDF` to extract content from textbook PDFs.
2. **Prompt Engineering**: Carefully crafted prompts help LLMs identify educational structure.
3. **Model Use**: Utilizes local LLMs (Mistral, LLaMA3) through the Ollama interface.
4. **Data Structuring**: Content is grouped by chapter-topic-subtopic in Excel sheets.

---

## 📂 Sample Output

> A sample Excel output contains columns like:
- Chapter
- Topic
- Sub-topic
- Content Type (e.g., Definition, QA, Formula)
- Content

---

## 🚀 Applications

- Question Answering Systems
- Curriculum Mapping
- Chatbot Knowledge Bases
- AI-Powered Learning Platforms
- Flashcard Generation

---

## 👨‍💻 Contributors

- **Vatsalya Shivhare** – Prompt Engineering, LLM Integration, Data Pipeline

---


