from PIL import Image
def decode_image(image):
    # 从图像中提取像素值
    pixels = list(image.getdata())
    # 将像素值转换为二进制
    pixels_binary = [format(i, "08b") for sublist in pixels for i in sublist]
    # 提取最低有效位
    msg = [pixels_binary[i][-1] for i in range(len(pixels_binary))]
    # 将二进制转换为 ASCII 字符
    result = ''
    for i in range(0, len(msg), 8):
        nchar = chr(int(''.join(msg[i:i + 8]), 2))
        if not nchar.isascii: # 如果不是ASCII字符就截断
            break
        result += nchar
    return result
# 读取图像
image = Image.open("encoded_image.png")
# 解码图像
msg = decode_image(image)
# 将消息写入文件
open("decoded_text.txt", "w", encoding='utf-8').write(msg)