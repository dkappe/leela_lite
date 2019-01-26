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

if len(sys.argv) == 3:
    weights = sys.argv[1]
    nodes = int(sys.argv[2])
    type = "uct"
elif len(sys.argv) == 4:
    weights = sys.argv[1]
    nodes = int(sys.argv[2])
    if sys.argv[3] == 'minimax':
        type = 'minimax'
    else:
        type = 'uct'
else:
    print("Usage: python3 engine.py <weights file or network server ID> <nodes>")
    print(len(sys.argv))
    exit(1)

network_id = None
try:
    # If the parameter is an integer, assume it's a network server ID
    network_id = int(weights)
    weights = None
except:
    pass

def load_leela_network():
    global net, nn
    if network_id is not None:
        net = load_network(backend='net_client', network_id=network_id, policy_softmax_temp=2.2)
    else:
        net = load_network(backend='pytorch_cuda', filename=weights, policy_softmax_temp=2.2)
    nn = search.NeuralNet(net=net, lru_size=max(5000, nodes))


send("Leela Lite")
board = LeelaBoard()
net = None
nn = None



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
        send('uciok')
    elif tokens[0] == "quit":
        exit(0)
    elif tokens[0] == "isready":
        load_leela_network()
        send("readyok")
    elif tokens[0] == "ucinewgame":
        board = LeelaBoard()
    elif tokens[0] == 'position':
        board = process_position(tokens)
    elif tokens[0] == 'go':
        my_nodes = nodes
        if (len(tokens) == 3) and (tokens[1] == 'nodes'):
            my_nodes = int(tokens[2])
        if nn == None:
            load_leela_network()
        if type == 'uct':
            best, node = search.UCT_search(board, my_nodes, net=nn, C=3.0, material_ratio=0.0, stats=False)
        else:
            best, node = search.MinMax_search(board, my_nodes, net=nn, C=3.4)
        send("bestmove {}".format(best))

logfile.close()
