# PokerHyperSolver

This was a quick project that was thrown together to merge two of my passions: Poker and Code.

At it's root, this was a good program to get my feet wet with Python code which was a language I had admired from afar but had never really got down and dirty with, so here was my chance.

##What does it do?

Poker Stars stores the history of hands played in a local file. After every hand that is played, Poker Stars adds that hand into this hand history file.

Armed with this knowledge, I set about monitoring this hand history file and using that to help while playing Hyper Turbo sit and go tournaments. I extrapolated some necessary data from the hand history, such as total number of players at the table and all players chip stack sizes moving into the next hand.

This data was then sent to the browser and a GET request was made to the Holdem Resources ICM calculator to find the exact mathematical solution of the next preflop situation.

##Not a solution.

This is not a poker hand solver and does not provide a solution to the game in any way. What it does do, is use Holdem resources calculator to provide an approximated solution to the ICM situation for the current hand in real time. Theoretically allowing you to improve the level of you play in these shallow stack depth sit and goes.
