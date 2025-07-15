import json
import random

import ATS
import EIGamal
import HTLP_ADD
import HTLP_MUL
import IKEM
import NIZK
import Sig
import COM
import hashlib

def Setup(lamda, k, n, t, T):
    # ATS初始化
    q_ATS = ATS.q
    g_ATS = ATS.g
    pp_ATS = [g_ATS, q_ATS]
    sk_ATS, pk_ATS = ATS.Setup(lamda, n, t)
    # HTLP初始化
    pp_HTLP_ADD = HTLP_ADD.LHP_PSetup(lamda, T)
    pp_HTLP_MUL = HTLP_MUL.MHP_PSetup(lamda, T)
    # HC初始化
    pp_HC = COM.Setup(lamda)
    # IBE初始化
    pp_IBE, mk_IBE = IKEM.Setup(k)
    # EIGamal和Sig初始化
    # Combniner的密钥
    sk_com_EIGamal, pk_com_EIGamal = EIGamal.gen_key()
    sk_com_Sig, pk_com_Sig = Sig.KeyGen(lamda)
    # Tracer的密钥
    sk_tra_EIGamal, pk_tra_EIGamal = EIGamal.gen_key()
    # Admitter的密钥
    sk_adm_EIGamal, pk_adm_EIGamal = EIGamal.gen_key()
    # Verifier的密钥
    sk_ver_EIGamal, pk_ver_EIGamal = EIGamal.gen_key()
    # pk的承诺生成
    pki = pk_ATS[1]
    com_pk = []
    g, h, q = pp_HC
    for i in range(n):
        com_pki = COM.Comm(pki[i], g, h, q)
        com_pk.append(com_pki)
    pp = [pp_ATS, pp_HTLP_ADD, pp_HTLP_MUL, pp_HC, pp_IBE]
    PK = [pk_com_EIGamal, pk_com_Sig, pk_tra_EIGamal, pk_adm_EIGamal, pk_ver_EIGamal, com_pk]
    sk_com = [pk_ATS, sk_com_EIGamal, sk_com_Sig]
    sk_tra = [pk_ATS, sk_tra_EIGamal]
    sk_adm = [sk_adm_EIGamal, mk_IBE]
    return pp, sk_ATS, PK, sk_com, sk_tra, sk_adm, sk_ver_EIGamal

def Sign(sk_ATS, m, S, pki, PK, Sid, pp, pk_ATS):
    pp_ATS, pp_HTLP_ADD, pp_HTLP_MUL, pp_HC, pp_IBE = pp
    pk_com_EIGamal, pk_com_Sig, pk_tra_EIGamal, pk_adm_EIGamal, pk_ver_EIGamal, com_pk = PK
    # ATS签名
    sigma_all = ATS.Sign(sk_ATS, m, S, pki)
    # # 验证是否为有效ATS签名
    # R, z, S = ATS.Combine(pk_ATS, S, sigma_all)
    # pk = pk_ATS
    # n = pk[1].__len__()
    # t = S.__len__()
    # flag = textATS(S, pk, m, R, z, n, t)

    # # 验证Rz的cmt
    # R, z, S = ATS.Combine(pk_ATS, S, sigma_all)
    # R_m = 1
    # z_a = 0
    # g, h, q = pp_HC
    # cm1 = 1
    # for i in range(sigma_all.__len__()):
    #     R1 = sigma_all[i][0]
    #     z1= sigma_all[i][1]
    #     cmt = (pow(g,z1,q)*R1)%q
    #     cm1 = (cm1*cmt)%q
    # cmt_all = (pow(g,z,q)*R)%q
    # flag = cm1 == cmt_all

    # 使用Combiner的公钥来对Sid加密
    Eid_com = []
    for item in S:
        id_Enc2, id_Enc1 = EIGamal.encrypt(str(Sid), EIGamal.p, pk_com_EIGamal, EIGamal.r)
        id_Enc = [id_Enc2, id_Enc1]
        Eid_com.append(id_Enc)
    # 将加密后的Eid与sigma一一对应起来
    sigma_cor = []
    for i in range(S.__len__()):
        sigma_cori = [Eid_com[i], sigma_all[i]]
        sigma_cor.append(sigma_cori)
    # 使用Admitter的公钥来对Sid加密
    Eid_adm = []
    for item in S:
        id_Enc2, id_Enc1 = EIGamal.encrypt(str(Sid), EIGamal.p, pk_adm_EIGamal, EIGamal.r)
        id_Enc = [id_Enc2, id_Enc1]
        Eid_adm.append(id_Enc)
    # 生成Ri和zi的时间锁，同时将其与Eid对应起来
    sigma_HTLP_cor = []
    for i in range(S.__len__()):
        R, z = sigma_all[i]
        R_HTLP = HTLP_MUL.MHP_PGen(pp_HTLP_MUL, R)
        z_HTLP = HTLP_ADD.LHP_PGen(pp_HTLP_ADD, z)
        sigma_H = [R_HTLP, z_HTLP]
        sigma_HTLP_cori = [Eid_adm[i], sigma_H]
        sigma_HTLP_cor.append(sigma_HTLP_cori)
    # 生成每对Rz的承诺
    com_Rz = []
    g, h, q = pp_HC
    for item in sigma_all:
        R, z = item
        com_RZi = (pow(g, z, q) * R) % q
        com_Rz.append(com_RZi)
    # sigma_cor_string = json.dumps(sigma_cor)
    # sigma_cor_list = json.loads(sigma_cor_string)
    # sigma_HTLP_cor_string = json.dumps(sigma_HTLP_cor)
    # sigma_HTLP_cor_list = json.loads(sigma_HTLP_cor_string)
    # com_Rz_string = json.dumps(com_Rz)
    # com_Rz_list = json.loads(com_Rz_string)

    return sigma_cor, sigma_HTLP_cor, com_Rz

def Combine(Sid, sk_com, m, sigma_cor, PK, S, pp, idc):
    pk_com_EIGamal, pk_com_Sig, pk_tra_EIGamal, pk_adm_EIGamal, pk_ver_EIGamal, com_pk = PK
    pk_ATS, sk_com_EIGamal, sk_com_Sig = sk_com
    t_ATS, pki_ATS = pk_ATS
    # 把Sid解密出来以确定对应的Sigma组
    # flag = True
    sigma_cor_need = []
    for i in range(0, t_ATS):
        Eid_com, sigma_all = sigma_cor[i]
        Sid_new = EIGamal.decrypt(Eid_com[0], Eid_com[1], sk_com_EIGamal, EIGamal.p)
        if Sid_new == str(Sid):
            sigma_cor_need.append(sigma_cor[i])
    # 把对应的sigma取出来
    sigma_all = []
    for i in range(t_ATS):
        sigma_all.append(sigma_cor_need[i][1])
    # 进行组合
    R, z, S = ATS.Combine(pk_ATS, S, sigma_all)
    # print("R的初始值"+str(R))
    # print("z的初始值" + str(z))

    # #验证是否为有效ATS签名
    # pk = pk_ATS
    # n = pk[1].__len__()
    # t = S.__len__()
    # flag = textATS(S, pk, m, R, z, n, t)

    n = pki_ATS.__len__()
    # 根据S算b，以便生成零知识证明
    b = []
    for i in range(n):
        bi = 0
        if i in S:
            bi = 1
        b.append(bi)
    # 生成总的承诺
    pp_ATS, pp_HTLP_ADD, pp_HTLP_MUL, pp_HC, pp_IBE = pp
    g, h, q = pp_HC
    com_Rzall = (pow(g, z, q) * R) % q
    # 对z进行加密
    g = pp_IBE[0]
    z_G = pow(g, z, IKEM.p)
    z_map_G = []
    map = [z_G,z]
    z_map_G.append(map)
    z_Enc, r_1 = IKEM.Encrypt(z_G, pp_IBE, int(m))
    # 生成零知识证明
    pi = []
    pki = pk_ATS[1]
    c = int(hashlib.sha256((str(pki) + str(R) + m).encode()).hexdigest(), 16) % (ATS.q - 1)
    # 验证相等性
    left = pow(ATS.g, z, ATS.q)
    # right = 1
    # for i in range(pki.__len__()):
    #     right = (right * pow(pki[i], c*b[i], ATS.q))%ATS.q
    # right = right*R%ATS.q

    # Prove1.1的生成
    pi_11 = NIZK.prove_11(ATS.g, z, pk_ATS, b, c, R, ATS.q, pki.__len__())
    # flag = NIZK.verify_11(pi_11, left, pk_ATS, R, ATS.g, ATS.q, pki.__len__(), c)

    # Prove1.2的生成
    # 加密T
    g = EIGamal.r
    q = EIGamal.p
    r_gang = random.randint(pow(10, 20), q)
    t_Enc1 = pow(g, r_gang, q)
    t_Enc2 = (pow(g, t_ATS, q)*pow(pk_ver_EIGamal, r_gang, q)) % q
    t_Enc = [t_Enc1, t_Enc2]
    pi_12 = NIZK.prove_12(g, r_gang, pk_ver_EIGamal, b, q, pki.__len__(), t_Enc)
    # flag = NIZK.verify_12(pi_12,t_Enc[0],t_Enc[1],pk_ver_EIGamal,EIGamal.r,EIGamal.p, pki.__len__())

    # Prove1.3的生成
    # 加密b
    g = EIGamal.r
    q = EIGamal.p
    gama_b = random.randint(pow(10, 20), q)
    h = [random.randint(pow(10, 20), q) for _ in range(n)]
    pi.append(h)
    cb_0 = pow(g, gama_b, q)
    cb_1 = []
    for i in range(n):
        cb_i = (pow(g, b[i], q)*pow(h[i], gama_b, q)) % q
        cb_1.append(cb_i)
    alpha_b = int(hashlib.sha256((str(cb_0) + str(cb_1)).encode()).hexdigest(), 16) % q
    phi = []
    for i in range(n):
        phii = (pow(alpha_b, i, q-1)*gama_b*(1-b[i])) % (q-1)
        phi.append(phii)
    # 检查一下
    # left_check = 1
    # for i in range(n):
    #     high = (pow(alpha_b,i,q-1)*(1-b[i]))%(q-1)
    #     left_check = left_check * pow(cb_1[i], high, q)
    # right_check = 1
    # for i in range(n):
    #     right_check = right_check * pow(h[i], phi[i], q)
    # flag = left_check == right_check
    pi_13 = NIZK.prove_13(cb_0, cb_1, gama_b, alpha_b, phi, h, g, b, q, n)
    # flag = NIZK.verify_13(pi_13,cb_0, cb_1,g,h,alpha_b,q,n)

    # Prove2
    # com_pk = []
    # g, h, q = pp_HC
    # for i in range(n):
    #     com_pki = COM.Comm(pki[i], g, h, q)
    #     com_pk.append(com_pki)
    # com_Rz = COM.Comm(com_Rzall, g, h, q)
    g, h, q = pp_HC
    pi_2 = []
    for i in range(n):
        comm, x, r = com_pk[i]
        pi_2i = NIZK.prove_2(g, h, q, pki[i], r, comm)
        pi_2.append(pi_2i)
        flag = NIZK.verify_2(pi_2i, g, h, q, comm)
        #print(flag)

    # Prove3
    g_1, g_2, D= pp_IBE
    D_ID = 1
    fin = IKEM.p - 1
    for t in range(0, D.__len__()):
        high = pow(int(m), t, fin)
        mul = pow(D[t], high, IKEM.p)
        D_ID = D_ID * mul
    r_IKEM = r_1
    pi_3 =NIZK.prove_3(g_1, g_2, r_1, z, D_ID, IKEM.p, z_Enc)
    #flag = NIZK.verify_3(pi_3, g_1, g_2, IKEM.p, D_ID, z_Enc)
    pi_e = [pi_11, pi_12, pi_13, pi_2, pi_3, left, cb_0, cb_1]
    pi.extend(pi_e)

    # 对相关信息进行签名
    sig_data = [m, idc, com_Rzall, z_Enc, t_Enc, pi]
    signature_all = []
    for i in range(sig_data.__len__()):
        tosig = str(sig_data[i])
        if i==5:
            tosig = tosig.replace("(", "[")
            tosig = tosig.replace(")", "]")
        signature_comi = Sig.Sign(sk_com_Sig, tosig, pk_com_Sig)
        signature_all.append(signature_comi)
    # TiMTAPS的形成
    Em =  []
    Em_Enc2, Em_Enc1 = EIGamal.encrypt(m, EIGamal.p, pk_ver_EIGamal, EIGamal.r)
    Em.append(Em_Enc2)
    Em.append(Em_Enc1)

    signature_TiMTAPS = [idc, com_Rzall, Em, R, z_Enc, t_Enc, pi, signature_all,z_map_G]
    # signature_TiMTAPS_string = json.dumps(signature_TiMTAPS)
    # print(signature_TiMTAPS_string.__len__())
    # signature_TiMTAPS_list = json.loads(signature_TiMTAPS_string)

    # return signature_TiMTAPS
    return signature_TiMTAPS

def Verify(pp, PK, m, signature_TiMTAPS, com_Rz, pk_ATS,sk_ver_EIGamal):
    # 验证签名
    pp_ATS, pp_HTLP_ADD, pp_HTLP_MUL, pp_HC, pp_IBE = pp
    idc, com_Rzall, Em, R, z_Enc, t_Enc, pi, signature_all,z_map_G = signature_TiMTAPS
    pk_com_EIGamal,pk_com_Sig,pk_tra_EIGamal,pk_adm_EIGamal,pk_ver_EIGamal,com_pk = PK
    m = EIGamal.decrypt(Em[0], Em[1], sk_ver_EIGamal, EIGamal.p)
    sig_data = [m, idc, com_Rzall, z_Enc, t_Enc, pi]
    flag1 = True
    for i in range(signature_all.__len__()):
        sigma = signature_all[i]
        ms = str(sig_data[i])
        ms = ms.replace("(", "[")
        ms = ms.replace(")", "]")
        flag1 = flag1 and Sig.Verify(pk_com_Sig,ms,sigma)
    # 验证承诺
    g, h, q = pp_HC
    com_Rz_compute = 1
    for item in com_Rz:
        com_Rz_compute = (com_Rz_compute * item)%q
    flag2 = com_Rz_compute == com_Rzall
    # 验证零知识证明
    flag3 = True
    h, pi_11, pi_12, pi_13, pi_2, pi_3, left, cb_0, cb_1 = pi
    pki = pk_ATS[1]
    c = int(hashlib.sha256((str(pki) + str(R) + m).encode()).hexdigest(), 16) % (ATS.q - 1)
    flag3_11 = NIZK.verify_11(pi_11, left, pk_ATS, R, ATS.g, ATS.q, pki.__len__(), c)
    flag3_12 = NIZK.verify_12(pi_12,t_Enc[0],t_Enc[1],pk_ver_EIGamal,EIGamal.r,EIGamal.p, pki.__len__())
    g = EIGamal.r
    q = EIGamal.p
    alpha_b = int(hashlib.sha256((str(cb_0) + str(cb_1)).encode()).hexdigest(), 16) % q
    flag3_13 = NIZK.verify_13(pi_13, cb_0, cb_1, g, h, alpha_b, q, pki.__len__())
    flag3_2 = True
    g, h, q = pp_HC
    for i in range(pki.__len__()):
        comm, x, r = com_pk[i]
        flag = NIZK.verify_2(pi_2[i], g, h, q, comm)
        flag3_2 = flag3_2 and flag
    g_1, g_2, D = pp_IBE
    D_ID = 1
    fin = IKEM.p - 1
    for t in range(0, D.__len__()):
        high = pow(int(m), t, fin)
        mul = pow(D[t], high, IKEM.p)
        D_ID = D_ID * mul
    flag3_3 = NIZK.verify_3(pi_3, g_1, g_2, IKEM.p, D_ID, z_Enc)
    flag3 = flag3 and flag3_11 and flag3_12 and flag3_13 and flag3_2 and flag3_3
    return flag1 and flag2 and flag3

def Trace(pp, PK, sk_tra, sk_adm, m, signature_TiMTAPS, com_Rz,sk_ver_EIGamal):
    pk_ATS, sk_tra_EIGamal = sk_tra

    if not Verify(pp, PK, m, signature_TiMTAPS, com_Rz, pk_ATS,sk_ver_EIGamal):
        return False
    idc, com_Rzall, Em, R, z_Enc, t_Enc, pi, signature_all,z_map_G = signature_TiMTAPS
    # 解密z
    sk_adm_EIGamal, mk_IBE = sk_adm
    dk = IKEM.Extract(int(m), mk_IBE)
    z = IKEM.Decrypt(z_Enc, dk)
    for i in range(z_map_G.__len__()):
        if z == z_map_G[i][0]:
            z = z_map_G[i][1]
    # z = z_map_G[z]
    #print("R的值" + str(R))
    #print("z的解密值" + str(z))
    # 追踪
    n = pk_ATS[1].__len__()
    S = ATS.Trace(pk_ATS,m,R,z,ATS.g,n,pk_ATS[0])
    return S

def Open(S_id, sigma_HTLP_cor,sk_adm,pp):
    pp_ATS, pp_HTLP_ADD, pp_HTLP_MUL, pp_HC, pp_IBE = pp
    sk_adm_EIGamal, mk_IBE = sk_adm
    HTLP = []
    for item in sigma_HTLP_cor:
        Eid_adm, sigma_H = item[0], item[1]
        Eid_dec = EIGamal.decrypt(Eid_adm[0], Eid_adm[1], sk_adm_EIGamal, EIGamal.p)
        if Eid_dec == str(S_id):
            HTLP.append(sigma_H)
    R_HTLP = []
    z_HTLP = []
    for i in range(HTLP.__len__()):
        R_HTLP.append(HTLP[i][0])
        z_HTLP.append(HTLP[i][1])
    R_Puzzle = HTLP_MUL.MHP_PEval(pp_HTLP_MUL, R_HTLP)
    z_Puzzle = HTLP_ADD.LHP_PEval(pp_HTLP_ADD, z_HTLP)
    R = HTLP_MUL.MHP_PSolve(pp_HTLP_MUL, R_Puzzle)
    z = HTLP_ADD.LHP_PSolve(pp_HTLP_ADD, z_Puzzle)
    # print("R的解谜值" + str(R))
    # print("z的解谜值" + str(z))
    return R, z

def test_notDelay():
    k, n, t, T, Sid, idc = 5, 10, 5, 100, 1, 2
    m = "123746"
    S = random.sample(range(0, n), t)
    S.sort()
    #S = [0, 1, 2, 4, 7]
    print("签名者的序列是"+str(S))
    pp,sk_ATS,PK,sk_com,sk_tra,sk_adm,sk_ver_EIGamal = Setup(1,k,n,t,T)
    pk = sk_tra[0]
    pki = pk[1]
    sigma_cor, sigma_HTLP_cor, com_Rz = Sign(sk_ATS, m, S, pki, PK, Sid, pp, pk)
    signature_TiMTAPS = Combine(Sid,sk_com,m,sigma_cor,PK,S,pp,idc)
    flag = Verify(pp, PK, m, signature_TiMTAPS, com_Rz, pk,sk_ver_EIGamal)
    S_t = Trace(pp, PK, sk_tra, sk_adm, m, signature_TiMTAPS, com_Rz,sk_ver_EIGamal)
    S_t.sort()
    print("Verify是否正确"+str(flag))
    print("追踪到的序列是"+str(S_t))
    return S == S_t

def test_delay():
    k, n, t, T, Sid, idc = 5, 10, 5, 100, 1, 2
    m = "123746"
    S = random.sample(range(1, n), t)
    S.sort()
    # S = [2, 5, 7, 8]
    print("签名者的序列是" + str(S))
    pp, sk_ATS, PK, sk_com, sk_tra, sk_adm, sk_ver_EIGamal = Setup(1, k, n, t, T)
    pk = sk_tra[0]
    pki = pk[1]
    sigma_cor, sigma_HTLP_cor, com_Rz = Sign(sk_ATS, m, S, pki, PK, Sid, pp, pk)
    #signature_TiMTAPS = Combine(sk_com, m, sigma_cor, PK, S, pp, idc)
    R, z = Open(Sid, sigma_HTLP_cor, sk_adm, pp)
    S_t = ATS.Trace(pk,m,R,z,ATS.g,n,pk[0])
    S_t.sort()
    print("追踪到的序列是"+str(S_t))
    return S == S_t

def textATS(S, pk, m, R, z, n, t):
    g = ATS.g
    S_t = ATS.Trace(pk, m, R, z, g, n, t)
    S_t.sort()
    S.sort()
    return S_t == S


if __name__ == '__main__':

    test_notDelay()
    test_delay()

    # for i in range (50):
    #     if not test_delay():
    #     #if not test_notDelay():
    #         print("error!!!!!!!!!!!!!!!!!!!")
