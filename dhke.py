#!/usr/bin/python
import argparse
import random

#I come up with two prime numbers g and p and tell you what they are.

#You then pick a secret number (a), but you don't tell anyone. Instead you compute ga mod p and send that result back to me. (We'll call that A since it came from a).

#I do the same thing, but we'll call my secret number b and the computed number B. So I compute gb mod p and send you the result (called "B")

#Now, you take the number I sent you and do the exact same operation with it. So that's Ba mod p.

#I do the same operation with the result you sent me, so: Ab mod p.

class DHKE:

    
    verboseprint = lambda *a: None

    def __init__(self, prime_base, prime_mod, verbose, name):
        self.prime_base = prime_base
        self.prime_mod = prime_mod
        self.secret = 0
        self.my_mix = 0
        self.shared_mix = 0
        self.verbose = verbose
        self.name = name
        self.shared_secret = 0
        if self.verbose:
            def x(string):
                print string
            self.verboseprint = x

    def share_prime_base(self):
        print "Eve sees prime base {} from {}".format(self.prime_base, self.name)
        return self.prime_base

    def set_prime_base(self,base):
        self.verboseprint("{} sets prime base to {}".format(self.name, base))
        self.prime_base = base

    def share_prime_mod(self):
        print "Eve sees prime mod {} from {}".format(self.prime_mod, self.name)
        return self.prime_mod

    def set_prime_mod(self,mod):
        self.verboseprint("{} sets prime mod to {}".format(self.name, mod))
        self.prime_mod = mod

    def mix(self):
        print "{} mixes their numbers".format(self.name)
        self.my_mix = self.prime_base**self.secret
        self.my_mix = self.my_mix % self.prime_mod
        self.verboseprint("({} ^ {} ) mod {} = {}".format(self.prime_base, self.secret, self.prime_mod, self.my_mix) )

    def share_mixed(self):
        print "Eve sees mixed number {} from {}".format(self.my_mix, self.name)
        return self.my_mix

    def set_secret(self, secret):
        self.secret = secret

    def generate_secret(self):
        self.secret = random.randrange(0,1000)
        self.verboseprint("{} sets their secret to {}".format(self.name, self.secret))

    def set_shared_mix(self,mixed):
        self.shared_mix = mixed
        self.verboseprint("{} sets their friend's mixed number to {}".format(self.name, self.shared_mix))

    def generate_shared_secret(self):
        self.shared_secret = self.shared_mix**self.secret
        self.shared_secret = self.shared_secret % self.prime_mod
        print "{} calculated the shared secret to be {} = ( {} ^ {} ) mod {}".format(self.name, self.shared_secret, self.shared_mix, self.secret, self.prime_mod)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-A","--Alice", help="Set Alice to verbose", default=False,action='store_true')
    parser.add_argument("-B","--Bob", help="Set Bob to verbose", default=False,action='store_true')
    args = parser.parse_args()
    alice = DHKE(5,23,args.Alice,'Alice')
    bob = DHKE(5,11,args.Bob,'Bob')
    print "Alice -> Bob"
    bob.set_prime_base(alice.share_prime_base())
    print "\nAlice -> Bob"
    bob.set_prime_mod(alice.share_prime_mod())
    print "\nInternal"
    alice.generate_secret()
    bob.generate_secret()
    alice.mix()
    bob.mix()
    print "\nAlice -> Bob"
    bob.set_shared_mix(alice.share_mixed())
    print "\nBob -> Alice"
    alice.set_shared_mix(bob.share_mixed())
    print "\n"
    alice.generate_shared_secret()
    bob.generate_shared_secret()
    return 0

if __name__ == '__main__':
    main()

