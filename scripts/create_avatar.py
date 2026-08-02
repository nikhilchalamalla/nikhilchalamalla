import os
from PIL import Image

def create_square_avatar(input_path="source-photo.jpg", output_path="avatar.jpg"):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
        
    img = Image.open(input_path)
    w, h = img.size
    
    # Center crop square focusing on upper face/shoulders
    min_dim = min(w, h)
    
    # Crop box: left, upper, right, lower
    left = (w - min_dim) // 2
    top = int(h * 0.05) # slightly higher to capture hair & shoulders
    right = left + min_dim
    bottom = top + min_dim
    
    if bottom > h:
        bottom = h
        top = h - min_dim
        
    cropped = img.crop((left, top, right, bottom))
    resized = cropped.resize((600, 600), Image.Resampling.LANCZOS)
    resized.save(output_path, quality=95)
    print(f"Square profile avatar created at: {output_path}")

if __name__ == "__main__":
    create_square_avatar()
