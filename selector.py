import random
import bisect
import copy


class Selector:
    def __init__(self, seq, dcopy=False):
        self.seq = seq
        self.dcopy = dcopy

    def select(self):
        selection = random.choice(self.seq)
        if self.dcopy:
            return copy.deepcopy(selection)
        else:
            return selection


class SelectorWeighted(Selector):
    def __init__(self, seq, weights, dcopy=False):
        super().__init__(seq, dcopy)
        self.max_rint = sum(weights)
        trunc = weights[:-1]
        self.weights = [sum(trunc[0:idx+1]) for idx, _ in enumerate(trunc)]

    def select(self):
        rint = random.randrange(self.max_rint)
        idx = bisect.bisect(self.weights, rint)
        selection = self.seq[idx]
        if self.dcopy:
            return selection
        else:
            return copy.deepcopy(selection)


class SelectorBag(Selector):
    def __init__(self, seq, counts, dcopy=False):
        super().__init__(seq, dcopy)
        self.max_rint = sum(counts)
        trunc = counts[:-1]
        self.counts = [sum(trunc[0:idx+1]) for idx, _ in enumerate(trunc)]

    def select(self):
        if self.max_rint == 0:
            return None
        elif len(self.counts) == 0:
            self.max_rint -= 1
            return self.seq[0]
        rint = random.randrange(self.max_rint)
        idx = bisect.bisect(self.counts, rint)
        selection = self.seq[idx]
        self.counts = self.counts[:idx] + [v-1 for v in self.counts[idx:]]
        self.max_rint -= 1
        for idx, count in enumerate(self.counts):
            if len(self.counts) == 0:
                break
            elif count < 1:
                self.counts.pop(idx)
                self.seq.pop(idx)
        if self.dcopy:
            return selection
        else:
            return copy.deepcopy(selection)
