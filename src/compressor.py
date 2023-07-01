from collections import Counter
from datetime import datetime


def get_file(path):
    with open(path, 'rb') as f:
        bin_data = f.read()

    print(f"[{datetime.now()}] Read {path} into memory")
    return bin_data

def getProbabilities(binary: bytes) -> list[tuple[int, float]]:
    """
    Counts the number of occurences for each byte symbol

    Returns
    -------
    The sorted probabilities for all byte symbols in the form of a dict-like list where
    for each element of the list there exists a tuple[int, float] where tuple[0] is the 
    'key' or the symbol (byte) and tuple[1] is the 'value' or the probability occurence of the
    symbol referenced in the 'key'
    """
    symbol_occurences = Counter(binary)
    total_symbols = len(binary)
    probs = {symbol : occurs / total_symbols for symbol, occurs in symbol_occurences.items() }
    sorted_probs = list(reversed(sorted(probs.items(), key=lambda item: item[1])))
    print(f"[{datetime.now()}] Calculated and sorted symbol occurence probabilities")

    return sorted_probs

def partition(probs: list[tuple[int, float]]) -> tuple[list[tuple[int, float]]]:
    """
    Partitions a list of sorted probabilities P into two lists P1, P2 that are subsets of P
    
    Partition Split Condition
    ---
    The list P is split in two WHEN the difference of the sums of P1 and P2 is MINIMUM.
    In other words, partition when |sum(P1) - sum(P2)| == min

    Parameters
    ----------
    - probs: 
        The function takes dict-like object that has elements of type tuple[int, float] where
        tuple[0] is the symbol (byte) and tuple[1] is the probability of occurence

    Returns
    -------
    A 2-tuple that contains the split-in-two probs parameter
    """
    diffs = []
    for i in range(len(probs)):
        left = probs[:i]
        right = probs[i:]
        sum_left = sum([tup[1] for tup in left])
        sum_right = sum([tup[1] for tup in right])
        diffs.append((abs(sum_left - sum_right), i))

    partition_index = min(diffs, key=lambda item: item[0])[1]
    left_partition = probs[:partition_index]
    right_partition = probs[partition_index:]
    return (left_partition, right_partition)

def generateCode(partitioned_symbols: tuple[list[tuple[int, float]]]) -> dict[int, str]:
    """
    Generate codewords for each byte of a file based on the occurence probabilities of each byte.

    Parameters
    ----------
    - partitioned_symbols: 
        The 2-tuple containing the split-in-two dict-like list.

    Returns
    ---------
    A [symbol -> code] dictionary where:
        - symbol: the byte in int form 
        - code: the binary string of the code the byte was assigned 
    """
    partitioned_probs = partitioned_symbols[0] + partitioned_symbols[1]
    codes = {symbol : '' for symbol, _ in partitioned_probs}
    print(f"[{datetime.now()}] Beginning code generation using Fano-Shannon...")
    return generateCodesDAC(partitioned_symbols, codes)

# codes will be a {symbol: code} dictionary
def generateCodesDAC(symbols: tuple[list[tuple[int, float]]], codes: dict[int, str]) -> dict[int, str]:
    """
    Generates the codes recursively using a Divide and Conquer approach
    """
    left_part = symbols[0]
    right_part = symbols[1]
    left_len = len(left_part)
    right_len = len(right_part)

    if left_len == 0 or right_len == 0: return

    ilist = [symbol for symbol, _ in left_part]
    jlist = [symbol for symbol, _ in right_part]

    for i in ilist:
       codes[i] += '0'
    for j in jlist:
        codes[j] += '1'
    
    generateCodesDAC(partition(left_part), codes)
    generateCodesDAC(partition(right_part), codes)
    return codes

def add_padding(code: dict[int, str]) -> None:
    """
    Modify the code by reference and add pad each codeword so that len(codeword) == max(len(code))
    """
    max_digits = len(max([codeword for _, codeword in code.items()]))
    for key in code.keys():
        pad_amount = max_digits - len(code[key])
        code[key] += '0'*pad_amount
    print(f"[{datetime.now()}] Added padding to code")

def get_compression_code(file: bytes) -> dict[int, str]:
    """
    Perfoms a 'Fano-Shannon' like algorithm to obtain a compression code for the given file
    """
    probs = getProbabilities(file)
    part = partition(probs)
    code = generateCode(part)
    print(f"[{datetime.now()}] Finished generating codes using Fano-Shannon!")
    add_padding(code)

    print(f"[{datetime.now()}] Compression finished!")
    return code

def decompress(bytes_list: list[list[int]], compression_code: dict[int, str]) -> bytes:
    """
    Decompress a compressed file given in the form of a list[list[int]] object

    Parameters
    -----------
    - bytes_list:
        Contains the binary data of the compressed file
    - compression_code:
        The codebook that is required for decompression, use the same codebook that was generated during 
        compression in order to get the correct bytes back!

    Returns
    ----------
    The binary of the decompressed file
    """
    inverse_code = {value: key for key, value in compression_code.items()}
    decompressed_file = []
    for i, byte in enumerate([''.join(str(byte) for byte in byte_arr) for byte_arr in bytes_list]):
        try:
            decompressed_file.append(int(inverse_code[byte]))

        # This exception is caught when the file at some point has had 2 or more errors in one byte segment,
        # thus resulting in incorrect decoding. 
        # This is natural, thus we ignore the KeyError exception and move on!
        except KeyError as e:
            print(f"Key error in i={i}")
            print(e)
    return bytes(decompressed_file)