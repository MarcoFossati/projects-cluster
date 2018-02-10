def add(a, b):
    print "Add is %d + %d" % (a, b)
    return a + b

def subtract(a, b):
    print "Subract is %d - %d" % (a, b)
    return a - b

def multiply(a, b):
    print "Multiply is %d * %d" % (a, b)
    return a * b

def divide(a, b):
    print "Divide is %d / %d" % (a, b)
    return a / b

print "Let's do some maths with functions"

age = add(12, 8)
height = subtract(210, 33)
weight = multiply(16, 4)
IQ = divide(200, 10)

print "Age: %d\nHeight: %d\nWeight: %d\nIQ: %d" %(age, height, weight, IQ)

print "\nHere is a puzzle."

what = add(age, subtract(height, divide(weight, multiply(IQ, 2))))

print "\nThat is:", what, "Did you manage it by hand?"
