#!/usr/bin/python3

from var_dump import var_dump

def intcode(input, ic):

    _ptr = 0
    _rel = 0
    output = []

    while True:
        _oc = ic[_ptr] % 100

        _pm2 = (ic[_ptr] / 10000).__trunc__() % 10
        _pm1 = (ic[_ptr] / 1000).__trunc__() % 10
        _pm0 = (ic[_ptr] / 100).__trunc__() % 10

        #   Addition
        if _oc == 1:
            if _pm0 == 2:
                #   2 = relative mode
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                #   1 = immediate mode
                __opand0 = ic[_ptr+1]
            else:
                #   0 = position mode
                __opand0 = ic[ic[_ptr+1]]

            if _pm1 == 2:
                __opand1 = ic[ic[_ptr+2] + _rel]
            elif _pm1 == 1:
                __opand1 = ic[_ptr+2]
            else:
                __opand1 = ic[ic[_ptr+2]]

            if _pm2 == 2:
                __opand2 = ic[_ptr+3] + _rel
            elif _pm1 == 1:
                __opand2 = ic[_ptr+3]
            else:
                __opand2 = ic[_ptr+3]

            ic[__opand2] = __opand0 + __opand1
            _ptr += 4

        #   Multiplication
        if _oc == 2:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            if _pm1 == 2:
                __opand1 = ic[ic[_ptr+2] + _rel]
            elif _pm1 == 1:
                __opand1 = ic[_ptr+2]
            else:
                __opand1 = ic[ic[_ptr+2]]

            if _pm2 == 2:
                __opand2 = ic[_ptr+3] + _rel
            elif _pm1 == 1:
                __opand2 = ic[_ptr+3]
            else:
                __opand2 = ic[_ptr+3]

            ic[__opand2] = __opand0 * __opand1
            _ptr += 4

        #   Input
        if _oc == 3:
            ic[ic[_ptr+1] + _rel] = input.pop(0)
            _ptr += 2

        #   Output
        if _oc == 4:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            output.append(__opand0)
            _ptr += 2

        #   jump-if-true
        if _oc == 5:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            if _pm1 == 2:
                __opand1 = ic[ic[_ptr+2] + _rel]
            elif _pm1 == 1:
                __opand1 = ic[_ptr+2]
            else:
                __opand1 = ic[ic[_ptr+2]]

            if __opand0:
                _ptr = __opand1
            else:
                _ptr += 3

        #   jump-if-false
        if _oc == 6:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            if _pm1 == 2:
                __opand1 = ic[ic[_ptr+2] + _rel]
            elif _pm1 == 1:
                __opand1 = ic[_ptr+2]
            else:
                __opand1 = ic[ic[_ptr+2]]

            if not __opand0:
                _ptr = __opand1
            else:
                _ptr += 3

        #   less than
        if _oc == 7:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            if _pm1 == 2:
                __opand1 = ic[ic[_ptr+2] + _rel]
            elif _pm1 == 1:
                __opand1 = ic[_ptr+2]
            else:
                __opand1 = ic[ic[_ptr+2]]

            if _pm2 == 2:
                __opand2 = ic[_ptr+3] + _rel
            elif _pm1 == 1:
                __opand2 = ic[_ptr+3]
            else:
                __opand2 = ic[_ptr+3]

            if __opand0 < __opand1:
                ic[__opand2] = 1
            else:
                ic[__opand2] = 0

            _ptr += 4

        #   equals
        if _oc == 8:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            if _pm1 == 2:
                __opand1 = ic[ic[_ptr+2] + _rel]
            elif _pm1 == 1:
                __opand1 = ic[_ptr+2]
            else:
                __opand1 = ic[ic[_ptr+2]]

            if _pm2 == 2:
                __opand2 = ic[_ptr+3] + _rel
            elif _pm1 == 1:
                __opand2 = ic[_ptr+3]
            else:
                __opand2 = ic[_ptr+3]

            if __opand0 == __opand1:
                ic[__opand2] = 1
            else:
                ic[__opand2] = 0

            _ptr += 4

        #   adjust relative base
        if _oc == 9:
            if _pm0 == 2:
                __opand0 = ic[ic[_ptr+1] + _rel]
            elif _pm0 == 1:
                __opand0 = ic[_ptr+1]
            else:
                __opand0 = ic[ic[_ptr+1]]

            _rel = _rel + __opand0
            _ptr += 2

        #   halt
        if _oc == 99:
            return output


def xtend(f):
    def wrap(self, index, *args):
        if len(self) <= index:
            self.extend([self._gen()] * (index - len(self) + 1))
        return f(self, index, *args)
    return wrap

class defaultlist(list):
    def __init__(self, gen, lst = []):
        list.__init__(self, lst)
        self._gen = gen

    __setitem__ = xtend(list.__setitem__)
    __getitem__ = xtend(list.__getitem__)


ic = defaultlist(int, [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,252,1,1023,1102,36,1,1008,1102,24,1,1017,1101,25,0,1013,1102,479,1,1026,1101,0,259,1022,1102,1,38,1001,1102,1,713,1024,1101,0,708,1025,1102,1,22,1006,1101,0,32,1010,1101,476,0,1027,1102,1,516,1029,1102,1,34,1009,1101,0,23,1016,1102,1,37,1011,1102,525,1,1028,1101,0,35,1004,1102,31,1,1002,1102,39,1,1019,1102,28,1,1015,1102,1,1,1021,1101,0,30,1007,1101,0,27,1014,1101,21,0,1018,1101,0,29,1005,1102,26,1,1000,1102,1,0,1020,1101,0,20,1012,1101,33,0,1003,109,13,21108,40,40,6,1005,1019,199,4,187,1106,0,203,1001,64,1,64,1002,64,2,64,109,15,1205,-7,221,4,209,1001,64,1,64,1105,1,221,1002,64,2,64,109,-25,1208,-3,26,63,1005,63,243,4,227,1001,64,1,64,1106,0,243,1002,64,2,64,109,25,2105,1,-5,1001,64,1,64,1106,0,261,4,249,1002,64,2,64,109,-4,21108,41,42,-8,1005,1016,281,1001,64,1,64,1106,0,283,4,267,1002,64,2,64,109,-6,1206,2,301,4,289,1001,64,1,64,1105,1,301,1002,64,2,64,109,-4,21102,42,1,2,1008,1016,42,63,1005,63,323,4,307,1106,0,327,1001,64,1,64,1002,64,2,64,109,-7,2108,35,1,63,1005,63,343,1105,1,349,4,333,1001,64,1,64,1002,64,2,64,109,-13,1208,7,35,63,1005,63,369,1001,64,1,64,1106,0,371,4,355,1002,64,2,64,109,24,21102,43,1,-1,1008,1017,42,63,1005,63,391,1105,1,397,4,377,1001,64,1,64,1002,64,2,64,109,-13,2101,0,-4,63,1008,63,38,63,1005,63,419,4,403,1105,1,423,1001,64,1,64,1002,64,2,64,109,21,1206,-5,435,1106,0,441,4,429,1001,64,1,64,1002,64,2,64,109,-22,21101,44,0,10,1008,1014,44,63,1005,63,463,4,447,1105,1,467,1001,64,1,64,1002,64,2,64,109,25,2106,0,-2,1106,0,485,4,473,1001,64,1,64,1002,64,2,64,109,-19,2107,37,-2,63,1005,63,501,1106,0,507,4,491,1001,64,1,64,1002,64,2,64,109,8,2106,0,10,4,513,1001,64,1,64,1105,1,525,1002,64,2,64,109,-6,21107,45,46,0,1005,1012,547,4,531,1001,64,1,64,1105,1,547,1002,64,2,64,109,-5,1202,-1,1,63,1008,63,21,63,1005,63,567,1105,1,573,4,553,1001,64,1,64,1002,64,2,64,109,2,1207,-3,21,63,1005,63,589,1105,1,595,4,579,1001,64,1,64,1002,64,2,64,109,1,1201,-8,0,63,1008,63,34,63,1005,63,619,1001,64,1,64,1106,0,621,4,601,1002,64,2,64,109,-6,2102,1,-1,63,1008,63,33,63,1005,63,643,4,627,1105,1,647,1001,64,1,64,1002,64,2,64,109,10,21101,46,0,3,1008,1017,43,63,1005,63,667,1106,0,673,4,653,1001,64,1,64,1002,64,2,64,109,-13,2102,1,8,63,1008,63,35,63,1005,63,697,1001,64,1,64,1106,0,699,4,679,1002,64,2,64,109,23,2105,1,0,4,705,1105,1,717,1001,64,1,64,1002,64,2,64,109,-1,1205,-3,729,1106,0,735,4,723,1001,64,1,64,1002,64,2,64,109,-15,2101,0,0,63,1008,63,38,63,1005,63,755,1106,0,761,4,741,1001,64,1,64,1002,64,2,64,109,-2,2107,28,-1,63,1005,63,779,4,767,1106,0,783,1001,64,1,64,1002,64,2,64,109,-2,2108,35,0,63,1005,63,801,4,789,1105,1,805,1001,64,1,64,1002,64,2,64,109,1,1201,-5,0,63,1008,63,26,63,1005,63,831,4,811,1001,64,1,64,1105,1,831,1002,64,2,64,109,-5,1207,5,30,63,1005,63,849,4,837,1106,0,853,1001,64,1,64,1002,64,2,64,109,2,1202,-2,1,63,1008,63,26,63,1005,63,879,4,859,1001,64,1,64,1105,1,879,1002,64,2,64,109,15,21107,47,46,0,1005,1017,899,1001,64,1,64,1105,1,901,4,885,4,64,99,21102,1,27,1,21101,915,0,0,1106,0,922,21201,1,66416,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,942,1,0,1105,1,922,21202,1,1,-1,21201,-2,-3,1,21102,1,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22102,1,-2,-2,109,-3,2105,1,0])
#ic = defaultlist(int, [3,225,1,225,6,6,1100,1,238,225,104,0,2,106,196,224,101,-1157,224,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1002,144,30,224,1001,224,-1710,224,4,224,1002,223,8,223,101,1,224,224,1,224,223,223,101,82,109,224,1001,224,-111,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,10,50,225,1102,48,24,224,1001,224,-1152,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1102,44,89,225,1101,29,74,225,1101,13,59,225,1101,49,60,225,1101,89,71,224,1001,224,-160,224,4,224,1002,223,8,223,1001,224,6,224,1,223,224,223,1101,27,57,225,102,23,114,224,1001,224,-1357,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1001,192,49,224,1001,224,-121,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,1102,81,72,225,1102,12,13,225,1,80,118,224,1001,224,-110,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,677,226,224,102,2,223,223,1005,224,329,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,1108,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,374,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,389,1001,223,1,223,107,677,226,224,1002,223,2,223,1005,224,404,101,1,223,223,8,226,677,224,102,2,223,223,1005,224,419,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,449,1001,223,1,223,107,226,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,7,677,677,224,102,2,223,223,1005,224,509,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,524,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,539,101,1,223,223,1108,677,677,224,102,2,223,223,1005,224,554,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,569,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,584,101,1,223,223,1107,226,226,224,102,2,223,223,1006,224,599,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,614,101,1,223,223,1008,677,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226])
#ic = defaultlist(int, [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
#ic = defaultlist(int, [1102,34915192,34915192,7,4,7,99,0])
#ic = defaultlist(int, [104,1125899906842624,99])

print(intcode([1], ic))
