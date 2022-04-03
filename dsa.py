from random import randrange
from hashlib import sha1
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def generar_p_q(L, N):
    g = N  # g >= 160
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # generar q
        while True:
            s = xmpz(randrange(1, 2 ** (g)))
            a = sha1(to_binary(s)).hexdigest()
            zz = xmpz((s + 1) % (2 ** g))
            z = sha1(to_binary(zz)).hexdigest()
            U = int(a, 16) ^ int(z, 16)
            mask = 2 ** (N - 1) + 1
            q = U | mask
            if is_prime(q, 20):
                break
        # generar p
        i = 0  
        j = 2  
        while i < 4096:
            V = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = sha1(to_binary(arg)).hexdigest()
                V.append(int(zzv, 16))
            W = 0
            for qq in range(0, n):
                W += V[qq] * 2 ** (160 * qq)
            W += (V[n] % 2 ** b) * 2 ** (160 * n)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)
            p = X - c + 1
            if p >= 2 ** (L - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1


def generar_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g


def generar_llaves(g, p, q):
    x = randrange(2, q)  # x < q
    y = powmod(g, x, p)
    return x, y


def generar_parametros(L, N):
    p, q = generar_p_q(L, N)
    g = generar_g(p, q)
    return p, q, g


def firmar(M, p, q, g, x):
    """Firma el documento

    Args:
        M (string): Mesanje a firmar
        p (int)
        q (int)
        g (int)
        x (int)

    Raises:
        Exception: Parametros invalidos

    Returns:
        list: parametros que representan la firma
    """
    if not validar_parametros(p, q, g):
        raise Exception("Invalid params")
    while True:
        k = randrange(2, q)  # k < q
        r = powmod(g, k, p) % q
        m = int(sha1(M).hexdigest(), 16)
        try:
            s = (invert(k, q) * (m + x * r)) % q
            return r, s
        except ZeroDivisionError:
            pass


def verificar(M, r, s, p, q, g, y):
    """Valida si la firma es valida

    Args:
        M (string): mensaje cifrado
        r (int)
        s (int)
        p (int)
        q (int)
        g (int)
        y (int)

    Raises:
        Exception: Parametros invalidos

    Returns:
        boolean: True en caso de ser una firma valida, False en el caso contrario
    """
    if not validar_parametros(p, q, g):
        raise Exception("Parametros invalidos")
    if not validar_firma(r, s, q):
        return False
    try:
        w = invert(s, q)
    except ZeroDivisionError:
        return False
    m = int(sha1(M).hexdigest(), 16)
    u1 = (m * w) % q
    u2 = (r * w) % q

    v = (powmod(g, u1, p) * powmod(y, u2, p)) % p % q
    if v == r:
        return True
    return False


def validar_parametros(p, q, g):
    """Valida las reglas entre los parametros para permitir la generación de las llaves

    Args:
        p (int)
        q (int)
        g (int)

    Returns:
        boolean: True en caso de que cumpla con los reglas, y False en el caso de no serlo
    """
    if is_prime(p) and is_prime(q):
        return True
    if powmod(g, q, p) == 1 and g > 1 and (p - 1) % q:
        return True
    return False


def validar_firma(r, s, q):
    """Valida sí los parametros de la firma son validos

    Args:
        r (int)
        s (int)
        q (int)

    Returns:
        boolean: True si son validos los parametros, False de no serlo
    """
    if r < 0 and r > q:
        return False
    if s < 0 and s > q:
        return False
    return True


if __name__ == "__main__":
    N = 160
    L = 1024
    p, q, g = generar_parametros(L, N)
    x, y = generar_llaves(g, p, q)
    print("===========================================================================================================")
    print("============================================= DSA =========================================================")
    print(" ")
    
    text = input(" - Ingresa el mensaje a firmar: ")
    M = str.encode(text, "ascii")
    r, s = firmar(M, p, q, g, x)
    if verificar(M, r, s, p, q, g, y):
        print(f"Mesanje: {M}",f"Firma: ({r}, {s})",f"Parametros públicos:\n\t p = {p} \n\t q = {q} \n\t g = {g}",f"Llaves: \n\t Pública: {y} \n\t Privada: {x}", sep='\n')
    else :
        print("Hubo un problema en la generación de las Llaves")