from re import M
import sys
 
 
class Querier:
 
   def __init__(self, title_path: str, docs_path: str, words_path: str):
       self.title_path = title_path
       self.docs_path = docs_path
       self.words_path = words_path
 
   # what does querier tak in?
   def querier(self):
       pass
       # main method should support the following:
       # python3 query.py [--pagerank] <titleIndex> <documentIndex> <wordIndex>
 
 
if __name__ == "__main__":
   query = input(sys.argv)
   while (query != ":quit"):
 
       if (len(sys.argv) == 5):
           # include page rank
           pass
       elif (len(sys.argv) == 4):
           # no page rank
           pass
       else:
           pass
           # return print that says not enough args
       break  # not sure when but might need
       # call the helper that does relevance in while loop instead of printing
       # helper should take in a string?
       # then break it into a set, then execute the algorithm in 2-g
       # have an if statement for if page rank is included (5 args or 4)
       # return the document titles in order of priority (might need a line to print 1-10 in front of doc name)
   exit
 
   # ask user for query
 
   #read in query
 
   # answer query by scoring terms and returning top 10 results
 
   # repeat under :quit
