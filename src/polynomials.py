def shift(arr, shamt):
    """
    Cyclically shifts the elements of 'arr' by 'shamt' bits

    e.g: arr = [x0, x1, x2, x3], then shift(arr, 1) = [x3, x0, x1, x2]
    """
    n = len(arr)
    if (shamt < 0) or shamt % n == 0:
        return arr
    
    old_arr = arr[:]
    new_arr = [0]*n
    for i in range(shamt % n):
        if i > 0: 
            old_arr = new_arr[:]
        new_arr[0] = old_arr[-1]
        new_arr[-1] = old_arr[-2]
        for j in range(1, n - 1):
            new_arr[j] = old_arr[j - 1]
    return new_arr

def deg(x: list[int]):
    """
    Gets the degree of a polynomial representation as a list of coefficients
    """
    idxs = [i for i, coef in enumerate(x) if coef == 1]
    return max(idxs) if len(idxs) != 0 else 0

def xor(x: list[int], y: list[int]):
    """
    Perform the bitwise XOR operation for every bit of x and y
    """
    if len(x) != len(y): 
        raise ValueError(f"x XOR y requires x and y to have equal length! len(x) = {len(x)} | len(y) = {len(y)}")
    l = len(x)
    result = [0 for _ in range(l)]
    for i in range(l):
        result[i] = int(x[i] ^ y[i])
    return result

def divide(a: list[int], b: list[int]) -> tuple[list[int], list[int]]:
    """
    Divides two polynomials a and b.
    a and b are expected to be the coeffiecients of the polynomials

    Returns
    -----------
    A tuple containing the quotient and remainder
    """
    deg_a = deg(a)
    deg_b = deg(b)
    x = a.copy()
    q = [0 for _ in range(len(a))]
    y = b.copy()
    while deg_a >= deg_b:
        shamt = deg_a - deg_b
        q[shamt] = 1
        shy = shift(y, shamt)
        x = xor(x, shy)

        deg_a = deg(x)
        deg_b = deg(y)
    
    return (q, x)