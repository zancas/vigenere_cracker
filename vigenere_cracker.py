def chunker(iterable, chunksize):
    for i in xrange(0, len(iterable), chunksize):
        yield iterable[i:i+chunksize]

def collect_modular_elements(vigenere_cyphertext):
    modulus_streams = {}
    max_len = len(vigenere_cyphertext)
    for stream_length in xrange(1, max_len):
        print "stream length: %s" % stream_length
        modulus_streams[stream_length] = create_Nth_stream(vigenere_cyphertext, stream_length)
        print

    return modulus_streams

def create_Nth_stream(iterable, N):
    Nth_stream = {}
    for index, element in enumerate(iterable):
        try:
            Nth_stream[index%N].append(element)
        except KeyError:
            Nth_stream[index%N] = [element]
    find_scaled_most_freq_in_Nth_stream(Nth_stream, N)
    return Nth_stream

def create_freq_dict(iterable):
    count_dict = {}
    for element in iterable:
        try:
            count_dict[element] = count_dict[element] + 1
        except KeyError:
            count_dict[element] = 1
    return count_dict

def most_freq_in_list(iterable):
    count_dict = create_freq_dict(iterable)
    most_frequent = max(count_dict.values())
    return most_frequent

def find_scaled_most_freq_in_Nth_stream(Nth_stream, scaling_factor):
    count_of_most_frequent = 0
    for obs_vals in Nth_stream.values():
        max_count = most_freq_in_list(obs_vals)
        #print max_count
        scaled_max = max_count * scaling_factor
        if count_of_most_frequent < scaled_max:
            count_of_most_frequent = scaled_max
    print "count_of_most_frequent is %s" % count_of_most_frequent
    return count_of_most_frequent

def main():
    import sys
    if sys.argv[1] == 'length':
        fc = (open(sys.argv[2], 'r').read()).strip()
        chunked_cyphertext = [x for x in chunker(fc, 2)]
        collect_modular_elements(chunked_cyphertext)

    elif sys.argv[1] == 'key':
        fc = (open(sys.argv[2], 'r').read()).strip()
        chunked_cyphertext = [x for x in chunker(fc, 2)]
        stream_len = create_Nth_stream(chunked_cyphertext, int(sys.argv[3]))

if __name__ == '__main__':
    main()
