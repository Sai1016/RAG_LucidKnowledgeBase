import streamlit as st
import requests

st.set_page_config(page_title="Lucid Owner Manual", page_icon="📄")
st.title("Lucid Owner Manual Q&A System")

st.markdown("""
Upload a PDF and ask questions about its content. 
The system uses a vector DB + LLM to provide context-aware answers.
""")

# --- Upload PDF ---
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
if uploaded_file:
    # Send PDF to FastAPI backend
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    try:
        pdf_response = requests.post("http://127.0.0.1:8000/process-pdf/", files=files)
        if pdf_response.status_code == 200:
            st.success("PDF processed successfully! You can now ask questions.")
        else:
            st.error(f"Failed to process PDF: {pdf_response.status_code}")
            st.text(pdf_response.text)
    except Exception as e:
        st.error(f"Error contacting backend: {e}")

# --- Ask Questions ---
query = st.text_input("Ask a question about the PDF")
if st.button("Ask"):
    if not query:
        st.warning("Please enter a question!")
    else:
        try:
            # Use 'data' to send form data (like FastAPI Form)
            response = requests.post(
                "http://127.0.0.1:8000/query/",
                data={"query": query}
            )

            # Check response first
            if response.status_code == 200:
                data = response.json()
                if "answer" in data:
                    st.subheader("Answer:")
                    st.write(data["answer"])
                elif "error" in data:
                    st.error(f"Backend error: {data['error']}")
                else:
                    st.error("Unexpected response from backend")
            else:
                st.error(f"Backend returned status {response.status_code}")
                st.text(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")




