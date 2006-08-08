import re, datetime, MoinMoin.search, MoinMoin.Page

def timedelta_regexp(prefix):
    if prefix is None:
        open,close='?:(?#',')'
    else:
        open,close='?P<' + prefix,'>'
    return r"""
    ((%(open)syears%(close)s[0-9]+)\s*y(ears?)?)?
    \s*
    ((%(open)sweeks%(close)s[0-9]+)\s*w(eeks?)?)?
    \s*
    ((%(open)sdays%(close)s[0-9]+)\s*d(ays?)?)?
    \s*
    ((%(open)shours%(close)s[0-9]+)\s*h(ours?)?)?
    \s*
    ((%(open)sminutes%(close)s[0-9]+)\s*m(inutes?)?)?
    \s*
    ((%(open)sseconds%(close)s[0-9]+)\s*s(econds?)?)?
    \s*
    ((%(open)smiliseconds%(close)s[0-9]+)\s*(ms | miliseconds?))?
    \s*
    ((%(open)smicroseconds%(close)s[0-9]+)\s*(us | microseconds?))?
    """ % {'open': open, 'close': close}

timedelta_regexp_pattern = re.compile(r'^%s$' % timedelta_regexp(''), re.UNICODE + re.MULTILINE + re.IGNORECASE + re.DOTALL + re.VERBOSE)

def datetime_regexp(prefix):
    if prefix is None:
        open,close='?:(?#',')'
    else:
        open,close='?P<' + prefix,'>'
    return r"""
    (%(open)sdawnoftime%(close)sdawn \s of \s time)
    |
    (%(open)snow%(close)snow)
    |
    (
        in
        \s*
        (%(open)sfuture%(close)s%(future)s)
    )
    |
    (
        (%(open)spast%(close)s%(past)s)
        \s*
        ago
    )
    |
    (
        (
            (%(open)sdate1%(close)s
                (%(open)syear1%(close)s19\d{2} | 20\d{2} | \d{2} )
                [./-]
                (%(open)smonth1%(close)s1[012] | 0[1-9] | [1-9])
                [./-]
                (%(open)sday1%(close)s3[01] | 0[1-9] | [12]\d | [1-9])
            )
            |
            (%(open)sdate2%(close)s
                (%(open)smonth2%(close)sjanuary|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sep|october|oct|november|nov|december|dec)
                [ ]+
                (%(open)sday2%(close)s3[01] | 0[1-9] | [12]\d | [1-9])
                (?: st | nd | rd | th )?
                [ ,]+
                (%(open)syear2%(close)s19\d{2} | 20\d{2} | \d{2})
            )
            |
            (%(open)sdate3%(close)s
                (%(open)syear3%(close)s19\d{2} | 20\d{2} | \d{2} )
                (%(open)smonth3%(close)s1[012] | 0[1-9])
                (%(open)sday3%(close)s3[01] | 0[1-9] | [12]\d)
            )
        )
        \s*
        (
            (%(open)stime1%(close)s
                (%(open)shour1%(close)s 1[0-2] | [0]?[1-9] )
                (
                        (?: [.:])
                        (%(open)sminute1%(close)s[0-5]\d{0,1} | [6-9])
                        (
                            (?: [.:])
                            (%(open)ssecond1%(close)s[0-5]\d{0,1} | [6-9])
                        )?
                )?
                [ ]*
                (%(open)sam1%(close)s am | pm | p | a )
            )
            |
            (%(open)stime2%(close)s
                (%(open)shour2%(close)s | [01]\d{0,1} | 2[0-3] | [1-9])
                (
                        (?: [.:])
                        (%(open)sminute2%(close)s[0-5]\d{0,1} | [6-9])
                        (
                            (?: [.:])
                            (%(open)ssecond2%(close)s[0-5]\d{0,1} | [6-9])
                        )?
                )?
            )
            |
            (%(open)stime3%(close)s
                (%(open)shour3%(close)s [01]\d | 2[0-3])
                (%(open)sminute3%(close)s [0-5]\d)?
                (%(open)ssecond3%(close)s[0-5]\d{0,1} | [6-9])?
            )
            |
            (%(open)stime4%(close)s
                (%(open)shour4%(close)s 0[1-9] | 1[0-2])
                (%(open)sminute4%(close)s [0-5]\d)?
                (%(open)ssecond4%(close)s[0-5]\d{0,1} | [6-9])?
                [ ]*
                (%(open)sam4%(close)s am | pm | p | a )
            )
        )?
    )
    """ % {'open': open, 'close': close,
           'future': timedelta_regexp(None),
           'past': timedelta_regexp(None)}

datetime_regexp_pattern = re.compile(r'^%s$' % datetime_regexp(''), re.UNICODE + re.MULTILINE + re.IGNORECASE + re.DOTALL + re.VERBOSE)

def item_regex(prefix):
    return r"""
(?P<%(prefix)sitem>^
 \s*
 \{
   (?P<%(prefix)sstatus>[123])
  \}
 \s*
 (?P<%(prefix)stitle>.*?)\s
 (?P<%(prefix)sstart>%(start)s)
 \s*-\s*
 (?P<%(prefix)send>%(end)s)
 \s*
$)
""" % {'prefix': prefix,
       'start': datetime_regexp(None),
       'end': datetime_regexp(None)}

item_regex_pattern = re.compile(r'^%s$' % item_regex(''), re.UNICODE + re.MULTILINE + re.IGNORECASE + re.VERBOSE)


def read_timedelta(string):
    match = timedelta_regexp_pattern.search(string)
    assert(match)

    years = weeks = days = hours = minutes = seconds = miliseconds = microseconds = 0
    if match.group('years'): years = int(match.group('years'))
    if match.group('weeks'): weeks = int(match.group('weeks'))
    if match.group('days'): days = int(match.group('days'))
    if match.group('hours'): hours = int(match.group('hours'))
    if match.group('minutes'): minutes = int(match.group('minutes'))
    if match.group('seconds'): seconds = int(match.group('seconds'))
    if match.group('miliseconds'): miliseconds = int(match.group('miliseconds'))
    if match.group('microseconds'): microseconds = int(match.group('microseconds'))
    return datetime.timedelta(years * 365 + weeks * 7 + days,
                              hours * 60 * 60 + minutes * 60 + seconds,
                              miliseconds * 1000 + microseconds)

def read_datetime(string):
    match = datetime_regexp_pattern.search(string)
    assert(match)

    if match.group('dawnoftime'):
        return datetime.datetime(datetime.MINYEAR, 1, 1)
    elif match.group('now'):
        return datetime.datetime.now()
    elif match.group('future'):
        return datetime.datetime.now() + read_timedelta(match.group('future'))
    elif match.group('past'):
        return datetime.datetime.now() - read_timedelta(match.group('past'))

    # yyyy/mm/dd: 2006/05/10; 06/05/10, 
    if match.group('date1'):
        if len(match.group('year1')) == 2:
            year = '20%s' % match.group('year1')
        else:
            year = match.group('year1')

        month = match.group('month1')
        day = match.group('day1')

    # M dd, yyyy: May 10, 2006; Jan 10th, 2006; Jan 10, 06
    elif match.group('date2'):
        if len(match.group('year2')) == 2:
            year = '20%s' % match.group('year2')
        else:
            year = match.group('year2')

        month = getNumericalMonth(match.group('month2'))
        if not month:
            raise EventcalError('invalid_date')

        day = match.group('day2')

    # yyyymmdd: 20060510, 060510
    elif match.group('date3'):
        if len(match.group('year3')) == 2:
            year = '20%s' % match.group('year3')
        else:
            year = match.group('year3')

        month = match.group('month3')
        day = match.group('day3')

    elif len(string.strip()) == 0:
        return ''
    
    else:
        raise EventcalError('invalid_date')
        
    # 12h with ':': 12:00; 9:00pm
    if match.group('time1'):
        hour = int(match.group('hour1'))
        if match.group('minute1'):
            min = int(match.group('minute1'))
        else:
            min = 0

        if hour < 12 and match.group('am1').lower() == 'pm':
            hour += 12

    # 24h with ':': 12:00; 23:00
    elif match.group('time2'):
        hour = int(match.group('hour2'))
        if match.group('minute2'):
            min = int(match.group('minute2'))
        else:
            min = 0

    # 24h without ':': 1200; 2300
    elif match.group('time3'):
        hour = int(match.group('hour3'))
        if match.group('minute3'):
            min = int(match.group('minute3'))
        else:
            min = 0

    # 12h without ':': 1200; 0900pm
    elif match.group('time4'):

        hour = int(match.group('hour4'))
        if match.group('minute4'):
            min = int(match.group('minute4'))
        else:
            min = 0

        if hour < 12 and match.group('am4').lower() == 'pm':
            hour += 12

    elif len(string.strip()) == 0:
        return ''

    else:
        raise EventcalError('invalid_time X%sX' % repr(string))

    return datetime.datetime(int(year), int(month), int(day), int(hour), int(min))


def searchPages(request, needle):
    return MoinMoin.search.searchPages(
        request,
        MoinMoin.search.QueryParser().parse_query(needle)).hits

class multisearch:
    def __init__(self, pattern, string):
        self.pattern = pattern
        self.string = string
        self.pos = 0
    def __iter__(self):
        return self
    def next(self):
        m = self.pattern.search(self.string, self.pos)
        if m is None: raise StopIteration
        self.pos = m.end() + 1
        return m


def parsePage(request, page):
    items = []
    for matchitem in multisearch(item_regex_pattern, page.get_raw_body()):
        item = {}
        item['page'] = page.page_name
        item['categories'] = page.page_name.split('/')
        item['status'] = int(matchitem.group('status'))
        item['title'] = matchitem.group('title')
        item['start'] = read_datetime(matchitem.group('start'))
        item['end'] = read_datetime(matchitem.group('end'))
        item['length'] = item['end'] - item['start']
        items.append(item)
    return items

def parseCategory(request, category):
    items = []
    for page in searchPages(request, category):
        items.extend(parsePage(request, MoinMoin.Page.Page(request, page.page_name)))
    return items
