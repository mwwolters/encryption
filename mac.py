#!/usr/bin/python
from hashlib import md5
import struct
import argparse

class mac(object):
    def __init__(self):
        return 0

class hmac(object):
    verboseprint = lambda *a: None

    def __init__(self, verbose):
        if verbose:
            def x(string):
                print string
            self.verboseprint = x

    #HMAC(K,m) = H( (K xor opad) || H ( (K xor ipad) || m ) )
    def hmac_md5(self,key,message):
        blocksize = md5().block_size
        if len(key) > blocksize:
            key = md5.digest(key)
        elif len(key) < blocksize:
            pad = '\x00'* (blocksize - len(key))
            key += pad
        o_key_pad = [ord('\x5c')^ord(b) for b in key]
        i_key_pad = [ord('\x36')^ord(b) for b in key]
        #print o_key_pad
        #print i_key_pad
        format = ">" + "B"*(blocksize)
        o_key_pad = struct.pack(format, *o_key_pad)
        i_key_pad = struct.pack(format, *i_key_pad)
        self.verboseprint("o_key_pad: {}\ni_key_pad: {}\nkey:       {}".format(o_key_pad.encode("hex"), i_key_pad.encode("hex"), key.encode("hex")))
        inner =  md5(i_key_pad + message).digest()
        result = md5(o_key_pad + inner).digest()
        self.verboseprint("Result  =  {} = md5( o_key_pad || md5( i_key_pad || message ) )".format(result.encode("hex")))
        return result

def test():
    print "Test Case\n" + "+"*45
    hm = hmac(True)
    h = hm.hmac_md5(b"Jefe", b"what do ya want for nothing?")
    print "Result     {}\nshould be  {}".format(h.encode("hex"), "750c783e6ab0b503eaa86e310a5db738")
    

#test cases
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="prints a test hmac message to compare to a precalculated one", default=False, action='store_true')
    parser.add_argument("-m", "--message", help="The message to authenticate", default="Test Message")
    parser.add_argument("-k", "--key", help="The key to use", default="Password1")
    parser.add_argument("-v", "--verbose", help="Verbose output", default=False, action='store_true')

    args = parser.parse_args()
    
    if args.test:
        test()
    else:
        hm = hmac(args.verbose)
        h = hm.hmac_md5(args.key, args.message)
        print "Result:    {}".format(h.encode("hex"))

if __name__ == "__main__":
    main()
