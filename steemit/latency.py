import threading

# constant time to reply on posts
steemit_reply_latency = 20

# empty func for timer
def empt():
    pass

# wrapper on function which simulates posting comments latency
def post_latency(fn):
    
    def wrapper(x, y=None):
        #print(threading.active_count(), 'count')
        if threading.active_count() < 2:
            threading.Timer(steemit_reply_latency, empt, ()).start()
            fn(x, y)
        else:
            time_pause = (threading.active_count() - 1) * steemit_reply_latency
            threading.Timer(time_pause, fn, (x, y)).start() 
            print(time_pause, "sec pause")

    return wrapper

