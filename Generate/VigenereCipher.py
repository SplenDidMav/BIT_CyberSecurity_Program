def Getplaintext():
    #读取文件
    with open('plaintext.txt', 'r') as f:
        plaintextoriginal = f.read()
    #过滤标点符号和空格
    plaintext = ''
    for i in plaintextoriginal:
        if i in "!@#$%^&*()_+=-`~[]{}|;':\",./<>?":
            continue
        elif i.islower():
            plaintext += i.upper()
        else:
            plaintext += i
    plaintext = plaintext.replace(' ', '')
    return plaintext
def Getkey():
    #获取密钥
    key = input()
    return key
def Getciphertext(plaintext,key):
    #获取密文
    ciphertext = ''
    for i in range(len(plaintext)):
        ciphertext += chr((ord(plaintext[i]) + ord(key[i % len(key)])) % 26 + 65)
    return ciphertext
def Writeciphertext(ciphertext):
    #写入文件
    with open('ciphertext.txt', 'w') as f:
        f.write(ciphertext)
def main():
    plaintext = Getplaintext()
    print(plaintext)
    key = Getkey()
    ciphertext = Getciphertext(plaintext,key)
    Writeciphertext(ciphertext)
    print(ciphertext)
main()

