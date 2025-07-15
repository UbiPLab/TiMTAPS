import random
import hashlib
import time
from itertools import combinations
import datetime

q = 154134170538138396189964328785507020323
g = random.randint(1, q)


def Setup(lamd,n,t):
    ski = [random.randint(1, q) for _ in range(n)]
    pki = [pow(g,ski[i],q) for i in range(n)]
    pk = [t,pki]
    sk = ski
    return sk,pk

def Sign(sk,m,S,pki):
    t = S.__len__()
    sigma_all = []
    R_all = 1
    R_map = {}
    r_map = {}
    for item in S:
        r = random.randint(1, q)
        R = pow(g, r, q)
        r_map[item] = r
        R_map[item] = R
        R_all = R_all * R
    for item in S:
        c = int(hashlib.sha256((str(pki) + str(R_all) + m).encode()).hexdigest(), 16) % (q-1)
        z = (r_map[item] + sk[item] * c) %(q-1)
        sigma = [R_map[item], z]
        left = pow(g,z,q)
        right = (pow(pki[item],c,q)*R_map[item])%q
        flag = left == right
        sigma_all.append(sigma)

    return sigma_all

def Combine(pk,S,sigma_all):
    # starttimeCNN = datetime.datetime.now()
    # print(starttimeCNN)
    t = pk[0]
    if sigma_all.__len__() != t:
        return False
    z = 0
    R = 1
    for item in sigma_all:
        R = R * item[0]
        z = z + item[1]

    # endtimeCNN = datetime.datetime.now()
    # print(endtimeCNN)
    return R,z,S

def Verify(pk,m,R,z,S,g):
    t, pki = pk
    pk_C = 1
    for item in S:
        pk_C = pk_C*pki[item]
    c = int(hashlib.sha256((str(pki) + str(R) + m).encode()).hexdigest(),16)%(q-1)
    # l = pow(g,z,p)
    # l_n = (pow(pk_C,c,p)*R)%p
    if len(S) == t and pow(g,z,q)==(pow(pk_C,c,q)*R)%q:
        return True
    else:
        return False

def Trace(pk, m, R, z, g, n, t):
    #便利由1-n中数字组成的长度为t的C序列
    C_list = combinations(range(0, n), t)
    for (i, item) in enumerate(C_list):
        #对每个C序列进行验证，如果验证成功输出C
        flag = Verify(pk, m, R, z, list(item), g)
        if flag:
            return list(item)
    #失败输出空集
    return []

def data():
    n = 100
    t = 50
    m = ""
    # m为长度1024的由0，1组成的字符串
    for i in range(1024):
        m += str(1)
    S = random.sample(range(1, n), t)
    # 进行加密解密追踪
    sk, pk = Setup(1, n, t)
    pki = pk[1]

    starttime = datetime.datetime.now()
    sigma_all = Sign(sk, m, S, pki)
    endtime = datetime.datetime.now()
    thetime = endtime - starttime
    print("Sign测量数据为：" + str(thetime))

    starttimeC = datetime.datetime.now()
    R, z, C = Combine(pk, S, sigma_all)
    endtimeC = datetime.datetime.now()
    thetime = endtimeC - starttimeC
    print("Combine测量数据为：" + str(thetime))

    starttime = datetime.datetime.now()
    flag = Verify(pk, m, R, z, S, g)
    endtime = datetime.datetime.now()
    thetime = endtime - starttime
    print("Verify测量数据为：" + str(thetime))

    #print(flag)

    # starttime = datetime.datetime.now()
    # C_n = Trace(pk, m, R, z, g, n, t)
    # endtime = datetime.datetime.now()
    # thetime = endtime - starttime
    # print("Trace测量数据为：" + str(thetime))
    # print(S)
    # print(C_n)

if __name__ == '__main__':
    # for i in range(10):
    #     data()
    # starttime = datetime.datetime.now()
    # for i in range(1000):
    #     t=1;
    # endtime = datetime.datetime.now()
    # thetime = endtime - starttime
    # print("Verify测量数据为：" + str(thetime))
    data()
