from collections import Counter

def get_file(path):
    with open(path, 'rb') as f:
        bin_data = f.read()

    print(f"Read {path} into memory")
    return bin_data

def getProbabilities(binary: bytes):
    symbol_occurences = Counter(binary)
    total_symbols = len(binary)
    probs = {symbol : occurs / total_symbols for symbol, occurs in symbol_occurences.items() }
    sorted_probs = list(reversed(sorted(probs.items(), key=lambda item: item[1])))
    print("Calculated and sorted symbol occurence probabilities")

    return sorted_probs

def partition(probs: list):
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

def generateCode(symbols: tuple):
    probs = symbols[0] + symbols[1]
    codes = {symbol : '' for symbol, _ in probs}
    print("Beginning code generation using Fano-Shannon...")
    return generateCodesDAC(symbols, codes)

# codes will be a {symbol: code} dictionary
def generateCodesDAC(symbols: tuple, codes: dict):

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

def add_padding(code: dict):
    max_digits = len(max([codeword for _, codeword in code.items()]))
    for key in code.keys():
        pad_amount = max_digits - len(code[key])
        code[key] += '0'*pad_amount
    print("Added padding to code")

def get_compression_code(file: bytes) -> dict[int, str]:
    probs = getProbabilities(file)
    part = partition(probs)
    code = generateCode(part)
    print("Finished generating codes using Fano-Shannon!")
    add_padding(code)

    print("Compression finished!")
    return code

def decompress(bytes_list: list[list[int]], compression_code: dict[int, str]) -> bytes:
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