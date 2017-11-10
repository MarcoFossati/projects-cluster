from sys import exit

def gold_room():
    print "This room is full of gold. How much do you take?"

    next = int(raw_input('> '))
    if next > 50:
        dead("You need to type a number in")
    if next < 50:
        print "Well done, you are a humble being. WINNER!"

def bear_room():
    print "There is a bear here."
    print "The bear has a lot of honey."
    print "The fat bear is in front of a door."
    print "How are you going to get to the door?"
    bear_moved = False

    while True:
        next = raw_input('> ')
        if next == "steal honey":
            dead("The bear doesn't like that... He bits your head off.")
        elif next == "spook bear" and not bear_moved:
            print "The bear is thoroughly spooked. He clears away from the door!"
            bear_moved = True
        elif next == "spook bear" and bear_moved:
            print "The bear is sick of your human games. He breaks your legs, puts them back together, and breaks them again."
        elif next == "open door" and bear_moved:
            gold_room()
        else:
            print "That isn't a great choice..."

def cuth_room():
    print "You see a hot mess."
    print "He eats shit and throws it at people when he is no longer hungry."
    print "Do you run away from the hot mess, or do you try to dodge his steamy shit?"

    next = raw_input('> ')
    if "run away" in next:
        start()
    elif "dodge shit" in next:
        dead("You eat shit...")
    else:
        cuth_room()

def dead(why):
    print why, "What a shame :("
    exit(0)

def start():
    print "You are in a blidingly bright room"
    print "There are doors above and below you"
    print "Which one shall you take?"

    next = raw_input('> ')
    if next == "above":
        bear_room()
    if next == "below":
        cuth_room()
    else:
        dead("You did not select above or below. You remain blinded by the room until your death")

start()