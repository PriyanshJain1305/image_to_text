from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

# Path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image)
    return text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file found in the request'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No image file selected'}), 400

    try:
        # Open the image file
        image = Image.open(io.BytesIO(image_file.read()))
        text = extract_text_from_image(image)
        return jsonify({'extracted_text': text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
