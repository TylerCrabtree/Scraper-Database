# Scrape 
![Style](https://media.giphy.com/media/tGrq4uzKIJaLuI3uz7/giphy-downsized.gif)

This repo contains:


ReadMe: Scraper.py 

Description: 
This is a python program that scrapes Wikipidea’s API. The data that is scraped (and parsed) is then stored in a MySQL database. The database is initially empty. To gather data, simply run the scrape.py program (either with terminal, or the IDE PyCharm). From there, the program will prompt the user with 10 options on the terminal. Options 1-5 will scrape different Wikipediea pages and store the information in the database “Berserk” with tables, “BerserkTable” and “Reception” contained inside the database. The program will also print to  To view the databases, MySQL commands to access data (explicit instructions below).Command “6” exits the program, “7” deletes BerserkTable and “8” deletes the Reception table. Command “9” crawls several pages, and command “10” lets the user search for their own topic. 


Requirements:
There is an internet connection.
Make sure all of these imports are installed on your machine: import wikipedia  import sys import warnings import MySQLdb import unidecode
import lxml.etree
 
Run Instructions: 
1. In the directory with scrape.py
2. $ Python scrape.py
3. Upon running the program, enter inputs 1 through 5 or command 9.
4. Open MySQL and view the data with the following commands
5. $  mysql -u root -p;
6. $ SELECT * FROM berserk.BerserkTable;
7. $ SELECT * FROM berserk.Reception;
8.  The database should be filled with two tables containing data.
9.  Go back to python program, enter commands 7 and 8 to delete tables.
10. Enter command 6 to exit.


Contact Info:

Tyler Crabtree

WSU: 11361828

Email: Crabtree.tyler@gmail.com


