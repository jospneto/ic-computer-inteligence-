const interpret = (perception) => {
  return perception; 
}

const goalAchieved = (state) => {
  return state.rooms.every(room => room.clean === true);
}

const plan = (currentState) => {
  let actions = [];

  currentState.rooms.forEach((room, index) => {
    if (!room.clean) {
      actions.push({ action: "CLEAN", room: index });
    }
  });

  return actions;
}

const firstAction = (plan) => {
  if (plan && plan.length > 0) {
    return plan[0];
  }
  return { action: "NONE" };
}

const goalBasedAgent = (perception) => {
  const currentState = interpret(perception);
  const achieved = goalAchieved(currentState);

  if (achieved) {
    return { action: "NONE" };
  } else {
    const actions = plan(currentState);
    return firstAction(actions);
  }
}

const perception = {
  rooms: [
    { name: "A", clean: true },
    { name: "B", clean: false }
  ]
};

console.log("result ===> ", goalBasedAgent(perception));

