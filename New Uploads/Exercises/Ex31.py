import time
print "Welcome..."
time.sleep(1.5)
print "TO THE SHITTY GAME!"
time.sleep(1.5)
print "Please enter your name"
name = raw_input('Name: ')
print "\nAh yes, it is good to meet you young %s." % name
time.sleep(2)
print "\nI am the mighty GRIMWALL! I shall guide you through your short journey today..."
time.sleep(2)
print "Let us begin..."
time.sleep(4)
print "\nYou find yourself locked in a cramped wooden cabin. To your right you see a door. To your left, you see..."
time.sleep(6)
print "ANOTHER DOOR!"
time.sleep(1)
print "Which door would you like to try and open?"
print "1. Left door"
print "2. Right door"
choice1 = raw_input('> ')
if choice1 == "1":
    print "You attempt to open the door, but it appears to be locked BY A MAGICAL CURSE!"
    time.sleep(3)
    print "Yeah, that's right..."
    time.sleep(2)
    print "You roll up your sleeves and cast your mind back to wizardry school. You remember a few spells that may help you out in this situation."
    print "Which spell would you like to try?"
    print "1. Alacazam!\n2.Openus dorius!\n3. Shamwow!"
    choice2 = raw_input('> ')
    if choice2 == "2":
        print "With complete ease you unlock the door and swing it open to reveal a freshly baked fudge cake."
        time.sleep(0.5)
        print "Do you, the mighty %s, devour the cake, or leave it to live out the rest of it's days as a happy cake?" % name
        print "1. Devour\n2. Leave the terrified cake in peace"
        choice3 = raw_input('> ')
        if choice3 == "1":
            print "You monster... The cake thinks of it's family as you consume it whole, never to be seen again."
        elif choice3 == "2":
            print "The fudge cake rewards your kindness with a hearty handshake and a sack of gold coins for your trouble."
        else:
            print "%d wasn't an option there. I will assume you meant to leave the cake be. He thanks you for your troubles with a sack of gold coins."
    else:
        print "Your spell backfires and destroys your very being from the core!"
        time.sleep(1)
        print "You are now a pile of ashes, my dear %s..." % name
if choice1 == "2":
    print "You open the door to reveal a huge bouncy castle!"
    time.sleep(0.2)
    print "What would you like to do?\n1. Enjoy the bouncy castle and have a good time\n2. Pop the bouncy castle and ruin all the potential fun you could have had\n3. Leave this room. Never to return again..."
    choice4 = raw_input('> ')
    if choice4 == "1":
        print "You have a wonderful time until the owner of the cabin comes back and offers you a cup of hot chocolate and a ride back home."
    if choice4 == "2":
        print "It appears you hate fun... The bouncy castle retaliates! With it's last ounch of energy it grapples you and suffocates you to bring you down with it."
    if choice4 == "3":
        print "A tame, but wise choice... Grimwall approves."
    else:
        print "I'm not sure what you meant by %d, Grimwall is easily confused. Here, have a cupcake and a congratulations!"

time.sleep(5)
print "Thank you for playing my little adventure! I hope you had a good time"
time.sleep(2)
print "xoxo"
