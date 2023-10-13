import streamlit as st 
import time 
from trubrics.integrations.streamlit import FeedbackCollector
from trubrics import Trubrics 

# app title 
st.set_page_config(page_title="Wing Warranty Chatbot")

left_c, cent_c, last_c = st.columns(3)
with cent_c:
    st.image('wing-warranty.png')


# store llm responses 
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can i help you ?"}]

# display chat messages
for message in st.session_state.messages:
    avatar=None 
    if message["role"] == "assistant":
        avatar = 'wing.png'
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# func for generating llm responses - echo
def generate_response(prompt_input):
    time.sleep(2)
    return f"GPT echos: {prompt_input}"

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# generate response if last message is not from assistant
    with st.chat_message("assistant", avatar='wing.png'):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

    collector = FeedbackCollector(
        email=st.secrets.TRUBRICS_EMAIL,
        password=st.secrets.TRUBRICS_PASSWORD,
        project="default"
    )

    user_feedback = collector.st_feedback(
        component="Chat Feedback",
        feedback_type="thumbs",
        model="gpt-3.5-turbo",
        prompt_id=None, #checkout collector.log_prompt() to log users prompts
        open_feedback_label="[Optional] Provide additional feedback",
        metadata={"prompt": prompt, "response": response}
    )
    logged_prompt = collector.log_prompt(
        config_model={"model": "gpt-3.5"},
        prompt=prompt,
        generation=response
    )
#    if user_feedback:
#        st.write('Feedback sent')
