import heapq

class Board:
    def __init__(self, tps):
        tps = tps.split() #split the board state from the turn indicator and the move counter
        self.turn = int(tps[1])
        self.movecount = int(tps[2])
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
        out = ''
        for i in range(self.size):
            row = ''
            for j in range(self.size):
                row += self.b[i][j].__str__() + ','
            row += '\n'
            out += row
        return out
    
    def tps(self): #returns TPS representation of the board
        out = ''
        for i in self.b:
            xcnt = 0
            for j in i:
                #print(j.type == 'empty')
                match j.type:
                    case 'empty':
                        xcnt += 1
                    case _:
                        if xcnt > 1:
                            out = f'{out}x{xcnt},'
                        elif xcnt > 0:
                            out = out + 'x,'
                        out = out + str(j) + ','
                        xcnt = 0
            if xcnt > 1:
                out = f'{out}x{xcnt},'
            elif xcnt > 0:
                out = out + 'x,'
            
            out = out[:-1] + '/'
        out = f'{out[:-1]} {self.turn} {self.movecount}'
        return out
            

    def getMoves(self): #at the moment only accounting for placing stones
        out = []
        for i in range(self.size):
            for j in range(self.size):
                p = self.b[i][j]
                rank = str(self.size - i)
                file = chr(97 + j) #ascii conversion for letter+number coords used by PTN
                #Placement moves:
                if p.type == 'empty':
                    out.append(file+rank)
                
                #Movement moves:
                elif p.team == self.turn:
                    dirlist = []
                    if i > 0:
                        dirlist.append('+')
                    if i < self.size-1:
                        dirlist.append('-')
                    if j > 0:
                        dirlist.append('<')
                    if j < self.size-1:
                        dirlist.append('>') 
                    for d in dirlist:
                        out.append(file+rank+d)

        return out
    
    def move(self, ptn): #takes an example PTN move, eg a3, and returns a new board with that move made
        out = Board(self.tps())
        type = ''
        ptn = [*ptn]
        #Movement moves:
        dir = None
        if '>' in ptn:
            dir = 0,1
        elif '<' in ptn:
            dir = 0,-1
        elif '+' in ptn:
            dir = -1, 0
        elif '-' in ptn:
            dir = 1, 0
        if dir != None:
            carryCount = 0
            if ptn[0].isdigit():
                carryCount = ptn[0]
                ptn = ptn[1:]
            file = ord(ptn[0])-97 #convert out of chr and back down by 97
            rank = out.size - int(ptn[1]) #-1 to get to 0 indexing
            dest = [i + j for i, j in zip((rank,file), dir)]
            p = out.b[rank][file]
            out.b[rank][file] = Piece()
            out.b[dest[0]][dest[1]].stack(p)
            out.turn = 3 - out.turn #this switches the turn from 2 to 1 or vice versa
            return out
        #Placement moves:
        if ptn[0].isupper():
            type = ptn[0]
            ptn = ptn[1:]
        file = ord(ptn[0])-97 #convert out of chr and back down by 97
        rank = self.size - int(ptn[1]) #-1 to get to 0 indexing
        pStr = str(out.turn) + type
        p = Piece(pStr)
        out.b[rank][file] = p
        out.turn = 3 - out.turn #this switches the turn from 2 to 1 or vice versa
        return out
        
    #def evaluate():
    
    def connected(self, coord): #takes in coordinate as a tuple in the form (row, column), returns list of pieces connected to the piece at that coordinate, or empty if there is no piece at that coordinate
        out = []
        p = self.b[coord[0]][coord[1]] #p = piece at coord
        team = p.team
        if team != 'empty':
            clist = ((coord[0]-1, coord[1]), (coord[0]+1, coord[1]), (coord[0], coord[1]-1), (coord[0], coord[1]+1))
            for i, j, in clist: #iterate through spaces adjacent to coord                   
                try:
                    if ((i,j) != coord):
                        #print(f'i: {i} j: {j}, coord: {coord}')
                        c = self.b[i][j]
                        if (c.team == p.team) & (c.type != 'wall'): #check if teams are equal, this also returns false if c is an empty space
                            out.append((i,j))
                except IndexError:
                    continue
        return out
                

    def roadLen(self, team): #takes in a team, returns the number of tiles theoretically needed to complete that team's longest road, not looking at obstacles
        #team = self.turn
        row0 = self.b[0]
        col0 = [self.b[i][0] for i in range(self.size)]
        maxRoad = 0
        for i in range(self.size): #find vertical roads
            if maxRoad > self.size - i:
                break
            for j in range(self.size):
                coord = (i,j)
                p = self.b[i][j]
                curRoad = 0
                if p.team == team: #finding start of road
                    curRoad = 1
                    closed = []
                    open = [coord] 
                    while True:
                        if len(open) == 0:
                            break
                        node = open.pop()
                        closed.append(node)
                        if (node[0] - i + 1) > curRoad: #check if the new node makes the road longer vertically
                            curRoad += 1

                        if curRoad >= (self.size): #return 0 if there is a full road
                            return curRoad
                        else:
                            children = [x for x in self.connected(node) if x not in closed]
                            open = children + open
                if curRoad > maxRoad:
                    maxRoad = curRoad

        for j in range(self.size): #find horizontal roads
            if maxRoad > self.size - j:
                break
            for i in range(self.size):
                coord = (i,j)
                p = self.b[i][j]
                curRoad = 0
                if p.team == team: #finding start of road
                    curRoad = 1
                    closed = []
                    open = [coord]
                    while True:
                        if len(open) == 0:
                            break
                        node = open.pop()
                        closed.append(node)
                        
                        if (node[1] - j + 1) > curRoad: #check if the new node makes the road longer horizontally
                            curRoad += 1

                        if curRoad >= (self.size): #return 0 if there is a full road
                            return curRoad
                        else:
                            children = [x for x in self.connected(node) if x not in closed]
                            open = children + open
                if curRoad > maxRoad:
                    maxRoad = curRoad      
        return maxRoad

    def flatCount(self): #Returns tuple of (player 1 falt count, player 2 flat count)
        white = 0
        black = 0
        for i in range(self.size):
            for j in range(self.size):
                p = self.b[i][j]
                if p.type == 'flat':
                    if p.team == 1:
                        white += 1
                    if p.team == 2:
                        black += 1
        return white, black
                

class Piece:
    def __init__(self, string = ''): #stores the tiles in the stack in self.tiles, the type of the top piece, and the team of the top piece for quick reference.
        if string == '':
            self.tiles = ['_']
            self.type = 'empty'
            self.team = 'empty'
            self.size = 0
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
            self.team = int(self.tiles[-1]) #team of all pieces is stored as them being either 1s or 2s, this is just to have the team that controls the stack for quick reference
            self.size = len(self.tiles)

    def __str__(self):
        out = ''.join(self.tiles)
        match self.type:
            case 'wall':
                t = 'S'
            case 'cap':
                t = 'C'
            case _:
                t = ''
        out = out + t
        return out
    
    def stack(self, p): #Function for this piece object being captured by piece p
        if self.type == 'empty':
            self.tiles = p.tiles
        else:
            self.tiles = self.tiles + p.tiles #Remember that the top piece is the last in the list
        self.type = p.type
        self.team = p.team
        self.size = len(self.tiles)