from openai import OpenAI
import streamlit as st
import time


# Translation Bot
def translation(text, language):

    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
        {"role": "system", "content": f"You are a localisation agent. You speak in real {language} as a {language} native speakers would speak. Step 1: Don't translate word by word. Read and understand the whole things. Step 2: Write it as {language} native speakers would do. The result should keep the format and tone of the original text. It should sounds natural and reflect the {language} culture."},
        {"role": "user", "content": text},
        ],
    )
    return stream.choices[0].message.content
    
# Summary Bot
def summary(prompt):

    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
        {"role": "system", "content": f"Your task is summarising the given text in the way customers want. Follow those steps to summarise:\nStep 1: Find all key sentences, don't choose any points without context. Step 2: Shorter all key sentences into key points. The sentences should be short and precise. Step 3: Do the step 1 and 2 again.\nStep4: Put two versions together, put the content of the output in triple quotes.\nStep 5: Always format it in the desired way mentioned in the text if it is given."},
        {"role": "user", "content": prompt},
        ],
    )

    output = stream.choices[0].message.content
    
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
        {"role": "system", "content": "You will be given a summary. Choose only the content inside the triple quotes precisely. Remove triple quotes."},
        {"role": "user", "content": f'{output}'},
        ],
    )
    return stream.choices[0].message.content
    
    
# Rewrite Bot
def rewrite(prompt):

    client = OpenAI()

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
        {"role": "system", "content": f"Your task is rewriting in the way customers want."},
        {"role": "user", "content": prompt},
        ],
    )
    return stream.choices[0].message.content
   
# Implement UI using streamlit    
st.title(" :violet[TextAI]")
st.caption("A streamlit textAI powered by OpenAI LLM")    
st.divider()

# Paragraph input
text = st.text_area("Please provide the text and your request to process:", height=300, value="", help="Enjoy")
st.caption(f'You wrote {len(text)} characters.')
st.write("\n")

with st.container(border=True):
    # Feature selection
    option = st.selectbox("What would you like me to perform?", ("Summary", "Translation", "Rewrite"))

    if option == "Translation":
        lang = st.selectbox('Language', ('English', 'Vietnamese', 'Japanese', 'Chinese'))


# Button
run = st.button("Submit", type="primary")


if run:
    if option == "Summary":
        # run summary bot
        output = summary(f'{text}')
        
    if option == "Translation":
        output = translation(text, lang)
    
    if option == "Rewrite":
        output = rewrite(text)
        
    st.divider()    
    st.markdown("Result")
    st.write("\n")
    output
    
    # Waiting time
    'Waiting for the next query...'
    bar = st.progress(0)

    for i in range(100):
      # Update the progress bar with each iteration.
      bar.progress(i + 1)
      time.sleep(0.3)

    '...and now we\'re done!'
    
    