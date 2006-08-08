import datetime

def mstime(td):
    return td.days*24*60*60*1000000+td.seconds*1000000+td.microseconds

def tdtime(ms):
    return datetime.timedelta(ms / (24*60*60*1000000), (ms / 1000000) % (24*60*60), ms % 1000000)

class sorteddict(dict):
    cmp = cmp
    key = None
    reverse=False
    def __init__(self, *arg, **kw):
	dict.__init__(self, *arg, **kw)
	self.__keys = dict.keys(self)
	self.__is_sorted = False

    def __get_keys(self):
	if not self.__is_sorted:
	    self.__keys.sort(cmp=self.cmp,
                           key=self.key,
                           reverse=self.reverse)
	    self.__is_sorted = True
	return self.__keys

    def __setitem__(self, key, value):
	if key not in self:
	    self.__keys.append(key)
	    self.__is_sorted = False
	return dict.__setitem__(self, key, value)

    def __delitem__(self, key):
	self.__keys.remove(key)
        dict.__delitem__(self, key)

    def iteritems(self):
	for key in self.__get_keys():
	    yield (key, self[key])

    def iterkeys(self):
        return iter(self.__get_keys())

    def itervalues(self):
        for key in self.__get_keys():
	    yield self[key]

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return self.__get_keys()

    def values(self):
        return list(self.itervalues())

    def clear(self):
        dict.clear(self)
        self.__keys = []

    def pop(self, key, *arg):
        if key in self:
            self.__keys.remove(key)
        return dict.pop(self, key, *arg)

    def popitem(self):
        key = self.__get_keys().pop()
        return key, dict.pop(self, key)

    def setdefault(self, key, default = None):
        if key in self: return self[key]
        self[key] = default
        return default

    def update(self, other):
        for key, value in other.iteritems():
            self[key] = value

    def __iter__(self):
        return self.itervalues()

    def __repr__(self):
        return '{' + ', '.join(["%s: %s" % item for item in self.iteritems()]) + '}'

    def __str__(self): return repr(self)

    def __unicode__(self): return repr(self)
    
class reversesorteddict(sorteddict):
    reverse=True
