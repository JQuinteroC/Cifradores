import random

def mcd(a, b):
    """Empleando el algoritmo de Euclides, para determinar el máximo común divisor

    Args:
        a (int): valor a
        b (int): valor b

    Returns:
        int: máximo común divisor entre a y b
    """
    while b != 0:
        a, b = b, a % b
    return a

def inverso_multiplicativo(e, phi):
    """Algoritmo extendido de Euclides para buscar el inverso multiplicativo de dos números

    Args:
        e (int): valor e
        phi (int): valor phi

    Returns:
        int: inverso multiplicativo
    """
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def es_primo(n):
    """Validación si es un número primo

    Args:
        num (int): número a verificar

    Returns:
        bool: true sí n es primo, false si no lo es
    """
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5)+2, 2):
        if n % i == 0:
            return False
    return True

def generar_llaves(p, q):
    """Generar las llaves de cifrador

    Args:
        p (int): primo p
        q (int): primo q

    Raises:
        ValueError: Ambos números deben ser primos
        ValueError: p y q deben ser diferentes

    Returns:
        list: Lista de llaves publicas y privadas
    """
    if not (es_primo(p) and es_primo(q)):
        raise ValueError('Ambos números deben ser primos.')
    elif p == q:
        raise ValueError('p y q deben ser diferentes')

    n = p * q

    phi = (p-1) * (q-1)

    # Coprimo menor que phi
    e = random.randrange(3, phi)
    g = mcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = mcd(e, phi)

    # inverso multiplicativo para determinar la llave privada
    d = inverso_multiplicativo(e, phi)

    # Llave publica (e, n) y llave privada (d, n)
    return ((e, n), (d, n))

def encriptar(llave_publica, texto_plano):
    """Combierte cada caracter al codigo ASCII y lo encripta

    Args:
        llave_publica (int): llave publica para cifrar el texto
        texto_plano (string): texto que se busca cifrar

    Returns:
        string: texto cifrado
    """
    llave, n = llave_publica
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    texto_cifrado = [pow(ord(char), llave, n) for char in texto_plano]
    
    return texto_cifrado

def desencriptar(llave_privada, texto_cifrado):
    """Desencripta el mensaje y combierte cada caracter de ASCII a su letra correspondiente

    Args:
        llave_privada (int): llave privada
        texto_cifrado (string): texto cifrado

    Returns:
        string: texto desencriptado
    """
    llave, n = llave_privada
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    aux = [str(pow(char, llave, n)) for char in texto_cifrado]
    
    texto_plano = [chr(int(char2)) for char2 in aux]
    return ''.join(texto_plano)

if __name__ == '__main__':
    print("===========================================================================================================")
    print("============================================= RSA =========================================================")
    print(" ")

    print("Por favor ingrese:")
    p = int(input(" - Número primo (17, 19, 23, etc) p: "))
    q = int(input(" - Otro número primo (diferente) q: "))

    print(" - Generando los pares de llaves . . .")

    public, private = generar_llaves(p, q)

    print(f" - Tu llave publica es:  {public} y las llaves privadas son: {private}")

    message = input(" - Ingresa el mensaje a encriptar con la llave publica: ")
    encrypted_msg = encriptar(public, message)

    print(f" - Tu mensaje encriptado será: {''.join(map(lambda x: str(x), encrypted_msg))}" )
    print(f" - Desencriptando con la llave privada {private} . . .")
    print(f" - Tu mensaje es: {desencriptar(private, encrypted_msg)}")

    print(" ")
    print("===========================================================================================================")