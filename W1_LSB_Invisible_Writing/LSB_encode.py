from PIL import Image
def LSB_encode(msg, img):
    #将消息转换为二进制
    msg_binary = ''.join([format(ord(i), "08b") for i in msg])
    #获取图像的像素值
    pixels = list(img.getdata())
    #将图像的像素值转换为二进制
    pixels_binary = [format(i, "08b") for sublist in pixels for i in sublist]
    #将消息的二进制值替换到图像RGB像素值中
    for i in range(len(msg_binary)):
        pixels_binary[i] = pixels_binary[i][:-1] + msg_binary[i]
    #将像素值转换为整数
    pixels = [int(i, 2) for i in pixels_binary]
    #将像素值转换为图像
    pixels = [tuple(pixels[i:i + 3]) for i in range(0, len(pixels), 3)]
    img.putdata(pixels)
    return img
#读取图像
img = Image.open("encode_image.png")
#读取消息
msg = open("encode_text.txt", "r").read()
#编码图像
img = LSB_encode(msg, img)
#保存图像
img.save("encoded_image.png")