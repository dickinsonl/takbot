# Credit for parser goes to:
# https://github.com/Abyssal-Tak/2TPS
#
# Minor changes have been made from the original code
import re
from math import ceil


# file = input('Name of the PTN file that you would like to parse?\n')
# # file = 'fwwwwibib vs Gerrek 2016.08.12.ptn'
# try:
#     #plyNumber = set(input('At how many plys would you like the TPS to be printed?\n'))
#     s = input('At how many plys would you like the TPS to be printed?\n')
#     plyNumber = set(map(int, s.split(',')))
# except ValueError:
#     print("Invalid input! Defaulting to end of game position...")
#     plyNumber = {1000}



class Error(Exception):
    """Base Error Class"""
    pass

class SizeError(Error):
    """Supported board sizes will be 5x5, 6x6"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Board:
    # W and B represent white and black flats, C and D are white and black caps (respectively)
    # S and T are white and black walls
    def __init__(self, length):
        self.length = length

        if self.length == 5:
            self.b = [[],[],[],[],[]]
            for lists in self.b:
                for items in range(length):
                    self.b[items].append('')

        elif self.length == 6:
            self.b = [[],[],[],[],[],[]]
            for lists in self.b:
                for items in range(length):
                    self.b[items].append('')
        else:
            raise SizeError('Unsupported Board Size!')


    def print_board(self):
        for xx in range(self.length):
            print(self.b[xx])

    def place_flat(self, player, tile):
        if player is 'black':
            self.b[tile[0]][tile[1]] = 'B'
        elif player is 'white':
            self.b[tile[0]][tile[1]] = 'W'

    def place_cap(self, player, tile):
        if self.b[tile[0]][tile[1]] is '':
            if player is 'black':
                self.b[tile[0]][tile[1]] = 'D'
            elif player is 'white':
                self.b[tile[0]][tile[1]] = 'C'

    def place_wall(self, player, tile):
        if self.b[tile[0]][tile[1]] is '':
            if player is 'black':
                self.b[tile[0]][tile[1]] = 'T'
            elif player is 'white':
                self.b[tile[0]][tile[1]] = 'S'

    def new_move_stack(self, sourceTile, howMany, direction, toWhere):
        howMany = int(howMany)
        movement = [0, 0]
        newTiles = [] # First a tuple denoting the square which will receive tiles, then an int of how many tiles
        if direction == "+":
            movement[0] = -1
        elif direction == "-":
            movement[0] = 1
        elif direction == "<":
            movement[1] = -1
        elif direction == ">":
            movement[1] = 1

        for n in range(1,len(toWhere) + 1):
            move = [(movement[0])*n + sourceTile[0],(movement[1])*n + sourceTile[1]]
            newTiles.append((move, int(toWhere[n-1])))

        fs = self.b[sourceTile[0]][sourceTile[1]] # The contents of the source tile
        string = fs[-1 * howMany:] # Tiles which are being picked up
        string2 = fs[:-1 * howMany] # Tiles which aren't being picked up

        for m in newTiles:
            mm = m[0]
            self.b[mm[0]][mm[1]] += string[:m[1]]
            if len(re.findall(r'[STCD]', self.b[mm[0]][mm[1]])) > 1: # Checks if a wall was flattened
                self.b[mm[0]][mm[1]] = re.sub('S', 'W', self.b[mm[0]][mm[1]])
                self.b[mm[0]][mm[1]] = re.sub('T', 'B', self.b[mm[0]][mm[1]])
            temp = string[m[1]:]
            string = temp

        self.b[sourceTile[0]][sourceTile[1]] = string2



def playMoves(moves, fileString, boardSize = 6, breakPly = {1000}):
    outFile = 'TPS.txt'
    plyCount = 1

    lastPly = len(moves)
    for num in breakPly:
        if num > lastPly:
            breakPly.add(lastPly)
            break
    x = Board(boardSize)
    flatDict = {}
    with open(outFile, 'a') as f:
        f.write(fileString + ' :' + '\n')
    # The coordinate systems are confusing, but they're made with TPS in mind.
    if x.length == 5:
        flatDict = {'a1': (4,0), 'a2': (3,0), 'a3': (2,0), 'a4': (1,0), 'a5': (0,0),
                    'b1': (4,1), 'b2': (3,1), 'b3': (2,1), 'b4': (1,1), 'b5': (0,1),
                    'c1': (4,2), 'c2': (3,2), 'c3': (2,2), 'c4': (1,2), 'c5': (0,2),
                    'd1': (4,3), 'd2': (3,3), 'd3': (2,3), 'd4': (1,3), 'd5': (0,3),
                    'e1': (4,4), 'e2': (3,4), 'e3': (2,4), 'e4': (1,4), 'e5': (0,4)}
    elif x.length == 6:
        flatDict = {'a1': (5,0), 'a2': (4,0), 'a3': (3,0), 'a4': (2,0), 'a5': (1,0), 'a6': (0,0),
                    'b1': (5,1), 'b2': (4,1), 'b3': (3,1), 'b4': (2,1), 'b5': (1,1), 'b6': (0,1),
                    'c1': (5,2), 'c2': (4,2), 'c3': (3,2), 'c4': (2,2), 'c5': (1,2), 'c6': (0,2),
                    'd1': (5,3), 'd2': (4,3), 'd3': (3,3), 'd4': (2,3), 'd5': (1,3), 'd6': (0,3),
                    'e1': (5,4), 'e2': (4,4), 'e3': (3,4), 'e4': (2,4), 'e5': (1,4), 'e6': (0,4),
                    'f1': (5,5), 'f2': (4,5), 'f3': (3,5), 'f4': (2,5), 'f5': (1,5), 'f6': (0,5)}
    else:
        raise SizeError('Size 5 and 6 only, for now.')

    for eachMove in moves:
        if plyCount > 2:
            if plyCount % 2 == 1:
                pl = 'white'
            else:
                pl = 'black'
        elif plyCount == 1:
            pl = 'black'
        else:
            pl = 'white'


        if len(eachMove) == 2:
            x.place_flat(pl, flatDict[eachMove])
        elif 'C' in eachMove:
            x.place_cap(pl, flatDict[eachMove[1:]])
        elif 'S' in eachMove:
            x.place_wall(pl, flatDict[eachMove[1:]])
        else: #by deduction, a stack move
            if '+' in eachMove:
                direct = '+'
                splitMove = re.split('\+', eachMove)
            elif '-' in eachMove:
                direct = '-'
                splitMove = re.split('-', eachMove)
            elif '>' in eachMove:
                direct = '>'
                splitMove = re.split('>', eachMove)
            else:
                direct = '<'
                splitMove = re.split('<', eachMove)

            if len(splitMove[0]) == 2: #Implicit move of a single tile
                tilesToMove = 1
                x.new_move_stack(flatDict[splitMove[0]], tilesToMove, direct, str(tilesToMove))
            else:
                tilesToMove = splitMove[0][0]
                if len(splitMove[1]) > 0:
                    #print(splitMove[1])
                    x.new_move_stack(flatDict[splitMove[0][1:]], tilesToMove, direct, str(splitMove[1][:]))
                else:
                    x.new_move_stack(flatDict[splitMove[0][1:]], tilesToMove, direct, str(tilesToMove))

        if plyCount in breakPly:
            thisBP = plyCount
            TPString = '[TPS "'
            for eachRow in x.b:
                counter2 = 0
                for eachTile in eachRow:
                    if eachTile is not '':
                        counter2 += 1
                        for eachChar in eachTile:
                            if eachChar is 'W':
                                TPString += '1'
                            elif eachChar is 'B':
                                TPString += '2'
                            elif eachChar is 'S':
                                TPString += '1S'
                            elif eachChar is 'T':
                                TPString += '2S'
                            elif eachChar is 'C':
                                TPString += '1C'
                            elif eachChar is 'D':
                                TPString += '2C'
                            else:
                                pass
                        if counter2 < x.length:
                            TPString += ','
                    else:
                        counter2 += 1
                        TPString += 'x1'
                        if counter2 < x.length:
                            TPString += ','
                TPString += '/'

            TPString = TPString[:-1]
            if len(moves) % 2 == 0:
                TPString += ' 1 '
            else:
                TPString += ' 2 '
            if thisBP > len(moves):
                moveNumber = ceil(len(moves) / 2)
            else:
                moveNumber = ceil(thisBP / 2)
            TPString += str(moveNumber)
            TPString += '"]'
            print(TPString)

            with open(outFile, 'a') as f:
                f.write(TPString + '\n')

        plyCount += 1
        return x
        # End func playMoves




def parsePTN(inFile):
    m = []
    with open(inFile,'r') as f:
        rl = f.readlines()
        for lines in rl:
            if re.match('\d', lines):
                splitLine = re.split(' ', lines)
                m.append(splitLine[1])
                try:
                    if '\n' in splitLine[2]:
                        m.append(splitLine[2][:-1])
                    else:
                        m.append(splitLine[2])
                except IndexError:
                    pass
            elif re.match('\[Size', lines):
                size = int(re.split('"', lines)[1])

    return m, size


# gameMoves, bs = parsePTN(file)

# playMoves(gameMoves, boardSize = bs, breakPly = plyNumber)



