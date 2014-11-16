def chunker(iterable, chunksize):
    for i in xrange(0, len(iterable), chunksize):
        yield iterable[i:i+chunksize]

def collect_modular_elements(vigenere_cyphertext):
    modulus_streams = {}
    max_len = len(vigenere_cyphertext)
    for stream_length in xrange(1, max_len):
        print "stream length: %s" % stream_length
        modulus_streams[stream_length] = create_Nth_stream(vigenere_cyphertext, stream_length, max_len)

    return modulus_streams

def create_Nth_stream(iterable, N, max_len):
    stream = {}
    for index, element in enumerate(iterable):
        try:
            stream[index%N].append(element)
        except KeyError:
            stream[index%N] = [element]
    print "stream: %s" % stream
    scaling_factor = float(max_len) / float(N)
    find_scaled_most_freq_in_stream(stream, scaling_factor)
    return stream

def most_freq_in_list(iterable):
    count_dict = {}
    for element in iterable:
        try:
            count_dict[element] = count_dict[element] + 1
        except KeyError:
            count_dict[element] = 1

    most_frequent = max(count_dict.values())
    return most_frequent

def find_scaled_most_freq_in_stream(stream, scaling_factor):
    max_seen = 0
    for obs_vals in stream.values():
        scaling_factor = 
        max_count = most_freq_in_list(obs_vals)
        if max_seen < max_count:
            max_seen = max_count
    print "max_seen is %s" % max_seen

def main():
    import sys
    fc = (open(sys.argv[1], 'r').read()).strip()
    chunked_cyphertext = [x for x in chunker(fc, 2)]
    collect_modular_elements(chunked_cyphertext)

if __name__ == '__main__':
    main()
