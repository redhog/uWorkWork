import datetime

def mstime(td):
    return td.days*24*60*60*1000000+td.seconds*1000000+td.microseconds

def tdtime(ms):
    return datetime.timedelta(ms / (24*60*60*1000000), (ms / 1000000) % (24*60*60), ms % 1000000)
