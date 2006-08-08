import datetime, Utils

def byNone(items, subSorts):
    assert not subSorts
    total = datetime.timedelta(0)
    for item in items:
        total += item['length']
    return (total, items)

def byPage(items, subSorts):
    byPage = Utils.reversesorteddict()
    total = datetime.timedelta(0)
    for item in items:
        total += item['length']
        if item['page'] not in byPage: byPage[item['page']] = ([], datetime.timedelta(0))
        byPage[item['page']][0].append(item)
        byPage[item['page']][1] += item['end'] - item['start']
    if subSorts:
        for page, items in byPage.iteritems():
            byPage[page] = subSorts[0](items, subSorts[1:])
    return (total, byPage)

def byCategory(items, subSorts):
    byCategory = Utils.reversesorteddict()
    total = datetime.timedelta(0)
    for item in items:
        total += item['length']
        for category in item['categories']:
            if category not in byCategory: byCategory[category] = []
            byCategory[category].append(item)
    if subSorts:
        for category, items in byCategory.iteritems():
            byCategory[category] = subSorts[0](items, subSorts[1:])
    return (total, byCategory)

def byStatus(items, subSorts):
    byStatus = Utils.reversesorteddict()
    total = datetime.timedelta(0)
    for item in items:
        total += item['length']
        if item['status'] not in byStatus: byStatus[item['status']] = []
        byStatus[item['status']].append(item)
    if subSorts:
        for status, items in byStatus.iteritems():
            byStatus[status] = subSorts[0](items, subSorts[1:])
    return (total, byStatus)

def byPeriod(start, length):
    mslength = Utils.mstime(length)
    def byPeriod(items, subSorts):
        byPeriod = Utils.reversesorteddict()
        total = datetime.timedelta(0)
        for item in items:
            assert start <= item['start']
            total += item['length']
            # For some reason timedelta doesn't support the % operation, so we do it by hand...:
            offset = (item['start'] - start)
            msoffset = Utils.mstime(offset)
            bucket = start + Utils.tdtime((msoffset // mslength) * mslength)
            if bucket not in byPeriod: byPeriod[bucket] = []
            byPeriod[bucket].append(item)
        if subSorts:
            for bucket, items in byPeriod.iteritems():
                byPeriod[bucket] = subSorts[0](items, subSorts[1:])
        return (total, byPeriod)
    return byPeriod

def inPeriod(start, end):
    def inPeriod(items, subSorts):
        inPeriod = []
        total = datetime.timedelta(0)
        for item in items:
            if start <= item['start'] <= end:
                total += item['length']
                inPeriod.append(item)
        if subSorts:
            dummy, inPeriod = subSorts[0](inPeriod, subSorts[1:])
        return (total, inPeriod)
    return inPeriod

def sort(items, ops = []):
    ops += [byNone]
    return ops[0](items, ops[1:])
