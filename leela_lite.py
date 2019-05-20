#!/usr/bin/python3
from lcztools import load_network, LeelaBoard, list_backends
import search
import chess
import chess.pgn
import sys
import time


def load_leela_network(weights, backend):
    if backend == 'net_client':
        network_id = int(weights)
        return load_network(backend='net_client', network_id=network_id, policy_softmax_temp=2.2)

    return load_network(backend=backend, filename=weights, policy_softmax_temp=2.2)

def get_search_algos():
    from inspect import getmembers, isfunction

    methods = {}
    for key, value in getmembers(search, isfunction):
        if key.endswith('_search'):
            methods[key.rsplit('_',1)[0].lower()] = value
    return methods

def play(args):
    nodes = args.nodes
    net = load_leela_network(args.weights, args.backend)
    nn = search.NeuralNet(net=net, lru_size=min(5000, nodes))

    search_func = get_search_algos()[args.algo]

    SELFPLAY = True

    board = LeelaBoard()
    while True:
        if not SELFPLAY:
            print(board.unicode())
            print("Enter move: ", end='')
            sys.stdout.flush()
            line = sys.stdin.readline()
            line = line.rstrip()
            board.push_uci(line)
        print(board.unicode())
        print("thinking...")
        start = time.time()
        best, node = search_func(board, nodes, net=nn, C=3.4)
        elapsed = time.time() - start
        print("best: ", best)
        print("Time: {:.3f} nps".format(nodes/elapsed))
        print(nn.evaluate.cache_info())
        board.push_uci(best)
        if board.pc_board.is_game_over() or board.is_draw():
            result = board.pc_board.result(claim_draw=True)
            print("Game over... result is {}".format(result))
            print(board.unicode())
            print()
            pgn_game = chess.pgn.Game.from_board(board.pc_board)
            pgn_game.headers['Result'] = result
            print(pgn_game)
            break

if __name__ == '__main__':
    algos = get_search_algos().keys()

    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('weights', help='weights file or network server ID')
    parser.add_argument('nodes', type=int, help='nodes per move')
    parser.add_argument('-a', '--algo', default='uct', help='search algo to use', choices=algos)
    parser.add_argument('-b', '--backend', default='pytorch_cuda', choices=list_backends(), help='nn backend')

    args = parser.parse_args()
    play(args)
