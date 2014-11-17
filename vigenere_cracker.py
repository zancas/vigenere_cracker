def chunker(iterable, chunksize):
    for i in xrange(0, len(iterable), chunksize):
        yield iterable[i:i+chunksize]

class Analyzer(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data


class VigenereAnalyzer(Analyzer):
    def __init__(self, raw_data):
        Analyzer.__init__(self, raw_data)
        print "self.raw_data: %s" % self.raw_data
        self.data_length = len(raw_data)
        self.modulus_streams = self.collect_modular_elements()

    def collect_modular_elements(self):
        """
        return a dict with keys which are possible key lengths
        """
        modulus_streams = {}
        for posited_key_length in xrange(1, self.data_length):
            print "key length guess: %s" % posited_key_length
            modulus_streams[posited_key_length] = self.create_Nth_stream(self.raw_data, posited_key_length)
            print

        return modulus_streams

    def create_Nth_stream(self, iterable, N):
        """
        return a dict where a key is an offset start positions, and a value is a list of bytes sampled
        from that offset with a perfiod set by the "N" parameter
        """
        Nth_stream = {}
        for index, element in enumerate(iterable):
            period = index%N
            try:
                Nth_stream[period].append(element)
            except KeyError:
                Nth_stream[period] = [element]
        #self.find_scaled_most_freq_in_Nth_stream(Nth_stream, N)
        return Nth_stream

    def create_freq_dict(self, iterable):
        count_dict = {}
        for element in iterable:
            try:
                count_dict[element] = count_dict[element] + 1
            except KeyError:
                count_dict[element] = 1
        return count_dict

    def most_freq_in_list(self, iterable):
        count_dict = self.create_freq_dict(iterable)
        most_frequent = max(count_dict.values())
        return most_frequent

    def find_scaled_most_freq_in_Nth_stream(self, Nth_stream, scaling_factor):
        count_of_most_frequent = 0
        for obs_vals in Nth_stream.values():
            max_count = self.most_freq_in_list(obs_vals)
            scaled_max =  max_count * scaling_factor
            if count_of_most_frequent < scaled_max:
                count_of_most_frequent = scaled_max
            print "count_of_most_frequent is %s" % count_of_most_frequent
        return count_of_most_frequent

    def guess_key_length(self):

def main():
    import sys
    if sys.argv[1] == 'length':
        fc = (open(sys.argv[2], 'r').read()).strip()
        chunked_cyphertext = [x for x in chunker(fc, 2)]
        analyzer = VigenereAnalyzer(chunked_cyphertext)
        analyzer.guess_key_length()
        
    """elif sys.argv[1] == 'key':
        fc = (open(sys.argv[2], 'r').read()).strip()
        chunked_cyphertext = [x for x in chunker(fc, 2)]
        stream_len = create_Nth_stream(chunked_cyphertext, int(sys.argv[3]))
    """

if __name__ == '__main__':
    main()
