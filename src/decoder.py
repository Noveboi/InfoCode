import polynomials as p

def convert_to_binary_str(file_bin: bytes, num_bytes: int, n: int) -> list[str]:
    """
    Convert a pure binary file into its binary string representation.
    """
    bin_list = []
    for i in range(0, len(file_bin) - num_bytes + 1, num_bytes):
        bin_str = ''.join(format(b, '08b') for b in file_bin[i:i+num_bytes])[8*num_bytes - n:]
        bin_list.append(bin_str)
    return bin_list

def decode(enc_file: list[str], generator_polynomial: list[int], encoding: str):
    """
    Decode the encoded file (represented in binary string form) using polynomial division

    Process
    -------
    Suppose for each binary string in enc_file the following polynomials:
        - r(x): received polynomials (the received bytes)
        - m(x): the original message polynomial
        - g(x): the generator polynomial
    
    When encoding, the process was c(x) = m(x)g(x), where c(x) is the codeword polynomial
    to get the original message back, we do m(x) = c(x)/g(x)!

    Notice that r(x) = c(x) + e(x) where e(x) is some error.

    We then have:
        - m(x) = r(x)/g(x) <=> m(x) = (c(x) + e(x))/g(x)

    How do we detect e(x)?
    ----------------------
    When doing (c(x) + e(x))/g(x), c(x) will be the quotient and e(x) will be the remainder
    IFF e(x) = 0 OR e(x) = x^n for some valid n.
    If e(x) has two or more terms, the quotient will NOT be the correct c(x)!   
    """
    errors = 0
    fixed = 0
    decoded = []
    n = len(enc_file[0])
    deg = p.deg(generator_polynomial)
    generator_polynomial += [0] * (n - deg - 1)

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
                fixed += 1
            elif r.count(1) > 1:
                errors += 1

            for _ in range(deg):
                q.pop()

            decoded.append(q)
        return (decoded, errors, fixed)
    else:
        return None
