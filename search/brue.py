import numpy as np
import math
from random import choices
import lcztools
from lcztools import LeelaBoard
import chess
from collections import OrderedDict


class BRUENode():
    def __init__(self, board, parent=None, prior=0):
        self.board = board
        self.parent = parent  # Optional[UCTNode]
        self.children = OrderedDict()  # Dict[move, UCTNode]
        self.prior = prior         # float
        self.total_value = 0. # float
        self.number_visits = 0     # int
        self.uncertainty = .15

    def Q(self):
        return self.total_value/(self.number_visits+1)
        
    def exploit(self):
        children = self.children
        return max(self.children.values(), key=lambda node: node.prior+0.)
    
    def explore(self):
        children = self.children
        return choices(list(children.values()), [node.prior for node in children.values()])[0]
    
    def expand(self, child_priors):
        for move, prior in child_priors.items():
            self.add_child(move, prior)

    def add_child(self, move, prior):
        child = self.build_child(move)
        self.children[move] = BRUENode(child, parent=self, prior=prior)

    def build_child(self, move):
        board = self.board.copy()
        board.push_uci(move)
        return board
        
    def backup(self, value_estimate: float):
        current = self
        # Child nodes are multiplied by -1 because we want max(-opponent eval)
        turnfactor = -1
        while current.parent is not None:            
            current.number_visits += 1
            current.total_value += (value_estimate *
                                    turnfactor)
            current = current.parent
            turnfactor *= -1
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

def BRUE_search(board, num_reads, net=None, C=1.0):
    assert(net != None)
    root = BRUENode(board)
    for n in range(num_reads):
        switchingPoint = n%10
        #print('run ', n, 'switch ', switchingPoint)
        level = 0
        current = root
        #print(current.number_visits)
        while current.number_visits > 0 and current.uncertainty != 0:
            if level < switchingPoint:
                current = current.explore()
                #print('explore', level+1, current.number_visits)
            else:
                current = current.exploit()
                #print('exploit', level+1, current.number_visits)
            level += 1
        
        child_priors, reward, current.uncertainty  = net.evaluate(current.board)
        current.expand(child_priors)
        current.backup(reward)
    
    #for action, child in root.children.items():
    #    print(action, child.number_visits, child.Q())
    return max(root.children.items(), key=lambda item: item[1].Q())



#num_reads = 10000
#import time
#tick = time.time()
#UCT_search(GameState(), num_reads)
#tock = time.time()
#print("Took %s sec to run %s times" % (tock - tick, num_reads))
#import resource
#print("Consumed %sB memory" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
