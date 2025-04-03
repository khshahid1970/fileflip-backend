from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from fpdf import FPDF
from PIL import Image

app = FastAPI()

# ✅ Allow frontend to connect
origins = [
    "https://fileflip-frontend.onrender.com",  # Frontend Render URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route for testing
@app.get("/")
async def root():
    return {"message": "Backend is up and running!"}

# ✅ File upload directory
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Conversion route
@app.post("/convert")
async def convert_file(file: UploadFile = File(...), conversion_type: str = Form(...)):
    ext = file.filename.split(".")[-1].lower()
    uid = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, f"{uid}_{file.filename}")
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path = input_path

    if conversion_type == "pdf-to-word":
        from pdf2docx import Converter
        output_path = input_path.replace(".pdf", ".docx")
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
    elif conversion_type == "txt-to-pdf":
        output_path = input_path.replace(".txt", ".pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(input_path, "r", encoding="utf-8") as txt_file:
            for line in txt_file:
                pdf.multi_cell(0, 10, line)
        pdf.output
