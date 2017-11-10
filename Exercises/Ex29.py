people = 20
cats = 19
dogs = 21

A = people < cats


if A == True:
    print "We're fecked! Too many cats."

if A != True:
    print "Hooray! There are more people than cats."

B = people < dogs

if B == True:
    print "There are too many dugs!"

if B == False:
    print "Yay! We are safe from the dugs."

print "\nNow if there are more dogs...\n"

dogs += 5

if people >= dogs:
    print "People are greater or equal to doggos!"

if people <= dogs:
    print "People are less than or equal to doggos."

if people == dogs:
    print "People are dogs..."
