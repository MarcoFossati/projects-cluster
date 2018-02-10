import time

def squr_rt(z):
    print "take square root of %r" % z
    return round(z**0.5, 3)

def prcnt(x):
    print "taking 42%% of %r" % x
    return round(x * 0.42, 3)

def multiply(y, j):
    print "multiplying %r and %r together" % (y, j)
    return round(y * j, 3)

result1 = squr_rt(59.0)
result2 = prcnt(93.0)
result3 = multiply(6.0, 19.0)

print "Square root answer: %r\nPercentage answer: %r\nMultiplication answer: %r" % (result1, result2, result3)

print "More complex functions are as follows:"

result4 = squr_rt(multiply(prcnt(39),2))

print "Which is then: %r" % result4

print "Time to enter your own variables..."

time.sleep(2)

print "Choose a value to for the square root of"
raw_value = float(raw_input('> '))

result5 = squr_rt(raw_value)

print "Which ends up being: %r" % result5