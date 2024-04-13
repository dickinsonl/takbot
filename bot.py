import tak
def evaluate(b, player):
    roadWeight = 1.0 #Weights to be tuned
    flatWeight = 0.0
    wflats, bflats = b.flatCount()
    fcd = wflats - bflats #Flat Count Differential
    teamLen = b.roadLen(player) #player's longest road
    oppLen = b.roadLen(3 - player) #opponent's longest road
    # if teamLen >= b.size:
    #     return float('inf')
    # if oppLen >= b.size:
    #     return float('-inf')
    road = 0
    if teamLen > oppLen:
        road = teamLen
    elif oppLen > teamLen:
        road = -oppLen
    return roadWeight*road + flatWeight*fcd #could probably just return teamLen - oppLen but this improves readability for debugging

def maxi(b, depth, team): #returns value, move pair
    #team = b.turn
    if (depth == 0) | (b.roadLen(team) == b.size) | (b.roadLen(3-team) == b.size):
        L = evaluate(b, team)
        return L, None
    v = float('-inf')
    #print("movelist", b.getMoves())
    move = None
    for m in b.getMoves():
        temp = b.move(m)
        (v2, m2) = mini(temp, depth - 1,team)
        #print(f'maxi v: {v}, v2: {v2}, move: {m}')
        if v2 > v:
            v, move = v2, m
    #print(f'maxi v: {v}, move: {move, b.turn}')
    return v, move

def mini(b, depth, team): #returns value, move pair
    #team = b.turn
    if (depth == 0) | (b.roadLen(team) == b.size) | (b.roadLen(3-team) == b.size):
        L = evaluate(b, team)
        return L, None
    v = float('inf')
    move = None
    
    for m in b.getMoves():
        #print("m:", m)
        temp = b.move(m)
        #print(temp)
        v2, m2 = maxi(temp, depth - 1, team)
        #print(f'pre mini v2: {v2}, m2: {m2}, m: {m}')
        if v2 < v:
            v, move = v2, m
            #if v == float('inf')
    #print(f'mini v: {v}, move: {move, b.turn}')
    return v, move

def minimax(b, depth): #returns a move, currently only works for white
    player = b.turn
    (value, move) = maxi(b, depth, player)
    return move, value

tps = input()
print(f'Input tps: {tps}')
board = tak.Board(tps)
print(board)
board = board.move('b2>')
# board = board.move('b4')
# board = board.move('a3')
# board = board.move('a4')
# board = board.move('c3')
# board = board.move('c4')
print(board.flatCount())
#c, v = minimax(board,3)
#print(c, v)


print(board)