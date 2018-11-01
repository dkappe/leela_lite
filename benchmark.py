from lcztools import load_network, LeelaBoard
import search
import chess
import chess.pgn
import sys
import datetime

weights = sys.argv[1]

board = LeelaBoard()

net = load_network(backend='pytorch_cuda', filename=weights, policy_softmax_temp=2.2)
nn = search.NeuralNet(net=net)
NODES = 10000

def do_nn():
    best, node = search.UCT_search(board, NODES, net=net, C=3.4)

start = datetime.datetime.now()
do_nn()
fini = datetime.datetime.now()

diff = fini - start
msecs = diff.microseconds + (diff.seconds*1000000.0)
nps = round(NODES*1000000.0/(msecs))

print("{} nps".format(nps))





