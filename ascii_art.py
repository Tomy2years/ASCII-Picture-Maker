import sys
import requests
from PIL import Image
from io import BytesIO

# PASTE YOUR API KEY HERE (from https://www.remove.bg/api)
API_KEY = "Copy and Past your key from the website"

# List of ASCII characters for shading
ASCII_CHARS = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
# If using a white background, comment out this line (It inverts the characters and is intended for a dark mode background)
ASCII_CHARS = ASCII_CHARS[::-1] 

def remove_background_api(image_path):
    """
    Sends image to remove.bg and returns a PIL Image object
    """
    print("Sending image to remove.bg API...")
    
    try:
        with open(image_path, 'rb') as file:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': file},
                data={'size': 'auto'},
                headers={'X-Api-Key': API_KEY},
            )
        
        if response.status_code == 200:
            # Convert raw bytes response directly to a PIL Image
            return Image.open(BytesIO(response.content))
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            sys.exit()
            
    except Exception as e:
        print(f"Connection Error: {e}")
        sys.exit()

def resize_image(image, new_width=250):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.5) 
    return image.resize((new_width, new_height))

def pixels_to_ascii(image):
    image = image.convert("RGBA")
    pixels = image.getdata()
    ascii_str = ""
    
    div = 255 / (len(ASCII_CHARS) - 1)
    
    for pixel in pixels:
        r, g, b, a = pixel
        
        # If pixel is transparent, use a space
        if a < 50: 
            ascii_str += " "
        else:
            # Calculate brightness
            brightness = int(0.299*r + 0.587*g + 0.114*b)
            index = int(brightness / div)
            index = min(max(index, 0), len(ASCII_CHARS) - 1)
            ascii_str += ASCII_CHARS[index]
            
    return ascii_str

def main():
    path = "my_photo.jpg"  # <--- Your filename (or just name the image 'my_photo.jpg')
    
    if API_KEY == "Copy and Past your key from the website":
        print("Error: You forgot to paste your API Key in the script!")
        return

    # Remove Background via API
    image = remove_background_api(path)

    # Resize image
    image = resize_image(image)
    
    # Convert image to ASCII
    ascii_data = pixels_to_ascii(image)
    
    # Format the ASCII string into lines 
    pixel_count = len(ascii_data)
    width = 250
    ascii_img = "\n".join(
        [ascii_data[index:(index + width)] 
         for index in range(0, pixel_count, width)]
    )
    
    # Save to a txt file
    with open("ascii_person.txt", "w") as f:
        f.write(ascii_img)
    print("Done. Open 'ascii_person.txt' and ZOOM OUT.")

if __name__ == "__main__":
    main()
