from parseVRP import *


#Testujemy mierzenie odległosci
X = Point()
Y = Point(1, 1)
print(X.Distance(Y))

#Testujemy tworzenie VRP z pliku
a = VRP("okul12D.vrp")
print(a.__dict__)

print("Locations points:")
for ind in a.locations:
	print(str(ind) + ": " + str(a.location_coords[ind]))

print("Depots time windows:")
for ind in a.locations:
	print(str(ind) + ": " + str(a.times[ind]))
	


