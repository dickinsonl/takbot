class Board:
    def __init__(self, tps):
        tps = tps.split() #split the board state from the turn indicator and the move counter
        self.turn = tps[1]
        x = tps[0].split("/")
        self.size = len(x)
        self.b = []
        for i in range(self.size): #i is row number
            self.b.append([]) #add row to the board
            y = x[i].split(",") #e.g. y would be [x3, 2, x1]
            for j in y: #j is a string denoting piece(s) on a space
                if j[0] == 'x':
                    try:
                        blanks = int(j[1])
                        for k in range(blanks):
                            self.b[i].append(Piece())
                    except IndexError:
                        self.b[i].append(Piece())
                else:
                    self.b[i].append(Piece(j))

    def __str__(self):
        # col0 = [self.b[i][1] for i in range(self.size)]
        # [print(i) for i in col0]
        print(self.b[2][0])
        out = ''
        for i in range(self.size):
            row = ''
            for j in range(self.size):
                row += self.b[i][j].__str__() + ','
            row += '\n'
            out += row
        return out
    
    def connected(self, coord): #takes in coordinate as a tuple in the form (row, column), returns list of pieces connected to the piece at that coordinate, or empty if there is no piece at that coordinate
        out = []
        p = self.b[coord[0]][coord[1]] #p = piece at coord
        team = p.team
        if team != 'empty':
            print('range:', coord)
            for i in range(coord[0]-1, coord[0]+1):
                for j in range(coord[1]-1, coord[1]+2): #iterate through spaces adjacent to coord                   
                    if ((i,j) != coord):
                        print(f'i: {i} j: {j}, coord: {coord}')
                        c = self.b[i][j]
                        if c.team == p.team: #check if teams are equal, this also returns false if c is an empty space
                            out.append((i,j))
        return out
                

    def roadLenNeeded(self, team): #takes in a team, returns the number of tiles theoretically needed to complete that team's longest road, not looking at obstacles
        row0 = self.b[0]
        col0 = [self.b[i][0] for i in range(self.size)]
        for count, piece in enumerate(row0):
            con = self.connected(())

            


class Piece:

    def __init__(self, string = ''): #stores the tiles in the stack in self.tiles, the type of the top piece, and the team of the top piece for quick reference.
        if string == '':
            self.tiles = ['_']
            self.type = 'empty'
            self.team = 'empty'
        else:
            self.tiles = [*string]
            t = self.tiles[-1]
            if t == 'S':
                self.type = 'wall'
                self.tiles[0:-1]
            elif t == 'C':
                self.type = 'cap'
                self.tiles[0:-1]
            else:
                self.type = 'flat'
            self.team = self.tiles[-1] #team of all pieces is stored as them being either 1s or 2s, this is just to have the team that controls the stack for quick reference

    def __str__(self):
        out = ''.join(self.tiles)
        return out
    