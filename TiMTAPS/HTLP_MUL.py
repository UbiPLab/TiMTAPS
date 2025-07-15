import datetime

p = 131722411294720076454329602853430782398142322258021570755384899236197290463556613673909225434949994513184761419362368067456769922455573927172754739164312052130476515146467175039030287527010186625303826669181358870133783332901165286705557526407444253682452793075429549470159641080073449480970627785408994223219
q = 98167088059027539567638444489737738247734679812410413175432534977381676975769883190212505472378091302915337152761056540157952711803980347480478411686173587939513581441876485004974868656001808185462148513194833584113136804125675224102474149928529338502934408634579468456051884454931734463157877339826166671103

import random

def MHP_PSetup(lamda,t):
    N=p*q
    g_hat  = random.randint(1, N-1)
    g = (-1*pow(g_hat, 2))%N
    fin_N = (p-1)*(q-1)

    High = pow(2,t,fin_N>>1)
    h = pow(g,High,N)
    pp = [t,N,g,h]
    return pp
def MHP_PGen(pp,s):
    t,N,g,h = pp

    r = random.randint(1, N*N)
    u = pow(g, r, N)
    v = (pow(h, r, N)*s)%N
    # mo = N * N
    # # t1 = pow(u , pow(2,t) , N)
    # # t2 = pow(t1, N, mo)
    # # t3 = (t2*pow(1+N, s, mo))%mo
    #
    # v = (pow(h, r*N, mo)*pow(1+N, s, mo))%mo
    # # low = pow(t2,-1,mo)
    # # t4 = (v * low)%mo
    # # t5 = pow(1+N, s, mo)

    Z = [u,v]
    return Z
def MHP_PSolve(pp,Z):
    t,N,g,h = pp
    u,v = Z
    omaga = pow(u,pow(2,t),N)
    omaga = pow(omaga, -1, N)
    s = (v*omaga)%N
    # mo = N*N
    # low = pow(omaga, N, mo)
    # low = pow(low, -1, mo)
    # fenzi = (v*low)% mo - 1
    # s = fenzi//N
    return s
def MHP_PEval(pp,Z_list):
    l = len(Z_list)
    t,N,g,h = pp
    mo = N*N
    u_hat = 1
    v_hat = 1
    for i in range(0,l):
        u,v = Z_list[i]
        u_hat = (u_hat*u)%N
        v_hat = (v_hat*v)%mo
    Z_hat = [u_hat,v_hat]
    return Z_hat
def test():
    pp = MHP_PSetup(1, 20)
    N = p * q
    s1 = random.randint(1, p)
    s2 = random.randint(1, q)
    Z1 = MHP_PGen(pp, s1)
    Z2 = MHP_PGen(pp, s2)
    Z_all = MHP_PEval(pp, [Z1, Z2])
    s = MHP_PSolve(pp, Z_all)
    print("先计算后解谜" + str(s1 * s2))
    print("先解谜后计算" + str(s))
    print("解谜是否正确" + str(s == s1 * s2))

def time_cor():
    N = p * q
    s1 = random.randint(1, q)
    for i in range(1,10):
        print("第"+str(i)+"次：")
        t = i*100000
        starttime = datetime.datetime.now()
        pp = MHP_PSetup(1, t)
        endtime = datetime.datetime.now()
        t1 = endtime-starttime
        starttime = datetime.datetime.now()
        Z1 = MHP_PGen(pp, s1)
        endtime = datetime.datetime.now()
        t2 = endtime-starttime
        starttime = datetime.datetime.now()
        s = MHP_PSolve(pp, Z1)
        endtime = datetime.datetime.now()
        t3 = endtime-starttime
        print("初始化:" + str(t1) + "构造:" + str(t2) + "解谜:" + str(t3))


if __name__ == '__main__':
    time_cor()