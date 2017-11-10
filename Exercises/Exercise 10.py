tabby_cat = "\tI'm tabbed in."
persian_cat = "I'm Split\non a line."
backslash_cat = "I'm \\ a \\ cat."

fat_cat = """
I'll do a list:
\t* Cat Food
\t* Fishes
\t* Catnip\n\t* Grass
"""

print tabby_cat
print persian_cat
print backslash_cat
print fat_cathui

while True:
    for i in ["/","-","|","\\","|"]:
        print "%s\r" % i,
