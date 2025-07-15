import random
import hashlib
def prove_11(g,z,pk,b,c,R,q,n):

    #验证等式g^z = \sum_{i=1}^n b_i p_i^c
    pki = pk[1]
    left_dengshi = pow(g, z, q)
    right_dengshi = 1
    for i in range(pki.__len__()):
        right_dengshi = (right_dengshi * pow(pki[i], c * b[i], q)) % q
    right_dengshi = right_dengshi * R % q
    flag = left_dengshi == right_dengshi

    belta_z = random.randint(1, q)
    belta_b = [random.randint(1, q) for i in range(n)]

    left_A = pow(g, belta_z, q)
    right_A = 1
    for i in range(pki.__len__()):
        right_A = (right_A * pow(pki[i], c * belta_b[i], q)) % q
    A = (left_A * pow(right_A,-1,q)) % q

    h = int(hashlib.sha256((str(left_dengshi) + str(A)).encode()).hexdigest(), 16) % q

    z_hat = z*h+belta_z

    b_hat = []
    for i in range(n):
        b_hati = b[i]*h+belta_b[i]
        b_hat.append(b_hati)
    pi = [A,z_hat,b_hat]

    # left_check = 1
    # for i in range(n):
    #     left_check = (left_check * pow(pki[i], c*b_hat[i], q)) % q
    # left_check = (A * pow(R, h, q) * left_check)% q
    # right_check = pow(g, z_hat, q)
    #
    # flag_check = left_check == right_check
    # print(flag_check)

    return pi

def verify_11(pi,g_z,pk,R,g,q,n,c):
    A,z_hat,b_hat = pi
    pki = pk[1]
    h = int(hashlib.sha256((str(g_z) + str(A)).encode()).hexdigest(), 16) % q
    left_check = 1
    for i in range(n):
        left_check = (left_check * pow(pki[i], c * b_hat[i], q)) % q
    left_check = (A * pow(R, h, q) * left_check) % q
    right_check = pow(g, z_hat, q)

    flag_check = left_check == right_check
    return left_check == right_check

def prove_12(g,r_,pk_V_end,b,q,n,t_Enc):
    t_Enc11 = pow(g, r_, q)
    b_sum = 0
    for i in range(n):
        b_sum = b_sum+b[i]
    t_Enc21 = (pow(g, b_sum, q) * pow(pk_V_end, r_, q)) % q
    flag1 = t_Enc11 == t_Enc[0]
    flag2 = t_Enc21 == t_Enc[1]
    #随机数生成
    r = random.randint(1, q)
    belta = [random.randint(1, q) for i in range(n)]
    #计算A
    A = pow(g,r,q)
    #计算B
    high = 0
    for i in range(0,n):
        high = high + belta[i]
    B = (pow(g,high,q)*pow(pk_V_end,r,q))%q
    #计算hash值
    h = int(hashlib.sha256((str(t_Enc[0]) + str(t_Enc[1]) + str(A) + str(B)).encode()).hexdigest(), 16) % q
    #计算传递的值
    r_hat = r_*h + r
    b_hat = []
    for i in range(0, n):
        b_11 = b[i] * h + belta[i]
        b_hat.append(b_11)

    #检查
    # left_checkA = (A*pow(t_Enc[0],h,q))%q
    # right_checkA = pow(g,r_hat,q)
    # high = 0
    # for i in range (n):
    #     high = high + b_hat[i]
    # left_checkB = (B*pow(t_Enc[1],h,q))%q
    # right_checkB = (pow(g,high,q)*pow(pk_V_end,r_hat,q))%q
    #
    # flag3 = left_checkA == right_checkA
    # flag4 = left_checkB == right_checkB


    pi = [A,B,r_hat,b_hat]
    return pi

def verify_12(pi,ct0,ct1,pk_V_end,g,q,n):
    A, B, r_hat, b_hat = pi
    h = int(hashlib.sha256((str(ct0) + str(ct1) + str(A) + str(B)).encode()).hexdigest(), 16) % q
    left_checkA = (A * pow(ct0, h, q)) % q
    right_checkA = pow(g, r_hat, q)
    high = 0
    for i in range(n):
        high = high + b_hat[i]
    left_checkB = (B * pow(ct1, h, q)) % q
    right_checkB = (pow(g, high, q) * pow(pk_V_end, r_hat, q)) % q

    flag3 = left_checkA == right_checkA
    flag4 = left_checkB == right_checkB
    return flag3 and flag4

def prove_13(c_0,c_b,gama,alpha,phi,h,g,b,q,n):
    #随机数生成
    belta_gama = random.randint(1,q)
    belta_b = [random.randint(1, q) for _ in range(n)]
    belta_phi = [random.randint(1, q) for _ in range(n)]
    #计算A
    A = pow(g,belta_gama,q)
    #计算B
    B = []
    for i in range(0,n):
        B_i = (pow(g,belta_b[i],q)*pow(h[i],belta_gama,q))%q
        B.append(B_i)
    #计算C
    C = 1
    for i in range(0,n):
        high = (pow(alpha,i,q-1)*belta_b[i])%(q-1)
        C_i = (pow(c_b[i],high,q)*pow(h[i],belta_phi[i],q))%q
        C = (C*C_i)%q
    #计算hash值
    hash = int(hashlib.sha256((str(c_0) + str(c_b) + str(A) + str(B)+ str(C)).encode()).hexdigest(),16) % q
    #计算传递的值
    gama_hat = gama*hash + belta_gama
    b_hat = []
    for i in range(0,n):
        b_11 = b[i]*hash + belta_b[i]
        b_hat.append(b_11)
    phi_hat = []
    for i in range(0,n):
        phi_11 = phi[i]*hash + belta_phi[i]
        phi_hat.append(phi_11)
    #检查一下
    left_checkA = (A*pow(c_0,hash,q))%q
    right_checkA = pow(g,gama_hat,q)
    flag1 = left_checkA == right_checkA
    flag2 = True
    for i in range(n):
        left_checkB = (B[i]*pow(c_b[i],hash,q))%q
        right_checkB = pow(g,b_hat[i],q)*pow(h[i],gama_hat,q)%q
        flag2 = flag2 and (left_checkB == right_checkB)
    left_checkC = C
    for i in range(n):
        high = (pow(alpha,i,q-1)*hash)%(q-1)
        left_checkC = (left_checkC*pow(c_b[i],high,q))%q
    right_checkC = 1
    for i in range(n):
        high = (pow(alpha, i, q - 1) * b_hat[i]) % (q - 1)
        mul = (pow(c_b[i],high,q)*pow(h[i],phi_hat[i],q))%q
        right_checkC = (right_checkC*mul)%q
    flag3 = left_checkC == right_checkC
    pi = [A,B,C,gama_hat,b_hat,phi_hat]
    return pi

def verify_13(pi,c_0,c_b,g,h,alpha,q,n):
    A, B, C, gama_hat, b_hat, phi_hat = pi
    hash = int(hashlib.sha256((str(c_0) + str(c_b) + str(A) + str(B) + str(C)).encode()).hexdigest(),16) % q
    left_checkA = (A * pow(c_0, hash, q)) % q
    right_checkA = pow(g, gama_hat, q)
    flag1 = left_checkA == right_checkA
    flag2 = True
    for i in range(n):
        left_checkB = (B[i] * pow(c_b[i], hash, q)) % q
        right_checkB = pow(g, b_hat[i], q) * pow(h[i], gama_hat, q) % q
        flag2 = flag2 and (left_checkB == right_checkB)
    left_checkC = C
    for i in range(n):
        high = (pow(alpha, i, q - 1) * hash) % (q - 1)
        left_checkC = (left_checkC * pow(c_b[i], high, q)) % q
    right_checkC = 1
    for i in range(n):
        high = (pow(alpha, i, q - 1) * b_hat[i]) % (q - 1)
        mul = (pow(c_b[i], high, q) * pow(h[i], phi_hat[i], q)) % q
        right_checkC = (right_checkC * mul) % q
    flag3 = left_checkC == right_checkC

    return flag1 and flag2 and flag3

def prove_2(g,h,q,pk_i,r,cmt_pki):
    # flag_check = (cmt_pki == (pow(g, pk_i, q)*pow(h, r, q))%q)
    alpha_1 = random.randint(1,q)
    alpha_2 = random.randint(1,q)
    A = (pow(g,alpha_1,q)*pow(h,alpha_2,q))%q
    hash = int(hashlib.sha256((str(cmt_pki) + str(A) + str(g) + str(h)).encode()).hexdigest(),16) % q
    alpha_1_hat = pk_i * hash + alpha_1
    alpha_2_hat = r * hash + alpha_2

    #检查一下
    # left_check = (A*pow(cmt_pki,hash,q))%q
    # right_check = (pow(g,alpha_1_hat,q)*pow(h,alpha_2_hat,q))%q
    # flag = left_check == right_check
    pi = (A,alpha_1_hat,alpha_2_hat)
    return pi

def verify_2(pi, g, h, q, cmt_pki):
    A, alpha_1_hat, alpha_2_hat = pi
    hash = int(hashlib.sha256((str(cmt_pki) + str(A) + str(g) + str(h)).encode()).hexdigest(), 16) % q
    left_check = (A * pow(cmt_pki, hash, q)) % q
    right_check = (pow(g, alpha_1_hat, q) * pow(h, alpha_2_hat, q)) % q
    flag = left_check == right_check
    return flag

def prove_3(g_1, g_2, r_1, z, D_m, p, z_ENC):
    alpha_1 = random.randint(1, p)
    alpha_2 = random.randint(1, p)
    A = pow(g_1, alpha_1, p)
    B = pow(g_2, alpha_1, p)
    C = pow(g_1, alpha_2 , p) * pow(D_m, alpha_1, p)
    hash = int(hashlib.sha256((str(A) + str(B) + str(C) + str(z_ENC)).encode()).hexdigest(), 16) % p
    alpha_1_hat = r_1 * hash + alpha_1
    alpha_2_hat = z * hash + alpha_2
    #检查一下
    left_checkA = (A * pow(z_ENC[0], hash, p)) % p
    right_checkA = pow(g_1, alpha_1_hat, p)
    flag1 = left_checkA == right_checkA
    left_checkB = (B * pow(z_ENC[1], hash, p)) % p
    right_checkB = pow(g_2, alpha_1_hat, p)
    flag2 = left_checkB == right_checkB
    left_checkC = (C * pow(z_ENC[2], hash, p)) % p
    right_checkC = (pow(g_1, alpha_2_hat, p) * pow(D_m, alpha_1_hat, p)) % p
    flag3 = left_checkC == right_checkC
    pi = [A, B, C, alpha_1_hat, alpha_2_hat]
    return pi

def verify_3(pi, g_1, g_2, p, D_m, z_ENC):
    A, B, C, alpha_1_hat, alpha_2_hat = pi
    hash = int(hashlib.sha256((str(A) + str(B) + str(C) + str(z_ENC)).encode()).hexdigest(), 16) % p
    left_checkA = (A * pow(z_ENC[0], hash, p)) % p
    right_checkA = pow(g_1, alpha_1_hat, p)
    flag1 = left_checkA == right_checkA
    left_checkB = (B * pow(z_ENC[1], hash, p)) % p
    right_checkB = pow(g_2, alpha_1_hat, p)
    flag2 = left_checkB == right_checkB
    left_checkC = (C * pow(z_ENC[2], hash, p)) % p
    right_checkC = (pow(g_1, alpha_2_hat, p) * pow(D_m, alpha_1_hat, p)) % p
    flag3 = left_checkC == right_checkC
    flag = flag1 and flag2 and flag3
    return flag