import random
import getpass

def criba(n):
    """Recibe un valor n al cual se buscaran los números primos menores que el mismo.

    Args:
        n (int): Entero máximo hasta que se buscaran los números primos con el metodo de la criba de eratóstenes

    Returns:
        list: lista de primos menos a n
    """
    primo = []
    no_primos = set()

    for i in range(2, n+1):
        if i in no_primos:
            continue

        for j in range(i*2, n+1, i):
            no_primos.add(j)

        primo.append(i)
    return primo

def esEntero(s):
    """Verifica si el valor ingresado es un número entero

    Args:
        s (string): valor ingresado por consola

    Returns:
        int: el entero S
    """
    try:
        return int(s)
    except ValueError:
        return esEntero(getpass.getpass(f"{s} no es un entero, Intentelo nuevamente: "))

if __name__ == "__main__":
    tope = random.randint(5,10000)
    primos = criba(tope)

    g = random.randint(5,10000)
    if g in primos:
        primos.remove(1)
    p = random.choice(primos)

    print("Valor g:", g)
    print("Valor p:", p)

    a = esEntero(getpass.getpass("Número secreto \"a\": "))
    b = esEntero(getpass.getpass("Número secreto \"b\": "))

    A = (g**a)%p
    B = (g**b)%p

    print("-------------------------------------------------------\n")
    print("Calculo de la llave compartida de \"a\":\n")
    print("El número secreto de \"a\" es", a, "")

    print("Se calcula la llave publica de A\n Formula: g^a mod p = A")
    print(str(g)+"^"+str(a)+" mod "+str(p)+" =", A, "= A")

    print("Luego de recibir el valor de \"B\"")
    print(" Llave privada = B^a mod p")
    privadaA = (B**a)%p
    print(str(B)+"^"+str(a)+" mod "+str(p)+" =", privadaA)
    print("La llave privada calculada desde \"a\" es:", privadaA)


    print("-------------------------------------------------\n")
    print("Calculo de la llave compartida de \"b\":\n")
    print("El numero privada de \"b\" es", b, "")

    print("Se calcula la llave publica de B\n Formula: g^b mod p = B")
    print(str(g)+"^"+str(b)+" mod "+str(p)+" =", B, "= B")


    print("Luego de recibir el valor de \"A\"")
    print(" Llave privada = A^b mod p")
    privadaB = (A**b)%p
    print(str(A)+"^"+str(b)+" mod "+str(p)+" =", privadaB)
    print("La llave privada calculada desde \"b\" es:", privadaB)

    print("-------------------------------------------------------\n")
