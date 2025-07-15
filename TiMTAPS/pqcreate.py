import random

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137,
                139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
                223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
                293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
                383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
                463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
                569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643,
                647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
                743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
                839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937,
                941, 947, 953, 967, 971, 977, 983, 991, 997]


def rabin_miller(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s >>= 1
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    # 排除0,1和负数
    if num < 2:
        return False
    # 创建小素数的列表,可以大幅加快速度
    # 如果是小素数,那么直接返回true
    if num in small_primes:
        return True
    # 如果大数是这些小素数的倍数,那么就是合数,返回false
    for prime in small_primes:
        if num % prime == 0:
            return False
    # 如果这样没有分辨出来,就一定是大整数,那么就调用rabin算法
    return rabin_miller(num)


# 素数默认位数
P_LEN = pow(2,10000)


# 随机生成一个安全素数
def primeGen(P_len=P_LEN):
    p_floor = 2 ** (P_len - 1) + 1
    p_ceiling = 2 ** P_len - 1
    while True:
        p = random.randint(p_floor, p_ceiling)
        # (p - 1)/2也是素数，确保p为安全素数
        if is_prime(p) and is_prime(p >> 1):
            break
    return p

if __name__ == '__main__':
    file = open('pqcreate_store.txt', mode='a')
    for i in range(10,12):
        len = pow(2,i)
        file.write('长度为'+str(len)+'的强素数：\n')
        print('长度为'+str(len)+'的强素数：\n')
        for i in range(5):
            p = primeGen(1024)
            print(p)
            file.write(str(p)+'\n')
            print(is_prime(p))
            file.write(str(is_prime(p)) + '\n')
            print(p >> 1)
            file.write(str(p >> 1) + '\n')
            print(is_prime(p >> 1))
            file.write(str(is_prime(p >> 1)) + '\n')

