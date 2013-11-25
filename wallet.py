# Wallet by Zach Lucas
# 20 Nov 2013
import re
print("Welcome to the wallet app!")
#Array of objects:
array = []
from collections import namedtuple
User = namedtuple("User","name cardnum balance feed")

# Luhn check
def luhn(cardnum):
    sum = 0
    num_digits = len(cardnum)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(cardnum[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )

# Creating a user
def handleUser(username):
	if (len(username) < 4 or len(username) > 15):
		print('username too big or small')
		return
	else:
		if re.match(r'^[A-Za-z0-9_-]+$', username):
			print('Looks good. Adding user: '+username)
			array.append(User(username,"",0,""))
		else:
			print('Username can only contain alphanumerics and dashes and underscores')

# Adding a card to a user
def handleAdd(username,cardnum):
	if (luhn(cardnum) == False):
		print('Invalid card number.')
	else:
		count = 0
		for i in array:
			if i.cardnum == cardnum:
				count+=1
		if (count > 0):
			print('Card is already in use. Fraud!')
		else:
			print('Card is unique. Good.')
			for i,j in enumerate(array):
				if j.name == username:
					tempBalance = j.balance
					tempNote = j.feed
					del array[i]
					array.append(User(username,cardnum,tempBalance,tempNote))
					print(username+'\'s card is added.')
			
# Show balance
def handleBalance(username):
	for i in array:
		if (username == i.name):
			print(username+'\'s balance is: $'+str("{0:.2f}".format(i.balance)))

# Paying user
def handlePayment(actor,target,amount,note):
	if (amount[0]=='$'):
		amount = amount[1:]
	amount = float(amount)
	for count,i in enumerate(array):
		if (i.name == actor):
			if (i.cardnum == ""):
				print(i.name + " does not have a card.")
				return
			else:
				for j,k in enumerate(array):
					if (k.cardnum == ""):
						print(k.name +" does not have a card.")
						return
					if (k.name == target):
						tempBalance = k.balance
						tempCardNum = k.cardnum
						tempName = k.name
						tempNote = k.feed
						del array[j]
						tempBalance += float(amount)
						tempNote += 'You were paid $'+"{0:.2f}".format(amount)+' by '+i.name+' for ' + note + '\r\n'
						array.append(User(tempName,tempCardNum,tempBalance,tempNote))
						print(tempName+' is paid by '+i.name)
						return

# Show a user's feed
def handleFeed(username):
	for i  in array:
		if (i.name == username):
			print(i.feed)

while(1):
	# Get input:
	var = raw_input("> ")
	split = var.partition(" ")
	if (split[0] == 'user'):
		handleUser(split[2])
	elif (split[0] == 'add'):
		split2 = split[2].partition(" ")
		handleAdd(split2[0],split2[2])
	elif (split[0] == 'pay'):
		split2 = split[2].partition(" ")
		split3 = split2[2].partition(" ")
		split4 = split3[2].partition(" ")
		handlePayment(split2[0],split3[0],split4[0],split4[2])
	elif (split[0] == 'feed'):
		handleFeed(split[2])
	elif (split[0] == 'balance'):
		handleBalance(split[2])
	else:
		print('Unrecognized Command') 



