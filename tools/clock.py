# coding=utf-8
import time

class Clock:

    def Start(self):
        self.start_time = time.time()

    def End(self):
        self.end_time = time.time()

    def Time(self):
        t = int(self.end_time-self.start_time)
        if t >= 3600:
            print('用时 %d 时 %d 分 %d 秒' % (t//3600, (t%3600)//60, t%60))
        elif t >= 60:
            print('用时 %d 分 %d 秒' % (t//60, t%60))
        else:
            print('用时 %d 秒' % t)