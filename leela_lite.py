from lcztools import load_network, LeelaBoard
import search
import chess
import chess.pgn
import sys

if len(sys.argv) != 3:
    print("Usage: python3 leela_lite.py <weights file> <nodes>")
    print(len(sys.argv))
    exit(1)
else:
    weights = sys.argv[1]
    nodes = int(sys.argv[2])


board = LeelaBoard()

net = load_network(filename=weights, policy_softmax_temp=2.2)
nn = search.NeuralNet(net=net)
#policy, value = net.evaluate(board)
#print(policy)
#print(value)
#print(uct.softmax(policy.values()))

SELFPLAY = True

while True:
    if not SELFPLAY:
        print(board)
        print("Enter move: ", end='')
        sys.stdout.flush()
        line = sys.stdin.readline()
        line = line.rstrip()
        board.push_uci(line)
    print(board)
    print("thinking...")
    best, node = search.BRUE_search(board, nodes, net=nn)
    print("best: ", best, 'eval', node.Q())
    board.push_uci(best)
    
    best, node = search.UCT_search(board, nodes, net=nn)
    print("best: ", best, 'eval', node.Q())
    board.push_uci(best)
    if board.pc_board.is_game_over() or board.is_draw():
        print("Game over... result is {}".format(board.pc_board.result(claim_draw=True)))
        print(board)
        print(chess.pgn.Game.from_board(board.pc_board))
        break

