import matplotlib.pyplot as plt


def bar_chart(index # 下标
              ,values # 值
              ,width=0.35):
    # 创建一个点数为  6x 4 的窗口, 并设置分辨率为 80像素/每英寸
    plt.figure(figsize=(6, 4), dpi=80)

    # 再创建一个规格为 1 x 1 的子图
    plt.subplot(1, 1, 1)
    # 绘制柱状图, 每根柱子的颜色为紫罗兰色
    plt.bar(index,values,width, label="rainfall", color="#87CEFA")
    plt.show()