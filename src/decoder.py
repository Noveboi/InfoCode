import polynomials as p

def convert_to_binary_str(file_bin: bytes, num_bytes: int, n: int) -> list[str]:
    bin_list = []
    for i in range(0, len(file_bin) - num_bytes + 1, num_bytes):
        bin_str = ''.join(format(b, '08b') for b in file_bin[i:i+num_bytes])[8*num_bytes - n:]
        bin_list.append(bin_str)
    return bin_list

def decode(enc_file: list[str], generator_polynomial: list[int], encoding: str) -> tuple[list[list[int]], int]:
    errors = 0
    decoded = []
    n = len(enc_file[0])
    deg = p.deg(generator_polynomial)
    if encoding == 'cyclic':
        for bin_str in enc_file:
            codeword = [int(bit) for bit in bin_str]
            div = p.divide(codeword, generator_polynomial)   
            q = div[0]
            r = div[1]

            # If remainder = 0, then no errors are present and the quotient is the original message
            # If remainder = x^n, for some n, then a single error is present
            if r.count(1) == 1:
                errors += 1
                err = r.index(1)
                q[err] = int(not q[err])
            elif r.count(1) > 1:
                errors += 1

            for _ in range(deg):
                q.pop()

            decoded.append(q)
        return (decoded, errors)
    else:
        return None

def decompress(dec_file: list[str], compression_algorithm: str):
    pass