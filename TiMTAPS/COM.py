#import sympy
import random

def Setup(lamda):
    q = 264926624393126082647786234614522411169
    g = random.randint(1, q-1)
    h = random.randint(1, q-1)
    return g, h, q

def Comm(x, g, h, q):
    r = random.randint(1, q-1)
    left = pow(g, x, q)
    right =pow(h, r, q)
    comm = (left*right)%q
    return comm, x, r

def Open(comm, x, r, g, h, q):
    left = pow(g, x, q)
    right = pow(h, r, q)
    comm_1 = (left * right) % q
    if comm_1 == comm:
        return True
    else:
        return False

if __name__ == '__main__':
    g, h, q =Setup(1)
    print("Setup is down")
    value = 12345
    comm, x, r = Comm(value, g, h, q)
    print("Setup is down")
    result = Open(comm, x, r, g, h, q)
    print("Open is down")
    print(result)