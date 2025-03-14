import sqlite3
#Connecting to sqlite

connection=sqlite3.connect('Student.Db') # here once we call that it is getting saved 

# we create a cursor object that perform insertion, deletion , create table and retrieve
cursor=connection.cursor() # Creating the object, see here connection itself an instance or object of the sqlite3.connect, here we are returning the configured class instance actually
print (cursor ) # Here this cursor actually pointing to the database, this cursor may point to different different location everytime we run, because it is an instance to some other class, but always points to the same db from the start as we mentioned
# Creating the table information
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS  VARCHAR(25),SECTION VARCHAR(25), MARKS INT);

"""
cursor.execute(table_info) # Creating the table with the information provided , it will execute whatever we written in the table_info  , once created it will stored in the database
# Creating the insert info
insert_info="""
insert into student (NAME,CLASS,SECTION,MARKS) values('Amartya', '10th', 'A', 85),
('Jane Smith', '10th', 'B', 90),
('Alice Johnson', '11th', 'A', 78),
('Bob Brown', '11th', 'B', 82)


"""
cursor.execute(insert_info)
show_info="""
select *from STUDENT


"""
data=cursor.execute(show_info)
print('Data created')
for row in data:
    print(row)
#Connection commiting 
connection.commit() # we need to commit otherwise the inserting records won't be saved ,without that it might show inserted to that db but won't save if we run again
connection.close()


