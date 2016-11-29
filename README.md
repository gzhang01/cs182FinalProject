# CS182FinalProject

# How to Run
To run the simulator, cd into the blackjack directory and type "python game.py [flags]"

## Available Flags
+ *-a [agent], -agent [agent]*
	+ Runs selected agent
 	+ Available agents: *random*, *basic*
 	+ Default agent: *player* (user-controlled)
+ *-m [amount]*
	+ Sets starting money for agent to *amount*
	+ Default amount: 1000
+ *-np, -noPrint*
	+ Does not print anything during program execution


# To-Do List
- Implement Random Agent - Done (tested)
- Implement Q-Learning Agent (for hit/stand) - On qlearning branch
- Implement double / split
- Implement Basic Strategy - Done (tested)
- Implement Q-Learning for all actions
- Implement card counting
