"""
The team.py file is where you should write all your code!

Write the __init__ and the step functions. Further explanations
about these functions are detailed in the wiki.

List your Andrew ID's up here!
bwei1
lrwalker
alexs1
"""
from awap2019 import Tile, Direction, State
import numpy as np
import heapq
from collections import defaultdict

class Team(object):
    def checktile(self,i,j,rows,cols,initial_board):
        if i < 0 or i >= rows or j < 0 or j >= cols:
            return 2**31
        elif initial_board[i][j].get_booth() != None:
            return 2**31
        else:
            return initial_board[i][j].get_threshold()
    def __init__(self, initial_board, team_size, company_info):
        """
        The initializer is for you to precompute anything from the
        initial board and the company information! Feel free to create any
        new instance variables to help you out.

        Specific information about initial_board and company_info are
        on the wiki. team_size, although passed to you as a parameter, will
        always be 4.
        """
        self.graph = defaultdict(list)
        for i in range(len(initial_board)):
            for j in range(len(initial_board[0])):
                tile = initial_board[i][j]
                if tile.get_booth() != None:
                    self.graph[(i,j)] = [2**31]*4
                else:
                    tileup = self.checktile(i-1,j,len(initial_board),len(initial_board[0]),initial_board)
                    tiledown = self.checktile(i+1,j,len(initial_board),len(initial_board[0]),initial_board)
                    tileright = self.checktile(i,j+1,len(initial_board),len(initial_board[0]),initial_board)
                    tileleft = self.checktile(i,j-1,len(initial_board),len(initial_board[0]),initial_board)
                    self.graph[(i,j)] = [tileup,tiledown,
                                         tileleft,tileright]
        print(self.graph)
        print("\n")

        self.lines = defaultdict(list)
        for i in range(len(initial_board)):
            for j in range(len(initial_board[0])):
                tile = initial_board[i][j]
                if tile.is_end_of_line():
                    self.lines[tile.get_line()] = [(i, j)]

        for company, start in self.lines.items():


        print(initial_board)


        self.board = initial_board
        self.team_size = team_size
        self.team_name = "Player 2"# Add your team name here!

        compAsList = [ [k,v] for k, v in company_info.items() ]
        compAsList.sort(key = lambda x: -x[1])
        q = PriorityQueue()
        for x in compAsList:
            name, pts = x
            q.push(name, pts)
        self.pq = q

        self.company_info = company_info
        self.booths = dict()
        for i in range(len(initial_board)):
            for j in range(len(initial_board[0])):
                tile = initial_board[i][j]
                if tile.get_booth() != None:
                    self.booths[tile.get_booth()] = (i,j)

        self.targets = [None,None,None,None]



    def step(self, visible_board, states, score):
        """
        The step function should return a list of four Directions.

        For more information on what visible_board, states, and score
        are, please look on the wiki.
        """

        moves = [0,0,0,0]

        for index in range(4):
            bot = states[index]
            bot_coord = (bot.x, bot.y)
            if bot.line_pos != -1:
                moves[index] = Direction.NONE
            elif visible_board[bot.x][bot.y].get_line() != None:
                moves[index] = Direction.ENTER
                self.targets[index] = None
            else:
                if self.targets[index] == None:
                    company = self.pq.pop()
                    new_company_pts = self.company_info[company] / 2
                    self.company_info[company] = new_company_pts
                    self.pq.push(company, new_company_pts)
                    self.targets[index] = company
                company_coord = self.booths[self.targets[index]]
                moves[index] = shortest_path(bot_coord, company_coord, visible_board)



        return moves

def shortest_path(source, dest, visible_board):
    return Direction.UP

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
