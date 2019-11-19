#python3 author Silencce Lu
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


while True:
    print("开始工作！")
    Screenshot()

    print("休息中……")
    print("\n")
    # 5 minute = 60 * 5
    time.sleep(300)

