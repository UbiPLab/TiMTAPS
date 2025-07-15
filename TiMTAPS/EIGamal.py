import random
import sys
import datetime

# q
p = 135410250898599446603827879283006844712836537334634139477281182264755944407199483483840386951271773793849590628522802188686253163300149799072592452561040845064640735897996146993818262957280771832549537283485414761962881680478691820243  # 获得大素数q
# g
r = 51320500147494313260576095305465705911698834495652597778015393849527989926920389745664579119862278771332478438737761963842544930018850697910422620520061233174428083990798624946760731485453661794134278764910219603843473293195096572021 # 得r


def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

    # Generating large random numbers

def e_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = e_gcd(b, a % b)
    return g, y, x - a // b * y

def gen_key():
    # sk是随机选取的私钥
    sk = random.randint(pow(10, 20), p)
    while gcd(p, sk) != 1:
        sk = random.randint(pow(10, 20), p)
    # pk是根据sk计算的
    pk = power(r, sk, p)
    return sk, pk


# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c


# 将msg分为一个个小于q大小的片段，防止逐字符加密费时较长
def msg_part(msg):
    for char in msg:
        if char.isalpha():
            msg = str(int(msg, 16))
            break
    l_m = len(msg)
    l_p = len(str(p))
    l = int(l_m / (l_p - 1) + 1)
    # print(l)
    msg_part = []
    for i in range(0, l):
        part = msg[i * (l_p - 1):(i + 1) * (l_p - 1)]
        # print(len(part))
        part = int(part)
        msg_part.append(part)
    return msg_part



# 将msg分为一个个小于q大小的片段，并放在G中，防止逐字符加密费时较长
def msg_part_G(msg):
    for char in msg:
        if char.isalpha():
            msg = str(int(msg, 16))
            break
    l_m = len(msg)
    l_p = len(str(p))
    l = int(l_m / (l_p - 1) + 1)
    # print(l)
    msg_part = []
    for i in range(0, l):
        part = msg[i * (l_p - 1):(i + 1) * (l_p - 1)]
        # print(len(part))
        part = int(part)
        part = pow(r, part, p)
        msg_part.append(part)
    return msg_part

# Asymmetric encryption
def encrypt(msg, p, pk, r):
    en_msg = []
    b = gen_key()[0]  # 得b
    K = power(pk, b, p) # K=(Sa)^b mod p
    C1 = power(r, b, p)  #  C1=Sb=r^b mod p

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    # print("(Sa)^b mod p used : ", K)
    for i in range(0, len(en_msg)):
        en_msg[i] = K * ord(en_msg[i])
    return en_msg, C1

def encrypt_G(msg, p, h, r):
    C1 = []
    C1.append(0)
    for char in msg:
        if char.isalpha():
            C1[0] = 1
            msg = str(int(msg, 16))
            break
    en_msg = []
    b = gen_key()[0]  # 得b
    K = power(h, b, p) # K=(Sa)^b mod p
    C11 = power(r, b, p)
    C1.append(C11)#  C1=Sb=r^b mod p
    l_m = len(msg)
    l_p = len(str(p))
    l = int(l_m/(l_p-1)+1)
    #print(l)
    C2 = msg_part_G(msg)
    # print("(Sa)^b mod p used : ", K)
    for i in range(0, len(C2)):
        C2[i] = (K * C2[i])% p
    return C2, C1, b

def decrypt(C2, C1, sk, p):
    dr_msg = []
    h = power(C1, sk, p)
    for i in range(0, len(C2)):
        dr_msg.append(chr(int(C2[i] / h)))

    return ''.join(dr_msg)

def decrypt_G(C2, C1, a, p):
    flag = C1[0]
    C_1 = C1[1]
    dr_msg = []
    h = power(C_1, a, p)
    d = e_gcd(h, p)[1]
    for i in range(0, len(C2)):
        en_msg = C2[i]
        dr = en_msg * d % p
        #print(dr)
        dr_msg.append(dr)
    dm = ''
    for i in range(0, len(dr_msg)):
        dm = dm + str(dr_msg[i])
    if flag == 1:
        dm = int(dm)
        dm = hex(dm)[2:]
        dm = str(dm)
    return dm

# Driver code
def text_nopart():
    msg = ""
    for i in range(1024):
        msg += str(1)
    # msg = '01010asdasd'               # 共125位数字，1000bit
    msg = '03269EC5729E41CBEBC6F5341684C90FE4C2E7C9138A95EA136FB32A0A6762C139D0684E69554E937895D73CF73C8A440280C0E6D3F4251A338DF3940E0A2B5E8A'
    sk, pk = gen_key()  # Private key for receiver
    C2, C1 = encrypt(msg, p, pk, r)
    dmsg = decrypt(C2, C1, sk, p)
    print("解密后文 :", dmsg)
    print(dmsg == msg)
    print("encrypt overhead:%s KB" % (sys.getsizeof(C2) / 1024))

def text_part():
    msg = '3269EEA8224BEBC6F5341684C90FE4C2E7C9138A95EA136FB32A0A6762C139D0684E69554E937895D73CF73C8A440280C0E6D3F4251A338DF3940E0A2B5E8A03269EC5729E41CBEBC6F5341684C90FE4C2E7C9138A95EA136FB32A0A6762C139D0684E69554E937895D73CF73C8A440280C0E6D3F4251A338DF3940E0A2B5E8A'
    msgparG = msg_part_G(msg)
    de = ''
    for i in range(0, len(msgparG)):
        de = de + str(msgparG[i])
    print(de)
    dm = int(de)
    dm = hex(dm)[2:]
    dm = str(dm)
    print(msgparG)
    sk, pk = gen_key()
    C2, C1, b = encrypt_G(msg, p, pk, r)
    dmsg = decrypt_G(C2, C1, sk, p)
    print("解密后文 :", dmsg)
    print(dmsg == dm)
if __name__ == '__main__':
    text_part()
