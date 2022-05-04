Group members: Our group members are Eric Long Him Ko and Mikayla Walsh. 

Bugs: There are no bugs in our code that we are aware of. 

How a user interacts with the program: In order to interact with our program, a user must first run the indexer 
on the desired xml file by typing $ python3 index.py [wiki file] titles.txt docs.txt words.txt into their terminal. 
Next, the user will run the querier on the files by typing $ python3 query.py titles.txt docs.txt words.txt into 
their terminal or $ python3 query.py --pagerank titles.txt docs.txt words.txt for pagerank. After this, they will 
be prompted to type in a query they wish to search. By hitting enter, they will be given a list of the top 10 (or
less if there is not 10) documents that match that query. This process will continue until the user types :quit. 

How the pieces of your program fit together: When the indexer is ran on an xml file and the corresponding txt files, 
the first txt file is the titles file. This file gets populated with a dictionary from page ids to titles based on the 
xml file. The second txt file is the words file which is populated with a double dictionary from words to ids to relevance 
based on the xml file. The last txt file is the docs file which is populated with a dictionary from ids to page rank based 
on the xml file. These files are what is passed into the querier, along with a boolean value which tells the querier whether 
or not to use page rank. If the boolean value is False, the querier runs using a no_page_rank_score function which uses the 
values in the double dictionary from the words file. Once the top 10 ids are found for a given query, the dictionary from the 
titles file is used to find the corresponding titles and that is returned. Similarly, if the boolean value is True the querier 
runs using a page_rank_score function which multiplies the values in the double dictionary from the words file and the page 
rank dictionary from the docs file. Once the top 10 ids are found for a given query, the dictionary from the titles file is 
used to find the corresponding titles and that is returned.

Features you failed to implement, as well as any extra features you implemented: We haven't failed to implement anything nor 
did we implement any extra features. 

How you tested your program, and ALL of your system tests: We tested our program as we went by using the Interactive Window
and writing unit tests for small parts of our program which are in our test_index.py and test_query.py files. Things we did 
not test in these files include system tests as well as testing when our query does not produce any titles. First, we did 
system tests with small files to make sure our query was working as expected by prompting the user for a query and then 
returning a list of titles labeled 1 to 10 (or less if there was not 10) and then again prompting the user for a query until 
the user typed in :quit. We used our unit tests to make sure these were in fact the top 10 most relevant titles. We also used 
the system tests to assure that when the incorrect number of inputs was provided for index (anything except 4) that a ValueErroris
raised. In addition, we made sure that for query if there are 4 inputs we are not using page rank, if there
are 5 inputs we are using page rank, and if there is any other number the user is informed that it is an invalid input via a ValueError.
Another case we tested with system tests were when no titles were returned. When this is the case for a provided query, our program 
prints out "no results were found!" and allows the user to type in a new query. We did not throw an error here so that the 
user could type in a new query. If we threw an error, the program would terminate. In addition, we used system tests to assess
our runtime by writing time before our command inputs. Finally, we used the MedWiki results posted on Ed to compare them to our 
results to make sure we were getting similar outputs. Some of those are depicted in the next section.


Examples of system tests include testing various queries and pasting the results:

python3 index.py MedWiki.xml med_titles.txt med_docs.txt med_words.txt 
python3 query.py med_titles.txt med_docs.txt med_words.txt
query: baseball 
results: 
1:Oakland Athletics
2:Minor league baseball
3:Kenesaw Mountain Landis
4:Miami Marlins
5:Fantasy sport
6:Out
7:October 30
8:January 7
9:Hub
10:February 2

python3 index.py MedWiki.xml med_titles.txt med_docs.txt med_words.txt 
python3 query.py --pagerank med_titles.txt med_docs.txt med_words.txt
query: baseball 
results: 
1:Ohio
2:February 2
3:Oakland Athletics
4:Kenesaw Mountain Landis
5:Netherlands
6:Miami Marlins
7:Minor league baseball
8:Kansas
9:Pennsylvania
10:Fantasy sport

python3 index.py MedWiki.xml med_titles.txt med_docs.txt med_words.txt 
python3 query.py med_titles.txt med_docs.txt med_words.txt
query: fire 
results: 
1:Firewall (construction)
2:Pale Fire
3:Ride the Lightning
4:G?tterd?mmerung
5:FSB
6:Keiretsu
7:Hephaestus
8:KAB-500KR
9:Izabella Scorupco
10:Justin Martyr

python3 index.py MedWiki.xml med_titles.txt med_docs.txt med_words.txt 
python3 query.py --pagerank med_titles.txt med_docs.txt med_words.txt
query: fire 
results:
1:Falklands War
2:Justin Martyr
3:Firewall (construction)
4:Empress Suiko
5:New Amsterdam
6:Pale Fire
7:Montoneros
8:Hermann G?ring
9:Nazi Germany
10:Navy

python3 index.py MedWiki.xml med_titles.txt med_docs.txt med_words.txt 
python3 query.py med_titles.txt med_docs.txt med_words.txt
query: battle 
results: 
1:Paolo Uccello
2:Navy
3:J.E.B. Stuart
4:Heart of Oak
5:Irish mythology
6:Front line
7:Oda Nobunaga
8:Girolamo Aleandro
9:Lorica segmentata
10:Mehmed II

python3 index.py MedWiki.xml med_titles.txt med_docs.txt med_words.txt 
python3 query.py --pagerank med_titles.txt med_docs.txt med_words.txt
query: battle 
results:
1:Falklands War
2:Navy
3:Nazi Germany
4:Netherlands
5:Portugal
6:History of the Netherlands
7:Montoneros
8:Paolo Uccello
9:Norway
10:Normandy

(test when the query does not appear in any pages)
python3 index.py xml-files/test_tf_idf.xml txt-files/titles.txt txt-files/docs.txt txt-files/words.txt
python3 query.py txt-files/titles.txt txt-files/docs.txt txt-files/words.txt
query: water
return:
no results were found!

(test when index does not get the correct number of args)
python3 index.py xml-files/test_tf_idf.xml txt-files/titles.txt txt-files/docs.txt
return:
Traceback (most recent call last):
  File "/Users/mikaylawalsh/Desktop/cs200/projects/search-ERICEX2025-mikaylawalsh/index.py", line 239, in <module>
    raise ValueError("Wrong number of arguments!!!")
ValueError: Wrong number of arguments!!!

(test when index does not get the correct number of args)
python3 index.py xml-files/test_tf_idf.xml txt-files/titles.txt txt-files/docs.txt txt-files/words.txt
python3 query.py txt-files/titles.txt txt-files/docs.txt
return:
Traceback (most recent call last):
  File "/Users/mikaylawalsh/Desktop/cs200/projects/search-ERICEX2025-mikaylawalsh/query.py", line 173, in <module>
    raise ValueError("invalid number of args")
ValueError: invalid number of args

(test to assess runtime)
time python3 index.py BigWiki.xml big_titles.txt big_docs.txt big_words.txt
return:
python3 index.py BigWiki.xml big_titles.txt big_docs.txt big_words.txt  299.12s user 1.47s system 100% cpu 4:59.15 total