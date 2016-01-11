#/usr/bin/python

import time

ERATOSTHENES = 0



#check all divisions

def sieve_of_eratosthenese(min,max):
    primes = [2]
    remaining = range(3,max,2)
    while not remaining == []:
        prime = remaining[0]
        primes.append(prime)
        remaining = [x for x in remaining if not x%prime == 0]
    primes = [x for x in remaining if x > min]
    return primes

def sieve_of_sundaram(max):
    
    return 0

#generate primes in range using method:
def generate_prime_in_range(min,max,method):
    return 0 

def determine_primality(number):
    return 0

def fermat_composite_test(number):
    return 0

def miller_rabin_test(number):
    return 0

def guess_primality(number, method):
    return 0
