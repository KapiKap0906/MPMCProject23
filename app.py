import sqlite3
import statistics

THRESHOLD = 5

crsr = sqlite3.connect('Marks.sqlite')

c = crsr.cursor()

def createTable(tableName, Cols, Datatypes,):
    crsr = sqlite3.connect('Marks.sqlite')

    c = crsr.cursor()
    with crsr:
            try:
                query = f"CREATE TABLE IF NOT EXISTS {tableName} ("

                columns_info = [f"{col_name} {col_type}" for col_name, col_type in zip(Cols, Datatypes)]

                query += ', '.join(columns_info)
                query += ");"

                crsr.execute(query)
                print(f"Table '{tableName}' created successfully.")
            except sqlite3.Error as e:
                print(f"Error creating table '{tableName}': {e}")

def updateStudent(table_name, column_name, new_value, condition_column, condition_value):
    crsr = sqlite3.connect('Marks.sqlite')

    c = crsr.cursor()

    try:
        query = f"UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?"
        
        crsr.execute(query, (new_value, condition_value))
        
        c.commit()

        print(f"Value in column '{column_name}' updated to '{new_value}' where '{condition_column}' is '{condition_value}'.")
    except sqlite3.Error as e:
        print(f"Error updating value in column '{column_name}': {e}")
    finally:
        c.close()
        crsr.close()
        updateAverages(table_name)


def updateAverages(tableName):
    c.execute(f"PRAGMA table_info({tableName})")
    columns = [column[1] for column in c.fetchall()]
    columns = columns[1:]
    for column in columns:
        calculateAverage(tableName,column)

def calculateAverage(tableName, columnNames):
    crsr = sqlite3.connect('Marks.sqlite')

    c = crsr.cursor()

    try:
        c.execute(f"SELECT {columnNames} FROM {tableName}")
        column_values = c.fetchall()

        column_average = statistics.mean([value[0] for value in column_values[1:]])

        #The below code will be used for larger scale updates and is used as a reference for upscaling

        '''query = f"UPDATE {tableName} SET "

        c.execute(f"PRAGMA table_info({tableName})")
        columns = [column[1] for column in c.fetchall()]
        columns = columns[1:]

        for index in range(len(columns)-1):
            query = query + str(columns[index]) + f" = {column_average}, "
        query = query + str(columns[-1]) + f" = {column_values} WHERE name = 'Average'"

        c.execute(query)
        
        crsr.commit()'''

        c.execute(f"UPDATE {tableName} SET {columnNames} = {column_average} WHERE name = 'Average'")

        crsr.commit()

        print(f"Updated average to'{column_average}'.")
    except sqlite3.Error as e:
        print(f"Error updating value in column: {e}")
    finally:
        c.close()
        crsr.close()

def insertStudent(studentName, TheoryMarks, LabMarks):
    with crsr:
        c.execute(f"INSERT INTO TheoryMarks VALUES('{studentName}', {TheoryMarks[0]}, {TheoryMarks[1]}, {TheoryMarks[2]})")
        c.execute(f"INSERT INTO LabMarks VALUES('{studentName}', {LabMarks[0]}, {LabMarks[1]})")
    updateAverages('TheoryMarks')
    updateAverages('LabMarks')

def getStudentMarks(tableName, studentName):
    c.execute(f"SELECT * FROM {tableName}  WHERE name = '{studentName}'")
    markList = c.fetchone()
    markList = markList[1:]
    return markList

def getAverageMarks(tableName):
    c.execute(f"SELECT * FROM {tableName} WHERE name = 'Average'")
    avgMarks = c.fetchone()
    avgMarks = avgMarks[1:]
    return avgMarks

def studentAverageDeviation(tableName, studentName):
    markList = getStudentMarks(tableName,studentName)
    avgMarks = getAverageMarks(tableName)
    markCount = len(markList)

    for row in markList:
        row = int(row)
    for row in avgMarks:
        row = int(row)
    
    markDeviations = []

    for index in range(markCount):
        markDeviations.append(markList[index]-avgMarks[index])
    return (sum(markDeviations)/len(markDeviations))

def StudentPerfomance(studentName):
    TheoAvgDev = studentAverageDeviation('TheoryMarks', studentName)
    LabAvgDev = studentAverageDeviation('LabMarks', studentName)
    performanceCoefficient =  TheoAvgDev - LabAvgDev

    if performanceCoefficient > THRESHOLD or performanceCoefficient*-1 > THRESHOLD:
        if sum(getStudentMarks('TheoryMarks', studentName))/len(getStudentMarks('TheoryMarks', studentName)) > sum(getAverageMarks('TheoryMarks'))/len(getAverageMarks('TheoryMarks')):
            print(f"{studentName} is good but can improve in Practicals")
            return True
        elif sum(getStudentMarks('LabMarks',studentName))/len(getStudentMarks('LabMarks',studentName)) > sum(getAverageMarks('LabMarks'))/len(getAverageMarks('LabMarks')):
            print(f"{studentName} is good but can improve in Theory")
            return True
        else:
            if performanceCoefficient > 0:
                print(f"{studentName} is slow in Practicals")
                return False
            elif performanceCoefficient < 0:
                print(f"{studentName} is slow in Theory")
                return False
            else:
                print(f"{studentName} is a Slow Learner")
                return False
    else:
        print(f"{studentName} is an competant student")
        return True


#Main Function
'''
c.execute("SELECT name FROM TheoryMarks")
nameList =  c.fetchall()
remedialList = []
for name in nameList:
    if not (StudentPerfomance(name[0])):
        remedialList.append(name[0])

print("The following students need remedial classes:\n")
for index in range(len(remedialList)):
    print(remedialList[index])
'''
updateAverages('LabMarks')