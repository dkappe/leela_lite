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
    board = chess.Board()

    offset = 0

    if tokens[1] ==  'startpos':
        offset = 2
    elif tokens[1] == 'fen':
        fen = " ".join(tokens[2:8])
        board = chess.Board(fen=fen)
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
else:
    print("Usage: python3 engine.py <weights file or network server ID> <nodes>")
    print(len(sys.argv))
    exit(1)

try:
    # If the parameter is an integer, assume it's a network server ID
    network_id = int(weights)
    weights = None
except:
    pass

def load_network():
    global nn
    nn = search.EPDLRUNet(search.MaterialNet(), 8000)


send("Leela Lite")
board = chess.Board()
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
        load_network()
        send("readyok")
    elif tokens[0] == "ucinewgame":
        board = chess.Board()
    elif tokens[0] == 'position':
        board = process_position(tokens)
    elif tokens[0] == 'go':
        my_nodes = nodes
        if (len(tokens) == 3) and (tokens[1] == 'nodes'):
            my_nodes = int(tokens[2])
        if nn == None:
            load_network()
        best, node = search.UCT_search(board, my_nodes, net=nn, C=3.0)

        send("bestmove {}".format(best))

logfile.close()
