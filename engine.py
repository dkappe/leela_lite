from lcztools import load_network, LeelaBoard
import search
import chess
import chess.pgn
import sys

logfile = open("leelalite.log", "w")
LOG = False

def log(str):
    if LOG:
        logfile.write(str)
        logfile.write("\n")
        logfile.flush()

def send(str):
    log(">{}".format(str))
    sys.stdout.write(str)
    sys.stdout.write("\n")
    sys.stdout.flush()

def process_position(tokens):
    board = LeelaBoard()

    offset = 0

    if tokens[1] ==  'startpos':
        offset = 2
    elif tokens[1] == 'fen':
        fen = " ".join(tokens[2:8])
        board = LeelaBoard(fen=fen)
        offset = 8

    if offset >= len(tokens):
        return board

    if tokens[offset] == 'moves':
        for i in range(offset+1, len(tokens)):
            board.push_uci(tokens[i])

    return board

if len(sys.argv) != 3:
    print("Usage: python3 engine.py <weights file> <nodes>")
    print(len(sys.argv))
    exit(1)
else:
    weights = sys.argv[1]
    nodes = int(sys.argv[2])

send("Leela Lite")
board = LeelaBoard()
net = None
mm = None



while True:
    line = sys.stdin.readline()
    line = line.rstrip()
    log("<{}".format(line))
    tokens = line.split()
    if len(tokens) == 0:
        continue

    if tokens[0] == "uci":
        send('id name Leela Lite')
        send('id author Dietrich Kappe')
        send('option name List of Syzygy tablebase directories type string default')
        send('uciok')
    elif tokens[0] == "quit":
        exit(0)
    elif tokens[0] == "isready":
        net = load_network(backend='pytorch_cuda', filename=weights, policy_softmax_temp=2.2)
        nn = search.NeuralNet(net=net)
        send("readyok")
    elif tokens[0] == "ucinewgame":
        board = LeelaBoard()
    elif tokens[0] == 'position':
        board = process_position(tokens)
    elif tokens[0] == 'go':
        if nn == None:
            net = load_network(backend='pytorch_cuda', filename=weights, policy_softmax_temp=2.2)
            nn = search.NeuralNet(net=net)
        best, node = search.UCT_search(board, nodes, net=nn, C=3.4)
        send("bestmove {}".format(best))

logfile.close()
