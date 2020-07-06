from random import randrange
from os import system
from getch import getch
import re

#TODO===
#wrap text
#more than 2 players
#sound effects

#difficulty parameter defaults
MAX_MEN = 4
HOME_WIN = 3
CASUALTIES_LOSE = 12

turndie = ['new man', 'add one', 'subtract one', 'move by factor', 'move by factor', 'move by factor']

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




while 1 : #main loop
	class player :
		def __init__(self) :
			self.home = 0
			self.casualties = 0
			self.men = []
		
	player1 = player() 
	player2 = player()
		
	current = player1
	opponent = player2
	playing = True
	
	#settings page
	while 1 :
		settings_page = f'''       ---Man Home---
	
    Difficulty Parameters

[M]ax Men = {MAX_MEN}
[H]ome Win = {HOME_WIN}
[C]asualties Lose = {CASUALTIES_LOSE}

[R]ules
[Any other key] to Play!
'''
		system('clear')
		print(settings_page)
		c = getch()
		if c in ['m', 'M'] :
			n = input('Enter new Max Men\n4 is the default: ')
			n = re.findall('[0-9]', n)
			n = ''.join(n)
			if n == '' : n = 4
			else : n = int(n)
			MAX_MEN = n
		elif c in ['h', 'H'] :
			n = input('Enter new Home Win\n3 is the default: ')
			n = re.findall('[0-9]', n)
			n = ''.join(n)
			if n == '' : n = 3
			else : n = int(n)
			HOME_WIN = n
		elif c in ['c', 'C'] :
			n = input('Enter new Casualties Lose\n12 is the default: ')
			n = re.findall('[0-9]', n)
			n = ''.join(n)
			if n == '' : n = 12
			else : n = int(n)
			CASUALTIES_LOSE = n
		elif c == 'r' :
			system('clear')
			rules = f'''        ---Man Home---

Object of the game: Be the first player to get {HOME_WIN} men home (One), without losing {CASUALTIES_LOSE} men on the way.

The maximum number of men you can have is {MAX_MEN}. If exceeded, you must sacrifice a man.

Only one man can occupy the same number. You can kill your opponent by moving to a number they occupy.
 
Game play and movement on the number line is determined by a roll of the die. The 6 sides of the die are:
- new man
- add one
- subtract one
- move by a factor
- move by a factor
- move by a factor

Half of the time, you will be moving by a factor. So, it is a good idea to move your men to numbers with multiple factors. You may add or subtract by any factor of the number you occupy.

One is Home. Only positive integers are allowed. Zero is allowed, but it is the only place where a man can die from attempting to go negative with a roll of "subtract one". At Zero anyone on a prime number can take you. Likewise, from Zero you can move to or take any man on a prime number.

A new man is decided by rolling two 10-sided dice for a random positive integer from 0 to 99. There is also a 1% chance of rolling a One, which is an instant Man Home!

Press any key

'''
			print(rules)
			getch()
		else : break
	
	#game loop
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

		#win or lose	
		if player1.home >= HOME_WIN :
			print(f'\nGame Over\nPlayer 1 wins!\nPlayer 1 got {HOME_WIN} men home')
			getch()
			break
		if player2.home >= HOME_WIN :
			print(f'\nGame Over\nPlayer 2 wins!\nPlayer 2 got {HOME_WIN} men home')
			getch()
			break
		if player1.casualties >= CASUALTIES_LOSE :
			print(f'\nGame Over\nPlayer 2 wins!\nPlayer 1 lost {CASUALTIES_LOSE} men')
			getch()
			break
		if player2.casualties >= CASUALTIES_LOSE :
			print(f'\nGame Over\nPlayer 1 wins!\nPlayer 2 lost {CASUALTIES_LOSE} men')
			getch()
			break
		
		
		#roll the die, unless you have no men
		if len(current.men) == 0 : roll = 'new man'
		else : roll = turndie[randrange(6)]
		print(f'You rolled: {roll}\n')
		
		if roll == 'new man' :
			if len(current.men) >= MAX_MEN :
				while 1 :
					man = input(f'The maximum men allowed is {MAX_MEN}.\nYou must sacrifice a man to\ncontinue: ')
					man = re.findall('[0-9]', man)
					man = ''.join(man)
					if man == '' : man = 0
					else : man = int(man)
					if man in current.men :
						current.men.pop(current.men.index(man))
						current.casualties += 1
						print(f'{man} was sacrificed')
						break
					else : continue
			else : #go ahead with new man roll
				new = randrange(100)
				print(f'New man roll: {new}')
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
					pos = input('Pick a man: ')
					pos = re.findall('[0-9]', pos)
					pos = ''.join(pos)
					if pos == '' : pos = 0
					else : pos = int(pos)
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
					pos = input('Pick a man: ')
					pos = re.findall('[0-9]', pos)
					pos = ''.join(pos)
					if pos == '' : pos = 0
					else : pos = int(pos)
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
					pos = input('Pick a man: ')
					pos = re.findall('[0-9]', pos)
					pos = ''.join(pos)
					if pos == '' : pos = 0
					else: pos = int(pos)
					if pos in current.men : break
					else : continue
			while 1 :
				new = input(f'Move {pos} to? ')
				new = re.findall('[0-9]', new)
				new = ''.join(new)
				if new == '' : new = 0
				else : new = int(new)
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
		
		player1.men.sort()
		player2.men.sort()
		
		#next player
		current, opponent = opponent, current
		getch()
			



