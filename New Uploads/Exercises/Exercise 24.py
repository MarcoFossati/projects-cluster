print "Let's practice everything covered."
print "I will need to know about \"escape sequences\" with \\ that do \nnew lines and\ttabs."

poem = """\tThe lovely world
with logic so firmly planting
cannot discern\nthe needs for love
nor comprehend passion from institution
and requires an explanation
\n\ttwhere there is none."""

print "-" * 40
print poem
print "-" * 40

five = 10 - 2 + 3 - 6
print "This should be five: %s" % five

def secret_formula(variable):
    one = variable * 500
    two = one / 1000
    three = two /1000
    return one, two, three

start_point = 10000
beans, jars, crates = secret_formula(start_point)

print "With a starting point of: %d" % start_point
print "We'd have %d beans, %d jars, and %d crates." % (beans, jars, crates)

start_point =start_point / 10

print "We can also do it this way (with lower values this time)"
print "We'd have %d beans, %d jars, and %d crates." % secret_formula(start_point)