from PIL import Image
def LSB_encode(msg, img):
    msg_binary = ''.join([format(ord(i), "08b") for i in msg])
    pixels = list(img.getdata())
    pixels_binary = [format(i, "08b") for sublist in pixels for i in sublist]
    for i in range(len(msg_binary)):
        pixels_binary[i] = pixels_binary[i][:-1] + msg_binary[i]
    pixels = [int(i, 2) for i in pixels_binary]
    pixels = [tuple(pixels[i:i + 3]) for i in range(0, len(pixels), 3)]
    img.putdata(pixels)
    return img
img = Image.open("encode_image.png")
msg = open("encode_text.txt", "r").read()
img = LSB_encode(msg, img)
img.save("encoded_image.png")
