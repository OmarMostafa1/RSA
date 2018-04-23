import random
import os

def ExtendedEuclidean(r0, r1): #r0 > r1
    s0 = 1
    t0 = 0
    s1 = 0
    t1 = 1
    while r1 != 0:
        q = r0 / r1
        r1, r0 = [ r0%r1, r1 ]
        s0, t0, s1, t1 = [ s1 - q*s0, t1 - q*t0, s0, t0 ]
    return [ r0, t1, s1 ] 
    
def modularInverse(mod, a):
    gcd, s1 , inv = ExtendedEuclidean(mod, a)
    
    return None if gcd != 1 else (inv % mod)
    

def getParameters():
    p = primeGen()
    q = primeGen()
    n = p*q
    print n
    numberOfPrimes = (p-1)*(q-1)
    minD = int(0.3*(len(bin(n))-2))
    e,d = select_E(numberOfPrimes,minD)
 
    
    return p,q,e,d
   
def squareAndMultiply(x,e,mod): 
    e = [int(i) for i in list(bin(e)[3:])]  
    base = x
    for i in e:
        x = (x**2) % mod
        if i == 1: 
            x = (x*base) % mod
    return x
    
def encrypt(plainText,publicKey):
    n,e = publicKey
    return squareAndMultiply(plainText,e,n)
    
def decrypt(cipherText,privateKey,p,q,useCRT = False):
    if useCRT == False:
        n = q*p
        return squareAndMultiply(cipherText,privateKey,n)
    else:
        return decryptUsingCRT(cipherText,privateKey,p,q)

def decryptUsingCRT(cipherText,privateKey,p,q):
    yp = cipherText % p
    yq = cipherText % q
    dp = privateKey % (p-1)
    dq =  privateKey % (q-1)
    xp = squareAndMultiply(yp,dp,p)
    xq = squareAndMultiply(yq,dq,q)
    cp = modularInverse(p,q%p)
    cq = modularInverse(q,p%q)
    x = ((q*cp*xp) + (p*cq*xq)) % (p*q)
    return x

def MillerRabin(primeCandidate):
    for i in range(1,40): 
        a = random.SystemRandom().randint(2,primeCandidate-2) 
        r=primeCandidate-1
        u=1
        while r % 2 == 0: 
            u+=1
            r /= 2
        z = squareAndMultiply(a,r,primeCandidate)
        if z != 1 and z != primeCandidate-1:
            for j in range(1,u):
                z = (z**2) % primeCandidate
                if z == 1:
                    return False  
            if z != primeCandidate-1:
                return False  
    return True   

    
def primeGen():
     p = int(os.urandom(64).encode('hex'),16)
     while not MillerRabin(primeCandidate=p) :  
         p = int(os.urandom(64).encode('hex'),16)
     return p


def select_E(limit,minD):
    d = None
    while d == None:
        e = int(random.randint(1,limit-1))
        d = modularInverse(limit,e)
        if d != None:
            if len(bin(d))-2 < minD:
                d = None
    return e,d


def stringToAscii(s):
    return int(''.join((str(ord(c)+100)) for c in s)) # +100 to make all numbers have 3 digits


def asciiToString(a):
    x = [i for i in str(a)]
    res = []
    i=0
    while i < len(x)-2:
        a = [x[i],x[i+1],x[i+2]]
        res.append(''.join(a))
        i+=3
    res = [int(c)-100 for c in res]
    return ''.join(chr(i) for i in res)

def partitioningPlainText(text): 
     length=100;                   
     return [text[i:i+length] for i in range(0, len(text), length)]

useCRT = True

print "Generating parameters..."
p,q,e,d = getParameters()

n = p*q
publicKey = [n,e]
privateKey = d
print "Generated Sucessfully!\n"

Input = raw_input("Enter the PlainText : ")
partitionedInput = partitioningPlainText(Input)
asciiInput = [stringToAscii(aa) for aa in partitionedInput ]



cipherText = [encrypt(aa,publicKey) for aa in asciiInput ]
print  "Encrypted Message :" + str(cipherText) + "\n" 

plainText = [decrypt(aaa,privateKey,p,q,useCRT=useCRT) for aaa in cipherText]



output = [asciiToString(z) for z in plainText]
print "PlainText after decryption :" + ''.join(output)

