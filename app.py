import io
from fastapi import File, UploadFile, FastAPI
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\suraj.sikhar\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"],  
)



@app.post('/extract')
async def extract(file:UploadFile =File(...)):
    with open("temp.pdf","wb") as f :
        f.write(await file.read())
    images = convert_from_path("temp.pdf", poppler_path=r"C:\Users\suraj.sikhar\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin")
    text_output = ""
    for img in images:
        text_output += pytesseract.image_to_string(img)
    # print(f"Pages converted: {len(images)}")
    return {"text": text_output}

@app.post('/image')
async def imagetopdf(file:UploadFile=File(...)):
    img = await file.read()
    image = Image.open(io.BytesIO(img))

    text = pytesseract.image_to_string(image)
    return{text}