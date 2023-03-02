print("Hello-world")
x = 1
if x == 1:
    #is this is how a comment done in py
    print("x is 1")

x=2.0
if x==2:
    print("x is now 2!!")

y= float(3)
if y == 3:
    print("y is 12 too!!!")

myname = 'Bob'
print("My name is "+myname)

mylaptop = "this is Amar's laptop"
print(mylaptop)

xy = x*y
print("xy:"+ str(xy)) 

firstname="Bob"
lastname="Vance"

print("Fullname...."+firstname+" "+lastname)

a,b=5,6
print(a,b)

print("X is %s and Y is %s" % (x,y))
print("a is {} and b is{}".format(a,b))
print(f'{firstname} {lastname}')

#Lists
mylist = []
mylist.append(1)
mylist.append(2.0)
mylist.append("cool")
print(mylist[0])
print(mylist[1])
print(mylist[2])

print("Lets loop that mylist")
for x in mylist:
    print(x)

#Operators
numberOpr= 1+2*3/4   
print("numberOpr..."+str(numberOpr))

remainder=11%3
print("remainder..."+ str(remainder))

## power of!
squared= 7**2
cubed= 6**3

print("squared.....{}".format(squared))
print("Cubed.....%s" % (cubed))

#repeat string so many time
lotsofhellos= "hello " * 10
print(lotsofhellos)

even_numbers=[2,4,6,8]
odd_numbers=[1,3,5,7]
allnumbers=even_numbers+odd_numbers
print(even_numbers)
print(odd_numbers)
print("try sort!")
allnumbers=sorted(allnumbers)
print(allnumbers)

#Array multiplying
print(even_numbers * 3)

#String Formatting

"""
%s - String (or any object with a string representation, like numbers)

%d - Integers

%f - Floating point numbers

%.<number of digits>f - Floating point numbers with a fixed amount of digits to the right of the dot.

%x/%X - Integers in hex representation (lowercase/uppercase)
"""
data = ("John", "Doe", 53.44)
format_string = "Hello %s %s. Your current balance is $%s."

print(format_string % data)

