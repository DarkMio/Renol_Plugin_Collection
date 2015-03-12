import re
import logging


ID = "anagram"
permission = 0


##########################################################################
# Function    : filterWordsBasedOnLength
# Parameters  : jumbledWord(String) and dictionary reference word(String)
# Returns     : String
# Description : This function matches the two given string for 
#               their length and returns the word if the lenghts are same.
##########################################################################
def lengthfilter(jumbledWord,word):
    if len(jumbledWord) == len(word):
        return word


##########################################################################
# Function    : computeValuForEachWord
# Parameters  : filteredWord(String) and jumbledWord(String)
# Returns     : boolean
# Description : This computes the unicode value of each sting to filter out
#               the words and then if the value matches it then checks
#      whether the characters match if they do it return true else
#        false
########################################################################## 
def value(filteredWord,jumbledWord):
    filteredWordValue = 0
    jumbledWordValue = 0
    for character in filteredWord:
        filteredWordValue += ord(character)

    for char in jumbledWord:
        jumbledWordValue += ord(char)
    filteredWord = list(filteredWord)
    if filteredWordValue == jumbledWordValue:
        for w in jumbledWord:
            if w not in filteredWord:
                return False
        else:
                del filteredWord[filteredWord.index(w)] # For filtering out cases where value becomes same due to multi occurence of same char
        return True
    else:
        return False


def execute(self, name, params, channel, userdata, rank):
    logger = logging.getLogger("Anagram")

    if len(params) > 0:

        answer = []
        error = None
        try:
            inputFile = open("commands/data/dictionary.txt","r")
        except Exception, e:
            self.sendNotice(name, "Exception while reading the dictionary file. Sorry.")
            logger.error("Exception while reading the dictionary file. Following are the details of the exception :\n\r" + str(e))
            return
        fileContents = words = inputFile.read().strip() #Striping whitespaces
        words = re.split("[\s\n\r]+",fileContents) #Splitting the file into word tokes based on either spaces/new line/carriage return

        jumbledWord = params[0].lower()
        filteredWords = [lengthfilter(jumbledWord,word) for word in words]
        filteredWords = filter(None,filteredWords)
        for dictionaryWord in filteredWords:
            if value(dictionaryWord.lower(),jumbledWord.lower()) and not jumbledWord.lower() == dictionaryWord.lower(): 
                for letter in dictionaryWord.lower():
                    if not letter.lower() in jumbledWord.lower():
                        error = 1

                if not error == 1:
                    answer.append(dictionaryWord)


        if len(answer) == 1:
            self.sendMessage(channel, "I've found following fitting word: "+str(answer[0]))
        elif len(answer) > 1:
            answers = ", ".join(answer)
            self.sendMessage(channel, "I've found multiple words: "+answers)
        else:
            self.sendMessage(channel, "There is nothing in my dictionary that fits.")

    else:
        self.sendNotice(name, "Incorrect syntax. Please give any input to process.")