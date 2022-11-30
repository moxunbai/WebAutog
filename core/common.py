

import re

# [0.,0.,0.] = ti.math.[0.,0.,0.]

def splitStr(s,chart=' '):
    return  re.sub(' +',' ',s).strip().split(' ')


def parsePxValue(s):
    return float(s[:len(s)-2]) if s.endswith('px') else 0       