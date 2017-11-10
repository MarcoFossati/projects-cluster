def sticks_and_leaves(sticks_count, leaves_count):
    print "There are %d sticks." % sticks_count
    print "There are also %d total leaves." %leaves_count
    print "Some comment!"
    print "Another random comment. \n"

print "We can give the function numbers directly:"
sticks_and_leaves(35.0,51.0)

print "Or, just use variables from the script:"
amount_of_sticks = 32.0
amount_of_leaves = 71.0

sticks_and_leaves(amount_of_sticks, amount_of_leaves)

print "Doing maths too..."
sticks_and_leaves(amount_of_sticks + 10.0, amount_of_leaves + 20)

print "Now you choose how many sticks and leaves there are:"
print "How many sticks do you want?"
sticks_num = int(raw_input("Sticks: "))

print "Okay, so now select how many leaves you would like"
leaves_num = int(raw_input("Leaves: "))

sticks_and_leaves(sticks_num, leaves_num)
