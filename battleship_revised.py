import random #have bot choose randomly from all possibilities of ship orientations
import time
import os
from battlefield_info import n_to_l, l_to_n, possible, letters, bot_data
clear = lambda: os.system('cls')

class Ship():
    def __init__(self, map, name):
        self.map = map
        self.name = name
        self.used = [] #coordinates that the ship is located on
        self.used_copy = [] #used for extracting bordering cells once ship has fallen

    def ship_orientation(self, type):
        if type == 1 or type == 2:
            clear()
            print(f'Current ship ({self.name}): \n{self.map}')
            choice = input('How do you want your ship orientation? Type \'V\' for vertical, \'H\' for horizontal: ')
            choice = choice.upper()
            
            while choice != 'V' and choice != 'H':
                choice = input('Type \'V\' for vertical, \'H\' for horizontal: ')
                choice = choice.upper()                       
        elif type == 3: choice = 'H'
        elif type == 4: choice = 'V'
        
        cell_count = self.map.count('X')
        if choice == 'H':
            self.map = 'X ' * (cell_count-1) + 'X' #account for the extra space
            clear()
            return 'H'
        elif choice == 'V':
            self.map = 'X\n' * (cell_count-1) + 'X' #account for the extra newline
            clear()
            return 'V'

    def ship_location(self, x, y): #tests possibility of placing ships in the specified coordinates
        count = self.map.count('X')
        places = []
        if '\n' not in self.map:
            if y + count-1 > 9:
                return False
            for i in range(count):
                places.append([x, y+i])
                self.used.append(f'{n_to_l[x]}{y+i}')
                self.used_copy.append(f'{n_to_l[x]}{y+i}')
            return places
        else:
            if x + count-1 > 9:
                return False
            for i in range(count):
                places.append([x+i, y])
                self.used.append(f'{n_to_l[x+i]}{y}')
                self.used_copy.append(f'{n_to_l[x+i]}{y}')
            return places

    def border_cells(self): #returns list of all cells bordering the current ship
        coordinates = []
        border = []
        for cell in self.used_copy:
            x = l_to_n[cell[0]]
            y = int(cell[1])
            coordinates.append((x, y))
        
        for x, y in coordinates:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (x+i, y+j) in coordinates or x+i < 0 or y+j < 0:
                        continue
                    border.append((x+i, y+j))    
        return border
                
class Board():
    def __init__(self, player, type):
        self.player = player
        self.type = type

        #initialize grid
        self.grid = [['~' for i in range(10)] for i in range(10)]
        self.temp = [['~' for i in range(10)] for i in range(10)]

        #initialize ships
        self.ship1 = Ship('X X X X', 'Ship One')
        self.ship2 = Ship('X X X', 'Ship Two')
        self.ship3 = Ship('X X X', 'Ship Three')
        self.ship4 = Ship('X X', 'Ship Four')
        self.ship5 = Ship('X X', 'Ship Five')
        self.ship6 = Ship('X X', 'Ship Six')
        self.ship7 = Ship('X', 'Ship Seven')

        self.ships = [self.ship1, self.ship2, self.ship3, self.ship4, self.ship5, self.ship6, self.ship7]

        self.targets = [] #list of cells with a part of a ship on them; database for opposing player's attacks
        self.chosen = [] #list of cells by which self has attacked on opponent's board
        self.used_coords = [] #list of cells for random ship placement

    def placement(self, ship_index):
        clear()
        current_ship = self.ships[ship_index]
        print(f'{self.player}\'s placement')
        self.change_orientation(current_ship)

        self.show_board(1)
        print(f'Current ship ({current_ship.name}):\n{current_ship.map}')

        print('Input the position you want the top left corner of your ship to be in.')
        print('For example, if you want your vertical ship to be {A0, B0, C0}, then type "A0".')
        pos = input('Enter position: ')
        while pos not in possible or self.temp[l_to_n[pos[0]]][int(pos[1])] != '~':
            pos = input('Incorrect input. Enter position: ')
        pos = pos.upper()
        inputs = [i for i in pos]
        inputs[0] = l_to_n[inputs[0]]

        ship_cells = current_ship.ship_location(int(inputs[0]), int(inputs[1]))
        if ship_cells == False:
            self.targets.clear()
            for ship in self.ships:
                ship.used.clear()
                ship.used_copy.clear()
            print('Ship out of range! Restarting placement...')
            time.sleep(3)
            self.temp = [['O' for i in range(8)] for i in range(8)]
            return self.placement(0)
        
        #checks availability for every potential cell in current ship
        for cell in ship_cells:
            if f'{n_to_l[cell[0]]}{cell[1]}' in self.targets or self.temp[cell[0]][cell[1]] != '~':
                self.targets.clear()
                for ship in self.ships:
                    ship.used.clear()
                print('Ship position already taken! Restarting placement...')
                time.sleep(3)
                self.temp = [['~' for i in range(10)] for i in range(10)]
                return self.placement(0)
            
            self.temp[cell[0]][cell[1]] = 'X'


            cell[0] = n_to_l[cell[0]]
            self.targets.append(f'{cell[0]}{cell[1]}')
        
        #account for bordered cells
        bordercells = current_ship.border_cells()
        for x, y in bordercells:           
            try:
                self.temp[x][y] = '_'
            except IndexError:
                continue
        clear()

        if ship_index == len(self.ships)-1:
            self.show_board(1)
            print('These are your selections.')
            time.sleep(3)
            return
        else:
            ship_index += 1
            self.placement(ship_index)

    def change_orientation(self, ship):
        if ship.name == 'Ship Seven':
            return
        print(f'Current ship ({ship.name}):\n{ship.map}')
        change_o = input('Would you like to change your ship orientation? Type \'Y\' for yes, \'N\' for no: ')
        change_o = change_o.upper()
        while change_o != 'Y' and change_o != 'N':
            change_o = input('Incorrect input. Type \'Y\' for yes, \'N\' for no: ')
        while change_o == 'Y':
            ship.ship_orientation(self.type)
            print(f'Current ship ({ship.name}):\n{ship.map}')
            change_o = input('Would you like to change your ship orientation? Type \'Y\' for yes, \'N\' for no: ')
            change_o = change_o.upper()
        clear()

    def bot_placement(self):
        for ship in self.ships:
            state = True
            while state == True:
                ship.ship_orientation(random.choice([3, 4]))
                x = random.randint(0, 7)
                y = random.randint(0, 7)
                ship_cells = ship.ship_location(x, y)

                if ship_cells == False:
                    print('failed')
                    continue
                
                x = True
                for position in ship_cells:
                    if self.temp[position[0]][position[1]] != '~':
                        x = False
                
                if x == False:
                    continue
                
                for position in ship_cells:
                    self.temp[position[0]][position[1]] = 'X'
                    self.targets.append(f'{n_to_l[position[0]]}{position[1]}')

                    bordercells = ship.border_cells()
                    for t in bordercells:
                        try:
                            self.temp[t[0]][t[1]] = '_'
                        except IndexError:
                            continue
                state = False

    def play(self, turn, botpos=None, botupdated=None, botdirection=None, botfailed=None): #0 = same player, 1 = different player ; pos paramter is for bot play
        clear()
        if turn == 1:
            print(f'{self.player}\'s turn')
            #time.sleep(3)
            clear()

        if self.type == 1:
            opponent = p2
        elif self.type == 2:
            opponent = p1
        elif self.type == 4:
            opponent = p3
        
        self.show_board(0)

        pos = input('Choose a position to attack: ')
        while pos not in possible or pos in self.chosen: #checks to see if target cell has already been fired at
            pos = input('Invalid selection. Choose an open position to attack: ')

        self.chosen.append(pos)
        inputs = [i for i in pos]
        inputs[0] = l_to_n[inputs[0]]
        x, y = inputs[0], int(inputs[1])

        if pos in opponent.targets:
            opponent.grid[x][y] = 'X'
            clear()
            self.show_board(0)
            print('Hit!')
            for ship in opponent.ships:
                if pos in ship.used:
                    ship.used.remove(pos)
                if len(ship.used) == 0:
                    print(f'You sunk {ship.name}!')
                    opponent.ships.remove(ship)
                    print(f'{len(opponent.ships)} ship(s) left to go')
                    bordercells = ship.border_cells()
                    print(bordercells)
                    for i, j in bordercells:
                        try:
                            opponent.grid[i][j] = '_'
                        except IndexError:
                            continue
                        self.chosen.append(f'{n_to_l[i]}{j}')
            
            if len(opponent.ships) == 0:
                print(f'{self.player} wins! Good game.')
                return
            time.sleep(2)
            self.play(0, botpos, botupdated, botdirection, botfailed)
        else:
            opponent.grid[x][y] = '_'
            clear()
            self.show_board(0)
            print('Miss!')
            time.sleep(2)
            clear()
            if opponent == p3:
                opponent.bot_play(botpos, botupdated, botdirection, botfailed)
                return
            opponent.play(1)

    def bot_play(self, pos=None, updated=None, direction=None, failed=False):
        self.show_board(0)
        print('The computer is deciding. . .')
        time.sleep(3)

        if failed == True:

            if direction == 'right':
                guess = (pos[0] - 1, pos[1])
                direction = 'left'
            
            elif direction == 'left':
                guess = (pos[0] + 1, pos[1])
                direction = 'right'
            
            elif direction == 'up':
                guess = (pos[0], pos[1] + 1)
                direction = 'down'
                    
            elif direction == 'down':
                guess = (pos[0], pos[1] - 1)
                direction = 'up'
      
        if pos == None: #if there is nothing stored from previous turn
            guess = random.choice(bot_data)
            while p1.grid[guess[0]][guess[1]] != '~':
                bot_data.remove(guess)
                guess = random.choice(bot_data)
      
        elif updated == None: #if previous turn initially found ship 
            possible = {'right': (pos[0] + 1, pos[1]), 'left': (pos[0] - 1, pos[1]), 'up': (pos[0], pos[1] + 1), 'down': (pos[0], pos[1] - 1)}

            guess = random.choice(['right', 'left', 'up', 'down'])
            while possible[guess] not in bot_data:
                guess = random.choice(['right', 'left', 'up', 'down'])

            direction = guess
            guess = possible[direction]

        elif failed == False: #if more than 2 cells of ship is already found, and the direction has not failed yet

            if direction == 'right':
                guess = (updated[0] + 1, updated[1])
                if guess[0] > 9:
                    guess = (pos[0] - 1, pos[1])
                    direction = 'left'

            elif direction == 'left':
                guess = (updated[0] - 1, updated[1])
                if guess[0] < 0:
                    guess = (pos[0] + 1, pos[1])
                    direction = 'right'
            
            elif direction == 'up':
                guess = (updated[0], updated[1] - 1)
                if guess[1] < 0:
                    guess = (pos[0], pos[1] + 1)
                    direction = 'down'
                    
            elif direction == 'down':
                guess = (updated[0], updated[1] + 1)
                if guess[1] > 9:
                    guess = (pos[0], pos[1] - 1)
                    direction = 'up'
        
        if guess in bot_data:
            bot_data.remove(guess)

        x = guess[0]
        y = guess[1]
        target = f'{n_to_l[x]}{y}'

        if target in p1.targets:
            p1.grid[x][y] = 'X'
            clear()
            self.show_board(0)
            print('The computer made a hit!')
            time.sleep(3)
            shipdown = False
            
            for ship in p1.ships:
                if target in ship.used:
                    ship.used.remove(target)
                    #print(ship.name)
                    #print(len(ship.used))
                    #time.sleep(5)
                if len(ship.used) == 0:
                    print(f'The computer sank {ship.name}!')
                    bordercells = ship.border_cells()
                    for x, y in bordercells:           
                        try:
                            p1.grid[x][y] = '_'
                        except IndexError:
                            continue
                    p1.ships.remove(ship)
                    shipdown = True
                    print(f'{len(p1.ships)} ship(s) to go.')
                    time.sleep(3)
                    #guess = None
            
            if len(p1.ships) == 0:
                print(f'The computer wins!')
                return

            if shipdown == True:
                self.bot_play(None, None, None, False)
            elif pos == None:
                self.bot_play(guess, None, None, False)
            else:                
                updated = guess
                self.bot_play(pos, updated, direction, False)
        
        else:
            p1.grid[x][y] = '_'
            clear()
            self.show_board(0)
            print('The computer missed!')
            time.sleep(3)
            clear()
            if pos != None:
                p1.play(1, pos, updated, direction, True) 
            p1.play(1, pos, updated, direction, False)

    def bot_play_draft(self, pos=None):
        self.show_board(0)
        print('The computer is deciding. . .')
        time.sleep(3)
        options = []
        if pos == None:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            while p1.grid[x][y] != '~':
                x = random.randint(0, 7)
                y = random.randint(0, 7)
            options = (x, y)
            cell = f'{n_to_l[x]}{y}'
        else:
            i = l_to_n[pos[0]]
            j = int(pos[1])
            try:
                if self.grid[i][j-1] == '~':
                    options.append((i, j-1))
            except IndexError:
                pass
            try:
                if self.grid[i][j+1] == '~':
                    options.append((i, j+1))
            except IndexError:
                pass
            try:
                if self.grid[i-1][j] == '~':
                    options.append((i-1, j))
            except IndexError:
                pass
            try:
                if self.grid[i+1][j] == '~':
                    options.append((i+1, j))
            except IndexError:
                pass
            options = random.choice(options)
            x = options[0]
            y = options[1]
            cell = f'{n_to_l[x]}{y}'
        
        instance = True
        if cell in p1.targets:
            p1.grid[x][y] = 'X'
            clear()
            self.show_board(0)
            print('The computer made a hit!')
            time.sleep(3)
            for ship in p1.ships:
                if cell in ship.used:
                    ship.used.remove(cell)
                if len(ship.used) == 0:
                    print(f'The computer sank {ship.name}!')
                    p1.ships.remove(ship)
                    print(f'{len(p1.ships)} ship(s) to go.')
                    time.sleep(3)
                    instance = False
            if len(p1.ships) == 0:
                print(f'The computer wins!')
                return
            if instance:
                clear()
                self.bot_play(cell)
            else:
                self.bot_play(None)
        else:            
            p1.grid[x][y] = '_'
            clear()
            self.show_board(0)
            print('The computer missed!')
            time.sleep(2)
            clear()
            p1.play(1)

    def show_board(self, board): #board=0: grid; board=1: temp
        if board == 1:
            count = -1
            for j in self.temp:
                if count == -1:
                    print('  ', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
                count += 1
                print(f'{letters[count]}: {j}')
        
        #define opponent
        else:
            if self.type == 1:
                opponent = p2
            elif self.type == 2:
                opponent = p1
            elif self.type == 3:
                opponent = p1
            elif self.type == 4:
                opponent = p3
            
            count = -1
            for j in opponent.grid:
                if count == -1:
                    print('  ', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
                count += 1
                print(f'{letters[count]}: {j}')
            print(f'{opponent.player}\'s Board')

clear()
print('Welcome to Battleship!\n')

choice = input('Are you playing singleplayer or multiplayer? Type \'s\' or \'m\': ')
while choice != 's' and choice != 'm':
    choice = input('Wrong input. Are you playing singleplayer or multiplayer? Type \'s\' or \'m\': ')

clear()
if choice == 'm':
    name1 = input('Player One, enter your name: ')
    clear()
    name2 = input('Player Two, enter your name: ')
    clear()
    while name2 == name1:
        name2 = input('Please don\'t enter the same name as Player One. Enter your name: ')
    p1 = Board(name1, 1)
    p2 = Board(name2, 2)
    p3 = Board('Computer', 3)
    input_type = input('Player One, type \'m\' to have manual ship positioning, or type \'a\' to have automatic ship positioning: ')
    while input_type != 'm' and input_type != 'a':
        input_type = input('Type \'m\' to have manual ship positioning, or type \'a\' to have automatic ship positioning: ')
    if input_type == 'a':
        p1.bot_placement()
    else:
        p1.placement(0)
    
    input_type = input('Player Two, type \'m\' to have manual ship positioning, or type \'a\' to have automatic ship positioning: ')
    while input_type != 'm' and input_type != 'a':
        input_type = input('Type \'m\' to have manual ship positioning, or type \'a\' to have automatic ship positioning: ')
    if input_type == 'a':
        p2.bot_placement()
    else:
        p2.placement(0)

    p1.play(1)

elif choice == 's':
    name1 = input('Player, enter your name: ')
    name2 = 'Null'
    clear()
    p1 = Board(name1, 4)
    p2 = Board(name2, 2)
    p3 = Board('Computer', 3)
    input_type = input('Player, type \'m\' to have manual ship positioning, or type \'a\' to have automatic ship positioning: ')
    while input_type != 'm' and input_type != 'a':
        input_type = input('Type \'m\' to have manual ship positioning, or type \'a\' to have automatic ship positioning: ')
    if input_type == 'a':
        p1.bot_placement()
    else:
        p1.placement(0)
    
    p3.bot_placement()
    print(p1.targets)
    print(p3.targets)
    input()
    p1.play(1)