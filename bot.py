import streamlit as st
from openai import OpenAI

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

if not GROQ_API_KEY:
    st.error("Please set the GROQ_API_KEY environment variable.")
    st.stop()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

st.title("OpenAI GROQ API")

st.session_state["groq_openai_model"] = st.sidebar.selectbox(
    "Model",
    ["llama3-8b-8192", "gemma2-9b-it", "mixtral-8x7b-32768", "llama-3.1-8b-instant"])
# show message what model is selected by toast messages
message = f"Model {st.session_state['groq_openai_model']} is selected"
st.toast(message)

if "groq_openai_model" not in st.session_state:
    st.session_state["groq_openai_model"] = "llama3-8b-8192"

if "messages" not in  st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hãy nhập vào yêu cầu?"):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        full_res = ""
        holder = st.empty()

        for response in client.chat.completions.create(
            model = st.session_state["groq_openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_res += (response.choices[0].delta.content or "")
            holder.markdown(full_res + "▌")
            holder.markdown(full_res)
        holder.markdown(full_res)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_res
        }
    )