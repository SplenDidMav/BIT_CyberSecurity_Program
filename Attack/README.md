<h1 align="center">
VigenereCipherAttack
</h1>

> 通过 [Kasiski测试法](https://en.wikipedia.org/wiki/Kasiski_examination)、[重合指数法](https://en.wikipedia.org/wiki/Index_of_coincidence)与[频率分析](https://en.wikipedia.org/wiki/Frequency_analysis) 来破解维吉尼亚密码，确定密钥，解密密文。

加密文档
-------------
```
ciphertext.txt
```
程序
-------------

  - ``kasiski.py  ``      
  #Kasiski测试法
  - ``ic.py    ``          
  #重合指数法
  - ``freq_analysis.py ``   
  #频率分析
  - ``processing.py ``    
  #处理密文 
  - ``const.py ``        
  #常量
  - ``attack.py  ``        
  #破解维吉尼亚密码

使用
-------------
```
双击run.bat  
在命令行状态下输入pip install -r requirements.txt
将密文放入ciphertext.txt中
运行python attack.py
键入需要使用的方法(Kasiski or IC)
文本输出到deciphered.txt
```
可能存在的bug
-------------
```
密文过短，可能导致kasiski测试法无法找到重复的子串，最后报错
```
