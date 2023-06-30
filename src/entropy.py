from collections import Counter
from math import log2

def calculate_entropy(bytes_object):
    byte_counts = Counter(bytes_object)
    total_bytes = len(bytes_object)

    entropy = 0.0
    for count in byte_counts.values():
        p = count / total_bytes
        entropy -= p*log2(p)
    return entropy