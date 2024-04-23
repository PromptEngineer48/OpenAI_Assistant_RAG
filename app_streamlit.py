from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_APIKEY"))

assistant_id = "asst_Z5PX4No30szF2QfS6ile64xS"
thread = client.beta.threads.create()
thread_id = thread.id

st.title("Prompt Engineer's Chatbot")


def chatter(user_input):

    # Add the user message to the Thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input,
    )

    print("thread_id=>", thread_id)

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )

    messages = list(
        client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id)
    )

    message_content = messages[0].content[0].text

    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    return message_content.value, "\n".join(citations)


input = st.text_input("Enter Your Message:")


if st.button("Submit"):
    if input:
        output, references = chatter(input)
        st.write(output)
        st.write(references)

# while True:
#     user_input = input("Type your message=> ")
#     output, references = chatter(user_input)
#     print(output)
#     print(references)
