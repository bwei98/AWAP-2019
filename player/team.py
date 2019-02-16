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

class Team(object):
    def __init__(self, initial_board, team_size, company_info):
        """
        The initializer is for you to precompute anything from the
        initial board and the company information! Feel free to create any
        new instance variables to help you out.

        Specific information about initial_board and company_info are
        on the wiki. team_size, although passed to you as a parameter, will
        always be 4.
        """
        self.board = initial_board
        self.team_size = team_size
        self.team_name = "Player 2"# Add your team name here!

        compAsList = [ [k,v] for k, v in company_info.items() ]
        compAsList.sort(key = lambda x: -x[1])
        self.sorted = compAsList
        self.company_info = company_info
        self.booths = dict()
        for i in range(len(initial_board)):
            for j in range(len(initial_board[0])):
                tile = initial_board[i][j]
                if tile.get_booth() != None:
                    self.booths[(i,j)] = tile.get_booth()
        print(self.booths)

    def shortestpath(sourcetile,desttile,visible_board):
        

        moveup = False
        movedown = False
        moveleft = False
        moveright = False
        if desttile[0] < sourcetile[0]:
            moveup = True
        else:
            movedown = True
        if destile[1] < sourcetile[1]:
            moveleft = True
        else:
            moveright = True
        if moveup and moveright:
            uptile = visible_board[inputx+1][inputy]
            righttile = visible_board[inputx][inputy]



        """
        Input: Source coordinates, Destination Coordinates
        Output: Direction to move in
        """



    def step(self, visible_board, states, score):
        """
        The step function should return a list of four Directions.

        For more information on what visible_board, states, and score
        are, please look on the wiki.
        """

        moves = [0,0,0,0]

        for index in range(4):
            bot = states[index]
            if bot.line_pos != -1:
                moves[index] = Direction.NONE
            elif visible_board[bot.x][bot.y].get_line() != None:
                moves[index] = Direction.ENTER
            else:
                moves[index] = Direction.UP


        return moves
