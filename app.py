import streamlit as st
from langchain_groq import ChatGroq

# Streamlit app title
st.title("LLama3 Model")

# Define API key
api_key = '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'

# Initialize ChatGroq model
llm = ChatGroq(
    temperature=0,
    groq_api_key=api_key,
    model_name="llama-3.1-70b-versatile"
)

query = st.text_input("Write anything...")

if query:
    st.write(f"User Input: {query}")

    try:
        response = llm.invoke(query)
        st.write(f"{response.content}")
    except Exception as e:
        st.write(f"Error: {e}")
