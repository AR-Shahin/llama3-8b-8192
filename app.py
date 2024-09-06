import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(
    page_title="LLama 3.1-70b",
    page_icon='🤖'
)
st.title("🤖 LLama3 Chatbot")

api_key = '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'

llm = ChatGroq(
    temperature=0,
    groq_api_key=api_key,
    model_name="llama-3.1-70b-versatile"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask anything ...")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.chat_history.append({"role": "user", "content": query})

    try:
        # Combine the entire chat history with the current query
        context = [{"role": message["role"], "content": message["content"]} for message in st.session_state.chat_history]
        context.append({"role": "user", "content": query})

        # Send the combined context and query to the LLM
        response = llm.invoke(" ".join([msg["content"] for msg in context]))
        assistant_response = response.content

        # Save the assistant's response in chat history
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

    except Exception as e:
        st.write(f"Error: {e}")
