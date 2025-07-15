import random

p = 131722411294720076454329602853430782398142322258021570755384899236197290463556613673909225434949994513184761419362368067456769922455573927172754739164312052130476515146467175039030287527010186625303826669181358870133783332901165286705557526407444253682452793075429549470159641080073449480970627785408994223219
q = 65861205647360038227164801426715391199071161129010785377692449618098645231778306836954612717474997256592380709681184033728384961227786963586377369582156026065238257573233587519515143763505093312651913334590679435066891666450582643352778763203722126841226396537714774735079820540036724740485313892704497111609

def Setup(k):
    g_1 = random.randint(1,q)
    w = random.randint(1,q)
    g_2 = pow(g_1,w,q)
    p_1 = [random.randint(1, p) for _ in range(k+1)]
    p_2 = [random.randint(1, p) for _ in range(k+1)]
    D = []
    for i in range(0, k+1):
        D_i = pow(g_1,p_1[i],p)*pow(g_2,p_2[i],p)%p
        D.append(D_i)
    params = [g_1,g_2,D]
    master_key = [p_1,p_2]
    return params, master_key

def Extract(ID,master_key):
    p_1_ID = 0
    p_2_ID = 0
    p_1, p_2 = master_key
    for i in range(0,p_1.__len__()):
        p_1_ID = (p_1_ID + p_1[i]*(pow(ID,i,p-1)))%(p-1)
        p_2_ID = (p_2_ID + p_2[i]*(pow(ID,i,p-1)))%(p-1)
    SK_ID = [p_1_ID,p_2_ID]
    return SK_ID

def Encrypt(m, params, ID):
    r_1 = random.randint(1,q-1)
    g_1, g_2, D = params
    u_1 = pow(g_1,r_1,p)
    u_2 = pow(g_2,r_1,p)
    D_ID = 1
    fin = p-1
    for t in range(0,D.__len__()):
        high = pow(ID,t,fin)
        mul = pow(D[t],high,p)
        D_ID = D_ID*mul
    s = pow(D_ID,r_1,p)
    c =(m*s)%p
    C = [u_1,u_2,c]
    return C,r_1

def Decrypt(C,SK_ID):
    u_1, u_2, c = C
    p_1_ID, p_2_ID = SK_ID
    s = (pow(u_1,p_1_ID,p)*pow(u_2,p_2_ID,p))%p
    s_f = pow(s,-1,p)
    m = (c*s_f)%p
    return m

if __name__ == '__main__':


    #step1
    params, master_key = Setup(3)
    g_1 = params[0]

    #算群G
    G = []
    for i in range(0, q):
        g_i = pow(g_1, i, p)
        G.append(g_i)

    #i_m = random.randint(1, q)
    #m = pow(g_1,i_m,p)

    # 找一个在G但是不在q的元素
    #while True:
    #    i_m = random.randint(1, q)
    #    m = pow(g_1,i_m,p)
    #    if m not in range(1,q):
    #        break

    # 找一个在p但是不在G的元素
    while True:
        m = random.randint(1, p)
        if m not in G:
            break


    #找一个在q但是不在G的元素
    #while True:
    #    m = random.randint(1, q)
    #    if m not in G:
    #        break

    #m = random.randint(1, q)
    ID = random.randint(1, q)
    #step2
    SK_ID = Extract(ID,master_key)
    #step3
    C = Encrypt(m, params, ID)
    #step4
    md = Decrypt(C,SK_ID)
    print('m是否在G中:'+str(m in G))
    print('m是否在p中:' + str(m in range(1, p)))
    print('解密是否正确:'+str(md==m))
    #print('m是否大于q || 解密是否正确:'+str(m>q)+' || '+str(md==m))
