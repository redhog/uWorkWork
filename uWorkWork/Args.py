def parseArgs(args):
    res = {}
    if args:
        sargs = args.split(',')
        for item in sargs:
            sitem = item.split('=')
            if len(sitem) == 2:
                key, value = sitem[0], sitem[1]
                res[key.strip()] = value.strip()
    return res
