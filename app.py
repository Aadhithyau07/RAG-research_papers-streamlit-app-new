import streamlit as st

from backend.rag_pipeline import (
    ask_new_question,
    ask_followup,
    is_followup
)

st.title("Research Paper RAG Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_first_question" not in st.session_state:
    st.session_state.is_first_question = True

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "sources" in message:

            with st.expander("📄 Sources"):

                for source in message["sources"]:
                    st.write(f"- {source}")

if prompt := st.chat_input(
    "Ask a question about the research papers..."
):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            if st.session_state.is_first_question:

                answer, sources = ask_new_question(prompt)

                st.session_state.is_first_question = False

            else:

                if is_followup(
                    prompt,
                    st.session_state.messages
                ):

                    answer = ask_followup(prompt,st.session_state.messages)

                    sources = []

                else:

                    answer, sources = ask_new_question(prompt)

        st.markdown(answer)

        if sources:

            with st.expander("📄 Sources"):

                for source in sources:
                    st.write(f"- {source}")

    assistant_message = {
        "role": "assistant",
        "content": answer
    }

    if sources:
        assistant_message["sources"] = sources

    st.session_state.messages.append(
        assistant_message
    )