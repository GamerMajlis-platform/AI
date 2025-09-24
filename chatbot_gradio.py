import os
import json
from dotenv import load_dotenv
from groq import Groq
import gradio as gr

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
    Please format this into a natural, user-friendly response, make it in bullet points and add emojis 
    like use the emojis that represent the point as the bullet point.
    """
    return chat_with_llm(prompt)


def handle_intent(intent: str, entities: dict = None):
    if intent in static_responses:
        return static_responses[intent]

    sql = queries.get_query(intent)
    return format_with_model(intent, sql)


def chatbot_fn(user_input, history):
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
        bot_reply = "Sorry, I didn’t understand that. (Parsing error)"
        history.append((user_input, bot_reply))
        return history, ""

    if intent == "none":
        bot_reply = chat_with_llm(user_input)
    else:
        results = handle_intent(intent, entities)
        bot_reply = results if results else chat_with_llm(user_input)

    history.append((user_input, bot_reply))
    return history, ""


# 🔹 Custom CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Roboto+Serif:wght@400;600&display=swap');

.gradio-container {
    background: linear-gradient(160deg, #C4FFF9, #1C2541);
    font-family: 'Roboto Serif', serif !important;
    display: flex;
    justify-content: center;   /* center horizontally */
    align-items: center;       /* center vertically */
    min-height: 100vh;         /* allow breathing space */
    padding: 40px 0;
}

/* Card wrapper for chatbot + input */
.main-card {
    max-width: 1200px;
    max-height: 90vh;          /* prevent stretching full screen */
    width: 100%;
    margin: auto;         
    border-radius: 20px;
    background: rgba(28, 37, 65, 0.85);
    padding: 10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
    align-items: center;      
    overflow: hidden;
}

/* Header row */
.header-row {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 20px;
    margin-bottom: 20px;
}

.header-row img {
    height: 180px;
    width: 180px;
}

.header-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.header-text h1 {
    margin: 0;
    color: #C4FFF9;
    font-size: 28px;
}

.header-text p {
    margin: 0;
    color: #E0F7FA;
    font-size: 15px;
}

/* Entire Chatbox container */
#gamer_chatbox,
#gamer_chatbox > div {
  border-radius: 30px !important;
  overflow: hidden !important;
  background: #C4FFF9 !important;
  padding: 20px !important;
  height: 400px !important;
  box-shadow: 0 8px 25px rgba(0,0,0,0.25) !important;
}

/* Kill ugly default title bar + icons */
#gamer_chatbox .wrap,
#gamer_chatbox label,
#gamer_chatbox .title,
#gamer_chatbox .chatbot-label,
#gamer_chatbox .delete,
#gamer_chatbox .icon,
#gamer_chatbox .copy-code,
#gamer_chatbox .copy-button {
    display: none !important;
}
button[aria-label="Clear"] {
    display: none !important;  /* hides delete/trash forever */
}
#gamer_chatbox > div:first-child {
    display: none !important;
}

/* Clear inner wrapper backgrounds */
#gamer_chatbox .bubble-wrap,
#gamer_chatbox .message-wrap,
#gamer_chatbox .placeholder-content,
#gamer_chatbox .overflow-y-auto,
#gamer_chatbox .chatbot-container {
  background: transparent !important;
}

/* Message bubbles */
#gamer_chatbox .user-row .message {
    background-color: #0f172a; 
    color: #fff !important;
    border-radius: 22px !important;
    padding: 5px 8px !important;
    font-size: 15px !important;
    max-width: 100% !important;
    display: inline-block !important;
    word-wrap: break-word !important;
    white-space: pre-wrap !important;
}

#gamer_chatbox .bot-row .message {
    background-color: #1C2541 !important;
    color: #fff !important;
    border-radius: 22px !important;
    padding: 5px 8px !important;
    font-size: 15px !important;
    max-width: 100% !important;
    display: inline-block !important;
    word-wrap: break-word !important;
    white-space: pre-wrap !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    logo_url = "https://cdn.discordapp.com/attachments/1402333446969360497/1403058351851704511/20250807_1951_Gamer_Platform_Logo_remix_01k22q0xj0f0zax3wp3dx9yerb.png?ex=68d4caaa&is=68d3792a&hm=6acc0a57fca1bccbc032cc6081ef27cb77e2554ac887fb620fcf0e9f91f89f5f&"
    with gr.Column(elem_classes="main-card"):
        gr.HTML(f"""
            <div class="header-row">
                <img src="{logo_url}" alt="Logo">
                <div class="header-text">
                    <h1>GamerMajlis Chatbot</h1>
                    <p>Your AI guide for our platform!</p>
                </div>
            </div>
        """)

        chatbot = gr.Chatbot(elem_id="gamer_chatbox", height=480, label="")
        
        # ✅ Only input textbox, no clear button
        msg = gr.Textbox(
            placeholder="Type your message...", 
            lines=1, 
            elem_id="gamer_input"
        )

        msg.submit(chatbot_fn, [msg, chatbot], [chatbot, msg])

if __name__ == "__main__":
    demo.launch(share=True)
