#　存储时间变量
import time

# 获取ms级别的时间
def getCurrentTime():
    t = time.time()
    return int(t * 1000)