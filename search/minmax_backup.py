import math
import heapq
from collections import OrderedDict


class MinMaxNode:
    def __init__(self, board=None, parent=None, move=None, prior=0):
        self.board = board
        self.move = move
        self.is_expanded = False
        self.parent = parent  # Optional[MinMaxNode]
        self.children = OrderedDict()  # Dict[move, MinMaxNode]
        self.prior = prior  # float
        self.total_value = 0  # float
        self.minmax_value = 0  # float
        self.number_visits = 0  # int

    def Q(self, alpha=0.25):
        return (1 - alpha) * self.total_value / (1 + self.number_visits) + alpha * self.minmax_value



    def U(self):  # returns float
        return math.sqrt(self.parent.number_visits) * self.prior / (1 + self.number_visits)

    def best_child(self, C, alpha):
        return max(self.children.values(),
                   key=lambda node: node.Q(alpha) + C*node.U())

    def select_leaf(self, C, alpha):
        current = self
        while current.is_expanded and current.children:
            current = current.best_child(C, alpha)
        if not current.board:
            current.board = current.parent.board.copy()
            current.board.push_uci(current.move)
        return current

    def expand(self, child_priors):
        self.is_expanded = True
        for move, prior in child_priors.items():
            self.add_child(move, prior)

    def add_child(self, move, prior):
        self.children[move] = MinMaxNode(parent=self, move=move, prior=prior)
    
    def backup(self, value_estimate: float):
        current = self
        current.total_value = -value_estimate
        current.minmax_value = -value_estimate
        current.number_visits += 1
        turnfactor = 1
        while current.parent is not None:
            current = current.parent
            current.number_visits += 1
            current.minmax_value = -max([n.minmax_value for n in current.children.values()
                                         if n.number_visits])

            current.total_value += value_estimate * turnfactor
            turnfactor *= -1
        current.number_visits += 1

    def dump(self, move, C, alpha):
        print("---")
        print("move: ", move)
        print("total value: ", self.total_value)
        print("visits: ", self.number_visits)
        print("prior: ", self.prior)
        print("Q: ", self.Q(alpha))
        print("U: ", self.U())
        print("BestMove: ", self.Q(alpha) + C * self.U())
        # print("math.sqrt({}) * {} / (1 + {}))".format(self.parent.number_visits,
        #      self.prior, self.number_visits))
        print("---")


def MinMax_search(board, num_reads, net=None, C=1.0, alpha=0.25):
    assert(net is not None)
    root = MinMaxNode(board)
    for _ in range(num_reads):
        leaf = root.select_leaf(C, alpha)
        child_priors, value_estimate = net.evaluate(leaf.board)
        leaf.expand(child_priors)
        leaf.backup(value_estimate)

    size = min(5, len(root.children))
    pv = heapq.nlargest(size, root.children.items(),
                        key=lambda item: (item[1].number_visits, item[1].Q(alpha)))
    #print('MinMax pv:', [(n[0], n[1].Q(alpha), n[1].number_visits) for n in pv])
    #print('prediction:', end=' ')
    next = pv[0]
    while len(next[1].children):
        next = heapq.nlargest(1, next[1].children.items(),
                                key=lambda item: (item[1].number_visits, item[1].Q(alpha)))[0]
        #print(next[0], end=' ')
    #print('')
    return max(root.children.items(),
               key=lambda item: (item[1].number_visits, item[1].Q(alpha)))
