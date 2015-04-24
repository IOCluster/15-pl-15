from parseVRP import *


#Testujemy mierzenie odległosci
X = Point()
Y = Point(1, 1)
print(X.Distance(Y))

#Testujemy tworzenie VRP z tekstu
text = open("okul12D.vrp").read()
a = VRP(text)

print("Locations points:")
for ind in a.locations:
	print(str(ind) + ": " + str(a.location_coords[ind]))

print("Depots time windows:")
for ind in a.locations:
	print(str(ind) + ": " + str(a.times[ind]))
	
#Testujemy tworzenie VRP z pliku
print('\n')
a = VRP.CreateFromFile("okul12D.vrp")
print(a.__dict__)

#Testujemy zamiane VRP na tekst
print("\n\n")
print(a)

#Testujemy kompatybilnosc
print("\n\n")
text1 = str(a).split("\n")
text2 = str(VRP(str(a))).split("\n")

for i in range( len(text1) ):
        print(text1[i] + text2[i].rjust(30))

