###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State


def ifelse(x, t, f):
  if (x):
    return t
  else:
    return f


class Plan:


  

  def ListList(self):
  #Creates the listlist for the initial and goal. this helps us quickly move around blockid's around stacks without having to access the actual objects and track down neighbors. Expensive to set up, however once it's set up it's free to use for the rest of hte plan. 
    
    accounted = False  #if the block is in, or added to the list.
    InitialListList = []
    GoalListList = []
  
    #Hackathon in march, linux ladies.
    #Check on.id == table?
    for block in self.initial_state:
      if block.on != None:  #so Table, and unused blocks are ignored!
        accounted = False 
        if (len(InitialListList) == 0):
          if (block.id == "table"):
            continue
          InitialListList.append(self.Helper(block))
        else:
          
          for stack in InitialListList:
             
            if block.id in stack:  #in a stack 
              accounted = True
              break
            if stack[-1] == block.on.id:  #place top of stack 
              stack.append(block.id)
              accounted = True
              break
          if accounted == False:  #not in stacks 
            InitialListList.append(self.Helper(block))
            #accounted = False
          accounted = False
  
    for block in self.goal_state:
      if block.on != None:
        accounted = False 
        if (len(GoalListList) == 0):
          if (block.id == "table"):
            continue
          GoalListList.append(self.Helper(block))
        else: 
          for stack in GoalListList: 
            if block.id in stack:  #in a stack 
              accounted = True
              break
            if stack[-1] == block.on.id:  #place top of stack 
              stack.append(block.id)
              accounted = True
              break
          if accounted == False:  #not in stacks 
            GoalListList.append(self.Helper(block))
            #accounted = False
          accounted = False
        #Reset for next block/list
        accounted = False
        #Repeat for goal list list
  
  
    return InitialListList, GoalListList

  def underBlock(self, blockID, ListList):
    #Find the block which is under our current blockID
    for stack in ListList:
      for block in range(len(stack)):
        if stack[block] == blockID:
          if block < len(stack) - 1:
            print("return", stack[block + 1], " amt: ", len(stack)-block)
            return stack[block + 1], len(stack)-(block+1) 
          else:            
            print("Return ", " None") #Represents under nothing
            return None, 0
    print("Error, expected: ",blockID, " In ", ListList)
    return None, -1

  def Helper(self, blockcp):
    if blockcp.id != 'table':  #Check if on table is correct
      print("Block ", blockcp, " not on table")

      huh = self.Helper(State.find(self.initial_state, blockcp.on.id))

      print("Show recursive list stack")
      huh.append(blockcp.id)
      for i in huh:
        print(i)

      return huh

    else:
      print("Block is table")
      return []
      #This may not be correct, might require passing in the list

    #In helper, add a seperate function that calculates the price of goal (underblock) and (overblock)

   
    
  def Heur(self, InitListList, GoalListList):
    retList=[]
    
    
    for stackIndex in range(len(InitListList)):
      retList.append([])
      n=1 
      for blockID in InitListList[stackIndex]:
        ontop = State.find(self.goal_state, blockID).on
        print(blockID,"Is on", ontop)
        under, underAmt = self.underBlock(blockID, GoalListList) #Block Id of what the block is under
        Hinit=len(InitListList[stackIndex])-n
        Hgoal=underAmt 
        print("Append", (blockID, Hinit, Hgoal ,ifelse(ontop.id == "table", None, ontop.id), under))
        retList[stackIndex].append(
          (blockID, Hinit, Hgoal,ifelse(ontop.id == "table", None, ontop.id), under))
        #(BlockID, blocks above in init, blocks above in goal, goalblock on, goalblock under) (id, Hinit, Hgoal, on, under)

        n=n + 1 
      n=1
      
    return retList  
       
   
  
  
  def SortHeur(self, CurrentListList, GoalListList, HIL):
    #Look at Goal State, grab base blocks place in search space (list)
    #Examine the top of CurrentListList, find base, or highest cost if in the list (so break ties based on cost), unstack
    #If not on top of stack, search one lower.
    que = []
    for stack in GoalListList:
      que.append(stack[0])  #Append base blocks to the que.
    #que will get the block on top of a base when it is found, the desired neighbor <-expensive is finding the neighbor again->

     
    
     
    while (que != []):
      FoundblockIndex, FoundStack =-1 #default. BlockIndex describes what to remove from the que.
      FoundLayer =0 # 
      layer = -1  #first layer of stacks (top of stacks)
      print(CurrentListList)
      for stack in range(len(CurrentListList)):
        if len(stack) < abs(layer):  #stack has no more blocks to check
          continue
        else:
          for blockIndex in range(len(que)):
            if stack(layer)==que[blockIndex]:
              FoundLayer=layer
              FoundStack=stack
              FoundblockIndex=blockIndex
              
              break; #Record layer and index
            else:
              #in a lower layer must be
              layer=layer-1
            
          #if block in stack[layer] in que, record the stack, and layer. then break.
          #else lower the layer

          #Now that we found a block from the que.
          #If the layer!=-1, then we have blocks to move from atop it.
          #As the block was a layer down, we simply move any block atop to the table.
          #If the layer == -1, then we know we have an appropriate place to put the block
          #For every stack, besides the one we took the block from search for, from the HIL (blockID, herusitic, over, under), so search for 'over', if None or Table we just make a new list. Then add the 'under' to the Que.
          #If there is no 'under' then we don't expand the que, and we know that stack is finished, so we can safely remove that from the current listlist, and the mathcing stack from our goal listlist (but this is optional and only improve sthe runtime)
          print()

    #Note that during the above execution, we are only manipulating a list of lists with block ID's, however we can still call the needed unstacks, stack, put on table,, etc functions we would want to do to the classes 'current state'. By the end of execution we'd expect (if all goes well) the goallistlist, initiallistlist, self.current_state, and our Hlist to match with our goal state.

    #Note: Can imporve structure a bit by providing tupples with values describing end state (layer) desired, and node above it desired (id.under).
    #Note: Can improve structure by having initial_list, and current list with current list pruned to not include locations already properly stacked. in this case we use current list as our 'space' to search, with our que on bases not accounted for, and such, and use initial list to inform where it should go, (since we'd only be looking at the ends of each list or making an ew one, and popping the list until found, the popping happens in current list until item is removed. Happens in same amount as initial list, except the current list no longer has the removed item, but has all other items remveod by the search as new sub lists.).

    
    #Look in tuple HIL for 
      
    #Under nothing currenlty (layer=-1), so it is clear to move whenever/however we want.
      if FoundLayer==-1:    
        ProperPlace(CurrentListList, HIL, FoundStack, FoundblockIndex, FoundLayer) 
        #Remove from que the Blockid, add to Que whatever it wants on top.
        
        #Search for appropraite 'on'
        blockTup=HIL[FoundStack].pop(FoundLayer) #Pop end of list. 
        if blockTup[3]==None: #Tupple says this block is ON NONE so on table
          #on table, putdown
          CurrentListList[FoundStack].pop(FoundLayer)
          CurrentListList.append([blockTup[0]]) #New stack
          HIL.append([blockTup]) #New stack
        else:
          #Not worth skipping found stack
          for stack in range(len(CurrentListList)):  
            CurrentListList[FoundStack].pop(-1) #pop end of list
            if stack[-1]==blockTup[3]: #block should be on, 
              CurrentListList[stack].append(blockTup[0]) #Putblock on that stack
              HIL[stack].append(blockTup)
                 
            
            
      else:
            #The block is under another block, Recurisvely check 'is this block under?' always unstack to table recursively.
          InitLayer=FoundLayer
          while(InitLayer!=-1):
            CurrentListList[FoundStack].pop(-1) #pop end
            CurrentListList.append([blockTup[0]]) #New stack
            blockTup=HIL[FoundStack].pop(-1)
            HIL.append([blockTup]) #New stack
            InitLayer=InitLayer+1
          #now we can do the above.
            #If on none, add to table
            #If on ID, add to stack with ID at -1.
            
      
    
    return None

  
  
  def __init__(self, initial_state, goal_state):
    """
        Initialize initial state and goal state
        :param initial_state: list of blocks in the initial state
        :type initial_state: list of block.Block objects
        :param goal_state: list of blocks in the goal state
        :type goal_state: list of block.Block objects
        """
    self.initial_state = initial_state
    self.goal_state = goal_state

  #***=========================================
  # First implement all the operators
  # I implemented two operators to give you guys an example
  # Please implement the remainder of the operators
  #***=========================================

  def putdown(self, block1):
    """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """

    # get table object from initial state
    table = State.find(self.initial_state, "table")

    if block1.air:
      block1.on = table
      block1.clear = True
      block1.air = False  #added.

  def unstack(self, block1, block2):
    """
        Operator to unstack block1 from block 2

        :param block1: block1 to unstack from block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: None
        """

    # if block1 is clear safe to unstack
    if block1.clear:

      # block1 should be in air
      # block1 should not be on block2
      # set block2 to clear (because block1 is in air)
      block1.clear = False
      block1.air = True
      block1.on = None

      block2.clear = True

  # ***=========================================
  # After you implement all the operators
  # The next step is to implement the actual plan.
  # Please fill in the sample plan to output the appropriate steps to reach the goal
  # ***=========================================

  def sample_plan(self):

     

    InitialListList, GoalListList =self.ListList() 
    #Returns listlist of initial state and goal state. 
    #Could simplify it more by taking a single state, but that's not required. Rather it's simpler to move the list along with the tuple and the actual state than to combine all the componenets.
    print("Init:", InitialListList)
    print("Goal:", GoalListList) 
    HInitialList=self.Heur(InitialListList, GoalListList) #Returns a list of lists of tupples that are in the order of the initial state, with tupples of (blockid, blocksunderInInit, blocksunderInGoal, ontopinGoalID, underinGoalID)
    
    CurrentState = InitialListList
    GoalState = GoalListList 
    print(CurrentState)
    print(GoalState)
    print(HInitialList)


    self.SortHeur(CurrentState, GoalState, HInitialList)
    #Thus function will find the base blocks, prioritize placing them on the table, then gradually expand the blocks in a que based on what is expected ontop of properly placed blocks (blocks that were moved from the que). 

    
    #Break
    # get the specific block objects
    # Then, write code to understand the block i.e., if it is clear (or) on table, etc.
    # Then, write code to perform actions using the operators (pick-up, stack, unstack).

    # Below I manually hardcoded the plan for the current initial and goal state
    # You must automate this code such that it would produce a plan for any initial and goal states.

    block_c = State.find(self.initial_state, "C")
    block_d = State.find(self.initial_state, "D")

    # Unstack the block
    self.unstack(block_d, block_c)

    # print the state
    action = f"unstack{block_d, block_c}"
    State.display(self.initial_state, message=action)

    # put the block on the table
    self.putdown(block_d)

    # print the state
    action = f"Putdown({block_d}, table)"
    State.display(self.initial_state, message=action)


if __name__ == "__main__":

  # get the initial state
  initial_state = State()
  initial_state_blocks = initial_state.create_state_from_file("input.txt")

  #display initial state
  State.display(initial_state_blocks, message="Initial State")

  # get the goal state
  goal_state = State()
  goal_state_blocks = goal_state.create_state_from_file("goal.txt")

  #display goal state
  State.display(goal_state_blocks, message="Goal State")
  """
    Sample Plan
    """

  p = Plan(initial_state_blocks, goal_state_blocks)
  p.sample_plan()
