import sys  # quit
import pygame
import copy
import random
import numpy as np
from constraint import *


#pygame setup

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(bg_color)

class Board:

    def __init__(self):
        self.squares=np.zeros((rows,cols))
        # self.mark_sqr(1,1,2)
        # print(self.squares)
        self.empty_sqrs=self.squares
        self.marked_sqrs=0

    def final_state(self,show=False):
        # return 0 if there is no win
        #return 1 if player1 wins
        # return 2 if player2 wins1

        #vertical wins
        for col in range(cols):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                if show:
                    color=cir_color if self.squares[0][col]==2 else cross_color
                    ipos=(col*sqsize+sqsize//2,20)
                    fpos=(col*sqsize+sqsize//2,HEIGHT-20)
                    pygame.draw.line(screen,color,ipos,fpos,linewidth)
                return self.squares[0][col]  # return player number
            
        #horizontal
        for row in range(rows):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                if show:
                    color=cir_color if self.squares[row][0]==2 else cross_color
                    ipos=(20,row*sqsize+sqsize//2)
                    fpos=(WIDTH-20,row*sqsize+sqsize//2)
                    pygame.draw.line(screen,color,ipos,fpos,linewidth)
                return self.squares[row][0]  # return player number
            
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0:
            if show:  
                color=cir_color if self.squares[1][1]==2 else cross_color
                ipos=(20,20)
                fpos=(WIDTH-20,HEIGHT-20)
                pygame.draw.line(screen,color,ipos,fpos,linewidth)
            return self.squares[1][1]
        
        if self.squares[2][0]==self.squares[1][1]==self.squares[0][2]!=0:
            if show:
                color=cir_color if self.squares[1][1]==2 else cross_color
                ipos=(20,HEIGHT-20)
                fpos=(WIDTH-20,20)
                pygame.draw.line(screen,color,ipos,fpos,linewidth)
            return self.squares[1][1]
        
        return 0


    def mark_sqr(self,row,col,player):
        self.squares[row][col]=player
        self.marked_sqrs+=1

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0
    

    #for AI
    def get_empty_sqrs(self):
        empty_sqrs=[]

        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))

        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs==9
    
    def isempty(self):
        return self.marked_sqrs==0
    
    
class AI:

    def __init__(self,level=1,player=2):   #level=0 random level=1 minimax
        self.level=level
        self.player=player


    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        idx=random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx]
    

    
    def minimax(self,board,maximizing):
        # terminal casea
        case=board.final_state()

        #player1 wins

        if case==1:
            return 1,None     # eval ,move
        
        #player2 wins

        if case==2:
            return -1,None
        
        elif board.isfull():
           return 0,None
        
        if maximizing:
            max_eval=-100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval=self.minimax(temp_board,False)[0]
                if eval>max_eval:
                    max_eval=eval
                    best_move=(row,col)
        
            return max_eval,best_move
        
        elif not maximizing:
            min_eval=100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval=self.minimax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
        
            return min_eval,best_move



    def eval(self,main_board):
        if self.level==0:
            #random choice
            eval='random'
            move=self.rnd(main_board)
        else:
            #minimax algo choice
            eval,move=self.minimax(main_board,False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of:{eval}')

        return move
    
class Game:
    
    def __init__(self):  # whenever new game object created this method call
        self.ai=AI()
        self.board=Board()    #console board
        self.player=1     # player1= cross player2=circle
        self.gamemode='ai' # pvp or AI
        self.running=True
        self.show_lines()

    

    def show_lines(self):

        screen.fill(bg_color)
        #vertical
                                            #start pos  #end pos
        pygame.draw.line(screen,line_color,(sqsize,0),(sqsize,HEIGHT),linewidth)
        pygame.draw.line(screen,line_color,(WIDTH-sqsize,0),(WIDTH-sqsize,HEIGHT),linewidth)

        #horizontal
        pygame.draw.line(screen,line_color,(0,sqsize),(WIDTH,sqsize),linewidth)
        pygame.draw.line(screen,line_color,(0,HEIGHT-sqsize),(WIDTH,HEIGHT-sqsize),linewidth)


    def next_turn(self):
        self.player=self.player%2+1    
    
    def draw_fig(self,row,col):
    
        if self.player==1:
            #des line
            start_des=(col*sqsize+offset,row*sqsize+offset)
            end_des=(col*sqsize+sqsize-offset,row*sqsize+sqsize-offset)
            pygame.draw.line(screen,cross_color,start_des,end_des,cross_width)
            #asc line
            start_asc=(col*sqsize+offset,row*sqsize+sqsize-offset)
            end_asc=(col*sqsize+sqsize-offset,row*sqsize+offset)
            pygame.draw.line(screen,cross_color,start_asc,end_asc,cross_width)

        elif self.player==2:
            center=(col*sqsize+sqsize//2,row*sqsize+sqsize//2)
            pygame.draw.circle(screen,cir_color,center,radius,cir_width)


    
    def change_gamemode(self):
        if self.gamemode=='pvp': self.gamemode='ai'
        else:
            self.gamemode='pvp'
    
    def isover(self):
        return self.board.final_state(show=True)!=0 or self.board.isfull()
    def reset(self):
        self.__init__()



def main():
    
    game=Game()  #object

    board=game.board
    ai=game.ai

    while True:

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:

                #g=gamemode

                if event.key==pygame.K_g:
                    game.change_gamemode()
                  
                #restart 
                if event.key==pygame.K_r:
                    game.reset()
                    board=game.board
                    ai=game.ai

                if event.key==pygame.K_o:
                    ai.level=0
                
                if event.key==pygame.K_1:
                    ai.level=1
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//sqsize
                col=pos[0]//sqsize
                # print(row,col)

                if board.empty_sqr(row,col) and game.running:
                    board.mark_sqr(row, col, game.player)
                    game.draw_fig(row, col)
                    game.next_turn()
                    
                    # print(board.squares)
                # print(game.board.squares)
            
                    if game.isover():
                        game.running=False
                

        if game.gamemode=='ai' and game.player==ai.player and game.running:
            pygame.display.update()    

            row,col=ai.eval(board)
            board.mark_sqr(row, col, ai.player)
            game.draw_fig(row, col)
            game.next_turn()
          
            if game.isover():
                game.running = False

        pygame.display.update()    

main()
