const interpret = (perception) => {
  return perception;
};

const actions = () => {
  const possibleActions = [
    { action: "CLEAN" },
    { action: "MOVE_LEFT" },
    { action: "MOVE_RIGHT" },
    { action: "NONE" }
  ]

  return possibleActions;
};

const simulate = (state, { action }) => {
  let newState = state;

  if (action === "CLEAN") {
    newState.rooms[newState.agentPos].clean = true;
  }

  if (action === "MOVE_LEFT" && newState.agentPos > 0) {
    newState.agentPos -= 1;
  }

  if (action === "MOVE_RIGHT" && newState.agentPos < newState.rooms.length - 1) {
    newState.agentPos += 1;
  }

  return newState;
};

const utilityFunction = (state) => {
  let score = 0;
  state.rooms.forEach(room => {
    if (room.clean) score += 10;
  });
  return score;
};

const utilityBasedAgent = (perception) => {
  const currentState = interpret(perception);
  const possibleActions = actions();
  let bestAction = { action: "NONE" };
  let bestUtility = -Infinity;

  possibleActions.forEach(action => {
    const resultState = simulate(currentState, action);
    const value = utilityFunction(resultState);

    if (value > bestUtility) {
      bestUtility = value;
      bestAction = action;
    }
  });

  return bestAction;
};

const perception = {
  rooms: [
    { name: "A", clean: false },
    { name: "B", clean: true }
  ],
  agentPos: 0
};

console.log("result ===> ", utilityBasedAgent(perception));
