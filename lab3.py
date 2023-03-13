# Name: Keara Polovick
# Computing ID: uzy2ws

import random
import math

file_name= str(input("File name: "))
f = open(file_name, "r")

final = ""
line= f.readlines()
final += str(line)
f.close()



correct= 0

tries= 20

while(tries>0):

	index = random.randint(0, len(final))

	print(final[index - 50: index])

	guess = input("Type a single character: ")

	if(guess== str(final[index+1])):
		correct +=1
	else:
		correct += 0

	tries = tries -1

print("You got " + str(correct) + " out of 20 guesses correct!")
print(math.log((20/correct),2))