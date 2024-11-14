import streamlit as st
import requests

st.title("Conversational LLM-based Search Assistant")

# Initialize session state for conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Input for user query
query = st.text_input("Ask me anything:")

# Function to display the latest conversation at the top and full conversation history below
def display_conversation():
    if st.session_state.conversation:
        # Display the most recent message
        latest_conversation = st.session_state.conversation[-2:]  # Last question and answer pair
        for chat in latest_conversation:
            if chat["role"] == "user":
                st.write(f"You: {chat['message']}")
            else:
                st.write(f"Assistant: {chat['message']}")
        
        # st.markdown("---")  # Separator for the full history

        # Display the full conversation history below, excluding the latest messages
        st.write("Conversation History:")
        for chat in st.session_state.conversation[:-2]:
            if chat["role"] == "user":
                st.write(f"You: {chat['message']}")
            else:
                st.write(f"Assistant: {chat['message']}")

# On clicking the "Ask" button, process the query
if st.button("Ask"):
    if query:
        try:
            # Append user's query to the conversation history
            st.session_state.conversation.append({"role": "user", "message": query})

            # Make a POST request to the Flask API
            response = requests.post("http://localhost:5001/query", json={"query": query})

            # Check if the request was successful
            if response.status_code == 200:
                # Retrieve and display the answer
                answer = response.json().get("answer", "No answer received.")
                
                # Append assistant's answer to the conversation history
                st.session_state.conversation.append({"role": "assistant", "message": answer})
                
                # Display the updated conversation
                display_conversation()
            else:
                st.error(f"Error {response.status_code}: {response.json().get('error', 'Unexpected error occurred.')}")
        
        except requests.exceptions.RequestException as e:
            st.error("Failed to connect to the backend. Please ensure the Flask server is running.")
    else:
        st.warning("Please enter a question to continue the conversation.")

# Display the conversation if there are messages (initial load or after an answer)
if st.session_state.conversation:
    display_conversation()
