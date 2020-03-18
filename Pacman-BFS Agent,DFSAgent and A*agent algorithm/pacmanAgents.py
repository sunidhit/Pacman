# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        print 'best score is:',bestScore
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        frontier=[]
        frontier.append(state)
        explored=[state]
        score={}
        if state.isWin() :
                 return 'you win'
        while (len(frontier)):
            node=frontier.pop(0) 
            legal = node.getLegalPacmanActions()
            successors = [( node.generatePacmanSuccessor(action), action) for action in legal]
            for state in successors:
                #print 'child direction is:' ,state[1]
                child=state[0]
                actiontochild=state[1]
                if child!=None:
                        if child not in explored or frontier or score:
                            if child.isWin(): #new change if added
                                return actiontochild
                            if child.isLose():
                                continue
                            frontier.append(child)
                            cost=admissibleHeuristic(child)   #finding the score for eacch child node and its action if not visited
                            score[child]=(cost,actiontochild,node)
                            explored.append(child)
                if child==None:
                        leaststate= min(score.items(),key=(lambda x:x[1]))
                        direction=leaststate[1][1]
                        return direction

                    
                                              
            
                
                             
                    

class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        frontier=[state]
        explored=[]
        path={}
        path[state]=None,None
        score={}
        if state.isWin():
            return 'you win'
        while (frontier):
            node=frontier.pop(len(frontier)-1)
            if node.isWin():
                print 'you won'
            if node in explored:
                continue
            explored.append(node)
            legalactions=node.getLegalPacmanActions()
            successorsdfs=[(node.generatePacmanSuccessor(action), action) for action in legalactions]
            for state in successorsdfs:
                nextstate=state[0]
                if nextstate not in frontier:
                    if state[0]!=None:
                        frontier.append(state[0])
                        path[state[0]]=state[1]# path contains the direction
                        cost=(admissibleHeuristic(state[0]),state[1])   #finding the score for eacch child node and its action if not visited
                        score[state[0]]=(cost,state[1],node)
                    if state[0]==None:
                        leaststatescore=min(score.items(),key=(lambda x:x[0]))
                        return leaststatescore[1][1]
    
        
 
                    

                        
 
 
 
                                       
        

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        search=[(state,0,0,None)]
        path=[]
        closed=[]
        g=0
        h=0
        f=0
        while (len(search)):
            leastcoststate=search.pop(0)
            leastcostnode=leastcoststate[0]
            fvalue=leastcoststate[1]
            gvalue=leastcoststate[2]
            allowedactions = leastcostnode.getLegalPacmanActions()
            childs=[(leastcostnode.generatePacmanSuccessor(action), action) for action in allowedactions]
            for nextchild in childs:
                child=nextchild[0]
                actiontochild=nextchild[1]
                if child is not None:
                    if child.isWin():
                        return actiontochild
                    g=gvalue+1
                    h=admissibleHeuristic(child)
                    f=g+h
                    for opennode in search:
                        if opennode[0]==child and f>opennode[1]:
                            continue
                    for closednode in closed:
                        if closednode[0]==child and f>closednode[1]:
                            continue
                    search.append([child,f,g,actiontochild])
                    path.append([child,f,g,actiontochild])
                if child is None:
                    #minstate = min(search)
                    #minstate=search.sort(key=lambda x:x[1])
                    minstate = sorted(path, key=lambda x:x[1])
                    return minstate[0][3]
            closed.append([leastcostnode,fvalue,gvalue])
            
