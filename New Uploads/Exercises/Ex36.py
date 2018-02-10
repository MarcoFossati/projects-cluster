list = "Apples Oranges Cats Dogs Buildings Cows"

print "There is a list of then things:\n",list
print "\nWait... that isn't ten things. Let's fix that\n"

stuff = list.split(' ')

more = "Bottles Cups Shoes Doors Lions Sharks Gnomes"

more_stuff = more.split(' ')

while len(stuff) != 10:
    add = more_stuff.pop()
    print "Adding:", add
    stuff.append(add)
    print "There are %d items now." % len(stuff)

print "Here the items are in a list format:", stuff

print "There are some things we can do with the list."

print stuff[1]
print stuff[-2]
print ' '.join(stuff)
extra = ' '.join(more_stuff)
print "Here is what is left in the overflow list:", extra
