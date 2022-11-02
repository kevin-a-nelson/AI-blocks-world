from state import State

initial_state = State()
initial_state_blocks = initial_state.create_state_from_file("input.txt")

print([(i, i.on, i.on.id) for i in initial_state_blocks])