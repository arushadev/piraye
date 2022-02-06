from normalizer import Normalizer
import time

if __name__ == '__main__':
    text = '.محمد & حمزﻫ در , تاریخ ۲۴/12 به ("دانشگاهِ شریف") رفتند '
    norm = Normalizer(['en'])
    start = time.time()

    start = time.time()
    for i in range(10000):
        norm.normalize(text, )
    end = time.time()
    print(end - start)
    # for 10 time = 5s ( first normalizer)
    # for 10 time = 4.110s ( second normalizer)
    # for 10 time = 0.059s ( third normalizer)
