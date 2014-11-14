def chunker(iterable, chunksize):
    for i in xrange(0, len(iterable), chunksize):
        yield iterable[i:i+chunksize]

def collect_modular_elements(iterable):
    modulus_streams = {}
    max_len = len(iterable)
    for mod in xrange(1,max_len):
        modulus_streams[mod] = create_stream(iterable, mod)

    return modulus_streams

def create_stream(iterable, modulus):
    stream = {}
    for index, element in enumerate(iterable):
        try:
            stream[index%modulus].append(element)
        except KeyError:
            stream[index%modulus] = [element]
    return stream

def main():
    import sys
    fc = open(sys.argv[1], 'r').read()
    chunked_cyphertext = [x for x in chunker(fc, 2)]
    print collect_modular_elements(chunked_cyphertext)

if __name__ == '__main__':
    main()
