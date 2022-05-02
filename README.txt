Your README should consist of the following:

the names of your group members
description of any known bugs with your program
instructions for use, describing how a user would interact with your program.
description of how the pieces of your program fit together
description of features you failed to implement, as well as any extra features you implemented
description of how you tested your program, and ALL of your system tests
Examples of system tests include testing various queries and pasting the results.

Our group members are Eric Long Him Ko and Mikayla Walsh. 

Bugs? 

In order to interact with our program, a user must first run the indexer on the desired xml file by typing
$ python3 index.py [wiki file] titles.txt docs.txt words.txt into thier terminal. Next, the user will run the 
querier on the files by typing $ python3 query.py titles.txt docs.txt words.txt into their terminal. After this, 
they will be prompted to type in a query they wish to search. By hitting enter, they will be given a list of the 
top 10 (or less if there is not 10) documents that match that query. This process will continue until the user types
:quit. 