import kasiski
import ic
import processing
import freq_analysis as fa
from const import (SEQ_LEN, MAX_KEY_LEN)
import string


def _decypher(cyphertext, key):
    # 用密钥解密
    letters = string.ascii_uppercase
    # 生成密钥表
    shifts = [letters.index(letter) for letter in key]
    # 分块
    blocks = processing.get_blocks(text=cyphertext,size=len(key))
    # 分列
    cols = processing.get_columns(blocks)
    # 解密
    decyphered_blocks = processing.to_blocks([fa.shift(col, shift) for col, shift in zip(cols, shifts)])
    # 合并
    decyphered = ''.join(decyphered_blocks)
    return decyphered


def Writeciphertext(decyphered):
    #写入文件
    with open('deciphertext.txt', 'w') as f:
        f.write(decyphered)


def attack(file, method):
    # 读取文件
    with open(file) as f:
        cyphertext = f.readlines()
        key_len = 0
        # 选择解密方法
        if method == 'kasiski':
            print('运行Kasiski测试法\n')
            key_len = kasiski.find_key_length(cyphertext=cyphertext[0], seq_len=SEQ_LEN, max_key_len=MAX_KEY_LEN)
        elif method == 'ic':
            print('运行指数重合法\n')
            key_len = ic.find_key_length(cyphertext=cyphertext[0], max_key_len=MAX_KEY_LEN)
        # 生成密钥
        key = fa.restore_key(cyphertext[0], key_len)
        decyphered = _decypher(cyphertext[0], key)
        print('密钥长度: '+str(key_len))
        print('密钥: '+str(key))
        print('Plaintext: '+str(decyphered))
        Writeciphertext(decyphered)

method = input('Choose method (kasiski or ic): ')
attack('ciphertext.txt', method)
