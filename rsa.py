#!/usr/bin/python
import argparse

#primes p and q
#compute n = pq
#compute totient = n-(p+q-1)
#select e: 1<e<totient and gcd(e,totient) = 1
#solve for d where d-e = 1 mod totient

class RSA(object):
    
    verboseprint = lambda *a: None
    public_key = (3233,17)
    private_key = 2753

    #potential args:
    #verbose
    #public_key (x,y)
    #private key
    #prime_p
    #prime_q
    #
    #ways to run
    #give p and q, generate key
    #give private and public
    def __init__(self, verbose, public_key, private_key, prime_p, prime_q):
        if verbose:
            def x(string):
                print string
            self.verboseprint = x
        self.public_key = public_key
        self.private_key = private_key  
        self.prime_p = prime_p
        self.prime_q = prime_q

    def encrypt(self, **kwargs):
        encrypted = 0
        if kwargs is not None:
            message = int(kwargs["message"])
            if len(kwargs) == 1: 
                encrypted = (message**self.public_key[1])%self.public_key[0]
                self.verboseprint("Encrypt( {} ) = {} = {}^{} mod {}".format(message, encrypted, message, self.public_key[1], self.public_key[0]))
            else:
                public_key = kwargs["public_key"]
                encrypted = (message**public_key[1])%public_key[0]
                self.verboseprint("Encrypt( {} ) = {} = {}^{} mod {}".format(message, encrypted, message, public_key[1], public_key[0]))
        return encrypted
 
    def decrypt(self,**kwargs):
        decrpyted = 0
        if kwargs is not None:
            message = int(kwargs["message"])
            if len(kwargs) == 1:
                decrypted = (message**self.private_key) % self.public_key[0]
                self.verboseprint("Decrypt( {} ) = {} = {}^{} mod {}".format(message, decrypted, message, self.private_key, self.public_key[0]))
        return decrypted

    
    def sign(self, m):
        key = (self.public_key[0],self.private_key)
        self.verboseprint("Signing using private key {} and {}".format(self.private_key, self.public_key[1]))
        signed = self.encrypt(message=m, public_key=key)
        return signed

    def verify(self, m):
        self.verboseprint("Verified using public key {}".format(self.public_key))
        verified = self.encrypt(message=m, public_key=self.public_key)
        return verified

def test(num):
    rsa = RSA(True, (3233,17), 2753, 61, 53)
    print "RSA Encryption and Decryption:\n"
    rsa.verboseprint("My public key is {}".format((3233,17)))
    rsa.verboseprint("It is made of two primes, {} and {}".format(61, 53))
    rsa.verboseprint("{} = {}*{}".format(3233, 61, 53))
    rsa.verboseprint("{} is another prime, coprime to ({}-1)*({}-1)".format(17, 61, 53))
    rsa.verboseprint("My private key is {} = {}^-1 mod ({}-1)*({}-1)".format(2753, 17, 61, 53)) 
    encrypted = rsa.encrypt(message=num)
    decrypted = rsa.decrypt(message=encrypted)
    print "+"*40 + "\n\n"
    print "RSA Signing"
    signed = rsa.sign(num)
    verified = rsa.verify(signed)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', help='Enables verbose output', default=False, action='store_true')
    parser.add_argument('-t', '--test', help='Test encrypt and decrypts', default=False, action='store_true') 
    parser.add_argument('-m', '--message', help='Message (integer) to encrypt / decrypt', default=65)
    parser.add_argument('-p', '--prime_p', help='The first prime for the key', default=61)
    parser.add_argument('-q', '--prime_q', help='The second prime for the key', default=53)
    parser.add_argument('-n', '--public_key', help='Part of the public key. n = p*q for primes p and q in (n, e) the public key', default=3233)
    parser.add_argument('-e', '--public_key_2', help='The other part of the public key, e in (n, e) the public key', default=17)
    parser.add_argument('-d', '--private_key', help='The private key, e^-1 mod t', default=2753)
    parser.add_argument('-E', '--encrypt', help='Encrypt the message', default=False, action='store_true')
    parser.add_argument('-D', '--decrypt', help='Decrypt the message', default=False, action='store_true')
    args = parser.parse_args()

    if args.test:
        test(int(args.message))
    else:
        rsa = RSA(True, (int(args.public_key), int(args.public_key_2)), int(args.private_key), int(args.prime_p), int(args.prime_q))
        encrypted = int(args.message)
        if args.encrypt:
            encrypted = rsa.encrypt(message=encrypted)
        if args.decrypt:
            decrypted = rsa.decrypt(message=encrypted)

    return 0

if __name__ == '__main__':
    main()
