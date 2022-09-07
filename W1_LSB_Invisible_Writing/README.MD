Regarding the LSB steganography problem:
The main issues are divided into two areas:
	1. Encryption of information to images;
	2. Image-to-information decryption
There are some problems with the first module:
	1. How to convert information into 8-bit binary?
	2. How to convert the picture to 8-bit binary?
	3. How to put information 8-bit binary into the image?
solution:
	1. Using the ord() function and the format() function,
	Convert the information to ASCII (UNICODE) code first,
	Convert to binary again.
	2. Learn to know:
	In the PILLOW library,
	There is a function .getdata() to directly obtain the pixel value of the picture,
	Then use the format() function to convert the pixel value to 8-bit binary.
	3. Replace the 8-bit binary of the information into the pixel values ​​of the image,
	Then reverse the 8-bit binary of the image,
	Convert it to an image again using the .putdata() function.
	Finally saved in "encoded_iamge.png"
There is a problem with the second module:
	1. How to extract the last digit after converting the RGB channel of the picture to 8-bit binary?
	2. How to convert the information into readable text after extracting the 8-bit binary?
	3. How to deal with the garbled characters in the remaining non-information part?
solution:
	1. After using the .getdata() function to obtain the RGB value of the image,
	Then use the list and format() function to convert the RGB value to 8-bit binary and store it in the list
	2. After using the for() loop to extract the last digit of the 8-bit binary of the picture,
	Convert binary to character using int(value, base) and chr() functions
	3. Since the length of the encrypted information is unknown, use the .isascii() function to judge whether the information is complete.
	Eliminate garbled characters.
	(There is a small bug. If there is non-ascii code in the information, the information from the program will be incomplete, but my ability is limited, so I can only try to write it like this)
	Finally save the information in "decoded_text.txt"
Program running problem:
	1. If you want to encrypt:
		Name the document to be encrypted "encode_text.txt",
		The image to be encrypted is named "encode_image.png",
		Create new image "encoded_image.png"
		Run LSB_encode.py in this directory
		encoded_image.png is the encrypted image
	2. If you want to decrypt:
		Name the image to be decrypted "encoded_image.png",
		Create new document "decoded_text.txt"
		Run LSB_decode.py in that directory
		decoded_text.txt is the decrypted document
关于LSB隐写问题：
主要问题分为两大板块：
	一.信息到图像的加密；
	二.图像到信息的解密
第一个模块存在问题：
	1.如何将信息转为8位二进制？
	2.图片如何转为8位2进制？
	3.如何将信息8位2进制放入图像？
解决方案：
	1.利用ord()函数与format()函数，
	将信息先转换为ASCII(UNICODE)码,
	再转换为二进制。
	2.学习得知：
	PILLOW库中，
	存在函数.getdata()直接获取图片像素值，
	再利用format()函数将像素值转换为8位2进制。
	3.将信息的8位二进制替换到图像的像素值中，
	再反向处理图像的8位2进制，
	利用.putdata()函数将其再次转换为图像。
	最后保存在"encoded_iamge.png"中
第二个模块存在问题：
	1.如何将图片RGB通道转为8位2进制后提取出最后一位？
	2.提取信息8位2进制后如何转换为可读文本？
	3.剩余非信息部分乱码如何处理？
解决方案：
	1.利用.getdata()函数获取图像RGB值后，
	再利用列表和format()函数将RGB值转换为8位2进制并存储在列表中
	2.利用for()循环将图片8位2进制最后一位提取出后，
	使用int(value, base)和chr()函数将2进制变为字符
	3.由于加密信息长度未知，利用.isascii()函数判断信息是否完整，
	排除乱码。
	(其中存在一个小bug，如果信息中存在非ascii码，程序跑出来的信息就会不全，但是本人能力有限，只能尽量写成这样了)
	最后将信息保存在"decoded_text.txt"
程序运行问题：
	1.如果想要加密:
		将待加密文档命名为"encode_text.txt",
		待加密图片命名为"encode_image.png",
		创建新图片"encoded_image.png"
		在该目录下运行LSB_encode.py
		encoded_image.png即为加密后图片
	2.如果想要解密：
		将待解密图片命名为"encoded_image.png",
		创建新文档"decoded_text.txt"
		在该目录下运行LSB_decode.py
		decoded_text.txt即为解密后文档
