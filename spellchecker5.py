from difflib import SequenceMatcher # library for checking how similar words are
import re # regular expression library used for removing non alphabetic characters from the sentence entered
import datetime # library for accessing dates and times
again = True # boolean to keep the program running as long as the user wants

# unicode characters for borders
horizontalLine = (u"\u2501") 
verticalLine = (u"\u2503")
topLeft = (u"\u250f") 
topRight = (u"\u2513") 
bottomLeft = (u"\u2517") 
bottomRight = (u"\u251b") 
tshape = (u"\u2523") 
# variable for spaces to save having of write out lots of spaces, can just do this * how many spaces required
space = " "

# reads the dictionary file and puts each word from it into a list
dictionary = []
file = open("EnglishWords.txt", "r")
for line in file:
    line = line.rstrip()
    dictionary.append(line)
file.close()


def spellCheckSentence(): # function to do the spell check
    total = 0 # variabled for total words, correctly spelt words and incorrectly spelt words
    correct = 0
    wrong = 0

    # menu for enter sentence part of the program
    print("\n" + topLeft + horizontalLine*30 + topRight
    + "\n" + verticalLine + space*8 + "Sentence Check" + space*8 + verticalLine
    + "\n" + tshape + horizontalLine*30 + bottomRight)
    
    sentence = input(bottomLeft + horizontalLine + "Enter sentence: ")
    print("")
    sentence = sentence.lower() #converts sentence to lower case so that no matter the case used it can be checked against the dictionary

    wordList = re.sub(r'[^a-z ]', '',sentence).split() # split the sentence into a list of words and removes characters that are not from a to z (lower case)
    #print(wordList)

    # the list of entered words is checked against the list of words from the text file to see if they are spelt correctly
    for wordIndex in range(len(wordList)):
        total += 1
        found = False
        for dictinaryIndex in range(len(dictionary)):
            if wordList[wordIndex] == dictionary[dictinaryIndex]:
                found = True
                correct += 1
                print(wordList[wordIndex], "spelt correctly")
        if found == False:  # boolean used to check if a word has been found in the dictionary 
            print(wordList[wordIndex], "not found in dictionary")
            wrong += 1

    # creates variables of sentences about the total number of words, as well as correclty and incorrectly spelt words
    totalSentence = "Number of words: " + str(total)
    correctSentence = "Number of correctly spelt words: " + str(correct)
    wrongSentence = "Number of incorreclty spelt words: " + str(wrong)

    # prints data about total words and spelling of words
    print("", "\n" + totalSentence + "\n" + correctSentence + "\n" + wrongSentence + "\n")


def spellCheckFile():
    total = 0 # variabled for total words, correctly spelt words and incorrectly spelt words
    correct = 0
    wrong = 0
    ignored = 0 # variables for choices when incorrect word encountered
    addtodict = 0
    marked = 0
    checkedSentence = "" # string that checked words will be appened to, then string written to file

    fileexist = False
    while fileexist == False: # validation so user has to enter a valid file name 
        try:
            # initial menu for file check part of the program
            print("\n" + topLeft + horizontalLine*30 + topRight
            + "\n" + verticalLine + space*10 + "File Check" + space*10 + verticalLine
            + "\n" + tshape + horizontalLine*30 + bottomRight)

            filename = input(bottomLeft + horizontalLine + "Enter filename: ")
            print("")

            # opens file based on the name the user enters
            file = open((filename+".txt"), "r")
            fileexist = True
        except:
            print("\nFile does not exist" + "\n")
            fileexist = False

    # creates a file, or overrides one if it already exists, so that is can be written to
    file2 = open((filename+"_checked.txt"), "w")

    # reads the contents of the file to be checked into a variable where it it turned into lower case
    fileWords = file.read()
    fileWords = fileWords.lower()

    # splits the variable of words from the file into a list, removing non alphabetic characters
    fileWordsList = []
    fileWordsList = re.sub(r'[^a-z ]', '',fileWords).split()

    # gets the time at the start of the spell check
    startTime = datetime.datetime.now()

    # loops through the the list of words from the file and checks them against words in the dictionary
    for wordIndex in range(len(fileWordsList)):
        currentword = fileWordsList[wordIndex]
        total += 1
        found = False
        for dictionaryIndex in range(len(dictionary)):
            if currentword == dictionary[dictionaryIndex]:
                found = True
                correct += 1
                checkedSentence += (currentword +" ")
        if found == False:  # boolean used to check if a word has been found in the dictionary
            wrong += 1
            suggestedWord = ""
            wordscore = 0
             # checks the incorrect words against every word in the dictionary to see how similar the words are,
             # the mot similar word is shown to the user and they are asked if this is what they meant.
            for i in range(0, len(dictionary)):
                currentscore = SequenceMatcher(None, dictionary[i], currentword).ratio()
                if currentscore > wordscore:
                    wordscore = currentscore
                    suggestedWord = dictionary[i]
                
           
        

            validChoice = False       
            while validChoice == False: # menu for dealing with incorrect words
                # menu to show incorrect word and suggested word
                print("\n" + topLeft + horizontalLine*30 + topRight
                + "\n" + verticalLine + space*8 + "Word Not Found" + space*8 + verticalLine
                + "\n" + verticalLine + currentword + space*(30-len(currentword)) + verticalLine
                + "\n" + verticalLine + "Did you mean?" + space*(30-13) + verticalLine
                + "\n" + verticalLine + suggestedWord + space*(30-len(suggestedWord)) + verticalLine
                + "\n" + tshape + horizontalLine*30 + bottomRight)

                suggestedWordChoice = input(bottomLeft + horizontalLine + "Enter [y] or [n]: ")
                suggestedWordChoice = suggestedWordChoice.lower()
            
                if suggestedWordChoice == "y": # changes incorrect word to suggested word
                    validChoice = True
                    checkedSentence += (suggestedWord + " ")
                elif suggestedWordChoice == "n": # word is chosen as wrong and user is given choice for what to do with it
                    validChoice = True
                    inputvalid = False
                    while inputvalid == False: # loops until valid input is entered
                        # menu for choices for incorrect word
                        print("\n" + topLeft + horizontalLine*30 + topRight
                        + "\n" + verticalLine + space*8 + "Word Incorrect" + space*8 + verticalLine
                        + "\n" + verticalLine + currentword + " not found" + space*(30-(10 + len(currentword))) + verticalLine
                        + "\n" + verticalLine + space*30 + verticalLine
                        + "\n" + verticalLine + "1. Ignore word" + space*(30-14) + verticalLine
                        + "\n" + verticalLine + "2. Mark words as incorrect" + space*(30-26) + verticalLine
                        + "\n" + verticalLine + "3. Add word to dictionary" + space*(30-25) + verticalLine
                        + "\n" + tshape + horizontalLine*30 + bottomRight)

                        incorrectchoice = input(bottomLeft + horizontalLine + "Please select an option: ")
                        print("")
                       
                        # 3 choices for an incorrect word
                        if incorrectchoice == "1": # ignore word
                            inputvalid = True
                            checkedSentence += ("!"+currentword+"! ")
                            ignored += 1
                        elif incorrectchoice == "2": # mark word as incorrect
                            inputvalid = True 
                            checkedSentence += ("?"+currentword+"? ")
                            marked += 1
                        elif incorrectchoice == "3": # add word to dictionary
                            inputvalid = True  
                            checkedSentence += ("*"+currentword+"* ")
                            file = open("EnglishWords.txt", "a")
                            file.write("\n" + currentword)
                            addtodict += 1             

    # gets time at end of spell check
    endTime = datetime.datetime.now()
    timeElapsed = endTime - startTime # gets time taken 
    totalSentence = "Number of words: " + str(total)
    correctSentence = "Number of correctly spelt words: " + str(correct)
    wrongSentence = "Number of incorreclty spelt words: " + str(wrong)
    ignoredSentence = "      Number or words ignored: " + str(ignored)
    markedSentence = "      Number of words marked: " + str(marked)
    addtodictSentence = "      Number of words added to dictionary: " + str(addtodict)

    print("", "\n" + totalSentence + "\n" + correctSentence + "\n" + wrongSentence + "\n" + ignoredSentence + "\n" + markedSentence + "\n" + addtodictSentence)
    print("\nTime taken: " + str(timeElapsed.microseconds) + " microseconds")


    # writes to file
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M") # gets date in form day-month-year and time in form hour:minute
    file2.write(str(now))
 
    file2.write("\n" + totalSentence)
    file2.write("\n" + correctSentence)
    file2.write("\n" + wrongSentence)
    file2.write("\n" + ignoredSentence)
    file2.write("\n" + markedSentence)
    file2.write("\n" + addtodictSentence)
    file2.write("\n")
    file2.write("\n" + checkedSentence)

    file.close() # closes the opened files
    file2.close()


while again == True: # gives user choice to do the spell check again, once check is done the menu is shown again to the user where they can quit or do another check
    
    
    # menu to show the user the option that they can choose
    print(topLeft + horizontalLine*31 + topRight
    + "\n" + verticalLine + space*9 + "Spell Checker" + space*9 + verticalLine
    + "\n" + verticalLine + space*31 + verticalLine
    + "\n" + verticalLine + " 1. Check a sentence" + space*11 + verticalLine 
    + "\n" + verticalLine + " 2. Check a file" + space*15  + verticalLine 
    + "\n" + verticalLine + space*31 + verticalLine 
    + "\n" + verticalLine + " 3. Quit" + space*23 + verticalLine 
    + "\n" + tshape + horizontalLine*31 + bottomRight)
    
    menuChoice = input(bottomLeft + horizontalLine + "Select an option: ")
   
    
    if menuChoice == "1":
        spellCheckSentence()
    elif menuChoice == "2":
        spellCheckFile()
    elif menuChoice =="3":
        again = False
    else:
        print("Please enter a valid option \n ")
