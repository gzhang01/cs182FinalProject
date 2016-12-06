# CS182FinalProject

# How to Run
To run the simulator, cd into the blackjack directory and type "python game.py [flags]"

## Available Flags
+ *-a [agent], -agent [agent]*
	+ Runs selected agent
 	+ Available agents: *random*, *basic*
 	+ Default agent: *player* (user-controlled)
+ *-cd, -collectData*
	+ Collects data on money per round
+ *-f [file], -file [file]*
	+ Saves collected data to *file*
	+ Default file: "data/default.csv"
+ *-m [amount], -money [amount]*
	+ Sets starting money for agent to *amount*
	+ Default amount: 1000
+ *-np, -noPrint*
	+ Does not print anything during program execution
+ *-qiter [iterations]*
	+ Trains the QLearning agent on *iterations* rounds
	+ Default value: 10000

# To-Do List
- Implement Random Agent - Done
- Implement Q-Learning Agent (for hit/stand) - Done
- Implement Basic Strategy - Done
- Implement double / split - on branch doubling
- Implement Q-Learning for all actions
- Implement card counting - on branch counting
- Implement strategic betting
