from lcztools import load_network, LeelaBoard
import uct
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

net = load_network(backend='pytorch_cuda', filename=weights)
nn = uct.NeuralNet(net=net)
#policy, value = net.evaluate(board)
#print(policy)
#print(value)
#print(uct.softmax(policy.values()))

while True:
    print(board)
    line = sys.stdin.readline()
    line = line.rstrip()
    board.push_uci(line)
    print(board)
    print("thinking...")
    best, node = uct.UCT_search(board, nodes, net=nn, C=3.4)
    print("best: ", best)
    board.push_uci(best)

