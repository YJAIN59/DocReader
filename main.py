import shutil
from PyPDF2 import PdfFileReader
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <html>
        <head>
            <title>File Uploader</title>
        </head>
        <body>
            <h2>Count the number of Pages in file </h2>
            <br>
            <form action = "/submitfiles/" method = "POST" enctype = "multipart/form-data">
                <input type = "file" name = "doc_file" />
                <input type = "submit"/>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/submitfiles/")
async def create_file(doc_file: UploadFile = File(...)):
    with open(doc_file.filename, "wb") as buffer:
        shutil.copyfileobj(doc_file.file, buffer)
    
    with open(doc_file.filename, "rb") as pdf_file:
        pdf_reader = PdfFileReader(doc_file.filename)
    #print("The total number of pages in the pdf document is:", pdf_reader.numPages)
#comment extra    
#a = await doc_file.read()
    #print(doc_file.file)
    return {
        "print": doc_file.filename,
        "Count pages in the file": pdf_reader.numPages,
    }
