from PIL import Image, ImageDraw, ImageOps
import os

def update_favicon():
    logo_path = "frontend/public/logo.png"
    favicon_path = "frontend/public/favicon.ico"
    
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path).convert("RGBA")
            
            # --- Create 256x256 canvas ---
            canvas_size = 256
            canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
            
            # --- Scale logo to fit inside canvas with padding ---
            padding = 20  # pixels of padding on all sides
            max_logo_size = canvas_size - (padding * 2)
            
            # Resize logo keeping aspect ratio
            img.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)
            
            # Center the logo on the canvas
            offset_x = (canvas_size - img.width) // 2
            offset_y = (canvas_size - img.height) // 2
            canvas.paste(img, (offset_x, offset_y), img)
            
            # Save as favicon.ico with multiple sizes
            canvas.save(favicon_path, sizes=[(256, 256), (64, 64), (32, 32), (16, 16)])
            print(f"Favicon updated with padding: {favicon_path}")
            
        except Exception as e:
            print(f"Error updating favicon: {e}")
    else:
        print(f"Logo not found at {logo_path}")

if __name__ == "__main__":
    update_favicon()
