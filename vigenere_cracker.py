import sys

def chunker(iterable, chunksize):
    for i in xrange(0, len(iterable), chunksize):
        yield iterable[i:i+chunksize]

class Analyzer(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data


class VigenereAnalyzer(Analyzer):
    def __init__(self, raw_data):
        Analyzer.__init__(self, raw_data)
        #print "self.raw_data: %s" % self.raw_data
        self.data_length = len(raw_data)
        self.modulus_streams = self.collect_modular_elements()

    def collect_modular_elements(self):
        """
        return a list of streams, each index is `key_length_guess - 1`
        """
        modulus_streams = []
        for posited_key_length in xrange(1, self.data_length):
            #print "key length guess: %s" % posited_key_length
            modulus_streams.append(self.create_Nth_stream(self.raw_data, posited_key_length))
            #print

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

    def collect_most_freq_from_Nth_stream(self, Nth_stream):
        most_freq_list = []
        for period in Nth_stream.values():
            most = self.most_freq_in_list(period)
            most_freq_list.append(most)
        return most_freq_list

    def guess_key_length(self):
        mod_stream_scaled_maxes = []
        guessed_lengths = []
        exceptions = []
        for kl_guess_minus_one, modulus_stream in enumerate(self.modulus_streams):
            kl_guess = kl_guess_minus_one + 1
            max_list = self.collect_most_freq_from_Nth_stream(modulus_stream)
            max_stat = sum(max_list) / float(kl_guess)
            mod_stream_scaled_maxes.append(max_stat)
        for i, current_ms_scaled_max in enumerate(mod_stream_scaled_maxes):
            try:
                previous_max = mod_stream_scaled_maxes[i-1]
            except IndexError:
                continue

            if previous_max < current_ms_scaled_max:
                try:
                    next_max = mod_stream_scaled_maxes[i+1]
                except IndexError:
                    continue

                previous_current_dist = abs(previous_max - current_ms_scaled_max)
                current_upcoming_dist = abs(current_ms_scaled_max - next_max)
                previous_upcoming_dist = abs(previous_max - next_max)
                if (previous_current_dist > (6*previous_upcoming_dist)) and (current_upcoming_dist > (6*previous_upcoming_dist)):
                    guessed_lengths.append(i+1)
                    #print "%s: %s" % (i-1,previous_max)
                    #print "%s: %s" % (i,current_ms_scaled_max)
                    #print "%s: %s" % (i+1,next_max)
        best_guess = guessed_lengths[0]
        for glen in guessed_lengths:
            if glen%guessed_lengths[0] == 0:
                continue
            else:
                #print "glen: %s not divisible by guessed_length[0]: %s Guess again!" % (glen, guessed_lengths[0])
                exceptions.append(glen)
        #print guessed_lengths
        #print exceptions
        multiples_of_best = [x for x in range(0, self.data_length, best_guess)[1:]]
        for mob in multiples_of_best:
            if mob not in guessed_lengths:
                print "mob not seen! mob: %s" % mob
        return guessed_lengths[0]

def main():
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
