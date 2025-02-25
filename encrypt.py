import cv2
import numpy as np
import os

def encrypt_message(image_path, message, password, output_path="encryptedImage.png"):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found!")
        return

    height, width, _ = img.shape
    max_message_length = (height * width * 3) - 4  # Reserve space for length storage

    if len(message) > max_message_length:
        print("Error: Message too long for the image!")
        return

    # Convert message to bytes and store the length in the first 4 pixels
    message_bytes = message.encode("utf-8")
    message_length = len(message_bytes)

    img[0, 0, 0] = (message_length >> 24) & 0xFF  # First byte
    img[0, 0, 1] = (message_length >> 16) & 0xFF  # Second byte
    img[0, 0, 2] = (message_length >> 8) & 0xFF   # Third byte
    img[0, 1, 0] = message_length & 0xFF          # Fourth byte

    # Encoding the message into pixel values
    row, col, channel = 0, 2, 0  # Start from pixel (0,2)
    for byte in message_bytes:
        img[row, col, channel] = byte
        channel += 1
        if channel == 3:
            channel = 0
            col += 1
            if col == width:
                col = 0
                row += 1

    # Save encrypted image (use PNG to avoid compression)
    cv2.imwrite(output_path, img)
    print(f"Message encrypted and saved as {output_path}")

    os.system(f"start {output_path}")  # Opens image in Windows

if __name__ == "__main__":
    image_path = input("Enter the image path: ")
    message = input("Enter secret message: ")
    password = input("Enter a passcode: ")

    encrypt_message(image_path, message, password)
