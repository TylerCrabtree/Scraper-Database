# Tyler Crabtree
# Web Scraper
# To run, ensure MySQl, warnings, unidecode, and the Wikipedia API are installed
# Also, ensure you are connected to the internet ;)

# import list:
import urllib
import sys
import wikipedia
import warnings
import MySQLdb as db
from unidecode import unidecode
import lxml.etree

password = ""           #global password function

#These first few functions are tailored to each page to get the best specific information
#I then Implement a more generic crawler/scraper into the later functions

# first function, parses Berserk's written source, the "manga"
def Manga():
    berserk = wikipedia.page("Berserk (manga)")      # get page
    print("Title :" + berserk.title)                 # print title
    print("Summary :" + berserk.summary)             # print summary
    print("Image: " + berserk.images[1])             # print image, I grabbed the second one since it represents thhe function
    print("Categories: " + berserk.categories[1]+ \
    ", "  + berserk.categories[0] + ", " \
    + berserk.categories[2])                         # print categories
    title = berserk.title                            #save variable names, get title
    summary = berserk.summary                        #get summary
    image = berserk.images[1]                        #get image
    cat = berserk.categories[1]                      #to condense, only chose one category
    reception = receptionParse(berserk)              # call function that parses for the critical reception
    reception = reception.lstrip()                   #just in case gets rid of extra whitespace
    print ("Reception:" + reception)                                #print
    summary = berserk.summary                        #so many of these pages had Japanese which would cause the data base to crash....
    reception = clean(reception)                     #so I clean it of "weird" characters
    reception = mediumTrim(reception)                     #so I clean it of "weird" characters
    reception = reception.replace('\n', '')         # remove new lines

    summary = clean(summary)                         #continue to clean code
    summary = trim(summary)                          #I wanted a longer summary, but the database becomes unreadable, so I trimmed it
    database(title,summary,image,cat,reception)      #pass all the variables to my database function

# first function, parses Berserk's 1997 anime
def Series():
    berserk = wikipedia.page("Berserk (1997 TV series)")  # get anime page
    print("Title: " + berserk.title)                  # title
    print("Summary: " + berserk.summary)              # summary
    print("Image: " + berserk.images[1])              # image
    print("Categories: " + berserk.categories[1] + \
    ", " + berserk.categories[0] + ", " + \
    berserk.categories[2])                            #print cat
    title = berserk.title                             #grab tile
    summary = trim(berserk.summary)                   #trim summary length
    image = berserk.images[1]                         #get image
    cat = berserk.categories[1]                       #get category, limit to 1 for presentation
    reception = receptionParse(berserk)               #call function that parses for the critical reception
    reception = reception.lstrip()                    #limit extra whitespace (probably not needed, but certainly doesn't hurt)
    print ("Reception:" + reception)                  #print
    summary = berserk.summary                         #grab summaray
    reception = clean(reception)                      #clean code
    reception = mediumTrim(reception)                     #so I clean it of "weird" characters
    reception = reception.replace('\n', '')             # remove new lines

    summary = clean(summary)                          #continue to clean
    summary = trim(summary)                           #shorten for database
    database(title,summary,image,cat,reception)       #database magic

def Game():
    berserk = wikipedia.page("Berserk and the Band of the Hawk")  # game page
    print("Title: " + berserk.title)                   # title
    print("Summary :" + berserk.summary)               # summary
    print("Image: " + berserk.images[0])               # image
    print("Categories: " + berserk.categories[1] + \
          ", " + berserk.categories[0] + ", " \
          + berserk.categories[2])                     # category
    receptionParse(berserk)                            # call function that parses for the critical reception
    title = berserk.title
    summary = berserk.summary
    image = berserk.images[0]
    cat = berserk.categories[0]
    reception = receptionParse(berserk)                 # call function that parses for the critical reception
    reception = reception.lstrip()
    summary = berserk.summary
    reception = clean(reception)
    reception = mediumTrim(reception)                     #so I clean it of "weird" characters
    reception = reception.replace('\n', '')  # remove used words
    print ("Reception:" + reception)                     #print

    summary = clean(summary)
    summary = trim(summary)
    database(title,summary,image,cat,reception)


def Berserk2016():
    berserk = wikipedia.page("Berserk(2016 TV series)")     # grab second series name
    print("Title: " + berserk.title)                        # print title
    print("Summary :" + berserk.summary)                    # summary
    print("Image: " + berserk.images[0])                    # print images
    print("Categories: " + berserk.categories[1] + ", " + berserk.categories[0] +", " + berserk.categories[2])
    title = berserk.title
    image = berserk.images[0]
    cat = berserk.categories[0]
    reception = receptionParse(berserk)                     # call function that parses for the critical reception
    reception = reception.lstrip()
    reception = shorten(reception)
    summary = berserk.summary
    reception = clean(reception)
    reception = mediumTrim(reception)
    reception = reception.replace('\n', '')         # remove new lines

    summary = clean(summary)
    summary = trim(summary)
    database(title,summary,image,cat,reception)


# first function, parses Berserk's written source, the "manga"
def Movie():
    berserk = wikipedia.page("Golden Age arc")      # get page
    print("Title :" + berserk.title)                 # print title
    print("Summary :" + berserk.summary)             # print summary
    print("Image: " + berserk.images[1])             # print image, I grabbed the second one since it represents thhe function
    print("Categories: " + berserk.categories[1]+ \
    ", "  + berserk.categories[0] + ", " \
    + berserk.categories[2])                         # print categories
    title = berserk.title                            #save variable names, get title
    summary = berserk.summary                        #get summary
    image = berserk.images[1]                        #get image
    cat = berserk.categories[1]                      #to condense, only chose one category
    reception = receptionParse(berserk)              # call function that parses for the critical reception
    print ("Reception:" + reception)                                #print
    summary = berserk.summary                        #so many of these pages had Japanese which would cause the data base to crash....
    reception = clean(reception)                     #so I clean it of "weird" characters
    reception = mediumTrim(reception)                     #so I clean it of "weird" characters
    reception = reception.replace('\n', '')  # remove used words

    summary = clean(summary)                         #continue to clean code
    summary = trim(summary)                          #I wanted a longer summary, but the database becomes unreadable, so I trimmed it
    if(len(reception) <= 1 ):
        reception = "null"
        summary = clean(summary)  # continue to clean code
    database(title,summary,image,cat,reception)      #pass all the variables to my database function



#I felt like the above functions were satisfactory, but I implemented the function below for a more generic crawl/scrape
#Below I scrape the xml file. above I technically do, but just to ensure I do everything asked for, I built these functions



#This narrows the xml down to the main media
# The next two functions are helper functions to extract names of webpages
def getMedia(berserk):
    mediaString = ""                                    # set empty screen
    i = 0;                                              # build iterator
    while (i < len(berserk) - 7):                       # parses xml code for title, this is less specific and I personally do the xml parsing
        # the line below parses the content of a page and searches for a specific word
        s1 = (
            berserk[i] + berserk[i + 1] + berserk[i + 2] + berserk[i + 3] +
            berserk[
                i + 4] + berserk[i + 5] + berserk[i + 6])
        s2 = '=Media='                                  # if media is found
        if (s1 == s2):                                  # checks to see if specific word was found
            i = i + 10;                                 #  offest to start section
            while (i < len(berserk) - 7 ):              # avoid overflow + set up to print section
                if (berserk[i] == '='):                 # break when next section is hit
                    break
                mediaString = mediaString + berserk[i]  # from media section ( which has generic title from the xml)
                i = i + 1                               # iterate
        i = i + 1                                       # iterate
    return mediaString

def getTitle(berserk):
    titleString = ""                                    # set empty screen
    switch = 0;                                         #for how I parsed, this is crucial
    i = 0;                                              # build iterator
    while (i < len(berserk) - 1):                       # avoid overflow
        s1 = ( berserk[i])
        s2 = '('
        if (s1 == s2):                                   # checks to see if specific word was found
            i = i + 1;                                   # offest to start section
            while (i < len(berserk) - 1 ):               # avoid overflow + set up to print section
                if (berserk[i] == ')'):                  # break when next section is hit
                    titleString = titleString + "|"
                    break
                titleString = titleString + berserk[i]

                i = i + 1  # iterate
        i = i + 1  # iterate
    return titleString                                   #return list of titles (although, has duplicates)



#simplify titles and remove duplicates, calls scraper with multiple titles, so I call this the crawl
def crawl(singles):
    firstword = ""
    switch = 0
    i = 0
    singles = singles.replace("video game", 'Berserk and the Band of the Hawk') #avoids irrlevant info
    while (i < len(singles)-50):                                                #avoids overflow (generic case, so bigger buffer for potentially long title)
        length = 0
        if(singles[i] == '|'):                                                  #This indicates word change, since duplicates, I have a switch involved
            switch = switch+1                                                   #switch for modding
            firstword = firstword.replace("working title", '')                  #avoids bad pages

            firstword = firstword.rstrip()
            if(firstword != ''):
                generic(firstword)                                              #call generic scraping/database function
            firstword = firstword.replace(firstword, '')                        #remove used words
            firstword = ''                                                      #clear
            i = i+1
        if(switch%2 == 0):                                                      #only grab half the words
            firstword = firstword + singles[i]
        i = i + 1


#this function pareses the xml of the "berserk" page for titles for sub categories:
def extract(title):
    title = "berserk"                                   #category
    params = {"format": "xml", "action": "query", "prop": "revisions", "rvprop": "timestamp|user|comment|content"} #query
    params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
    query = "&".join("%s=%s" % k for k in params.items())
    url = "http://en.wikipedia.org/w/api.php?%s" % query
    xml = lxml.etree.parse(urllib.urlopen(url))          #xml
    parsed = xml.xpath('//rev')                          #simplified
    mediaString = getMedia(parsed[-1].text)              #saves media section
    titles = getTitle(mediaString)                       #gets titles out of media
    crawl(titles)                                        #auto crawl then scrape



# first function, parses Berserk's written source, the "manga"
def generic(berserk):
    berserk = "Berserk ("+ berserk+")"
    berserk = wikipedia.page(berserk)                # get page
    print("Title :" + berserk.title)                 # print title
    print("Summary :" + berserk.summary)             # print summary
    print("Image: " + berserk.images[0])             # print image, I grabbed the second one since it represents thhe function
    print("Categories: " + berserk.categories[1]+ \
    ", "  + berserk.categories[0] + ", " \
    + berserk.categories[2])                         # print categories
    title = berserk.title                            #save variable names, get title
    summary = berserk.summary                        #get summary
    image = berserk.images[0]                        #get image
    cat = berserk.categories[0]                      #to condense, only chose one category
    reception = receptionParse(berserk)              # call function that parses for the critical reception
    reception = reception.lstrip()                   #just in case gets rid of extra whitespace
    print ("Reception:" + reception)                                #print
    summary = berserk.summary                        #so many of these pages had Japanese which would cause the data base to crash....
    reception = clean(reception)                     #so I clean it of "weird" characters
    reception = mediumTrim(reception)                     #so I clean it of "weird" characters
    reception = reception.replace('\n', '')  # remove used words

    #reception = longTrim(reception)
    summary = clean(summary)                         #continue to clean code
    summary = trim(summary)                          #I wanted a longer summary, but the database becomes unreadable, so I trimmed it
    database(title,summary,image,cat,reception)      #pass all the variables to my database function



# first function, parses Berserk's written source, the "manga"
def ultraGeneric(berserk):
    warnings.filterwarnings('ignore')                #so the program doesn't yell at you that a database may exist
    berserk = wikipedia.page(berserk)                # get page
    print("Title :" + berserk.title)                 # print title
    print("Summary :" + berserk.summary)             # print summary
    print("Image: " + berserk.images[0])             # print image, I grabbed the second one since it represents thhe function
    print("Categories: " + berserk.categories[1]+ \
    ", "  + berserk.categories[0] + ", " \
    + berserk.categories[2])                         # print categories
    title = berserk.title                            #save variable names, get title
    summary = berserk.summary                        #get summary
    image = berserk.images[0]                        #get image
    cat = berserk.categories[0]                      #to condense, only chose one category
    reception = receptionParse(berserk)              # call function that parses for the critical reception
    reception = reception.lstrip()                   #just in case gets rid of extra whitespace
    print ("Reception:" + reception)                                #print
    summary = berserk.summary                        #so many of these pages had Japanese which would cause the data base to crash....
    reception = clean(reception)                     #so I clean it of "weird" characters
    reception = mediumTrim(reception)                     #so I clean it of "weird" characters
    reception = reception.replace('\n', '')  # remove used words

    #reception = longTrim(reception)
    summary = clean(summary)                         #continue to clean code
    summary = trim(summary)                          #I wanted a longer summary, but the database becomes unreadable, so I trimmed it
    database(title,summary,image,cat,reception)      #pass all the variables to my database function




def clean(word):
    weirdError = ""
    word = word.replace( "'",weirdError)            # fixed error, parsing became confused by " ' " symbols, so i just took them out
    word = unidecode(word)                          # glorious, get rid of Japanese letters import
    return word

def shorten(reception):
    if(len(reception) > 200):                       # if too long
        clip = len(reception)/2
        reception = reception[:-(clip)]             # clip the length
        reception = reception + "..."               # add this for practical purposes
        return  reception



#the next three functions trim the length, I should have passed a second value in and limited by that size, but this works perfectly fine
#a little verbose though
def trim(summary):
        while(len(summary) > 40):   #shorten length of string function
            summary = summary[:-1]
        summary = summary + "..."
        return  summary

def mediumTrim(summary):
    while (len(summary) > 190):  # shorten length of string function
        summary = summary[:-1]

    summary = summary + "..."
    return summary
def longTrim(summary):
    while (len(summary) > 245):  # shorten length of string function
        summary = summary[:-1]

    summary = summary + "..."
    return summary


#looks at the reception section, and grabs it
def receptionParse(berserk):
    receptionString = ""                                                # set empty screen
    i = 0;                                                              #build iterator
    while (i < len(
            berserk.content) - 12):                                     # '= Reception =" is in the middle of the conent section, so I end a -12 early to avoid overflow (shouldn't change data though)
                                                                        # the line below parses the content of a page and searches for a specific word
        s1 = (
        berserk.content[i] + berserk.content[i + 1] + berserk.content[i + 2] + berserk.content[i + 3] + berserk.content[
            i + 4] + berserk.content[i + 5] + berserk.content[i + 6] + berserk.content[i + 7] + berserk.content[i + 8] +
        berserk.content[i + 9] + berserk.content[i + 10] + berserk.content[i + 11] + berserk.content[i + 12])
        s2 = '= Reception ='
        if (s1 == s2):                                                  # checks to see if specific word was found
            i = i + 14;                                                 # offest to start section
            count = 0;

            while (i < len(berserk.content) - 12):                      # avoid overflow + set up to print section
                if (berserk.content[i] == '='):                         # break when next section is hit
                    #sys.stdout.write("Reception:" + (receptionString))  # print section
                    break  # exit to main menu
                receptionString = receptionString + berserk.content[i]  # append string
                if(berserk.content[i]  == '='):
                    count = count +1                                     # I don't want the reception to be too long, so stop at two sentances
                    if (count%1 == 0):
                        break
                i = i + 1  # iterate
        i = i + 1  # iterate
    return receptionString


#database function
def database(title,summary,image,cat,reception):
    con = db.connect(host="localhost",              # your host, usually localhost
                     user="root",                   # your username
                     passwd=password,             # your password
                     )                  # name of the data base

    cur = con.cursor()                              #typical syntax for scraping
    warnings.filterwarnings('ignore')               #so the program doesn't yell at you that a database may exist
    #execute mysql commands:
    cur.execute('CREATE DATABASE IF NOT EXISTS Berserk;')   #create database with variables below
    cur.execute('USE Berserk;')                     # create database with variables below
    cur.execute("create table IF NOT EXISTS BerserkTable (Title varchar(50),Summary varchar(150), Images varchar(100),Categories varchar(50));")
    cur.execute( "INSERT INTO BerserkTable (Title, Summary, Images, Categories) Values ('" + title + "' ,'" + summary + "' ,'" + image + "' ,'" + cat + "');")
    cur.execute("create table IF NOT EXISTS Reception (Title varchar(50),Reception varchar(250));")
    cur.execute("INSERT INTO Reception (Title, Reception) Values ('" + title + "' ,'" + reception + "');")
    con.commit()
    con.close()

    #drop table
def deleteBerserkTable():
    con = db.connect(host="localhost",              # your host, usually localhost
                     user="root",                   # your username
                     passwd=password,             # your password
                     )                  # name of the data base

    cur = con.cursor()                               #typical syntax for scraping
    warnings.filterwarnings('ignore')                #so the program doesn't yell at you that a database may exist
    cur.execute('CREATE DATABASE IF NOT EXISTS Berserk;')   #create database with variables below
    cur.execute('USE Berserk;')                     #create database with variables below
    cur.execute("create table IF NOT EXISTS BerserkTable (Title varchar(50),Summary varchar(150), Images varchar(100),Categories varchar(50));")
    cur.execute("drop table BerserkTable;")
    con.commit()
    con.close()

    # drop table
def deleteRecpetionTable():
    con = db.connect(host="localhost",              # your host, usually localhost
                         user="root",               # your username
                         passwd=password,         # your password
                         )              # name of the data base

    cur = con.cursor()                              # typical syntax for scraping
    warnings.filterwarnings('ignore')               # so the program doesn't yell at you that a database may exist
    cur.execute('CREATE DATABASE IF NOT EXISTS Berserk;')  # create database with variables below
    cur.execute('USE Berserk;')                     # create database with variables below
    cur.execute("create table IF NOT EXISTS Reception (Title varchar(50),Reception varchar(250));")
    cur.execute("drop table Reception;")
    con.commit()
    con.close()




if __name__ == "__main__":
    #welcome and option prompt below, nothing too fancy
    password = raw_input("Please type your terminal password: ")

    print("Welcome to the 'Berserk Scraper'.")
    print("To read about the Berserk manga, please enter '1'")
    print("To read about the 1997 Berserk television series, please enter '2'")
    print("To learn the Berserk game, please enter '3'")
    print("To learn the about the 2016 Berserk series, please enter '4'")
    print("To learn the about the Berserk movie arc, please enter '5'")
    print("Please Enter '6' to exit.")
    print ("Press '7' to delete BerserkTable")
    print ("Press '8' to delete Reception")
    print ("Press '9' to generically crawl")
    print ("Feeling Lucky: '10' to search whatever you like (unsafe)")

    print("\n")
    while (1):                                    #loop through commands until user exits
        command = input('input: ')
        if (command == 1):
            Manga()
        elif (command == 2):
            Series()
        elif (command == 3):
            Game()
        elif (command == 4):
            Berserk2016();
        elif (command == 5):
            Movie();
        elif (command == 6):
            print("Thanks for using the Berserk Scraper! Exiting")
            exit();
        elif (command == 7):
            print("Delete: BerserkTable")
            deleteBerserkTable();
        elif (command == 8):
            print("Delete: Reception table")
            deleteRecpetionTable();
        elif(command == 9):
            extract("berserk")
        elif (command == 10):
            check = raw_input("Search:")
            check = unidecode(check)
            ultraGeneric(check)
        else:
            print("Try another command")

