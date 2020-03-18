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
import math

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

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.action_list = [];
        for i in range(0,5):
            self.action_list.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP
        all_actions=[]
        score=-100
        root=state
        terminate=False
        bestactions=[(None,-100)]
        if state.isWin():
             return
        all_actions=root.getAllPossibleActions()
        #initialize actions with random actions
        for i in range(0,len(self.action_list)):
                    self.action_list[i]=all_actions[random.randint(0,len(all_actions)-1)]
        # randomly generating next sequence
        while terminate is False:
            localscore=0
            next_action_sequence=self.action_list[:]
            for i in range(0,len(self.action_list)):
                if random.randint(0, 1) == 1:    #probability 50%
                    next_action_sequence[i]=all_actions[random.randint(0,len(all_actions)-1)]
            current=state
            for i in range(0,len(next_action_sequence)):
                if current.isWin() + current.isLose() == 0:
                    new_prev=current
                    current=current.generatePacmanSuccessor(next_action_sequence[i])
                    if current is None:
                        current=new_prev
                        terminate=True
                        break
                else:
                    break
            localscore=gameEvaluation(state,current)
            #print 'localscore is:',localscore
            #comparing new score with bestscore 
            if localscore >= score and localscore >=bestactions[len(bestactions)-1][1]:
                 score=localscore
                 bestactions.append((next_action_sequence[:],score))
                 self.action_list=bestactions[len(bestactions)-1][0][:]
        return bestactions[len(bestactions)-1][0][0]        
        #return Directions.STOP

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.action_list = [];
        for i in range(0,5):
            self.action_list.append(Directions.STOP);
        return;
    
    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        population=[]
        terminate=False
        bestscore=-100
        bestactions=[(None,-100)]
        #initializing population with random candidate solution
        all_actions=state.getAllPossibleActions()
        for i in range(0,8):
            #candidate_solution=[]
            for j in range(0,len(self.action_list)):
                #candidate_solution.append(all_actions[random.randint(0,len(all_actions)-1)])
                self.action_list[j]=all_actions[random.randint(0,len(all_actions)-1)]
            #population.append(candidate_solution[:])
            population.append(self.action_list[:])
        #print 'inital population is:',population
        while terminate is False:
            #evaluate fitness of candidates
            fitness_population=[]
            for i in range(0,len(population)):
                root=state
                fitness_score=0
                for j in range(0,len(self.action_list)):    
                    if root.isWin() + root.isLose() == 0:
                        prev=root
                        root=root.generatePacmanSuccessor(population[i][j])
                        if root is None:
                            root=prev
                            terminate=True
                            break
                    else:
                        break    #can be removed 
                fitness_score=gameEvaluation(state,root)
                fitness_population.append((population[i][:],fitness_score))

            #sorting the population based on fitness
            fitness_population=sorted(fitness_population,key=lambda x:x[1],reverse=True)
            highestpopulationscore = fitness_population[0][1]
            highestpopulation=fitness_population[0]
            if (highestpopulationscore >=bestscore and highestpopulationscore>=bestactions[len(bestactions)-1][1]):
                bestscore=highestpopulationscore
                bestactions.append(fitness_population[0][:])

            offspring=[]
            for i in range(0,4):
                rand1 = random.randint(0,35)
                rand2 = random.randint(0,35)
                #generating rank
                rank1=self.rank(rand1)    
                rank2=self.rank(rand2)
                while(rank1==rank2):    #needed to generate unique parents
                    rand2 = random.randint(0,35)
                    rank2 = self.rank(rand2)
                #selecting parents
                parent1=fitness_population[rank1][0][:]
                parent2=fitness_population[rank2][0][:]

                #cross-over operation
                child1=[]
                child2=[]
                #print 'parent1:',parent1
                #print 'parent2:',parent2
                rand_test_crossover = random.randint(1,10)
                if rand_test_crossover <= 7:    #perform only when P >70%
                    for i in range(0,5):
                        next_test = random.randint(0,1)
                        if next_test==0:
                            child1.append(parent1[i])
                            child2.append(parent2[i])
                        elif next_test==1:
                            child1.append(parent2[i])
                            child2.append(parent1[i])
                    offspring.append(child1[:])
                    offspring.append(child2[:])
                else:
                    offspring.append(parent1[:])
                    offspring.append(parent2[:])
            
            
            #mutation -only after total 8 offspring generated
            for i in range(0,len(offspring)):
                rand_test_mutation = random.randint(1,10)
                if rand_test_mutation <=1:
                    random_action=random.randint(0,4)
                    offspring[i][random_action]=all_actions[random.randint(0,len(all_actions)-1)]
        
            population= offspring
            #print 'bestaction array:',bestactions
            #print 'bestaction returned:',bestactions[len(bestactions)-1]
            bestaction = bestactions[len(bestactions)-1][0]
            #print 'bestaction:',bestaction
        return bestaction[0]

    def rank(self,number):
        if number in range(0,7):
            return 7
        elif number in range(8,14):
            return 6
        elif number in range(15,20):
            return 5
        elif number in range(21,25):
            return 4
        elif number in range(26,29):
            return 3
        elif number in range(30,32):
            return 2
        elif number in range(33,34):
            return 1
        else:
            return 0
        
        
               

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        root=state
        bestactions={}
        curr = Node(None)#Node(visitedcount,parent,score,action,children)
        #generating next children for root
        main_action=root.getLegalPacmanActions()
        #print 'actions:',main_action
        for i in main_action:
            nextchild=self.treePolicy(curr,root)
            if nextchild is None:
                break
            else:
                continue
            delta= self.defaultRollout(nextchild,root)
            self.backup(nextchild,delta)
        #checking for most visited node for root 
        max_visited = max([i.visited for i in curr.children])
        #returning action for most visited node

        bestactions = [k.action for k in curr.children if k.visited==max_visited]
        return bestactions[0]

    def defaultRollout(self,node,state):
        #rollout function upto 5 states
        #current=state
        all_actions=[]
        score=0
        current=node
        path=[]
        while current.parent is not None:
                path.append(current)
                current=current.parent
        path=path[::-1]
        current_state=state
        for i in path:
                prev=current_state
                current_state =current_state.generatePacmanSuccessor(i.action)
                if current_state is None:
                    current_state=prev
                    self.backup(i,gameEvaluation(state,prev))
                    return None
                if current_state.isWin():
                    self.backup(i,gameEvaluation(state,prev))
                    return 1
                if current_state.isLose():
                    self.backup(i,gameEvaluation(state,prev))
                    return 1
        

        for i in range(0,5):
            if current_state.isWin() + current_state.isLose() == 0:
                all_actions=current_state.getLegalPacmanActions()
                current_action=all_actions[random.randint(0,len(all_actions)-1)];
                prev=current_state
                current_state = current_state.generatePacmanSuccessor(current_action);
                if current_state is None:
                   current_state=prev
                   break
            else:
                break
        score=gameEvaluation(state,current_state)
        return score

    def treePolicy(self,node,root):
        #tree policy
        #getting the current state
        #print 'in tree policy'
        current=node
        path=[]
        terminate=False
        curr=node
        while terminate is False:
            while current.parent is not None:
                path.append(current)
                current=current.parent
            path=path[::-1]
            current_state=root
            for i in path:
                prev=current_state
                current_state =current_state.generatePacmanSuccessor(i.action)
                if current_state is None:
                    current_state=prev
                    terminate=True
                    break
            legal_actions=current_state.getLegalPacmanActions()
            if not (len(legal_actions)) == len(node.children):#not fully expanded
                #print 'in expansion'
                return self.expansion(node,root)
            else:
                #print 'select child'
                curr= self.bestChild(node)
        return curr
                    
    def backup(self,node,reward):
        #propagating the score back
        v=node
        while v is not None :
            v.visited=v.visited+1
            v.score=v.score + reward
            v= v.parent
        return

    def expansion(self,node,state):
        #expanding
        current_node=node
        path=[]
        #getting the curent state
        while current_node.parent is not None:
            path.append(current_node)
            current_node=current_node.parent
        path=path[::-1]
        current_state=state
        for i in path:
            prev=current_state
            current_state=current_state.generatePacmanSuccessor(i.action)
            if current_state is None: #reached terminal so backpropagate
                self.backup(i,gameEvaluation(state,prev))
                return None
            if current_state.isWin():
                self.backup(i,gameEvaluation(state,prev))
                return 1
            if current_state.isLose():
                self.backup(i,gameEvaluation(state,prev))
                return 1
    
        actions=current_state.getLegalPacmanActions()
        #untried actions implement
        triedactions = [j.action for j in node.children]
        for i in actions:
            if i not in triedactions:
                    node.children.append(Node(i,node)) #adding new child
                    break          
        return node.children[-1]
            
            
    def bestChild(self,node):
        # computing UCT scores and returning best children
        v=node
        bestscore=-100
        bestchild=[]
        s=0
        for i in v.children:
                    a= i.score / i.visited
                    b= 1 * (math.sqrt((2*math.log(i.visited)) / i.visited))
                    s = a + b
                    if (s > bestscore):
                         bestscore=s
                         bestchild=[i]
                    elif (s==bestscore):
                        bestchild.append(i)
        return bestchild[len(bestchild)-1]

class Node():
        def __init__(self,action,parent=None):
            self.children=[]
            self.visited=1
            self.action=action
            self.parent=parent
            self.score=0
        

                    
                    
                
    
     
                    
        
            
            
            
            
        
