#python3
#author Silencce Lu
import time
from PIL import ImageGrab
ts = 0
print('{times}{formats} '.format(times = ts ,formats ='.png'))
#print(time.localtime())

def Screenshot():
        nowtime = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
        print(nowtime)

        im = ImageGrab.grab()
        im.save('png\{times}.png'.format(times = nowtime))
        #你可以修改引号内png，改为你认为适合的文件夹位置。


while True:
    print("开始工作！")
    print("work begining!")
    Screenshot()

    print("休息中……")
    print("sleeping...")
    print("\n")
    # 5 minute = 60 * 5
    time.sleep(300)

