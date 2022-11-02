###=================================================
# This file is where you need to create a plan to reach the goal state form the initial state
# This file must accept any combination of with the given blocks: A, B, C, D, E
# This file should also reach the final state of any combination with the blocks above
# It must also display all intermediate states
###=================================================

from state import State
from copy import deepcopy
#J: I think if we do A*


class Queue:
  """
  A priority queue to house all the states to be explored. 
  Each element in the queue: [f, state]
  Where f = h + n
  """

  def __init__(self):
    self.states = []

  def add(self, state, moved="none"):
    """
    Insert state into the priority queue based on f
    """
    copy = deepcopy(state)
    State.display(copy.blocks, message="Moving " + moved)
    # Currently assumes heuristic of 1. Will add actual heuristic later
    # To add: Binary Search into proper location in self.states
    # To add: A bunch of heuristics (Block positions from goal current GLOBAL WORLD)
    self.states.append([1, copy])

  # def gen_heuristic(self, state) ## Generate heuristic code here 
    # param: state to explore
    # return: final heuristic for the state 
  def dequeue(self):

    return self.states.pop(0)[1]

  def __str__(self):
    for i in self.states:
      State.display(i[1].blocks, message="Queue")
    return ""


class Plan:

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

  def putdown(self, block1, state="default"):
    """
        Operator to put the block on the table
        :param block1: block1 to put on the table
        :type block1: Object of block.Block
        :return: None
        """
    if state == "default":
      table = State.find(self.initial_state, "table")
    # get table object from initial state
    else:
      table = State.find(state.blocks, "table")

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

  def stack(self, block1, block2):
    """
      Operator to stack block 1 onto block 2
      
        :param block1: block1 to stack onto block2
        :type block1: Object of block.Block
        :type block2: Object of block.Block
        :return: True if operation successful, False otherwise
    """
    if block1.air and block2.clear and block2.type == 1:
      block1.clear = True
      block2.clear = False
      block1.on = block2
      block1.air = False
      return True
    return False

  def pickup(self, block1):
    """
      Operator to pickup block1 from table
      
      :param block1: block1 pickup from table
      :type block1: Object of block.Block
      :return: True if operation successful, False otherwise
    """

    if block1.on.id == "table" and block1.clear and not block1.air:
      block1.air = True
      block1.clear = False
      return True
    return False

  def makecopy(self, id):
    """
      To make copy of the given state before operating on a block. 

      :param id: id of block about to be moved
      :return: Tuple: (block object in the new copy, new copy of state)
    """
    copy_state = deepcopy(self.given_state)
    return State.find(copy_state.blocks, id), copy_state

  def move(self, block1):
    """
      Explore all ways to move a given block1, using the 4 operators.

      :param block1: block to be moved
      :return: None
    """
    assert block1.clear

    if block1.on.id == "table":  # ways to move a block that is on a table

      block, copy_state = self.makecopy(block1.id)

      self.pickup(block)
      for b in copy_state.blocks:
        if b.id == block.id:
          continue
        if self.stack(block, b) and [1, copy_state] not in self.q.states:
          self.q.add(copy_state, block.id + " to " + b.id)
          self.unstack(block, b)

    else:  # ways to move a block on a stack
      block, copy_state = self.makecopy(block1.id)
      self.unstack(block, block.on)
      for b in copy_state.blocks:
        if b.id == block.id:
          continue
        if self.stack(block, b) and [1, copy_state] not in self.q.states:
          self.q.add(copy_state, block.id + " to " + b.id)
          self.unstack(block, b)
      if self.putdown(block, copy_state) and [1, copy_state
                                              ] not in self.q.states:
        self.q.add(copy_state, block.id + "to table")
        self.pickup(block)

  # ***=========================================
  # After you implement all the operators
  # The next step is to implement the actual plan.
  # Please fill in the sample plan to output the appropriate steps to reach the goal
  # ***=========================================

  def sample_plan(self):
    self.q = Queue()
    self.q.add(self.initial_state)

    # So far goes only searches one level deep and prints search results.
    while True:
      self.given_state = self.q.dequeue()
      for block in self.given_state.blocks:
        if not block.clear:
          continue
        self.move(block)
      # print(self.q)
      break


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

  p = Plan(initial_state, goal_state)
  p.sample_plan()
