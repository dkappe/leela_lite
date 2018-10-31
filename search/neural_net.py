import functools

class NeuralNet:

    def __init__(self, net=None, lru_size=5000):
        super().__init__()
        assert(net != None)
        self.net = net
        self.evaluate = functools.lru_cache(maxsize=lru_size)(self.evaluate)

    def evaluate(self, board):
        result = None
        
        if board.pc_board.is_game_over():
            result = board.pc_board.result()
        elif board.is_draw():
            # board.is_draw checks for threefold or fifty move rule
            # Don't use python-chess method, because threefold checks if next move can
            # be threefold as well            
            result = "1/2-1/2"
        
            
        if result:
            if result == "1/2-1/2":
                return dict(), 0.0
            else:
                # Always return -1.0 when checkmated
                return dict(), -1.0
            
        policy, value = self.net.evaluate(board)
        
        value2 = (2.0*value)-1.0
        #print("value: ", value)
        #print("value2: ", value2)
        #sm = temp_softmax(policy.values(), sm=2.2)
        #for i, k in enumerate(policy):
        #    policy[k] = sm[i]
        return policy, value2
