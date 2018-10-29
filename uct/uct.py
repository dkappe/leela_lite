import numpy as np
import math
import lcztools
from lcztools import LeelaBoard
import chess
from collections import OrderedDict
# from uct.util import temp_softmax



class UCTNode():
    def __init__(self, board, parent=None, prior=0):
        self.board = board
        self.is_expanded = False
        self.parent = parent  # Optional[UCTNode]
        self.children = OrderedDict()  # Dict[move, UCTNode]
        self.prior = prior  # float
        self.total_value = 0  # float
        self.number_visits = 0  # int

    def Q(self):  # returns float
        return self.total_value / (1 + self.number_visits)

    def U(self):  # returns float
        return (math.sqrt(self.parent.number_visits)
                * self.prior / (1 + self.number_visits))

    def best_child(self, C):
        return max(self.children.values(),
                   key=lambda node: node.Q() + C*node.U())

    def select_leaf(self, C):
        current = self
        while current.is_expanded and current.children:
            current = current.best_child(C)
        return current

    def expand(self, child_priors):
        self.is_expanded = True
        for move, prior in child_priors.items():
            self.add_child(move, prior)

    def add_child(self, move, prior):
        child = self.build_child(move)
        self.children[move] = UCTNode(
            child, parent=self, prior=prior)

    def build_child(self, move):
        board = self.board.copy()
        board.push_uci(move)
        return board
    
    def backup(self, value_estimate: float):
        current = self
        while current.parent is not None:
            if chess.WHITE == current.board.turn:
                turnfactor = 1
            else:
                turnfactor = -1
            #print("value: ", value_estimate)
            #print("turnfactor: ", turnfactor)
            current.number_visits += 1
            current.total_value += (value_estimate *
                                    turnfactor)
            current = current.parent
        current.number_visits += 1

    def dump(self, move, C):
        print("---")
        print("move: ", move)
        print("total value: ", self.total_value)
        print("visits: ", self.number_visits)
        print("prior: ", self.prior)
        print("Q: ", self.Q())
        print("U: ", self.U())
        print("BestMove: ", self.Q() + C * self.U())
        #print("math.sqrt({}) * {} / (1 + {}))".format(self.parent.number_visits,
        #      self.prior, self.number_visits))
        print("---")

def UCT_search(board, num_reads, net=None, C=1.0):
    assert(net != None)
    root = UCTNode(board)
    for _ in range(num_reads):
        leaf = root.select_leaf(C)
        child_priors, value_estimate = net.evaluate(leaf.board)
        leaf.expand(child_priors)
        leaf.backup(value_estimate)

    for m, node in root.children.items():
        node.dump(m, C)
    return max(root.children.items(),
               key=lambda item: item[1].number_visits)


class NeuralNet:

    def __init__(self, net=None):
        super().__init__()
        assert(net != None)
        self.net = net

    def evaluate(self, board):
        if board.pc_board.is_game_over(claim_draw=True):
            result = board.pc_board.result(claim_draw=True)
            print("Result is {}".format(repr(result)))
            if chess.WHITE == board.turn:
                turnfactor = 1.0
            else:
                turnfactor = -1.0
            if result == "1-0":
                return dict(), turnfactor
            elif result == "0-1":
                return dict(), -turnfactor
            else:
                return dict(), 0.0
        policy, value = self.net.evaluate(board)
        value2 = (2.0*value)-1.0
        #print("value: ", value)
        #print("value2: ", value2)
        #sm = temp_softmax(policy.values(), sm=2.2)
        #for i, k in enumerate(policy):
        #    policy[k] = sm[i]
        return policy, value2



#num_reads = 10000
#import time
#tick = time.time()
#UCT_search(GameState(), num_reads)
#tock = time.time()
#print("Took %s sec to run %s times" % (tock - tick, num_reads))
#import resource
#print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
