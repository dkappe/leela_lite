import numpy as np
import math
import heapq
from collections import OrderedDict


class BellmanNode:
    def __init__(self, board=None, parent=None, move=None, prior=0, depth=0):
        self.board = board
        self.move = move
        self.is_expanded = False
        self.parent = parent  # Optional[BellmanNode]
        self.children = OrderedDict()  # Dict[move, BellmanNode]
        self.prior = prior  # float
        self.number_visits = 0  # int
        self.leaf_visits = 0  # int
        self.tree_depth = depth
        self.Q = 0
        self.reward = 0

    def U(self):  # returns float
        return (math.sqrt(self.parent.number_visits)
                * self.prior / (1 + self.number_visits))

    def best_child(self, c):
        return max(self.children.values(),
                   key=lambda node: node.Q + c*node.U())

    def select_leaf(self, c):
        current = self
        while current.is_expanded and current.children:
            current = current.best_child(c)
        if not current.board:
            current.board = current.parent.board.copy()
            current.board.push_uci(current.move)
        return current

    def expand(self, child_priors):
        self.is_expanded = True
        for move, prior in child_priors.items():
            self.add_child(move, prior)

    def add_child(self, move, prior):
        self.children[move] = BellmanNode(parent=self, move=move, prior=prior, depth=self.tree_depth+1)
    
    def backup(self, value_estimate: float):
        current = self
        self.reward = -value_estimate
        self.Q = self.reward
        self.leaf_visits += 1
        self.number_visits += 1
        while current.parent is not None:
            current = current.parent
            # print('preupdate Q:', current.Q, len(current.children), current.number_visits)
            current.number_visits += 1
            # do we want to add in this reward? its more stable and will disappear with many evals
            current.Q = current.reward * current.leaf_visits / current.number_visits
            visits = current.leaf_visits
            for child in [n for n in current.children.values() if n.number_visits]:
                current.Q -= child.number_visits * child.Q / current.number_visits
                visits += child.number_visits
                # print('updating Q:', current.Q, current.number_visits, visits)
            # print('postupdate Q:', current.Q, current.number_visits, visits)

    def dump(self, move, C):
        print("---")
        print("move: ", move)
        # print("total value: ", self.total_value)
        print("visits: ", self.number_visits)
        print("prior: ", self.prior)
        print("Q: ", self.Q)
        print("U: ", self.U())
        print("BestMove: ", self.Q + C * self.U())
        # print("math.sqrt({}) * {} / (1 + {}))".format(self.parent.number_visits,
        #      self.prior, self.number_visits))
        print("---")


def Bellman_search(board, num_reads, net=None, C=1.0):
    assert(net is not None)
    root = BellmanNode(board)
    root.number_visits = 1
    for _ in range(num_reads):
        leaf = root.select_leaf(C)
        child_priors, value_estimate = net.evaluate(leaf.board)
        leaf.expand(child_priors)
        leaf.backup(value_estimate)

    size = min(5, len(root.children))
    pv = heapq.nlargest(size, root.children.items(),
                        key=lambda item: (item[1].number_visits, item[1].Q))

    print('Bellman pv:', [(n[0], n[1].Q, n[1].number_visits) for n in pv])
    return max(root.children.items(),
               key=lambda item: (item[1].number_visits, item[1].Q))
