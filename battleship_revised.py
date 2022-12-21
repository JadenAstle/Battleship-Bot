import random #have bot choose randomly from all possibilities of ship orientations
import time
import os
from battlefield_info import n_to_l, l_to_n, possible, letters
clear = lambda: os.system('cls')

class Ship():
    def __init__(self, map, name):
        self.map = map
        self.name = name
        self.used = [] #coordinates that the ship is located on

    def ship_orientation(self):
        clear()
        print(f'Current ship ({self.name}): \n{self.map}')
        choice = input('How do you want your ship orientation? Type \'V\' for vertical, \'H\' for horizontal: ')
        choice = choice.upper()
        
        while choice != 'V' and choice != 'H':
            choice = input('Type \'V\' for vertical, \'H\' for horizontal: ')
            choice = choice.upper()
        
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
            if y + count-1 > 7:
                return False
            for i in range(count):
                places.append([x, y+i])
                self.used.append(f'{n_to_l[x]}{y+i}')
            return places
        else:
            if x + count-1 > 7:
                return False
            for i in range(count):
                places.append([x+i, y])
                self.used.append(f'{n_to_l[x+i]}{y}')
            return places

class Board():
    def __init__(self, player, type):
        self.player = player
        self.type = type

        #initialize grid
        self.grid = [['O' for i in range(8)] for i in range(8)]
        self.temp = [['~' for i in range(8)] for i in range(8)]

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
        while pos not in possible:
            pos = input('Incorrect input. Enter position: ')
        pos = pos.upper()
        inputs = [i for i in pos]
        inputs[0] = l_to_n[inputs[0]]

        ship_cells = current_ship.ship_location(int(inputs[0]), int(inputs[1]))
        if ship_cells == False:
            self.targets.clear()
            for ship in self.ships:
                ship.used.clear()
            print('Ship out of range! Restarting placement...')
            time.sleep(3)
            self.temp = [['O' for i in range(8)] for i in range(8)]
            return self.placement(0)
        
        for cell in ship_cells:
            if f'{n_to_l[cell[0]]}{cell[1]}' in self.targets:
                self.targets.clear()
                for ship in self.ships:
                    ship.used.clear()
                print('Ship position already taken! Restarting placement...')
                time.sleep(3)
                self.temp = [['O' for i in range(8)] for i in range(8)]
                return self.placement(0)
            
            self.temp[cell[0]][cell[1]] = 'X'

            cell[0] = n_to_l[cell[0]]
            self.targets.append(f'{cell[0]}{cell[1]}')
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
        print(f'Current ship ({ship.name}):\n{ship.map}')
        change_o = input('Would you like to change your ship orientation? Type \'Y\' for yes, \'N\' for no: ')
        change_o = change_o.upper()
        while change_o != 'Y' and change_o != 'N':
            change_o = input('Incorrect input. Type \'Y\' for yes, \'N\' for no: ')
        while change_o == 'Y':
            ship.ship_orientation()
            print(f'Current ship ({ship.name}):\n{ship.map}')
            change_o = input('Would you like to change your ship orientation? Type \'Y\' for yes, \'N\' for no: ')
            change_o = change_o.upper()
        clear()

    def bot_placement(self):
        pass

    def play(self, turn): #0 = same player, 1 = different player
        clear()
        if turn == 1:
            print(f'{self.player}\'s turn')
            time.sleep(3)
            clear()

        if self.type == 1:
            opponent = p2
        elif self.type == 2:
            opponent = p1
        
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
            if len(opponent.ships) == 0:
                print(f'{self.player} wins! Good game.')
                return
            time.sleep(2)
            self.play(0)
        else:
            opponent.grid[x][y] = '_'
            clear()
            self.show_board(0)
            print('Miss!')
            time.sleep(2)
            clear()
            opponent.play(1)

    def bot_play(self):
        pass

    def show_board(self, board): #board=0: grid; board=1: temp
        #define opponent
        if board == 1:
            count = -1
            for j in self.temp:
                if count == -1:
                    print('  ', ['0', '1', '2', '3', '4', '5', '6', '7'])
                count += 1
                print(f'{letters[count]}: {j}')
        else:
            if self.type == 1:
                opponent = p2
            elif self.type == 2:
                opponent = p1
            
            count = -1
            for j in opponent.grid:
                if count == -1:
                    print('  ', ['0', '1', '2', '3', '4', '5', '6', '7'])
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
    p1.placement(0)
    p2.placement(0)
    p1.play(1)