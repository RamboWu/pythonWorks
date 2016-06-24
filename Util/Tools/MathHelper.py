

def percent(a, b):
    if (b == 0):
        b = 1
    return (float(a)/float(b))

def percentToString(a, b):
    if (b == 0):
        b = 1
    return "%.2f%%"%(float(a)/float(b)*100)
