import threading

#     t = MyThread(tesseract_ocr, args=(temp,))
class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


# 多线程，控制运行数量，并返回运行结果列表
def runthread(tasks, num=4):
    lent = len(tasks)
    result = []
    for i in range(1, lent + 1):
        if i % num == 0 or i == lent:
            for t in tasks[(int((i - 1) / num)) * num:i]:
                t.start()
            for t in tasks[(int((i - 1) / num)) * num:i]:
                t.join()
                result.append(t.get_result())
    return result