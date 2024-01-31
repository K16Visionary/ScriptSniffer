import PyPDF2
import json

def read_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

pdf_path = 'test.pdf'
result_text = read_text_from_pdf(pdf_path)

# Print the result as JSON to the console
print(json.dumps({'result_text': result_text}))
