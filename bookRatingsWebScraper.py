# Collecting Book Data
# Angel Henriquez and Kyle Hudson

# Run this code in R using RScript option on tab at bottom right of this panel
# install.packages("reticulate")
# install.packages("urllib")
# Confirm reticulate package is installed using installed.packages()
library(reticulate)

# Install python packages (using R) once
py_install("pandas")
py_install("requests")
py_install("bs4")

# turns RStudio into Python code
reticulate::repl_python()

# Run the rest of the code in Python
# Python packages
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Creating columns 
column1 = []
column2 = []
column3 = []
column4 = []
column5 = []
column6 = []

# loop to extract data from library things and goodreads
for book_number in range(1,10):
   try: # LibraryThings Author
      bookInfo = requests.get("https://www.librarything.com/work/" + str(book_number))
      bookInfo.raise_for_status()
      author = bs4.BeautifulSoup(bookInfo.text, 'html.parser').select('h2 a')[0].getText()
      column1.append(author)
   except:
      column1.append('N/A')
   try: # LibraryThings Title
      bookInfo = requests.get("https://www.librarything.com/work/" + str(book_number))
      bookInfo.raise_for_status()
      title = bs4.BeautifulSoup(bookInfo.text, 'html.parser').select('.headsummary h1')[0].getText()
      column2.append(title)
   except:
      column2.append('N/A')
   try: # LibraryThings Rating
      bookInfo = requests.get("https://www.librarything.com/work/" + str(book_number))
      bookInfo.raise_for_status()
      bookRating = float(bs4.BeautifulSoup(bookInfo.text, 'html.parser').select('.dark_hint')[0].getText().split('(')[1].split(')')[0])
      column3.append(bookRating)
   except:
      column3.append('N/A')
   try: # Goodreads Author
      bookInfo2 = requests.get("https://www.goodreads.com/book/show/" + str(book_number))
      bookInfo2.raise_for_status()
      author2 = bs4.BeautifulSoup(bookInfo2.text, 'html.parser').find("span", itemprop="name").getText()
      column5.append(author2)
   except:
      column4.append('N/A')
   try: # Goodreads Title
      bookInfo2 = requests.get("https://www.goodreads.com/book/show/" + str(book_number))
      bookInfo2.raise_for_status()
      title2 = bs4.BeautifulSoup(bookInfo2.text, 'html.parser').select('h1#bookTitle')[0].getText().strip()
      column4.append(title2)
   except:
      column5.append('N/A')
   try: # Goodreads Rating
      bookInfo2 = requests.get("https://www.goodreads.com/book/show/" + str(book_number))
      bookInfo2.raise_for_status()
      rating2 = float(bs4.BeautifulSoup(bookInfo2.text, 'html.parser').find("span", itemprop="ratingValue").getText().strip())
      column6.append(rating2)
   except:
      column6.append('N/A')

# Columns for Library Thing
df1 = pd.DataFrame(column1, columns=["LT Author"])
df2 = pd.DataFrame(column2, columns=["LT Title"])
df2 = df2.replace("&#039;", "'")
df3 = pd.DataFrame(column3, columns=["LT Rating"])

# Columns for Goodreads
df4 = pd.DataFrame(column4, columns=["GR Author"])
df5 = pd.DataFrame(column5, columns=["GR Title"])
df5 = df5.replace("&amp;", "&")
df5 = df5.replace("&quot;", '"')
df6 = pd.DataFrame(column6, columns=["GR Rating"])

# merged DataFrame
Books = [df1, df2, df3, df4, df5, df6]
Books = pd.concat(Books, axis=1, join="outer")
books1 = pd.DataFrame(Books)
# View(books1)

# Saving all book data to CSV file
# Books.to_csv('BookData.csv')
