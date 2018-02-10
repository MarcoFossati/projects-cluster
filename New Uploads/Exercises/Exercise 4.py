cars=100.0 #this is the total number of cars available
space_in_a_car=4.0 #this is the total number of seats in each car
drivers=30.0 #this is the total number of drivers
passengers=90.0 #this is the total number of people that need to be transported
cars_not_driven=cars-drivers
cars_driven=drivers
carpool_capacity=cars_driven*space_in_a_car
average_passengers_per_car=passengers/cars_driven
print "there are",cars,"cars available"
print "there are only",drivers,"drivers available"
print "there will be",cars_not_driven,"empty cars today"
print "we can transport",carpool_capacity,"people today"
print "we have",passengers,"to transport today"
print "we need to put exactly",average_passengers_per_car,"passengers in each car"
print "Are there exactly 100 available seats today?",100==carpool_capacity
