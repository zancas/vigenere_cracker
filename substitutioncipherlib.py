import string

lower_alphabet = string.ascii_lowercase

def key_string_indices(keystring):
    shift_keys = []
    print "lower_alphabet is %s" % lower_alphabet
    for l in keystring:
        print "l is: %s" % l
        ind = lower_alphabet.find(l)
        print "ind is: %s" % ind
        shift_keys.append(ind)
    return shift_keys


def shift_encrypt(shift_keys, plaintext):
    modulus = len(shift_keys)
    print "modulus is: %s" % modulus
    cyphertext = []
    print "plaintext: %s" % plaintext
    for index, p in enumerate(plaintext):
        key_shift = shift_keys[index%modulus]
        p_index = lower_alphabet.find(p)
        shift = (key_shift+p_index)%26
        print "shift is: %s" % shift
        c = lower_alphabet[shift]
        cyphertext.append(c)

    return cyphertext

def grouper(group_size, iterable):
    for i in xrange(0, len(iterable), group_size):
        yield iterable[i:i+group_size]

def ascii_armored_hex_to_int(aahs):
    int_list = [int(x, base=16) for x in grouper(2, aahs)]
    return int_list

def xor_encrypt(key_as_asciiarmored_hex, plaintext):
    key_as_list_of_ints = ascii_armored_hex_to_int(key_as_asciiarmored_hex)
    cypher_bytes = []
    for i, pt in enumerate(plaintext):
        ct = key_as_list_of_ints[i%len(key_as_list_of_ints)] ^ ord(pt)
        cypher_bytes.append(ct)
    return cypher_bytes

def main():
    import sys
    plaintext = sys.argv[2]
    if sys.argv[1] == 'shift':
        Vignere_key = sys.argv[3]
        shift_keys = key_string_indices(Vignere_key)
        print "shift_keys: %s" % shift_keys
        cypher_indices = shift_encrypt(shift_keys, plaintext)
        print cypher_indices
        #cypher_text = ''.join([lower_alphabet.find(ind) for ind in cypher_indices])

    elif sys.argv[1] == 'xor':
        aciihex = sys.argv[3]
        cypher_indices = xor_encrypt(aciihex, plaintext)
        print cypher_indices
        for ct in cypher_indices:
            print hex(ct)

if __name__ == '__main__':
    main()
