from PIL import Image, ImageDraw
import pytesseract
import json

# Specify the path to the Tesseract executable (update this with your actual path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def draw_word_rectangles(image_path, output_image_path, fill_color="red"):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Create an ImageDraw object to draw rectangles on the image
    draw = ImageDraw.Draw(img)

    # Perform OCR using pytesseract to get word regions
    words = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    # Iterate through detected words and draw rectangles around them
    for i in range(len(words['text'])):
        left, top, width, height = int(words['left'][i]), int(words['top'][i]), int(words['width'][i]), int(words['height'][i])
        if words['text'][i].strip() != '':
            draw.rectangle([left, top, left + width, top + height], outline=fill_color, fill=fill_color)

    # Save the image with filled rectangles around words
    img.save(output_image_path)
    print(f"Image with filled word rectangles saved as {output_image_path}")

if __name__ == "__main__":
    # Specify the path to the input image
    input_image_path = "adhar.jpg"

    # Specify the path for the output image with filled rectangles
    if '.jpg' in input_image_path:
        output_image_path = f'{input_image_path.replace(".jpg","")} masked.jpg'
    elif '.png' in input_image_path:
        output_image_path = f'{input_image_path.replace(".png","")} masked.png'
    elif '.jpeg' in input_image_path:
        output_image_path = f'{input_image_path.replace(".jpeg","")} masked.jpeg'

    # Specify the fill color for the rectangles (e.g., "red", "blue", "green", etc.)
    fill_color = "black"

    # Draw filled rectangles around the detected words in the input image
    draw_word_rectangles(input_image_path, output_image_path, fill_color)
