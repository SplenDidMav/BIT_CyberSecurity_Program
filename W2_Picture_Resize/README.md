## 项目名称为： ImageEnhance

## Goal 

  在不使用```Opencv```的```Resize()```函数情况下，对图像进行加工。

## Requirements

  ``python>=3.8.5``  
  ``fire>=0.4.0``  
  ``numpy>=1.23.1``  
  ``Opencv-python>=4.5.5.64``

## Usage

  - 1.将文件下载后，点击运行``run.bat``。
  - 2.在命令行中输入``pip install -r requirements.txt``，下载依赖库。
  - 3.在命令行中输入`` python ImageEnhance.py --path input.png --outpath output.png --height number1 --width number2 --algorithm xxx
``  。其中``xxx``只能为``nearest``或``bilinear``  
  > 示例：``` python ImageEnhance.py --path test.png --outpath bilinear1.png --height 900 --width 900 --algorithm bilinear```
  - 4.在同一文件夹下寻找名为```output.png```的文件，即为加工后图片。

## How It Works
  - 1.首先读取原图片，获得原图片的高度，宽度及通道数。  
  - 2.创建一个按照输入高度与宽度形成的空白图片。  
  - 3.按照加工计算方式的不同，遍历空白图片中的每一个像素点，并写进其中。
  - 4.输出图片
 
## Result
  输入图片：  
    ![图片](test.png)  
  输出1(最近差值法)：  
    ![nearest](nearest.png)  
  输出2(双线性差值):  
    ![bilinear](bilinear1.png)

---

#### 您可以通过以下方式联系到我：
- Mail **apexleapsean@gmail.com**




