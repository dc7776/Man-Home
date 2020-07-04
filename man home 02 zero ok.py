from random import randrange
from os import system
from getch import getch
#from textwrap import wrap
#from pprint import pprint

#TODO===
#more than 2 players
#move to own man = casualty?
#zero ok. negative = lose man

class player :
	def __init__(self) :
		self.home = 0
		self.casualties = 0
		self.men = []
	
player1 = player() 
player2 = player()

#difficulty parameters
max_men = 4
home_win = 3
casualties_lose = 12

turndie = ['new man', 'add one', 'subtract one', 'move by factor', 'move by factor', 'move by factor']

current = player1
opponent = player2
playing = True

#prime generator by division
def pgdiv(z) :
	q=[2]
	yield 2
	x=3
	
	while x<=z :
		for p in q :
			if x%p==0 : break
			if p>x**.5 : 
				yield x
				if x<=z**.5 : q.append(x)
				break
		else : yield x
		x+=1

def factor(z) :
	for x in pgdiv(z) :
		if z%x==0 :
			c=0
			while z%x==0 : 
				c+=1
				z//=x
			yield x #print(x,'^',c)
		if z==1 : break
		if x>=z**.5 :
			yield z #print(z,'^',1)
			break
	#print('\n')

#intro screen
intro = f'''        ---Home Run---
Object of the game: Be the first player to get {home_win} men home (One), without losing {casualties_lose} men on the way.

The maximum number of men you can have is {max_men}. If exceeded, you must sacrifice a man, which results in a casualty.
 
If the other player lands on a number you occupy, you will lose your man, resulting in a casualty.
 
Game play and movement on the number line is determined by a roll of the die. The 6 sides of the die are:
- new man
- add one
- subtract one
- move by a factor
- move by a factor
- move by a factor

Half of the time, you will be moving by a factor of the number your man is on. So, it is a good idea to move your men to numbers with multiple factors. One is Home. Only positive integers are allowed.

A new man is decided by rolling two 10-sided dice for a random positive integer from 0 to 99. There is also a 1% chance of rolling a One, which is an instant Man Home. Landing on an already-occupied space will kill your opponent there; if it is your own man, you will forfeit your new man.

Press any key to start'''

#FAILED TEXTWRAP
#intro = wrap(intro, width=28, replace_whitespace=True)
#for line in intro: print(line)

print(intro)
getch()

while playing :
	system('clear')
	print('       ---Home Run---')
	print(f'Player 1 ', end='')
	if current == player1 : print('*Your Turn*')
	else : print('')
	print(f'Men: {player1.men}\n   Home: {player1.home}   Casualties: {player1.casualties}')
	print(f'Player 2 ', end='')
	if current == player2 : print('*Your Turn*')
	else : print('')
	print(f'Men: {player2.men}\n   Home: {player2.home}   Casualties: {player2.casualties}\n')
	
	#roll the die, unless you have no men
	if len(current.men) == 0 : roll = 'new man'
	else : roll = turndie[randrange(6)]
	print(f'You rolled: {roll}\n')
	
	if roll == 'new man' :
		if len(current.men) >= max_men :
			while 1 :
				man = int(input(f'The maximum men allowed is {max_men}. You must sacrifice a man to continue: '))
				if man in current.men :
					current.men.pop(current.men.index(man))
					current.casualties += 1
					print(f'{man} was sacrificed')
					break
				else : continue
		else : #go ahead with new man roll
			new = randrange(100)
			print(f'New man roll: {new}')
			#if new == 0 :
				#print('Zero is off-limits\nNew man dead\n')
				#current.casualties += 1
			if new == 1 :
				print('Man home!')
				current.home += 1
			elif new in current.men :
				print(f'You already have a man on {new}')
				print('You lose your turn')
			elif new in opponent.men :
				print(f"Take opponent's man at {new}")
				opponent.men.pop(opponent.men.index(new))
				opponent.casualties += 1
				current.men.append(new)
			else :
				current.men.append(new)
				print(f"New man on {new}")
	
	elif roll == 'add one' :
		#pick a man, if more than one
		if len(current.men) == 1 :
			pos = current.men[0]
		else :
			while 1 :
				pos = int(input('Pick a man: '))
				if pos in current.men : break
				else : continue
		new = pos + 1
		if new in current.men :
			print(f'You already have a man on {new}')
			print('You lose your turn')
		elif new in opponent.men :
			print(f"Take opponent's man at {new}")
			opponent.men.pop(opponent.men.index(new))
			opponent.casualties += 1
			current.men[current.men.index(pos)] = new
		elif new == 1 :
			print('Man home!')
			current.men.pop(current.men.index(pos))
			current.home += 1
		else :
			current.men[current.men.index(pos)] = new
			print(f"Moved man from {pos} to {new}")
			
	elif roll == 'subtract one' :
		#pick a man, if more than one
		if len(current.men) == 1 :
			pos = current.men[0]
		else :
			while 1 :
				pos = int(input('Pick a man: '))
				if pos in current.men : break
				else : continue
		new = pos - 1
		if new < 0 :
			print('Casualty! Negative numbers\n are off-limits.\n')
			current.men.pop(current.men.index(pos))
			current.casualties += 1
		elif new in current.men :
			print(f'You already have a man on {new}')
			print('You lose your turn')
		elif new in opponent.men :
			print(f"Take opponent's man at {new}")
			opponent.men.pop(opponent.men.index(new))
			opponent.casualties += 1
			current.men[current.men.index(pos)] = new
		elif new == 1 :
			print('Man home!')
			current.men.pop(current.men.index(pos))
			current.home += 1
		else :
			current.men[current.men.index(pos)] = new
			print(f"Moved man from {pos} to {new}")

	elif roll == 'move by factor' :
		#pick a man, if more than one
		if len(current.men) == 1 :
			pos = current.men[0]
		else :
			while 1 :
				pos = int(input('Pick a man: '))
				if pos in current.men : break
				else : continue
		while 1 :
			new = int(input(f'Move {pos} to? '))
			diff = abs(new - pos)
			if pos == 0 :
				max1 = max(player1.men)
				max2 = max(player2.men)
				m = max([max1, max2])
				factors = [f for f in pgdiv(m)]
			else: factors = [f for f in factor(pos)]
			if diff in factors:
				break
			else : 
				print('Factors =', factors)
				continue
		if new in current.men :
			print(f'You already have a man on {new}')
			print('You lose your turn')
		elif new in opponent.men :
			print(f"Take opponent's man at {new}")
			opponent.men.pop(opponent.men.index(new))
			opponent.casualties += 1
			current.men[current.men.index(pos)] = new
		else :
			current.men[current.men.index(pos)] = new
			print(f"Moved man from {pos} to {new}")
	
	#win or lose	
	if player1.home >= home_win :
		print(f'\nGame Over\nPlayer 1 got {home_win} men home 1st!')
		break
	if player2.home >= home_win :
		print(f'\nGame Over\nPlayer 2 got {home_win} men home 1st!')
		break
	if player1.casualties >= casualties_lose :
		print(f'\nGame Over\nPlayer 1 lost {casualties_lose} men 1st!')
		break
	if player2.casualties >= casualties_lose :
		print(f'\nGame Over\nPlayer 2 lost {casualties_lose} men 1st!')
		break
	
	player1.men.sort()
	player2.men.sort()
	
	#next player
	current, opponent = opponent, current
	getch()
		



