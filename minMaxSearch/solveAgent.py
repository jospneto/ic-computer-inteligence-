def minConflict(problem, numIter=100000):
    print('number of iterations =', numIter)
    state = problem.getStartState()
    print("Initial State")
    problem.visualize(state)

    for i in range(numIter):
        var = problem.getVar(state)      
        if var == -1:
            print("Solution state found in", i, "iterations")
            problem.visualize(state)
            return state
        
        val = problem.getValue(state, var)
        state = problem.updateBoard(state, var, val)
    
    print("Solution not found! Try with high iterations")
    return [] 