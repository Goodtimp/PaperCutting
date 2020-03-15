from PIL import Image
import numpy
from Chart import bar_chart
from skimage import filters, io, color



# 得到图片的灰度值
def get_gray_value(img):
    # 把图片转换为灰度图
    gray_img = img.convert('L')
    width, height = img.size
    img_array = numpy.array(gray_img)  # 转换为数组
    average = numpy.mean(img_array)  # 计算平均亮度 返回
    count = numpy.bincount(numpy.ravel(img_array), minlength=255)  # 统计某个元素出现的个数，记录 count[1] : 2 表示1出现了两次

    word_gray = width * height * 0.08
    all = 0
    bar_chart(range(0, 255), count[0:255])

    for i in range(0, 255):
        all = all + count[i]
        if all > word_gray:
            return i


def skimage_gray_value(img_path):
    sk_img = io.imread(img_path)
    img = color.rgb2gray(sk_img)  # 获取灰度图片

    thresh = filters.threshold_otsu(img)  # 计算二值化阈值
    return thresh * 256

# img_path = 'image/test(2).jpg'
# sk_img = io.imread(img_path)
# # sk_img = data.chelsea()
#
# sk_gray_img = color.rgb2gray(sk_img)
# io.imshow(sk_gray_img)
# io.show()
# print(test_skimage(sk_gray_img)*255)
# print(sk_img.dtype.name, sk_gray_img.dtype.name)
# print(sk_gray_img)


# img = Image.open("image/test(2).jpg")
# print(get_gray_value(sk_gray_img))
