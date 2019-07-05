import sys
import re
import unicodedata

python_version = sys.version_info[0]

def remove_accents(s):
    if python_version < 3:
        s = s.decode('utf-8')
        s = re.sub(unichr(272), 'D', s)
        s = re.sub(unichr(273), 'd', s)
    else:
        s = re.sub('\u0110', 'D', s)
        s = re.sub('\u0111', 'd', s)
    if python_version < 3:
        return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')
    else:
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')