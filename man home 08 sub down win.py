from random import randrange
from os import system
from msvcrt import getwch
import re

#TODO===
#wrap text
#more than 2 players
#sound effects
#GUI

#difficulty parameter defaults
MAX_MEN = 5
NEW_RANGE = 60
HOME_WIN = 3
CASUALTIES_LOSE = 12

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
	
    Main Menu

[N]ew Man Range = {NEW_RANGE}
[R]ules
[Any other key] to Play!
'''
		system('cls')
		print(settings_page)
		c = getwch()
		if c in ['n', 'N'] :
			n = input('Easy -> Hard = 15 -> 150\nWhen rolling for a new man,\nthe range will be 0 to: ')
			n = re.findall('[0-9]', n)
			n = ''.join(n)
			if n == '' : n = NEW_RANGE
			else : n = int(n)
			if n < 15 : n = 15
			if n > 150 : n = 150
			NEW_RANGE = n
		elif c in ['r', 'R'] :
			system('cls')
			rules = f'''        ---Man Home---

Object of the game: "Home" is "1". Be the first player to get {HOME_WIN} men home, without losing {CASUALTIES_LOSE} men on the way.

You must subtract by any factor of the number your man is standing on. Alternatively, you can always subtract one. Zero is off-limits, so subtracting one is the only option for a man on a prime number.

Only one man can occupy the same number. You can kill your opponent by moving to a number they occupy. You cannot kill your own men. If your own men are in your way, you simply lose your turn.

Play begins with the roll of a six-sided die, which determines which man you must move. If you roll "1", you must move your 1st, or lowest-numbered man. Rolling a "2" means you must move your 2nd lowest-numbered man, and so on. If you roll a number larger than you man roster, you recieve a random new man.

A new man is decided by generating a random number from 1 to {NEW_RANGE}. There is a small chance of rolling a "1", which is an instant Man Home! The maximum range can be set in the main settings page. The larger you set this variable, the more difficult the game.

Press any key to return to the main menu...

'''
			print(rules)
			getwch()
		else : break
	
	#game loop
	while playing :
		system('cls')
		print('       ---Man Home---\n')
		if current == player1 : print('PLAYER 1  *Your Turn*')
		else : print('Player 1')
		print(f'Men: {player1.men}\n   Home: {player1.home}   Casualties: {player1.casualties}')
		if current == player2 : print('PLAYER 2  *Your Turn*')
		else : print('Player 2')
		print(f'Men: {player2.men}\n   Home: {player2.home}   Casualties: {player2.casualties}\n')

		#win or lose	
		if player1.home >= HOME_WIN :
			print(f'\nGame Over\nPlayer 1 wins!\nPlayer 1 got {HOME_WIN} men home')
			getwch()
			break
		if player2.home >= HOME_WIN :
			print(f'\nGame Over\nPlayer 2 wins!\nPlayer 2 got {HOME_WIN} men home')
			getwch()
			break
		if player1.casualties >= CASUALTIES_LOSE :
			print(f'\nGame Over\nPlayer 2 wins!\nPlayer 1 lost {CASUALTIES_LOSE} men')
			getwch()
			break
		if player2.casualties >= CASUALTIES_LOSE :
			print(f'\nGame Over\nPlayer 1 wins!\nPlayer 2 lost {CASUALTIES_LOSE} men')
			getwch()
			break
		
		#roll dice for man to move
		roll = randrange(1,7)
		print(f'Roll: {roll}')
	
		if roll > len(current.men) : 
			new = randrange(1, NEW_RANGE + 1)
			print(f'New man on: {new}')
			if new == 1 :
				print('Man home!')
				current.home += 1
			elif new in current.men :
				print(f'You already have a man on {new}')
				print('Forfeit turn')
			elif new in opponent.men :
				print(f"Take opponent's man at {new}")
				opponent.men.pop(opponent.men.index(new))
				opponent.casualties += 1
				current.men.append(new)
			else :
				current.men.append(new)
				
		else:
			pos = current.men[roll-1]
			factors = [f for f in factor(pos)]
			while 1 :
				if len(factors) == 1 and pos-factors[0] == 0 :
					new = pos-1
					print('Prime~ Can only move 1')
					print(f'Moved {pos} to {new}')
					break
				else :
					new = input(f'Move {pos} to? ')
					new = re.findall('[0-9]', new)
					new = ''.join(new)
					if new == '' : new = 0
					else : new = int(new)
				diff = pos - new
				if diff in factors or diff == 1 :
					break
				else : 
					print('Factors =', factors)
					continue
			if new == 1 :
				print('Man home!')
				current.men.remove(pos)
				current.home += 1
			elif new in current.men :
				print(f'You already have a man on {new}')
				print('Forfeit turn')
			elif new in opponent.men :
				print(f"Take opponent's man at {new}")
				opponent.men.pop(opponent.men.index(new))
				opponent.casualties += 1
				current.men[current.men.index(pos)] = new
			else :
				current.men[current.men.index(pos)] = new
		
		player1.men.sort()
		player2.men.sort()
		
		#next player
		current, opponent = opponent, current
		
		print('\nnext player...')
		print('or [A]bort')
		c = getwch()
		#abort back to settings
		if c in ['a', 'A'] : break



