import datetime
import sqlite3

# this python file shows different commands and SQL statements you can use
# remove the ''' ''' between commands to uncomment and execute certain statements
# such as printing out queries or inserting data into a database
# it can be helpful to print out the patrons, books, or staff tables to see
# what data is in there while we are testing the library program

# Connecting to database / creating a database

conn = sqlite3.connect('library.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
c = conn.cursor()

# Creating tables in the database
'''
c.execute("""CREATE TABLE patrons (
first_name text collate nocase,
last_name text collate nocase,
phone_number text,
address string collate nocase,
card_number int,
amount_owed real
)""")


c.execute("""CREATE TABLE staff (
first_name text collate nocase,
last_name text collate nocase,
user text,
pass text,
phone_number text,
is_admin int,
staff_id int
)""")


c.execute("""CREATE TABLE books (
title text collate nocase,
author text collate nocase,
subject text collate nocase,
isbn int,
book_id int,
checked_out int,
due_date timestamp,
owner int
)""")
'''

# Inserting data into tables

# Clear Table
c.execute("DELETE FROM patrons")
# Add sample Patrons
address = "123 Philly Street, Fayeteville, NC"
many_patrons = [('David', 'Campbell', '342-1346', address, 10001, 0.00),
                ('Emily', 'Walsh', '837-1749', address, 10002, 0.00),
                ('Jane', 'Brown', '463-7728', address, 10003, 0.00),
                ('John', 'Peterson', '992-4261', address, 10004, 0.00),
                ('Lucy', 'Smith', '201-3918', address, 10005, 0.00),
                ('Brian', 'Griffin', '883-6576', address, 10006, 0.00),
                ('Joseph', 'Rodgers', '212-3810', address, 10007, 0.00),
                ('Michael', 'Buffet', '552-8301', address, 10008, 0.00),
                ('Amy', 'Henderson', '400-3155', address, 10009, 0.00),
                ('Carl', 'Fields', '116-9188', address, 10010, 0.00),
                ('Robert', 'Cook', '653-0012', address, 10011, 0.00),
                ('Mary', 'Williams', '029-8344', address, 10012, 0.00),
                ('Simon', 'Smith', '119-3810', address, 10013, 0.00),
                ('Karen', 'Jackson', '442-1003', address, 10014, 0.00),
                ('Betty', 'Harris', '900-7361', address, 10015, 0.00),
                ('Charles', 'Moore', '193-1773', address, 10016, 0.00),
                ('Mark', 'Davis', '042-7664', address, 10017, 0.00),
                ('Edward', 'Clark', '313-7221', address, 10018, 0.00),
                ('Jason', 'Walker', '029-3515', address, 10019, 0.00),
                ('Helen', 'Lewis', '983-1173', address, 10020, 0.00),
                ('Brandon', 'Wright', '193-8831', address, 10021, 0.00),
                ('Shirley', 'Hall', '533-7163', address, 10022, 5.01)]

# c.execute("INSERT INTO patrons VALUES ('Anne', 'Cooper', 10004, 0.00)")
c.executemany("INSERT INTO patrons VALUES (?,?,?,?,?,?)", many_patrons)


# Clear Table
c.execute("DELETE FROM staff")
# Add sample staff
many_staff = [('Mingxian', 'Jin', 'Mjin', 'csc470!', '269-5853', 0, 100),
                ('Larry', 'Miller', 'lmiller', '321book', '155-0194', 1, 101),
                ('Elizabeth', 'Anderson', 'eanderson', '111password', '811-5564', 1, 102),
                ('Samuel', 'Lopez', 'slopez', 'P@ssW0rd', '914-2210', 0, 103),
                ('Debra', 'Turner', 'dturner', 'p@SsWoRD123', '133-2617', 0, 104),
                ('Tester', 'Librarian', 'l', '22', '420-6969', 0, 105),
                ('Tester', 'Admin', 'a', '22', '420-6969', 1, 106)]

c.executemany("INSERT INTO staff VALUES (?,?,?,?,?,?,?)", many_staff)


# Clear Table
c.execute("DELETE FROM books")
# Add Sample Books
due_date = datetime.datetime.now()
isbn = 112233445566
many_books = [("Harry Potter and the Philosopher's Stone", "J. K. Rowling", "Fantasy", isbn, 10001, 0, due_date, -1),
                ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", isbn, 10002, 0, due_date, -1),
                ("Nineteen Eighty-Four", "George Orwell", "Science Fiction", isbn, 10003, 0, due_date, -1),
                ("The Hunger Games", "Suzanne Collins", "Science Fiction", isbn, 10004, 0, due_date, -1),
                ("Pride and Prejudice", "Jane Austen", "Fiction", isbn, 10005, 0, due_date, -1),
                ("Dune", "Frank Herbert", "Science Fiction", isbn, 10006, 0, due_date, -1),
                ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Science Fiction", isbn, 10007, 0, due_date, -1),
                ("The Cat in the Hat", "Dr. Seuss", "Childrens", isbn, 10008, 0, due_date, -1),
                ("Fahrenheit 451", "Ray Bradbury", "Science Fiction", isbn, 10009, 0, due_date, -1),
                ("Lord of the Flies", "William Golding", "Fiction", isbn, 10010, 0, due_date, -1),
                ("Charlotte's Web", "E.B White", "Childrens", isbn, 10011, 0, due_date, -1),
                ("Dracula", "Bram Stoker", "Horror", isbn, 10012, 0, due_date, -1),
                ("A Game of Thrones", "George R.R. Martin", "Fantasy", isbn, 10013, 0, due_date, -1),
                ("The Odyssey", "Homer", "Epic Poetry", isbn, 10014, 0, due_date, -1),
                ("A Tale of Two Cities", "Charles Dickens", "Fiction", isbn, 10015, 0, due_date, -1),
                ("Little Women", "Louisa May Alcott", "Fiction", isbn, 10016, 0, due_date, -1),
                ("Anna Karenina", "Leo Tolstoy", "Fiction", isbn, 10017, 0, due_date, -1),
                ("War and Peace", "Leo Tolstoy", "Fiction", isbn, 10018, 0, due_date, -1),
                ("The Shining", "Stephen King", "Horror", isbn, 10019, 0, due_date, -1),
                ("The Adventures of Tom Sawyer", "Mark Twain", "Fiction", isbn, 10020, 0, due_date, -1),
                ("The Scarlet Letter", "Nathaniel Hawthorne", "Fiction", isbn, 10021, 0, due_date, -1),
                ("The Hobbit", "J.R.R. Tolkien", "Fantasy", isbn, 10022, 0, due_date, -1),
                ("The Lorax", "Dr. Seuss", "Childrens", isbn, 10023, 0, due_date, -1),
                ("Treasure Island", "Robert Louis Stevenson", "Fiction", isbn, 10024, 0, due_date, -1),
                ("The Canterbury Tales", "Geoffrey Chaucer", "Fiction", isbn, 10025, 0, due_date, -1),
                ("Murder on the Orient Express", "Agatha Christie", "Mystery", isbn, 10026, 0, due_date, -1),
                ("Romeo and Juliet", "William Shakespeare", "Tragedy", isbn, 10027, 0, due_date, -1),
                ("The Complete Sherlock Holmes", "Arthur Doyle", "Mystery", isbn, 10028, 0, due_date, -1),
                ("The Time Machine", "H.G. Wells", "Fiction", isbn, 10029, 0, due_date, -1),
                ("Things Fall Apart", "Chinua Achebe", "Fiction", isbn, 10030, 0, due_date, -1),
                ("The Martian", "Andy Weir", "Science Fiction", isbn, 10031, 0, due_date, -1),
                ("The Hunchback of Notre-Dame", "Victor Hugo", "Fiction", isbn, 10032, 0, due_date, -1),
                ("Emma", "Jane Austen", "Fiction", isbn, 10033, 0, due_date, -1),
                ("The Count of Monte Cristo", "Alexandre Dumas", "Fiction", isbn, 10034, 0, due_date, -1)
                ]

c.executemany("INSERT INTO books VALUES (?,?,?,?,?,?,?,?)", many_books)


# Making Queries
'''
c.execute("SELECT * FROM staff")
#c.fetchone()
#c.fetchmany(3)

print(c.fetchall())
'''

# Formatting Results
'''
c.execute("SELECT * FROM patrons")
items = c.fetchall()
print("--------------- PATRON DATABASE ---------------")
print("NAME" + "\t\tCARD ID" + "\t\tAMOUNT OWED")
print("-----------------------------------------------")

for item in items:
    print(item[0] + " " + item[1] + "\t" + str(item[2]) + "\t\t" + str(item[3]))

'''


# Other Queries
'''
c.execute("SELECT rowid, * FROM patrons")
items = c.fetchall()

for item in items:
    print(item)
'''

'''
c.execute("SELECT * FROM patrons WHERE card_num > 10005 LIKE first 'Em%' ")
items = c.fetchall()
for item in items:
    print(item)

'''

# Update Records

'''
c.execute("""UPDATE patrons SET first = 'Eric', last = 'Roberts', card_num = 10008
            WHERE rowid = 2
            """)

c.execute("SELECT rowid, * FROM patrons")
items = c.fetchall()

for item in items:
    print(item)
'''

# Delete Records

'''
c.execute("DELETE from patrons WHERE rowid = 2")

c.execute("SELECT rowid, * FROM patrons")
items = c.fetchall()

for item in items:
    print(item)

'''

# Ordering Results By

'''
c.execute("SELECT rowid, * FROM patrons ORDER BY first") # card_num DESC
items = c.fetchall()

for item in items:
    print(item)

'''

# Ordering the Database using AND/OR

'''
c.execute("SELECT rowid, * FROM patrons WHERE first LIKE 'J%' AND amount_owed = 0")
items = c.fetchall()

for item in items:
    print(item)
'''

# Limiting Results

'''
c.execute("SELECT rowid, * FROM patrons LIMIT 4")
items = c.fetchall()

for item in items:
    print(item)
'''

# Delete an Entire Table
'''
c.execute("DROP TABLE staff")
'''

# Commit Changes
conn.commit()

# Close the connection to database
conn.close()
