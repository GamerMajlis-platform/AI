# GamerMajlis Chatbot

Welcome to the **GamerMajlis Chatbot** repository! This project is a **mini-RAG-based chatbot system** designed for the gaming platform **GamerMajlis**, aimed at enhancing user experience and answering platform-related questions efficiently.

---

## 🚩 Platform Overview

**GamerMajlis** is a gaming platform that allows users to connect with other gamers, buy gaming gear, participate in events and tournaments, communicate seamlessly and access all gaming-related services in one place

The **chatbot** was designed to **simplify user interactions** and provide immediate answers to both static and dynamic questions.

---
## 🚩 Repository Structure

Here’s a breakdown of the files and their purpose:

| File / Folder                              | Description                                                                      |
| ------------------------------------------ | -------------------------------------------------------------------------------- |
| [`chatbot.py`](./chatbot.py)               | Main chatbot script that initializes without the Gradio UI and connects the system.      |
| [`db_connection.py`](./db_connection.py)   | Database connection logic for dynamic queries.                                   |
| [`queries.py`](./queries.py)               | Maps intents to SQL queries for dynamic platform questions.                      |
| [`static_intents.py`](./static_intents.py) | Dictionary of **static intents** and their responses.                            |
| [`system_prompt.txt`](./system_prompt.txt) | LLM prompt that sets its **role and rules**, including “no fake data.”           |
| `README.md`                                | Documentation for the project (this file).                                       |

## 🚩 How the Chatbot Works

The system relies on a **built-in LLM** called **`meta-llama/llama-4-scout-17b-16e-instruct`**, which is responsible for understanding queries and generating responses.

### Question Types

The chatbot can handle **three main types of user questions**:

1. **General Questions**

   * Not related to the platform.
   * Directly answered by the LLM.

2. **Dynamic Platform Questions**

   * Questions about **events, tournaments, or products** (dynamic data that changes).
   * The chatbot first identifies an **intent** from the question.
   * Each intent is mapped to a **specific database query**.
   * The result is formatted and sent back to the LLM for a **user-friendly response**.

3. **Static Platform Questions**

   * Questions that **don’t change**, e.g., “How do I change my password?”
   * Handled via a **predefined dictionary** called [**`static_intents.py`**](./static_intents.py).
   * LLM provides natural responses based on these static intents.

---

## 🚩 Key Features

* **Intent Extraction** – Each question generates an **intent key** to map queries securely.
* **Dynamic Queries** – Queries only run when needed, minimizing unnecessary database access.
* **Static Intents** – Common, unchanging questions are answered efficiently without querying the database.
* **Safety Prompting** – The LLM **never generates fake data**. If information is missing, it explicitly says so.
* **Customizable UI** – Built using **Gradio**, fully styled with CSS for a smooth user experience.

---



> **Note:** The `.env` file contains sensitive keys and is ignored in Git.

---

## 🚩 How to Run Locally

Follow these steps to get the project running on your machine:

```bash
# Clone the repository
git clone https://github.com/GamerMajlis-platform/AI.git
cd AI

# Install dependencies
pip install -r requirements.txt
```

### Configure Environment

1. Create a `.env` file with the following structure:

```
GROQ_API_KEY=<your_groq_api_key>
DATABASE_NAME=<your_db_name>
DATABASE_USER=<your_db_user>
DATABASE_PASSWORD=<your_db_password>
```

2. Ensure your **database matches** the queries in `queries.py`, or customize it.

3. Create a **Gradio API key** if required.

4. Run the chatbot:

```bash
python chatbot.py
```

Your Gradio UI will launch locally, ready for testing.

---

## 🚩 Customization Tips

* **Dynamic Tables / Queries:** Adjust `queries.py` to match your database structure.
* **Static Intents:** Modify `static_intents.py` for additional FAQs.
* **LLM Prompt:** Update `system_prompt.txt` to guide the chatbot behavior.
* **UI Customization:** Update CSS in `chatbot.py` to adjust colors, sizes, or layout.

---

### Database Query Flow

> Dynamic question → intent from queries → query → LLM formatting → response
> Static question → intent from ststic → query → LLM formatting → response
> Other question → LLM response 
