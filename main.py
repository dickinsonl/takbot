import parse
# while True:
#     try:
#         x = input()
#     except EOFError:
#         break
file = input('Name of the .ptn file?\n')
gameMoves, bs = parse.parsePTN(file)
plyNumber = {1000}
board = parse.playMoves(gameMoves, file, boardSize = bs, breakPly = plyNumber)
board.print_board()