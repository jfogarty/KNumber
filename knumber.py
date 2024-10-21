'''
# knumber main program.
# -----------------------------------------------------------------------------
# John Fogarty - https://github.com/jfogarty - johnhenryfogarty@gmail.com
# ----------------------------------------------------------------------------
# Description: 
#    The number 6174 is known as Kaprekar's constant after the Indian
#    mathematician D. R. Kaprekar.
#
#    A process, known as Kaprekar's routine is:
#      1. Take any four-digit number, using at least two different digits
#         (leading zeros are allowed).
#      2. Arrange the digits in descending and then in ascending order to
#         get two four-digit numbers, adding leading zeros if necessary.
#      3. Subtract the smaller number from the bigger number.
#      4. Go back to step 2 and repeat.
#
#    Any four digit positive integer will converge on 6174 within 6 iterations,
#    unless it violates rule 1 (i.e. all digits are identical)
#
#    This program introduces general classes of KNumbers which can have a radix
#    from 2 to 16, length greated than 2. These are used to play around with
#    variant forms of numbers to see if there are other constants similar to
#    Kaprekar's are available in other bases or number lengths.
#
#------------------------------------------------------------------------------
'''

from typing import Any, Self
import time

CHAR_CODES = '0123456789abcdef'
KAPREKARS_CONSTANT = 6174

#------------------------------------------------------------------------------
def int_to_str_radix(
            value:  int,
            radix:  int  = 10,
            digits: int  = 0,
            base_prefix: bool = False
        ) -> str:
    assert 16 >= radix >= 2, "Only bases from 2 to 16 are supported"
    assert value >= 0, "Only positive integers are supported"
    assert digits >= 0, "The digit count must be a positive integers"
    s = ''
    v = value
    while v > 0:
        c = CHAR_CODES[v % radix]
        s = c + s
        v = v // radix
    if digits:
        s = s.zfill(digits)
    if base_prefix:
        if radix == 16: s = '0x' + s
        if radix ==  8: s = '0o' + s
        if radix ==  2: s = '0b' + s
        if radix == 10: s = s + '.'
    return s


def max_value_in_radix(radix:int, digits:int) -> int:
    v = 0
    max_digit = radix - 1
    for n in range(digits): v = v*radix + max_digit
    return v


#------------------------------------------------------------------------------
class KNumberBase():
    '''
    '''
    def __init__(self, digits=4, radix=10):
        assert 10 >= digits > 1
        assert 16 >= radix  > 1
        self.digits = digits
        self.radix  = radix
        self.max    = max_value_in_radix(radix, digits)


    def __eq__(self, b:Self) -> bool:
        assert isinstance(b, KNumberBase)
        a = self
        return (a.digits, a.radix) == (b.digits, b.radix)


    def __str__(self) -> str:
        s = f"KB{self.radix}:{self.digits}"
        return s

#------------------------------------------------------------------------------
class KNumber():
    '''
    '''
    def __init__(self, value:int | str, kbase:KNumberBase):
        if type(value) is str:
            assert len(value) == kbase.digits, "Strings must match the exact class length"
            value = int(value, kbase.radix)
        if type(value) is int:
            assert value >= 0, "Only positive integers are supported"
            assert value < kbase.radix**kbase.digits, "Maximum value exceeded"
        else:
            assert False, "Only int and str inputs are allowed"
        self.value  = value
        self.kbase  = kbase
        self.radix  = kbase.radix
        self.digits = kbase.digits


    def as_str(self, base_prefix:bool=False) -> str:
        return int_to_str_radix(self.value,
                                self.kbase.radix, 
                                self.kbase.digits,
                                base_prefix)

    def min_str(self) -> str:
        return ''.join(sorted(self.as_str(), reverse=False, key=str.lower))


    def max_str(self) -> str:
        return ''.join(sorted(self.as_str(), reverse=True, key=str.lower))


    def min(self) -> Self:
        v = self.as_str()
        return KNumber(self.min_str(), self.kbase)


    def max(self) -> Self:
        v = self.as_str()
        return KNumber(self.max_str(), self.kbase)


    def __eq__(self, b:Self) -> bool:
        assert isinstance(b, KNumber)
        a = self
        return a.value == b.value


    def __ne__(self, b:Self) -> bool:
        assert isinstance(b, KNumber)
        a = self
        return a.value != b.value


    def __add__(self, b) -> Self:
        assert isinstance(b, KNumber)
        a = self
        assert a.kbase == b.kbase
        av = a.value
        bv = b.value
        v = av + bv
        #print(f"+++ Added {av}+{bv} --> {v}")
        if v > a.kbase.max:
            avf = int_to_str_radix(av, a.radix, a.digits, base_prefix=True)
            bvf = int_to_str_radix(bv, b.radix, b.digits, base_prefix=True)
            vf  = int_to_str_radix(v,  b.radix, b.digits, base_prefix=True)
            s = f"Adding {avf} + {bvf} is {vf}; Exceeded range for class."
            raise ValueError(s)
        kv = KNumber(v, self.kbase)
        return kv


    def __sub__(self, b) -> Self:
        assert isinstance(b, KNumber)
        a = self
        assert a.kbase == b.kbase
        av = a.value
        bv = b.value
        v = av - bv
        #print(f"+++ Subtracted {av}+{bv} --> {v}")
        if v < 0:
            avf = int_to_str_radix(av, a.radix, a.digits, base_prefix=True)
            bvf = int_to_str_radix(bv, b.radix, b.digits, base_prefix=True)
            s = f"Subtracting {avf} - {bvf} is negative; Not supported for class."
            raise ValueError(s)
        kv = KNumber(v, self.kbase)
        return kv


    def sum(self) -> Self:
        return self.max() + self.min()


    def diff(self) -> Self:
        return self.max() - self.min()


    def __str__(self) -> str:
        s = f"KNumber({self.as_str()} : {self.kbase})"
        return s

#------------------------------------------------------------------------------
def main():
    print("- KNumber (Kaprekar's routine) test")
    kbase   = KNumberBase(radix=16, digits=4)
    kb10_2  = KNumberBase(radix=10, digits=2)
    kb10_3  = KNumberBase(radix=10, digits=3)
    kb10_4  = KNumberBase(radix=10, digits=4)
    kb10_5  = KNumberBase(radix=10, digits=5)
    kb10_6  = KNumberBase(radix=10, digits=6)
    kb10 = kb10_4
    k  = KNumber('A234', kbase)
    k2 = KNumber('1234', kb10)

    print(f"- kbase is {kbase}")
    print(f"- kbase.max is {KNumber(kbase.max, kbase)}")

    print(f"- k is {k}")
    print(f"- k.min()     is {k.min()}")
    print(f"- k.max()     is {k.max()}")
    print(f"- k.max+k.min is {k.max()+k.min()}")
    print(f"- k.max-k.min is {k.max()-k.min()}")
    print(f"- k.sum       is {k.sum()}")
    print(f"- k.diff      is {k.diff()}")

    print(f"- kb10 is {kb10}")
    print(f"- kb10.max is {KNumber(kb10.max, kb10)}")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    for radix in [2, 8, 10, 16]:
        radix_start = time.time()
        print("="*80)
        print(f"+++++ BASE {radix} +++++")
        dr = [3, 4, 5, 6, 7]
        for digits in dr:
            digits_start = time.time()
            kb = KNumberBase(radix=radix, digits=digits)
            print("-"*80)
            kset = {
                'base'        : kb,
                'convergents' : {}
            }
            unconverged = 0
            for k1v in range(1, kb.max+1):
                k = KNumber(k1v, kb)
                k1 = k
                for i in range(1,22):
                    k1r = k1.diff()
                    if k1r.value == 0:
                        break
                    #print(f"  - {i} [{k}] k1.diff is {k1.diff()}")
                    if k1 == k1r:
                        break
                    k1 = k1r
                if k1r.value == 0:
                    continue

                if (i>20) :
                    unconverged += 1
                else:
                    kc = kset['convergents']
                    kv = k1r.as_str(base_prefix=True)
                    if kv not in kc:
                        kc[kv] = [0, {}]
                    # Count the number of times a value converged.
                    kc[kv][0] += 1
                    kn = kc[kv][1]
                    if i not in kn:
                        kn[i] = 0
                    kn[i] += 1

            kb = kset['base']
            kc = kset['convergents']
            print(f"- Base: {kb.radix}; {kb.digits} digits")
            for v in sorted(kc.keys()):
                converged_total = kc[v][0]
                converged_in    = kc[v][1]
                print(f"  - {v} was converged to {converged_total} times.")
                for n in sorted(converged_in.keys()):
                   print(f"    - {n} : {converged_in[n]}")
            if unconverged > 0:
                print(f"  - {unconverged} failures to converge!")
            digits_end = time.time()
            et = digits_end - digits_start
            print(f"  - elapsed time: {et:.4f} seconds.")

        radix_end = time.time()
        et = radix_end - radix_start
        print(f"+++++ BASE {radix} ended after {et:.2f} seconds.")


if __name__ == "__main__":

    main()
