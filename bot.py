import tak
import time

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

def maxi(b, depth, team, alpha, beta): #returns value, move pair
    #team = b.turn
    if (depth == 0) | (b.roadLen(team) == b.size) | (b.roadLen(3-team) == b.size):
        L = evaluate(b, team)
        return L, None
    v = float('-inf')
    move = None
    for m in b.getMoves():
        temp = b.move(m)
        (v2, m2) = mini(temp, depth - 1,team, alpha, beta)
        if v2 > v:
            v, move = v2, m
            alpha = max(alpha, v)
        if v >= beta: return v, move
    return v, move

def mini(b, depth, team, alpha, beta): #returns value, move pair
    #team = b.turn
    if (depth == 0) | (b.roadLen(team) == b.size) | (b.roadLen(3-team) == b.size):
        L = evaluate(b, team)
        return L, None
    v = float('inf')
    move = None
    
    for m in b.getMoves():
        temp = b.move(m)
        v2, m2 = maxi(temp, depth - 1, team, alpha, beta)
        if v2 < v:
            v, move = v2, m
            beta = min(beta, v)
        if v <= alpha: return v, move
    return v, move

def alphabeta(b, depth): #returns a move, currently only works for white
    player = b.turn
    (value, move) = maxi(b, depth, player, float('-inf'), float('inf'))
    return move, value

tps = input()
print(f'Input tps: {tps}')
board = tak.Board(tps)
print("Board State:")
print(board)

start = time.time()
c, v = alphabeta(board,4) #parameters are (board, depth)
end = time.time()

print(f'Player: {board.turn}, Move: {c}')
board = board.move(c)
print('Time elapsed:', end - start)
