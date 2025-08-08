"""
Create a simple icon for CommandEcho
"""

def create_icon():
    """Create a simple CommandEcho icon"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create assets directory
        os.makedirs("assets", exist_ok=True)
        
        # Create a 64x64 icon
        size = 64
        img = Image.new('RGBA', (size, size), (30, 30, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple robot face
        # Head circle
        draw.ellipse([8, 8, 56, 56], fill=(0, 120, 212, 255))
        
        # Eyes
        draw.ellipse([18, 20, 26, 28], fill=(255, 255, 255, 255))
        draw.ellipse([38, 20, 46, 28], fill=(255, 255, 255, 255))
        
        # Mouth
        draw.rectangle([24, 38, 40, 42], fill=(255, 255, 255, 255))
        
        # Save as PNG
        img.save("assets/icon.png")
        print("✅ Icon created: assets/icon.png")
        
        # Try to create ICO for Windows
        try:
            img.save("assets/icon.ico")
            print("✅ Windows icon created: assets/icon.ico")
        except:
            print("⚠️  Could not create .ico file (PIL may need additional support)")
            
    except ImportError:
        print("⚠️  PIL not available. Install with: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creating icon: {e}")

if __name__ == "__main__":
    create_icon()
