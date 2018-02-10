from sys import argv

script, user_name = argv
prompt = "-->> "

print "Hello %s, I'm the %s script" % (user_name, script)
print "I'd like to ask you a few questions."
print "Do you like me, %s?" % user_name
likes = raw_input(prompt)

print "Where do you live %s?" % user_name
lives = raw_input(prompt)

print "What brand of computer do you have?"
comp = raw_input(prompt)

print """Alright, so you said %s about liking me
You live in %r. That's a rather nice place...
And you have a %s computer. Very nice indeed""" % (likes, lives, comp)
