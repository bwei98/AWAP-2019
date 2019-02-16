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

    def in_bounds(self, coords):
        return 0 <= coords[0] and coords[0] < self.num_rows and 0 <= coords[1] and coords[1] < self.num_cols

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
        self.num_rows = len(initial_board)
        self.num_cols = len(initial_board[0])


        for i in range(self.num_rows):
            for j in range(self.num_cols):
                tile = initial_board[i][j]
                if tile.get_booth() != None:
                    self.graph[(i,j)] = [2**31]*4
                else:
                    tileup = self.checktile(i-1,j,self.num_rows,self.num_cols,initial_board)
                    tiledown = self.checktile(i+1,j,self.num_rows,self.num_cols,initial_board)
                    tileright = self.checktile(i,j+1,self.num_rows,self.num_cols,initial_board)
                    tileleft = self.checktile(i,j-1,self.num_rows,self.num_cols,initial_board)
                    self.graph[(i,j)] = [tileup,tiledown,
                                         tileleft,tileright]


        self.lines = defaultdict(list)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                tile = initial_board[i][j]
                if tile.is_end_of_line():
                    self.lines[tile.get_line()] = [(i, j)]

        for company in self.lines:
            (x, y) = self.lines[company][0]
            end = (x, y)
            while self.in_bounds((x-1, y)) and initial_board[x-1][y].get_line() == company:
                end = (x-1, y)
                x -= 1
            while self.in_bounds((x+1, y)) and initial_board[x+1][y].get_line() == company:
                end = (x+1, y)
                x += 1
            while self.in_bounds((x, y-1)) and initial_board[x][y-1].get_line() == company:
                end = (x, y-1)
                y -= 1
            while self.in_bounds((x, y+1)) and initial_board[x][y+1].get_line() == company:
                end = (x, y+1)
                y += 1
            self.lines[company].append(end)



        self.board = initial_board
        self.team_size = team_size
        self.team_name = "Player 2"# Add your team name here!


        compAsList = [ [k,v] for k, v in company_info.items() ]
        # compAsList.sort(key = lambda x: -x[1])
        # q = MaxPriorityQueue()
        # for x in compAsList:
        #     name, pts = x
        #     q.push(name, pts)
        #print(compAsList)
        self.companyList = compAsList
        self.num_companies = len(compAsList)

        self.company_info = company_info
        self.booths = dict()
        for i in range(self.num_rows):
            for j in range(self.num_cols):
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

        self.update_graph(states, visible_board)

        for index in range(4):
            bot = states[index]
            bot_coord = (bot.x, bot.y)
            if bot.line_pos != -1:
                moves[index] = Direction.NONE
            elif visible_board[bot.x][bot.y].get_line() != None and visible_board[bot.x][bot.y].is_end_of_line():
                moves[index] = Direction.ENTER
                self.targets[index] = None
            else:
                if self.targets[index] != None:
                    close_line = self.near_line(visible_board, index, bot)
                    if close_line != None:
                        moves[index] = close_line
                    else:
                        target_coord = self.lines[self.targets[index]][0]
                        moves[index] = self.shortest_path(bot_coord, target_coord)

                else:
                    def costs(company):
                        name, ptVal = company
                        comp_loc = self.lines[name][0]
                        dist = self.shortest_path(bot_coord, comp_loc)[1]
                        CONST = 1.2
                        return ptVal / (dist ** CONST)

                    costList = map(costs, self.companyList)
                    list_with_ind = [(v, i) for i, v in enumerate(costList)]
                    list_with_ind.sort(key = lambda x: -x[0])
                    i = 0
                    print(self.companyList)
                    print(list_with_ind)
                    while True:
                        nobody_going = True
                        company = self.companyList[list_with_ind[i][1]][0]
                        for c in self.targets:
                            if c == company:
                                nobody_going = False
                                i = i + 1
                                break;
                        if nobody_going:
                            break;
                        if i == self.num_companies:
                            company = self.companyList[list_with_ind[0][1]][0]
                            i = 0
                            break;

                    print("lllllll")
                    new_company_pts = self.company_info[company] / 2.0
                    self.company_info[company] = new_company_pts
                    self.companyList[i][1] = new_company_pts

                    self.targets[index] = company
                    print(self.targets)

        return moves


    def checktile(self,i,j,rows,cols,initial_board):
        if i < 0 or i >= rows or j < 0 or j >= cols:
            return 2**31
        elif initial_board[i][j].get_booth() != None:
            return 2**31
        else:
            return initial_board[i][j].get_threshold()

    def update_graph(self, states, visible_board):
        for index in range(4):
            bot = states[index]
            for xdiff in range(-2,3):
                for ydiff in range(-2,3):
                    x,y= bot.x + xdiff, bot.y + ydiff
                    if x >= 0 and y >= 0 and x < self.num_rows and y < self.num_cols:
                        t = visible_board[x][y].get_threshold()
                        if x+1 < self.num_rows:
                            self.graph[(x+1,y)][2] = t
                        if x > 0:
                            self.graph[(x-1,y)][3] = t
                        if y+1 < self.num_cols:
                            self.graph[(x,y+1)][0] = t
                        if y > 0:
                            self.graph[(x,y-1)][1] = t


    def shortest_path(self, source, dest):
        mapping = dict()
        j = 0
        for i in self.graph.keys():
            mapping[i] = j
            j += 1
        dist = [float("Inf")]*len(mapping)
        dist[mapping[(source)]] = 0
        heap = MyPriorityQueue()
        prev = [None]*len(mapping)
        prev[mapping[source]] = source
        visited = set()

        heap.push(source,dist[mapping[source]])

        while heap.isEmpty() != True:
            minval = heap.pop()
            node = minval[-1]
            visited.add(node)
            for i in range(4):
                if i == 0:
                    newnode = (node[0]-1,node[1])
                elif i == 1:
                    newnode = (node[0]+1,node[1])
                elif i == 2:
                    newnode = (node[0],node[1]-1)
                else:
                    newnode = (node[0],node[1]+1)
                if self.in_bounds(newnode) and newnode not in visited:
                    if dist[mapping[node]] + self.graph[node][i] < dist[mapping[newnode]]:
                        dist[mapping[newnode]] = dist[mapping[node]] + self.graph[node][i]
                        prev[mapping[newnode]] = node
                        heap.push(newnode,dist[mapping[newnode]])
        returnpath = [dest]
        cost = dist[mapping[dest]]
        start = prev[mapping[dest]]
        while(start != source):
            returnpath.append(start)
            start = prev[mapping[start]]
        #print(returnpath)
        returnpath.append(source)
        firstmove = returnpath[-2]
        if source[0] > firstmove[0]:
            return (Direction.UP,cost)
        elif source[0] < firstmove[0]:
            return (Direction.DOWN,cost)
        elif source[1] > firstmove[1]:
            return (Direction.LEFT,cost)
        else:
            return (Direction.RIGHT,cost)


    def near_line(self, visible_board, index, bot):
        if self.targets[index] == None:
            return None
        line_full = False
        end_line = None
        for xdiff in range(-2,3):
            for ydiff in range(-2,3):
                x,y= bot.x + xdiff, bot.y + ydiff
                if self.in_bounds((x, y)) and self.targets[index] == visible_board[x][y].get_line():
                    if visible_board[x][y].is_end_of_line():
                        end_line = (x, y)
                    if visible_board[x][y].get_num_bots() >= 3:
                        line_full = True
        if end_line != None:
            return self.shortest_path((bot.x, bot.y), end_line)
        elif line_full:
            return self.shortest_path((bot.x, bot.y), self.lines[self.targets[index]][1])
        else:
            return None


class MyPriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)

    def isEmpty(self):
        return len(self._queue) == 0

class MaxPriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)

    def isEmpty(self):
        return len(self._queue) == 0
