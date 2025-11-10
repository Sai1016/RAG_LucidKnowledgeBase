#FastAPI backend
from fastapi import FastAPI, UploadFile, Form
from app.PDFProcessor import PDFProcessor
from app.llm_integration import generate_answer

app = FastAPI()
pdf_proc = PDFProcessor()

@app.post("/process-pdf/")
async def process_pdf(file: UploadFile):
    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # read 1MB at a time
            f.write(chunk)


    pdf_proc.pdf_path = path
    pdf_proc.build_index()
    return {"message": "PDF processed and indexed successfully!"}

@app.post("/query/")
async def query_pdf(query: str = Form(...)):
    chunks = pdf_proc.retrieve(query)
    context = "\n".join(chunks)
    answer = generate_answer(context, query)
    return {"answer": answer}
