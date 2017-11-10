people = 30
cars = 40
buses = 15

if cars > people:
    print "We should take the cars."
if cars < people:
    print "We should NOT take the cars."
else:
    print "We don't know what to do..."

if buses > cars:
    print "That's too many buses."
if buses < cars:
    print "Maybe we could take the bus."
else:
    print "We still can't choose."

if people > buses:
    print "Okay, let's take the bus."
else:
    print "Fuck it. Let's stay at home..."
