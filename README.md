# RAG_LucidKnowledgeBase
  ## **Overview**

 
This project consists of a FastAPI backend and a Streamlit frontend. The backend handles API requests, while the frontend provides an interactive web interface for browsing files, downloading data, and asking questions.


## **Setup Instructions:**

### **1.Create and Activate a Virtual Environment**

python -m venv venv

### **Activate the environment:**

### **Windows:**

venv\Scripts\activate

### **macOS/Linux:**

source venv/bin/activate

### **2.Install Dependencies**

pip install -r requirements.txt

### **3.Run the FastAPI Backend**

Start the backend server using Uvicorn:

uvicorn app.main:app --reload

The backend will run at http://127.0.0.1:8000

### **4.Run the Streamlit Frontend**

Open a new terminal (keep backend running), then start the frontend:

streamlit run frontend/streamlit_app.py

Streamlit will automatically open a new browser tab. If not, visit http://localhost:8501

## **Usage:**

1.Browser files using frontend interface.

2.Download files directly from the UI.

3.Ask questions related to the uploaded content.
