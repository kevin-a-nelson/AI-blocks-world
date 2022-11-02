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

  def SortHeur(self, CurrentListList, Weight, GoalListList, HIL):
    #Look at Goal State, grab base blocks place in search space (list)
    #Examine the top of CurrentListList, find base, or highest cost if in the list (so break ties based on cost), unstack
    #If not on top of stack, search one lower.
    que = []
    for stack in GoalListList:
      que.append(stack[0])  #Append base blocks to the que.
    #que will get the block on top of a base when it is found, the desired neighbor <-expensive is finding the neighbor again->

    FoundblockIndex, FoundStack =-1 #default.
    FoundLayer =0
    
    layer = -1  #first layer of stacks (top of stacks)
    while (que != []):
      for stack in range(len(CurrentListList)):
        if len(stack) > abs(layer):  #stack still has blocks to check
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
    if HIL[FoundStack][FoundLayer][4]==None: #(ID, H, on, under):

      
        #Search for appropraite 'on'
        blockTup=HIL[FoundStack].pop(-1) #Pop end of list. 
        if blockTup[3]==None: #Tupple says this block is ON NONE so on table
          #on table, putdown
          CurrentListList[FoundStack].pop(-1) #pop end of list
          CurrentListList.append([blockTup[0]]) #New stack
          HIL.append([blockTup]) #New stack
        else:
          pass
          #go through each stack, checking whether the end of each stack  matches the desired ON.
          
          
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

  def underBlock(self, blockID, ListList):
    for stack in ListList:
      for block in range(len(stack)):
        if stack[block] == blockID:
          if block < len(stack) - 1:
            print("return", stack[block + 1])
            return stack[block + 1]
          else:
            return None
    return None

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

    #Built such that we will always have the stack built from the base up, or added on top of the base.
    #Takes approx. O(3n) time (+1 for each if statement which will always be evaluated, could double for the append that always will happen)
    #NOTE: Potential improvement would be 'if node not in stack', instead of adding on top of a stack when we come across, do a recursive up the stack until clear=True, that way we only have two if statements. this requires the blocks knowing whats above them, but they don't currenlty have that.

    accounted = False  #if the block is in, or added to the list.
    InitialListList = []
    GoalListList = []

    #Hackathon in march, linux ladies.
    #Check on.id == table?

    for block in self.initial_state:
      if block.on != None:  #so Table, and unused blocks are ignored!
        accounted = False
        print("Init List: ", block)
        if (len(InitialListList) == 0):
          if (block.id == "table"):
            continue
          InitialListList.append(self.Helper(block))
        else:
          print("Len of InitialListList is ", len(InitialListList))
          for stack in InitialListList:
            print("stack is ", stack)
            if block.id in stack:  #in a stack
              print("Block already in a stack")
              accounted = True
              break
            if stack[-1] == block.on.id:  #place top of stack
              print("Block placed on top of stack")
              stack.append(block.id)
              accounted = True
              break
          if accounted == False:  #not in stacks
            print("Make a new stack")
            InitialListList.append(self.Helper(block))
            #accounted = False
          accounted = False

    for block in self.goal_state:
      if block.on != None:
        accounted = False
        print("Goal List: ", block)
        if (len(GoalListList) == 0):
          if (block.id == "table"):
            continue
          GoalListList.append(self.Helper(block))
        else:
          print("Len of GoalListList is ", len(GoalListList))
          for stack in GoalListList:
            print("stack is ", stack)
            if block.id in stack:  #in a stack
              print("Block already in a stack")
              accounted = True
              break
            if stack[-1] == block.on.id:  #place top of stack
              print("Block placed on top of stack")
              stack.append(block.id)
              accounted = True
              break
          if accounted == False:  #not in stacks
            print("Make a new stack")
            GoalListList.append(self.Helper(block))
            #accounted = False
          accounted = False
        #Reset for next block/list
        accounted = False
        #Repeat for goal list list

    print("Init:", InitialListList)
    print("Goal:", GoalListList)

    #J: Assign heuristic cost of blocks from Goal State, in tupple form (id, h) . Faster to assign afterwards since the stacks change size.
    n = 1
    HGoalList = []
    HInitialList = []  #Khan wanted the initial costs for 'moveability' heursitic, though J thinks that the problem only cares about the order at the end, so movability is inevitable based on the cost and valuation, but we can experiment with large cases.
    for stack in GoalListList:
      for blockIDindex in range(len(stack)):
        HGoalList.append(
          (stack[blockIDindex], len(stack) - n,
           ifelse(blockIDindex != 0, stack[blockIDindex - 1], "Table"))
        )  #Assign tupples with the initial weight heuristic (Amount of blocks on top of a given block id)
        n + 1
      n = 1
    for stack in InitialListList:
      for blockID in stack:
        ontop = State.find(self.goal_state, blockID).on
        under = self.underBlock(blockID, GoalListList)
        print("Append",
              (blockID, len(stack) - n, ifelse(ontop == None, "Table",
                                               ontop.id), under))
        HInitialList.append(
          (blockID, len(stack) - n, ifelse(ontop == None, "Table",
                                           ontop.id), under))

        n + 1
      n = 1

  #NOTE Jacob Left off here. Check if it works later. Gotta make a quick TOH visit for a class. Then adivsory meeting.
  #Arguments, current state (list of lists), weight of each block (HInitialList). Initial search Space (drawn from goal state). Goal state (Goal list of list).

    n = 1
    HGoalList = []
    for stackIndex in range(len(GoalListList)):
      HGoalList.append([])
      for blockIDindex in range(len(GoalListList[stackIndex])):
        under = self.underBlock(GoalListList[stackIndex][blockIDindex],
                                GoalListList)
        print(
          "Append ", HGoalList[stackIndex].append(
            (GoalListList[stackIndex][blockIDindex],
             len(GoalListList[stackIndex]) - n,
             ifelse(blockIDindex != 0,
                    GoalListList[stackIndex][blockIDindex - 1], None), under))
        )  #Assign tupples with the initial weight heuristic (Amount of blocks on top of a given block id)
        n + 1
      n = 1

    CurrentState = InitialListList
    GoalState = GoalListList
    Heuristic = HGoalList
    print(CurrentState)
    print(GoalState)
    print(Heuristic)

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
