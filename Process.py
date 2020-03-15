from OCR import tesseract_ocr, baidu_orc, baidu_orc_pil
from Pretreatment import pre_run
from PIL import Image
from MyThread import MyThread, runthread
import re
import time


def get_xuhao(word):
    if word == None or word == "":
        return -1
    if word.isdigit():  # 纯数字则直接返回-1
        return -1
    i = 0
    for i in range(0, len(word)):
        if not word[i].isdigit():
            break
    if i == 0 or word[i].isalpha():  # 判断是否为汉字或者字母，此时多数为题干内容。isalpha()当为标点时返回Fasle
        return -1
    return int(word[0:i])


# 判断是否为无用行
def is_useless_row(word, is_engtest=False):
    if word is None:
        return True
    daxie = word[0:2]
    # 判断是否为序号
    if daxie == "一、" or daxie == "二、" or daxie == "三、" or daxie == "四、" or daxie == "五、" or daxie == "六、" or daxie == "七、" or daxie == "八、" or daxie == "九、" or daxie == "十、":
        return True
    if daxie == "一：" or daxie == "二：" or daxie == "三：" or daxie == "四：" or daxie == "五：" or daxie == "六：" or daxie == "七：" or daxie == "八：" or daxie == "九：" or daxie == "十：":
        return True
    if is_engtest:
        tempword = removePunctuation(word)
        c_ratio = get_chinese_ratio(tempword)
        e_ratio = get_english_ratio(tempword)
        if c_ratio > 0.8 or c_ratio > e_ratio:
            return True
    return False


# 得到字符串中中文站的比例
def get_chinese_ratio(word):
    cnt_ch = 0
    word.replace(" ", "")
    for s in word:
        # 中文字符范围
        if '\u4e00' <= s <= '\u9fff':
            cnt_ch = cnt_ch + 1
    return cnt_ch / (len(word))


# 删除所有的标点符号
def removePunctuation(text):
    punctuation = '-_!,;:?"\''
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip()


# 得到英文数量
def get_english_count(word):
    cnt_eng = 0
    for s in word:
        # 中文字符范围
        if (s >= u'\u0041' and s <= u'\u005a') or (s >= u'\u0061' and s <= u'\u007a'):
            cnt_eng = cnt_eng + 1
    return cnt_eng


# 得到一句话英文的比例
def get_english_ratio(word):
    word.replace(" ", "")
    cnt_eng = get_english_count(word)
    return cnt_eng / (len(word))


# 根据位置信息切题
def cut_question(img, pos, f=True):  # 将img切成pos部分，f为false传入img为path，否则为PIL
    """
        pos: 含有 top bottom left right
    """
    if not f:
        img = Image.open(img)
    return img.crop((pos["left"], pos["top"], pos["right"], pos["bottom"]))


# 得到题目范围
def get_pos(pre, this, words):
    pos = {"left": 100000, "right": 0, "top": 100000, "bottom": 0}
    if pre == this:
        this = this + 1
    for i in range(int(pre), int(this)):
        msg = words[i]["location"]
        pos["left"] = min(pos["left"], msg["left"])
        pos["right"] = max(pos["right"], msg["left"] + msg["width"])
        pos["top"] = min(pos["top"], msg["top"])
        pos["bottom"] = max(pos["bottom"], msg["top"] + msg["height"])

    pos["left"] = max(pos["left"] - 5, 0)
    pos["top"] = max(pos["top"] - 5, 0)

    # pos["bottom"] = max(pos["bottom"] + 5, 0)
    # pos["left"] = max(pos["left"] - 5, 0)

    return pos


# 判断是否为英文题
def is_english_test(content):
    content = content.replace(" ", "")  # 剔除空格影响
    content = removePunctuation(content)
    return get_english_ratio(content) > 0.8


# 得到 与i 同行的内容
def get_line_content(i, words):
    content = words[i]["words"]
    pos = words[i]["location"]

    for i in range(i + 1, len(words)):
        nex_pos = words[i]["location"]
        if (pos["top"] + pos["height"] / 2) >= nex_pos["top"]:  # 判断是否为同行
            content = content + " " + words[i]["words"]
            continue
        return content, i
    return content, i


# 得到序号列表
def get_list_title(words):
    title_num = []

    is_engtest = False

    for i in range(0, len(words)):
        # print(words[i]["words"])
        pre_pos = words[i - 1]["location"]
        if i > 0 and (pre_pos["top"] + pre_pos["height"] / 2) > words[i]["location"]["top"]:  # 判断是否为同行
            continue
        content, j = get_line_content(i, words)

        if is_useless_row(content, is_engtest):  # 剔除无用行（包括 "一、"，英文试卷中的中文字符占比过大）
            for u in range(i, j):
                title_num.append({"pos": u, "xuhao": -2})
            continue
        xuhao = get_xuhao(content)  # 得到序号
        # if len(title_num)<= 1:
        #     content = content + words[i]["words"]
        if xuhao != -1:
            title_num.append({"pos": i, "xuhao": xuhao})
            if len(title_num) == 1:
                is_engtest = is_english_test(content)

    title_num.append({"pos": len(words), "xuhao": "-1"})
    return title_num


def baidu_handle(path):
    result = baidu_orc(path)

    words = result["words_result"]
    title_num = get_list_title(words)  # 得到序号列表
    # print(title_num)

    for i in range(1, len(title_num)):  # 遍历序号列表，将相邻题目切出来
        if title_num[i - 1]["xuhao"] == -2:  # 无用行 or 最后一个
            continue
        pos = get_pos(title_num[i - 1]["pos"], title_num[i]["pos"], words)
        print(pos)
        # cut_question(path, pos, False).show()


def pro_run(path):
    baidu_handle(path)# 百度处理，得到切割信息
    # print("start pretreatment time:" + str(time.time()))
    # data = pre_run(path)  # 耗时在500ms内

    # print(data["cuty"])
    # print(data["disy"])
    # print(data["posy"])
    '''
    img = data["image"]
    # data["binarize_image"].show()
    width, height = img.size
    cuty = data["cuty"]
    print("start")

    # loop = asyncio.get_event_loop()
    tasks = []
    for i in range(1, len(cuty)):
        temp = img.crop((0, cuty[i - 1], width, cuty[i]))
        t = MyThread(tesseract_ocr, args=(temp,))
        tasks.append(t)
        # coroutine = asyncio.ensure_future(tesseract_ocr(temp))
        # task = asyncio.ensure_future(coroutine)
        # tasks.append(coroutine)
    result = runthread(tasks, 6)
    for i in result:
        print(i)

    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()
    '''


path = "image/math/11.png"
img = Image.open(path)
# img.show()
pro_run(path)
