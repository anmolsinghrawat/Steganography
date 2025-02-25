import cv2

def decrypt_message(image_path, password):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found!")
        return

    # Read message length from first 4 pixels
    message_length = (img[0, 0, 0] << 24) | (img[0, 0, 1] << 16) | (img[0, 0, 2] << 8) | img[0, 1, 0]

    if message_length == 0 or message_length > (img.shape[0] * img.shape[1] * 3):
        print("Error: No hidden message found or invalid length!")
        return

    # User enters passcode for decryption
    entered_password = input("Enter passcode for decryption: ")
    if entered_password != password:
        print("YOU ARE NOT AUTHORIZED")
        return

    # Decoding the hidden message
    row, col, channel = 0, 2, 0  # Start from pixel (0,2)
    message_bytes = bytearray()

    for _ in range(message_length):
        message_bytes.append(img[row, col, channel])
        channel += 1
        if channel == 3:
            channel = 0
            col += 1
            if col >= img.shape[1]:  # Prevent column overflow
                col = 0
                row += 1

    decrypted_message = message_bytes.decode("utf-8")
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    image_path = input("Enter the encrypted image path: ")
    password = input("Enter the original passcode used for encryption: ")

    decrypt_message(image_path, password)
