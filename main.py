import tak

tps = input()
print(f'Input tps: {tps}')
board = tak.Board(tps)
c = board.connected((2,1))
print(c)