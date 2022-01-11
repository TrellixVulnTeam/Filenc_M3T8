import random
import base64
from Crypto import Random
from Crypto.Cipher import AES

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def checkIfPrime(num):
    flag = True
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                flag = False
                break
    return flag


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def points_computing(x, y, primeNum, a):
    listOfPoints = [(x, y)]
    s = ((3 * pow(x, 2) + a) * pow(modinv(2 * y, primeNum), 1, primeNum)) % primeNum
    newX = (pow(s, 2) - x - x) % primeNum
    newY = (s * (x - newX) - y) % primeNum
    listOfPoints.append((newX, newY))

    i = 2
    while (newX - x) != 0:
        s = ((newY - y) * pow(modinv(newX - x, primeNum), 1, primeNum)) % primeNum
        newX = (pow(s, 2) - x - listOfPoints[i - 1][0]) % primeNum
        newY = (s * (x - newX) - y) % primeNum

        listOfPoints.append((newX, newY))
        i += 1
    listOfPoints.append(("Inf", "Inf"))
    return listOfPoints


def alice(aPkey, B, primeNum, a):
    # computes the points (2B, 3B, 4B and so on ...) suit to aPkey
    listOfPoints = points_computing(B[0], B[1], primeNum, a)
    if aPkey >= len(listOfPoints):
        aPkey = aPkey % len(listOfPoints)
    return listOfPoints[aPkey - 1]


def bob(bPkey, A, primeNum, a):
    # computes the points (2A, 3A, 4A and so on ...) suit to bPkey
    listOfPoints = points_computing(A[0], A[1], primeNum, a)
    if bPkey >= len(listOfPoints):
        bPkey = bPkey % len(listOfPoints)
    return listOfPoints[bPkey - 1]


# compute square root under modulo
def squareRoot(n, p):
    n = n % p
    for x in range(1, p):
        if ((x * x) % p == n):
            return x

    return False

# compute the key use in AES to make a unique key for every user while register
def ecdh():
    while True:
        try:
            # check correction of the inputs (prime number, a and b parameters and x
            primeNum = random.randint(3, 1000)
            while primeNum <= 3 or checkIfPrime(primeNum) is False:
                primeNum = random.randint(3, 1000)
            a = random.randint(0, 1000)
            b = random.randint(0, 1000)
            while (4 * pow(a, 3) + 27 * pow(b, 2)) % primeNum == 0:
                a = random.randint(0, 1000)
                b = random.randint(0, 1000)

            x = random.randint(0, 1000)
            E = pow(x, 3) + a * x + b
            while E < 0 or (x < 0 or x > primeNum - 1):
                x = random.randint(0, 1000)
                E = pow(x, 3) + a * x + b

            # compute y (compute square root under modulo)
            y = squareRoot(E, primeNum)

            # sometimes, there is no square root under modulo,
            # so it return false and the user have to enter new input of x variable
            if not y:
                x = random.randint(0, 1000)
                E = pow(x, 3) + a * x + b
                y = squareRoot(E, primeNum)
                while E < 0 or (x < 0 or x > primeNum - 1) or not y:
                    x = random.randint(0, 1000)
                    E = pow(x, 3) + a * x + b
                    y = squareRoot(E, primeNum)

            # compute the points (2P, 3P, 4P and so on ...)
            listOfPoints = points_computing(x, y, primeNum, a)

            while True:
                try:
                    # Alice keys
                    aPKey = random.randint(2, len(listOfPoints) - 1)
                    A = listOfPoints[aPKey - 1]

                    # Bob keys
                    bPKey = random.randint(2, len(listOfPoints) - 1)
                    B = listOfPoints[bPKey - 1]

                    if alice(aPKey, B, primeNum, a) == bob(bPKey, A, primeNum, a):
                        return A
                    else:
                        print("No common secret")
                    break
                except Exception:
                    pass
            break
        except Exception:
            pass


#
def aes_encrypt(A, password):
    key = '0' * (16 - len(str(A[0]))) + str(A[0])
    password = pad(password)
    print("pass key")
    iv = str(Random.new().read(AES.block_size))
    print("pass iv")
    cipher = AES.new(key.encode("utf8"), AES.MODE_EAX, iv.encode("utf8"))
    print("pass cipher")
    return base64.b64encode(iv.encode("utf8") + cipher.encrypt(password.encode("utf8"))), iv


def aes_decrypt(A, password, iv):
    key = '0' * (16 - len(str(A[0]))) + str(A[0])
    password = pad(password)
    cipher = AES.new(key.encode("utf8"), AES.MODE_EAX, iv.encode("utf8"))
    return base64.b64encode(iv.encode("utf8") + cipher.encrypt(password.encode("utf8"))), iv


# # try -2
# def aes_encrypt(A, password):
#     key = '0' * (16 - len(str(A[0]))) + str(A[0])
#     cipher = AES.new(key.encode('utf_8'), AES.MODE_EAX)
#     nonce = cipher.nonce
#     ciphertext, tag = cipher.encrypt_and_digest(password.encode('ascii'))
#     return (nonce, ciphertext, tag)


# def aes_decrypt(A, password):
#     key = '0' * (16 - len(str(A[0]))) + str(A[0])
#     print(password)
#     (nonce, ciphertext, tag) = (password[0], password[1], password[2])
#     print("yayyy ")
#     cipher = AES.new(key.encode('utf_8'), AES.MODE_EAX)
#     print("yayyy 2")
#     plaintext = cipher.decrypt(ciphertext)
#     try:
#         cipher.verify(tag)
#         return plaintext.decode('ascii')
#     except:
#         return False

