import datetime, uWorkWork.Args, uWorkWork.Parser, uWorkWork.Sort

defaultArgs = {
    }

def execute(macro, argstr):
    request = macro.request
    formatter = macro.formatter
    args = {
        'category': 'UWorkWork',
        'start': 'dawn of time',
        'length': '7 days',
        'end': 'now'
        }
    args.update(defaultArgs)
    args.update(uWorkWork.Args.parseArgs(argstr))
    for item in macro.form.items():
        args[item[0]]=item[1][0]
    items = uWorkWork.Parser.parseCategory(request, args['category'])
    start = uWorkWork.Parser.read_datetime(args['start'])
    length = uWorkWork.Parser.read_timedelta(args['length'])
    end = uWorkWork.Parser.read_datetime(args['end'])
    total, byStatusPeriodCategory = uWorkWork.Sort.sort(
        items,
        [uWorkWork.Sort.inPeriod(start, end),
         uWorkWork.Sort.byStatus,
         uWorkWork.Sort.byPeriod(start, length),
         uWorkWork.Sort.byCategory])
    result = []

    result.append('<h1>%s (%s)</h1>' % (args['category'], total))
    result.append("""
    <form method='get'>
     Display items between
     <input type="text" name='start' value='%(start)s' />
     and
     <input type="text" name='end' value='%(end)s' />
     in blocks of 
     <input type="text" name='length' value='%(length)s' />
     <input type="submit" name='submit' value='Submit' />
    </form>
    """ % args)
    result.append('<ul>')
    for status, (statusTotal, byPeriodCategory) in byStatusPeriodCategory.iteritems():
        statustag = args['category'] + '-' + str(status)
        result.append('<li><a href="#%s">%s (Total: %s)</a></li>' % (statustag, ['', 'Due items', 'In progress', 'Done'][status], statusTotal))
        result.append('<ul>')
        for period, (periodTotal, byCategory) in byPeriodCategory.iteritems():
            periodtag = statustag + '-' + str(period)
            result.append('<li><a href="#%s">%s - %s (Total: %s)</a></li>' % (periodtag, period, period + length, periodTotal))
            result.append('<ul>')
            for category, (categoryTotal, items) in byCategory.iteritems():
                categorytag = periodtag + '-' + category
                result.append('<li><a href="#%s">%s (Total: %s)</a></li>' % (categorytag, category, categoryTotal))
            result.append('</ul>')
        result.append('</ul>')
    result.append('</ul>')

    for status, (statusTotal, byPeriodCategory) in byStatusPeriodCategory.iteritems():
        statustag = args['category'] + '-' + str(status)
        result.append('<div class="status"><a name="%s"><h1>%s (Total: %s)</h1></a>' % (statustag, ['', 'Due items', 'In progress', 'Done'][status], statusTotal))
        for period, (periodTotal, byCategory) in byPeriodCategory.iteritems():
            periodtag = statustag + '-' + str(period)
            result.append('<div class="period"><a name="%s"><h2>%s - %s (Total: %s)</h2></a>' % (periodtag, period, period + length, periodTotal))
            for category, (categoryTotal, items) in byCategory.iteritems():
                categorytag = periodtag + '-' + category
                result.append('<div class="category"><a name="%s"><h3>%s (Total: %s)</h3></a>' % (categorytag, category, categoryTotal))
                for item in items:
                    result.append('<div class="item">')
                    result.append('%s - %s (%s) %s' % (item['start'], item['end'], item['length'], item['title']))
                    result.append('</div>')
                result.append('</div>')
            result.append('</div>')
        result.append('</div>')
    
    return formatter.rawHTML('\n'.join(result))
