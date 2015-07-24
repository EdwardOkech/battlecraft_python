# implementation of battlecraft using python
# Todo....implement using classess


import random

# Builds a 2D square gameboard of the desired size
def make_grid (grid_size):	
	grid =[]
	for x in range(grid_size):
		grid.append([])
		for y in range(grid_size):
			grid[x].append('x')
	return grid

# Takes a 2D game board of any size randomly selects an 'x'
def rand_point (grid):
	while 1:
		possible_coords = []
		count = 0
		for x in range(len(grid)):
			count += 1
			possible_coords.append(count)
		random.shuffle(possible_coords)
		x = possible_coords[0] - 1
		random.shuffle(possible_coords)
		y = possible_coords[0] - 1
		if grid[y][x] == 'x': 				#Selects a point that is not occupied
			break
		else:
			continue
	return (x, y)						#format 0-9,0-9

# Prints the grid to the screen in human readable form
def paint_grid (grid):
	count = 0
	for x in range(len(grid)):
		for x in grid[count]:
			print x,
		print ""
		count += 1

# Used when drawing boats, prevents boats from overlaping
def check_points (grid, points_list):
	for point in points_list:
		if grid[point[1]][point[0]] != 'x':
			return False
	return True


def make_boat (grid, length):							
	while 1:
		#Randomly decide boat orientation
		pos_orient = ['v','h']
		random.shuffle(pos_orient)
		orient = pos_orient[0]	
		#Get a random starting point for a new boat
		start_point = rand_point(grid)
		x = start_point[0]
		y = start_point[1]
		#List of all current boats points
		point_list = [(x,y)]		
		count = 0
		#Randomly decides whether to build boat from start-right or start-left
		#Changes random decision if it conflicts with the edge of the board
		if orient == 'h':				 
			pos_directions = ['l','r']
			random.shuffle(pos_directions)
			direction = pos_directions[0]
			if direction == 'r' and x + 1 + length > len(grid):
				direction = 'l' 		
			elif direction == 'l' and x - length < 0:
				direction = 'r'
		#Same as above but for vertical boats
		elif orient == 'v':				
			pos_directions = ['u','d']
			random.shuffle(pos_directions)
			direction = pos_directions[0]
			if direction == 'd' and y + 1 + length > len(grid):	
				direction = 'u'	
			elif direction == 'u' and y - length < 0:
				direction = 'd'
		#These four blocks generate the correct number of points 
		#for the curent boat, 
		if direction == 'l':
			for num in range(length - 1):
				count += 1
				point_list.append((x-count,y))
		if direction == 'r':
			for num in range(length - 1):
				count += 1
				point_list.append((x+count,y))
		if direction == 'u':
			for num in range(length - 1):
				count +=1
				point_list.append((x,y-count))
		if direction == 'd':
			for num in range(length - 1):
				count +=1
				point_list.append((x,y+count))
		#Rebuild the boat if it crosses another boat
		if check_points(grid, point_list) == False:
			continue
		else:
			break
	#Writes 'b's for each point of this boat to the computers game board
	for point in point_list:
		grid[point[1]][point[0]] = 'b'		
	
	return point_list		
	
#Computer game board and variables
grid = make_grid(10)		
scout = make_boat(grid, 3)
patrol = make_boat(grid, 2)
battleship = make_boat(grid, 4)
carrier = make_boat(grid, 5)
hit_list = scout + patrol + battleship + carrier

#User game board and variables
user_grid = make_grid(len(grid))
hits = []
scout_hits = []
patrol_hits = []
battleship_hits = []
carrier_hits = []
moves = 0
	
while 1:	
	moves += 1
	#Paint the users grid
	paint_grid(user_grid)
	print ""
	#Cheaters uncomment below
	paint_grid(grid)
	
	#Get coordinates from user
	while 1:
		try:
			coordx = int(raw_input('Enter an x coordinate from 1 to ' + str(len(grid)) + '\n' ))
		except ValueError:
			continue
		if coordx > 0 and coordx < 11: break
	while 1: 
		try:
			coordy = int(raw_input('Enter a y coordinate from 1 to ' + str(len(grid)) + '\n' ))
		except ValueError:
			continue
		if coordy > 0 and coordy < 11: break
	
	#Convert user perspective of x and y dimensions to a format compatible with the grid-list-matrix	
	user_point = (coordx - 1, len(grid) - coordy)
	userx = user_point[0]
	usery = user_point[1]
	
	#Prints user moves to the screen 
	if user_point in hit_list:
		user_grid[usery][userx] = 'h'
	else:
		user_grid[usery][userx] = 'm'	
		
	#Following blocks keep track of user hits on speciffic boats
	#if a hit occurs a message is displayed telling the user the boat type
	#**consider implimenting a boat class to reduce text and allow easy
	#change of boat roster**
	if user_point in scout:
		print "Scout Hit!"
		count = 0
		for point in scout:
			if scout[count] == user_point and user_point not in scout_hits:
				scout_hits.append(scout[count])
			count += 1
		if len(scout) == len(scout_hits):
			print "Scout Sunk!"

	elif user_point in patrol:
		print "Patrol Boat Hit!"
		count = 0
		for point in patrol:
			if patrol[count] == user_point and user_point not in patrol_hits:
				patrol_hits.append(patrol[count])
			count += 1
		if len(patrol) == len(patrol_hits):
			print "Patrol boat Sunk!"
 
	elif user_point in battleship:
		print "Battleship Hit!"
		count = 0
		for point in battleship:
			if battleship[count] == user_point and user_point not in battleship_hits:
				battleship_hits.append(battleship[count])
			count +=1
		if len(battleship) == len(battleship_hits):
			print "Battleship Sunk!"
	
	elif user_point in carrier:
		print "Carrier Hit!"
		count  = 0
		for point in carrier:
			if carrier[count] == user_point and user_point not in carrier_hits:
				carrier_hits.append(carrier[count])
			count += 1
		if len(carrier) == len(carrier_hits):
			print "Carrier Sunk!"
	
	else:	
		#If no boats are hit then a miss message is displayed
		#**Consider moving to block that writes user moves to the screen**
		print "Miss: No boats were hit"
		
	
	#Adds each hit to the users hit list
	count = 0
	for point in hit_list:
		if hit_list[count] == user_point and user_point not in hits:
			hits.append(hit_list[count])
		count += 1 	
	#Compares the user and computer hit lists
	#If the user has hit all targets possible the game ends
	if len(hit_list) == len(hits):
		print "You Win!!"
		print "Your score(lower = better): " + str(moves)
		break


