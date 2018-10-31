
import numpy as np
import math
from random import choices
import lcztools
from lcztools import LeelaBoard
import chess
from collections import OrderedDict


class CRAZYNode():
    def __init__(self, board, parent=None, prior=0):
        self.board = board
        self.is_expanded = False
        self.parent = parent  # Optional[UCTNode]
        self.children = OrderedDict()  # Dict[move, UCTNode]
        self.prior = prior
        if parent is None:
            self.value = 0.  # float
        else:
            self.value = -parent.value  # float
        self.Q2 = 0.1 #float
        self.number_visits = 0  # int

    def Q(self):  # returns float
        return self.value

    def U(self):  # returns float
        u = 0#self.prior * math.sqrt(self.parent.number_visits) / (1 + self.number_visits)
        var =  self.Q2 / (self.number_visits+1)
        return u+var
    
    def get_prob_max(self):
        children = self.children.values()
        best_child = max(children, key=lambda child: child.Q())
        best_q, best_U = best_child.Q(), best_child.U()
        return [math.e**(-1.7*(best_q - child.Q()) / (best_U+child.U())**.5) 
                for child in children]
    
    def select_child(self):
        children = list(self.children.values())
        weights = self.get_prob_max()
        #print(weights)
        return choices(children, weights)[0]

    def select_leaf(self):
        current = self
        while current.is_expanded and current.children:
            current = current.select_child()
        return current

    def expand(self, child_priors):
        self.is_expanded = True
        for move, prior in child_priors.items():
            self.add_child(move, prior)

    def add_child(self, move, prior):
        child = self.build_child(move)
        self.children[move] = CRAZYNode(
            child, parent=self, prior=prior)

    def build_child(self, move):
        board = self.board.copy()
        board.push_uci(move)
        return board
    
    def backup(self, reward: float):
        current = self
        # Child nodes are multiplied by -1 because we want max(-opponent eval)
        reward = -reward
        while current is not None:
            current.number_visits += 1
            delta = reward - current.value
            current.value = delta/current.number_visits
            delta2 = reward - current.value
            current.Q2 += delta * delta2
            current = current.parent
            reward *= -1

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

def CRAZY_search(board, num_reads, net=None, C=1.0):
    assert(net != None)
    root = CRAZYNode(board)
    for _ in range(num_reads):
        leaf = root.select_leaf()
        child_priors, reward, u = net.evaluate(leaf.board)
        leaf.expand(child_priors)
        #reward = .5*(reward+1)
        leaf.backup(reward)
        
    #assert -1<=root.Q()<=1, [c.value for c in root.children.values()]
    #assert 0<=root.U()
    for move, child in sorted(root.children.items(),
                          key=lambda item: -item[1].number_visits):
        pass
        #print(move, child.number_visits, child.Q(), child.U())
    return max(root.children.items(),
                key=lambda item: item[1].number_visits)
               #key=lambda item: item[1].Q() - item[1].U())
