import sys
import os
import cv2
import numpy as np
from PIL import Image

def prep_photo(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    # Read image using OpenCV
    img = cv2.imread(input_path)
    if img is None:
        # Fallback via PIL
        pil_img = Image.open(input_path).convert('RGB')
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Mild sharpening
    kernel = np.array([[0, -0.5, 0], [-0.5, 3.0, -0.5], [0, -0.5, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    # Save output
    cv2.imwrite(output_path, sharpened)
    print(f"Successfully prepped photo saved to: {output_path}")

if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    prep_photo(in_file, out_file)
