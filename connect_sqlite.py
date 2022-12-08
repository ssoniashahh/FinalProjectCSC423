import sqlite3
import pandas as pd

# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory
db_connect = sqlite3.connect('test.db')

# Instantiate cursor object for executing queries
cursor = db_connect.cursor()

# String variable for passing queries to cursor
query = """
    CREATE TABLE Clinic (
        clinicNo int NOT NULL primary key CHECK (clinicNo > 0),
        name varchar(255),
        address varchar(255) NOT NULL,
        telNo varchar(10) NOT NULL CHECK(length(telNo) == 10)
        );
    """
cursor.execute(query)

query = """
    CREATE TABLE Staff (
        staffNo int NOT NULL primary key CHECK (staffNo > 0),
        name varchar(255),
        address varchar(255),
        telNo varchar(10) CHECK(length(telNo) == 10),
        DOB date CHECK (DOB <= '2004-1-1'),
        position varchar(255),
        salary int CHECK (salary >= 0),
        clinicNo int,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo)
        );
    """
cursor.execute(query)

query = """
    CREATE TABLE Owner (
        ownerNo int NOT NULL primary key CHECK (ownerNo > 0),
        name varchar(255),
        address varchar(255),
        telNo varchar(10) CHECK(length(telNo) == 10),
        clinicNo int,
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) 
        );
    """
cursor.execute(query)

query = """
    CREATE TABLE Pet (
        petNo int NOT NULL primary key CHECK (petNo > 0),
        name varchar(255),
        DOB date,
        species varchar(255),
        breed varchar(255),
        color varchar(255),
        ownerNo int,
        clinicNo int,
        FOREIGN KEY (ownerNo) REFERENCES Owner(ownerNo),
        FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) 
        );
    """
cursor.execute(query)

query = """
    CREATE TABLE Examination (
        examNo int NOT NULL primary key,
        complaint varchar(255),
        description varchar(255),
        examDate date,
        action varchar(255),
        petNo int,
        staffNo int, 
        FOREIGN KEY (petNo) REFERENCES Pet(petNo),
        FOREIGN KEY (staffNo) REFERENCES Staff(staffNo)
        );
    """
cursor.execute(query)


# Insert row into table
clinics = [(11, 'Lake Highland', '653 S Ventura Avenue', '1112223333'),
           (12, 'Trinity', '888 Peanut Street', '2223334444'),
           (13, 'Bishop Moore', '63 E 53rd Street', '3334445555'),
           (14, 'Edgewater', '345 Carter Trail', '4445556666'),
           (15, 'AdventHealth', '7678 Yeehaw Junction', '5556667777')]
cursor.executemany('INSERT INTO Clinic VALUES(?,?,?,?);', clinics)

staff = [(16, 'Bart', '6655 W Manor Drive', '9875726490', '1987-10-23', 'Manager', 10000, 11),
         (18, 'Isa', '923 Sugarplum Trail', '9265820271', '1998-12-12', 'Vet', 20000, 11),
         (21, 'Gerald', '8913 Phillips Avenue', '5679209976', '1994-12-24', 'Vet', 30000, 11),
         (23, 'Vanessa', '9251 Point Rowe Drive', '8764561234', '2001-8-12', 'Nurse', 40000, 11),
         (17, 'Veronica', '10713 Factorial Park Drive', '9098874444', '1994-2-12', 'Receptionist', 50000, 11)]
cursor.executemany('INSERT INTO Staff VALUES(?,?,?,?,?,?,?,?)', staff)

owners = [(1, 'Martha', '123 SW Diane Avenue', '9352340000', 11),
         (2, 'Ron', '1251 N 7th Street', '1234567890', 11),
         (3, 'Julia', '619 Mills Drive', '7775564325', 11),
         (4, 'Samantha', '901 N Highland Avenue', '9998887777', 11),
         (5, 'Victor', '1635 N 3rd Street', '6665559922', 11)]
cursor.executemany('INSERT INTO Owner VALUES(?,?,?,?,?)', owners)

pets = [(6, 'Magic', '2012-11-7', 'Dog', 'Bichon', 'White', 2, 11),
        (7, 'Siddhu', '2017-12-11', 'Dog', 'Bichon', 'White', 5, 11),
        (8, 'Hari', '2020-10-19', 'Dog', 'Golden Doodle', 'White', 3, 11),
        (9, 'Janki', '2002-4-1', 'Monkey', 'Indian', 'Brown', 4, 11),
        (10, 'Aarav', '2003-11-4', 'Snake', 'Python', 'Red', 1, 11)]
cursor.executemany('INSERT INTO Pet VALUES(?,?,?,?,?,?,?,?);', pets)

exams = [(1, 'Broken Bone', 'Leg is broken', '2022-12-6', 'Adjust bone', 6, 18),
         (2, 'Allergies', 'Allergies bad when outside', '2022-12-6', 'Medication', 7, 21),
         (3, 'Broken Bone', 'Leg is broken', '2022-12-6', 'Adjust bone', 8, 18),
         (4, 'Rash', 'Rash on hip', '2022-12-6', 'Ointment Cream', 9, 21),
         (5, 'Tooth broken', 'Upper tooth is broken', '2022-12-6', 'Medication', 10, 18)]
cursor.executemany('INSERT INTO Examination VALUES(?,?,?,?,?,?,?);', exams)

# Select data
query = """
    SELECT s.staffNo, s.salary
    FROM staff s
    WHERE s.salary > 20000;
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print(' ')

query = """
    SELECT p.petNo, e.complaint
    FROM examination e, pet p
    WHERE p.petNo = e.petNo and e.complaint LIKE 'Allergies';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print(' ')

query = """
    SELECT COUNT(e.examNo), e.examDate
    FROM examination e
    WHERE examDate = '2022-12-6';
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print(' ')

query = """
    SELECT p.petNo, p.ownerNo
    FROM pet p
    WHERE p.petNo = 6;
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print(' ')

query = """
    SELECT s.clinicNo, COUNT(s.clinicNo)
    FROM staff s, clinic c
    WHERE c.clinicNo = s.clinicNo and s.clinicNo = 11;
    """
cursor.execute(query)
# Extract column names from cursor
column_names = [row[0] for row in cursor.description]
# Fetch data and load into a pandas dataframe
table_data = cursor.fetchall()
df = pd.DataFrame(table_data, columns=column_names)
# Examine dataframe
print(df)
print(df.columns)
print(' ')

# Commit any changes to the database
db_connect.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
db_connect.close()
