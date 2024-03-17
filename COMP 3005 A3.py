# COMP 3005 A3
# HARUN MWONDI
# 101207477


# This is the library required to connect postgreSQL to a python program

import psycopg2
from psycopg2 import IntegrityError

# This is the connection established to the school database where I will create the students table. Ensure this has been adjusted to suit you settings to ensure the connection is set up successfully.

conn = psycopg2.connect(database = "school", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)

#These are the function associated with the database

# getAllstudents()
def getAllstudents():
     

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command 
    cur.execute ('SELECT * FROM students;')
    stud_rows = cur.fetchall()

    # Close cursor 
    cur.close()
    
    print("\nThese are all the students currently in the database :\n ")
    for row in stud_rows:
        print(row)    

# addStudent() function

def addStudent():
    print("Please provide the first name :")
    fname=input()
    print(" second name :")
    sname=input()
    print( " email :")
    email=input()
    print("enrollment date in the format YYYY-MM-DD :")    
    date= input()
    
    cur = conn.cursor()
    
    cur.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    (%s , %s , %s, %s);""" , (fname , sname , email , date))

    # Make the changes to the database present
    conn.commit()
    

    print( "The student has been added to the database")

# updateStudentEmail()

def updateStudentEmail( ):
    
    # Request relevant data from the user 
    print("Please provide the student ID of the student you want to update")
    student_id=input()
    print("Please provide the new email")
    new_email=input()
    
    cur = conn.cursor()
    
    cur.execute("UPDATE students SET email = %s WHERE student_id = %s ;" , (new_email ,  student_id ))
    
    conn.commit()
    
    print( "The student email has been updated accordingly")
    
    

# deleteStudent()

def deleteStudent( ):
    print("Please provide the student ID of the student you want to remove")
    student_id=input()
    
    cur = conn.cursor()
    cur.execute(" DELETE FROM students WHERE student_id = %s ;" , (student_id,))
    conn.commit()
    cur.close()
    
# closes the connection to the databse before ending the program

def wipe():
    #close connection to database at end of program 
    conn.close()    
    

# Main function for the program

def main():

    # CREATING THE STUDENTS TABLE and POPULATE IT WITH DATA PROVIDED

    cur = conn.cursor()
    
    # Execute a command: create students table
    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        student_id SERIAL  PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        enrollment_date DATE);
                """)
    
    # Inserting original Data if it does not exist
    try:
        cur.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');""")
        print(" Data insertion was successful !")
        
    # If the data violates the unique constraint , the program alerts the user that the data already exists in the table
    
    except IntegrityError as e : 
        print("The values you are trying to insert either exist or happen to be a duplicate value !")

    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    
    
    # User is alerted that the database has been set up
    
    print ("\nDatabase is ready to go !\n")
    
    # Main program begins
    choice="0"
    
    while (choice):
        print("\nWelcome to the student database , what would you like to do today :\n( Choose number option)\n \n1.) Display all students \n2.) Add a student \n3.) Update a student's email \n4.) Remove a student from the database \n5.) Exit and wipe data from the table ")
        
        choice = input()
    
        if choice=="1":
            getAllstudents()
        elif choice=="2":
            addStudent()
        elif choice=="3":
            updateStudentEmail()
        elif choice=="4":
            deleteStudent()
        elif choice=="5":
            wipe()
            print("Ciao !")
            return
        choice="0"

        
    
main()