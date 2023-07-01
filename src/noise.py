import random
from datetime import datetime

def add_noise(enc: str, n: int, X: float) -> tuple[list[str], int]: 
    """
    Add X% noise to a pure binary string 
    """
    errors_generated = 0
    new_enc = ""
    if X < 0 or X > 1: 
        raise ValueError("X is a probability from 0 to 1!")

    for i in range(len(enc)):
        if random.random() < X:
            errors_generated += 1
            new_enc += str(int(not int(enc[i])))
        else:
            new_enc += enc[i]
    
    print(f"[{datetime.now()}] Generated {errors_generated} errors! ({errors_generated*100/len(enc)}% of bits flipped)")
    code = []
    for i in range(0, len(enc), n):
        code.append(new_enc[i:i+n])

    return (code, errors_generated)