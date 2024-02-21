import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io
from openai import OpenAI
import tempfile
import PyPDF2
from pdf2image import convert_from_bytes  # Changed from convert_from_path
import pytesseract

def pdf_to_text_ocr(uploaded_file):
    # Initialize the text variable to store the final text
    full_text = ""

    # Read the PDF directly from the UploadedFile (file-like object)
    reader = PyPDF2.PdfReader(uploaded_file)

    # Iterate through each page of the PDF
    for i in range(len(reader.pages)):
        page = reader.pages[i]

        # Attempt to extract text using PyPDF2
        text = page.extract_text()

        # If text extraction is successful, append the text
        if text:
            full_text += text
        else:
            # If text extraction fails, use OCR on the page image
            # Since OCR requires a file path, we need to save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                temp.write(uploaded_file.getvalue())  # Write the uploaded file's content to a temp file
                temp.seek(0)  # Seek back to the beginning of the file after writing
                images = convert_from_bytes(temp.read(), first_page=i+1, last_page=i+1)
                for image in images:
                    ocr_text = pytesseract.image_to_string(image)
                    full_text += ocr_text

    return full_text


def process_text_openai_llm(api_key,extracted_text,categories) : 
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"You are a great threat detector and given the following categories :{categories} "},
        {"role": "user", "content": f"check for PTAs(possible threat actors) in the following pdf text {extracted_text} based on the categories I gave you, and assign a risk score to it"}
    ]
    )
    response_text = completion.choices[0].message.content
    return response_text
