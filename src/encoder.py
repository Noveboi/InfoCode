from os import path
import polynomials as p
from datetime import datetime

try:
    log = open(path.abspath('./logs/process.txt'), 'w')
except:
    log = None
n = 0

def cyclic_encode(code: dict[int, str], generator: list[int]):
    print(f"[{datetime.now()}] Started encoding file into a cyclic linear code")
    global log
    k = len(list(code.values())[0])
    deg = p.deg(generator)

    global n
    n = k + deg

    # Add padding
    generator += [0] * (k - 1)    
    cyclic_code = {}

    print(f"n = {n}", file=log)
    print(f"k = {k}", file=log)
    print(f"deg(g(x)) = {deg}\n-------------", file=log)

    # Foreach message, we multiply it by the generator polynomial
    # PADDING: to the right 
    for key in code.keys():
        message = [int(bit) for bit in code[key]] + [0]*deg
        codeword = []

        # Loop through each bit (or coefficient) of the message (or polynomial) 'm'
        # Polynomial multiplication in binary form
        print(f"Generating codeword for message: {message}", file=log)
        for i in range(n):
            polynomial_coef = message[i]
            
            if polynomial_coef == 1:
                gen = p.shift(generator, i)
                print(f"{generator} --shift({i})--> {gen}", file=log)
                if len(codeword) == 0:
                    for g in gen: 
                        codeword.append(g)
                else:
                    temp = codeword.copy()
                    for j in range(n):
                        codeword[j] ^= gen[j]
                    print(f"{temp} XOR {gen} = {codeword}", file=log)
        if len(codeword) == 0:
            for _ in range(n):
                codeword.append(0)
        print(f"Codeword: {codeword}", file=log)
        print(file=log)
        codeword = [str(i) for i in codeword]
        cyclic_code[key] = ''.join(codeword)
        
    print("Generated cyclic linear code", file=log)
    for key in cyclic_code.keys():
        print(f"{key}: {cyclic_code[key]}", file=log)
    return cyclic_code

def encode_file(file: bytes, code: dict[int, str], generator: list[int]) -> str:
    """
    Encodes a file using cyclic linear encoding 

    Parameters
    ------
    file: The bytes object representing the file to be encoded 
    generator: The coefficients of the generator polynomial

    Returns
    ------
    The encoded binary in string format
    """
    cyclic_code = cyclic_encode(code, generator)
    print(f"[{datetime.now()}] Encoding process finished!")

    encoded_bin = ''
    for b in file:
        encoded_bin = ''.join((encoded_bin, cyclic_code[b]))

    print(f"[{datetime.now()}] File encoded successfully!")
    return encoded_bin

def convert_to_bytes(bins: list[str]) -> tuple[bytes, int]:
    k = len(bins[0])
    num_of_bytes = (k + 7) // 8
    byte_list = []
    print(f"[{datetime.now()}] For each binary string of length {k}, generating {num_of_bytes} bytes")
    # Each b is constant length k, same padding is applied foreach b
    for b in bins:
        padded_bin = b.zfill(num_of_bytes * 8)
        byte_list.append(int(padded_bin, 2).to_bytes(num_of_bytes))
    return (b''.join(byte_list), num_of_bytes)