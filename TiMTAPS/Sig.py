import random
import hashlib

q = 154134170538138396189964328785507020323
g = random.randint(1, q)

def KeyGen(lamda):
    sk = random.randint(1, q - 1)
    pk = pow(g, sk,q)
    return sk, pk

def Sign(sk, m, pk):
    r = random.randint(1, q - 1)
    R = pow(g, r, q)
    c = int(hashlib.sha256((str(pk) + str(R) + m).encode()).hexdigest(), 16)%(q-1)
    z = (r + sk* c) % (q-1)
    sigma = [R, z]
    return sigma

def Verify(pk, m, sigma):
    c = int(hashlib.sha256((str(pk) + str(sigma[0]) + m).encode()).hexdigest(), 16) % (q-1)
    l = pow(g, sigma[1], q)
    l_n = (pow(pk, c, q) * sigma[0]) % q
    if l == l_n:
        return True
    else:
        return False

if __name__ == '__main__':
    m = ""
    # m为长度1024的由0，1组成的字符串
    for i in range(1024):
        m += str(1)
    sk, pk = KeyGen(2)
    sigma = Sign(sk, m, pk)
    if Verify(pk, m, sigma):
        print("Signature")
    else:
        print("Not Signature")