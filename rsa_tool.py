
import random
import math

def is_prime(n):
    if n<2:
        return False
    small_primes=[2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n==p:
            return True
        if n%p==0:
            return False
    d=n-1
    s=0
    while d%2==0:
        d//=2
        s+=1
    for a in [2,3,5,7,11]:
        if a>n-2:
            continue
        x=pow(a,d,n)
        if x==1 or x==n-1:
            continue
        for _ in range(s-1):
            x=pow(x,2,n)
            if x==n-1:
                break
        else:
            return False
    return True

def gen_prime(bits=16):
    while True:
        p=random.getrandbits(bits)|1
        if is_prime(p):
            return p

def egcd(a,b):
    if b==0:
        return (1,0,a)
    x,y,g=egcd(b,a%b)
    return (y, x-(a//b)*y, g)

def modinv(a,m):
    x,y,g=egcd(a,m)
    if g!=1:
        raise Exception("no inv")
    return x % m

def gen_keys(bits=16):
    p=gen_prime(bits)
    q=gen_prime(bits)
    while q==p:
        q=gen_prime(bits)
    n=p*q
    phi=(p-1)*(q-1)
    e=65537
    if math.gcd(e,phi)!=1:
        for i in range(3,phi,2):
            if math.gcd(i,phi)==1:
                e=i
                break
    d=modinv(e,phi)
    return (e,n),(d,n)

def encrypt(m, pub):
    e,n=pub
    m_int=int.from_bytes(m.encode('utf-8'),'big')
    c=pow(m_int,e,n)
    return c

def decrypt(c, priv):
    d,n=priv
    m_int=pow(c,d,n)
    length=(m_int.bit_length()+7)//8
    return m_int.to_bytes(length,'big').decode('utf-8',errors='ignore')

if __name__=="__main__":
    pub,priv=gen_keys(20)
    msg="hello world"
    c=encrypt(msg,pub)
    p=decrypt(c,priv)
    print("pub",pub)
    print("cipher",c)
    print("plain",p)
