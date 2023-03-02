def mysplit(strng):
    return strng.split()


def myapp():
    print(mysplit("To be or not to be, that is the question"))
    print(mysplit("To be or not to be,that is the question"))
    print(mysplit("   "))
    print(mysplit(" abc "))
    print(mysplit(""))
    
def stringNumber():
    print('10' == '010')
    print('10' > '010')
    print('10' > '8')
    print('20' < '8')
    print('20' < '80')

stringNumber()