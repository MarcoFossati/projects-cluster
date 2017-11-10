i = 0
numbers = []

A = int(raw_input('Count to: '))
B = int(raw_input('By increments of: '))

while i < A:
    print "At the top i is %d" % i
    numbers.append(i)

    i += B
    print "Numbers now: ", numbers

    print "At the bottom i is %d" % i

print "The numbers: "

for num in numbers:
    print num

print "Now using for and lists.."

for i in range(0, A):
    print "At the top i is %d" % i
    print "Numbers now: ", numbers
    print "At the bottom i is %d" % i
