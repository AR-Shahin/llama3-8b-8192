import streamlit as st
from langchain_groq import ChatGroq
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load API key from environment variable
api_key = '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'
st.set_page_config( page_title="LLama 3.1-70b", page_icon='🤖' ) 
st.title("🤖 LLama3 Chatbot")


# Create a ChatGroq instance
llm = ChatGroq(
    temperature=0,
    groq_api_key=api_key,
    model_name="llama-3.1-70b-versatile"
)

def display_chat_history(chat_history):
    """Display the chat history"""
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_user_query():
    """Get the user query"""
    query = st.chat_input("Ask anything ...")
    return query

def send_query_to_llm(query, chat_history):
    """Send the query to the LLM"""
    try:
        context = [{"role": message["role"], "content": message["content"]} for message in chat_history]
        context.append({"role": "user", "content": query})
        response = llm.invoke(" ".join([msg["content"] for msg in context]))
        return response.content
    except ConnectionError as e:
        logging.error(f"Error sending query to LLM: {e}")
        raise

def main() :
    """Main function"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    display_chat_history(st.session_state.chat_history)

    query = get_user_query()
    if query:
        st.chat_message("user").markdown(query)
        st.session_state.chat_history.append({"role": "user", "content": query})

        try:
            assistant_response = send_query_to_llm(query, st.session_state.chat_history)
            if assistant_response:
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
                display_chat_history(st.session_state.chat_history)
            else:
                logging.error("Empty response from LLM")
        except Exception as e:
            logging.error(f"Error: {e}")
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()