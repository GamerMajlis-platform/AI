import os
import json
from dotenv import load_dotenv
from groq import Groq
import queries 
from static_intents import static_responses


# Load env vars
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# Init Groq client
client = Groq(api_key=API_KEY)

def chat_with_llm(prompt: str):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": open("system_prompt.txt").read()},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_completion_tokens=256,
    )
    return completion.choices[0].message.content



def format_with_model(intent: str, results):
    if results == "None currently":
        return results
    
    prompt = f"""
    You are a helpful assistant. 
    The user asked for: {intent}.
    Here are the raw database results: {results}
    Please format this into a natural, user-friendly response, make it in bullet points and add emojies 
    like use the emojis that represnt the point as the bullet point.
    """
    return chat_with_llm(prompt)



def handle_intent(intent: str, entities: dict = None):
    # If it's static info
    if intent in static_responses:
        return static_responses[intent]

    # If it's DB-based
    sql = queries.get_query(intent)
    return format_with_model(intent,sql)


if __name__ == "__main__":
    print("Chatbot ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("LLM: Goodbye 👋")
            break

        # Step 1: Ask LLM for intent & entities
        intent_prompt = f"""
        Extract the intent and any entities from this question.
        If no database lookup is needed, set "intent" to "none".
        Don't ever make up fake data.
        Answer in JSON only. Example:
        {{"intent": "next_event"}}
        or
        {{"intent": "none"}}

        User: {user_input}
        """
        response = chat_with_llm(intent_prompt)

        try:
            parsed = json.loads(response)
            intent = parsed.get("intent", "none")
            entities = {k: v for k, v in parsed.items() if k != "intent"}
        except Exception:
            print("LLM: Sorry, I didn’t understand that. (Parsing error)")
            continue

        # Step 2: Handle database intent or fallback
        if intent == "none":
            # Just let LLM answer naturally
            reply = chat_with_llm(user_input)
            print("LLM:", reply)
        else:
            results = handle_intent(intent, entities)
            if results:
                print("LLM:", results)
            else:
                # Fallback: LLM answers normally
                reply = chat_with_llm(user_input)
                print("LLM:", reply)
