from PIL import Image
import pytesseract
import os
from langdetect import detect
import fitz

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Set the path to the folder containing language data files
tessdata_path = r'C:\\Program Files\\Tesseract-OCR\\tessdata'

# Set the path for pytesseract to look for language data
os.environ['TESSDATA_PREFIX'] = tessdata_path

def extract_text_from_image(image_path, language):
    # Open the image using Pillow
    image = Image.open(image_path)

    # Perform OCR to extract text with specified language
    text = pytesseract.image_to_string(image, lang=language)

    return text

def get_text_language(text):
    try:
        # Use langdetect to determine the language
        language = detect(text)
        return language
    except:
        return "Language detection failed"

def extract_lines_from_text(text):
    # Split the text into lines
    lines = text.split('\n')
    # Remove empty lines and lines with digits
    valid_lines = [line.strip() for line in lines if line.strip()] # and not any(char.isdigit() for char in line)
    return valid_lines

def extract_images_and_text_from_pdf(pdf_path, output_folder, languages):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]

        # Get the images on the page
        image_list = page.get_images(full=True)

        for image_index, img in enumerate(image_list):
            image_index += 1  # Image index starts from 1

            # Get the image information
            base_image = pdf_document.extract_image(img[0])
            image_bytes = base_image["image"]

            # Save the image to a file
            image_filename = f"{output_folder}page{page_num + 1}_image{image_index}.png"
            with open(image_filename, "wb") as image_file:
                image_file.write(image_bytes)

            # Extract text from the image with the specified language
            text = extract_text_from_image(image_filename, languages)

            # Determine the language of the extracted text
            detected_language = get_text_language(text)

            # Extract lines from the text
            lines = extract_lines_from_text(text)

            print(f"Text from {image_filename} (Detected Language: {detected_language}):\n")
            for line_num, line in enumerate(lines, start=1):
                if not any(char.isdigit() for char in line):
                    print(f"Line {line_num}: {line}")
            print("\n")

    # Close the PDF document
    pdf_document.close()

if __name__ == "__main__":
    # Specify the path to the PDF file, output folder, and languages
    pdf_path = "test.pdf"
    output_folder = "C:\\Users\\Admin\\Downloads\\RECKON\\"
    languages = ['tel', 'eng']

    # Extract images and text from the PDF with specified languages (Telugu and English)
    for lang in languages:
        extract_images_and_text_from_pdf(pdf_path, output_folder, lang) 