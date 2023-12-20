import streamlit as st
from openai import OpenAI


# Base knowledge for chatbot
f = open("textBotData.txt", "r", encoding="utf-8")
data = f.read()
f.close()

f = open("textBotRules.txt", "r", encoding="utf-8")
rules = f.read()
f.close()

knowledge = f'\"""{data}\"""'

# Customer service agent chatbot
def agent(prompt, past=""):

    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
        {"role": "system", "content": "Act like you are a professional customer service agent providing accurate information to customers about the app.\n" + rules + "\n" + knowledge + "\n" + past},
        {"role": "user", "content": prompt},
        ],
    )
    return stream.choices[0].message.content
    
# UI
st.markdown("# TextBot")

if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Can I assist you with any enquiries?"}]
    
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

past = ""

if prompt := st.chat_input():

    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    msg = agent(prompt, past)
    past += f"User: {prompt}\nYou: {msg}" 
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)