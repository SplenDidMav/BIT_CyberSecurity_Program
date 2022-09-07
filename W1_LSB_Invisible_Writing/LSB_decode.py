from PIL import Image
def decode_image(image):
    pixels = list(image.getdata())
    pixels_binary = [format(i, "08b") for sublist in pixels for i in sublist]
    msg = [pixels_binary[i][-1] for i in range(len(pixels_binary))]
    result = ''
    for i in range(0, len(msg), 8):
        nchar = chr(int(''.join(msg[i:i + 8]), 2))
        if not nchar.isascii:
            break
        result += nchar
    return result
image = Image.open("encoded_image.png")
msg = decode_image(image)
open("decoded_text.txt", "w", encoding='utf-8').write(msg)
