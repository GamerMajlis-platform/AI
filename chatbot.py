import os
import re
import mysql.connector
from dotenv import load_dotenv
from groq import Groq

# load env vars
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# init client with key
client = Groq(api_key=API_KEY)

# connect to MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

def run_query(sql: str):
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if not rows:
            # detect which table the query is about
            sql_lower = sql.lower()
            if "from events" in sql_lower:
                return "There are no upcoming events at the moment."
            elif "from tournaments" in sql_lower:
                return "There are no upcoming tournaments right now."
            elif "from products" in sql_lower:
                return "No products are currently available."
            elif "from products_reviews" in sql_lower:
                return "No product reviews found yet."
            elif "from user_roles" in sql_lower:
                return "That user doesn’t seem to have a role assigned."
            elif "from chat_room_members" in sql_lower:
                return "There are no members in this chat room yet."
            elif "from event_attendances" in sql_lower:
                return "No one has registered attendance for this event yet."
            elif "from tournaments_participations" in sql_lower:
                return "No one has registered for this tournament yet."
            else:
                return "No relevant data found."

        # format output into text
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        if len(results) == 1:
            return ", ".join(f"{k}: {v}" for k, v in results[0].items())
        else:
            return "\n".join([", ".join(f"{k}: {v}" for k, v in r.items()) for r in results])
    except Exception as e:
        return f"Sorry, I couldn’t run that query. Error: {e}"


def chat_with_llm(prompt: str):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": open("system_prompt.txt").read()},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_completion_tokens=512,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("Chatbot ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("LLM: Goodbye 👋")
            break

        reply = chat_with_llm(user_input)

        # check if LLM gave SQL query
        sql_match = re.search(r"```sql\n(.*?)\n```", reply, re.DOTALL)
        if sql_match:
            sql_query = sql_match.group(1).strip()
            results = run_query(sql_query)
            print("LLM:", results)
        else:
            print("LLM:", reply)
