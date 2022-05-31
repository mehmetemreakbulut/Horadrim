import os
from bplustree import *
import time
import csv
import sys
## create type

trees = {}
# This function is for closing the database and making necessary saving operations to the files of the trees.
# Works only at the end of the program.
def closeDatabase():
    global trees
    for typeName in trees.keys():
        tree = trees[typeName]
        fileName = typeName + "_tree.txt"
        tree.writeFile(fileName)
# This function is for opening and initializing the database.
# Works at the beginning of the program.
# It opens the tree files and builts trees in order to use in the code as data structures.
def initializeDatabase():
    global trees
    f = open("file_name_count.txt","r")
    lines = f.readlines()
    f.close()
    for line in lines:
        typeName = line.split(",")[0]
        tree = BPlusTree(order = 4)
        fileName = typeName + "_tree.txt"
        tree.built(fileName)
        trees[typeName] = tree

# This function is for creating empty tree file and an empty tree as the data structure.
# It only takes typeName as the argument.
def createEmptyTreeFile(typeName):
    global trees
    fileName = typeName + "_tree.txt"
    f = open(fileName, "x")
    f.write("LastNode")
    f.close()
    tree = BPlusTree(order = 4)
    tree.built(fileName)
    trees[typeName] = tree

# This function is for creating empty files.
# Since we are creating files with blanks, it initializes a file while creating.
# A helper function.
# Takes the file object directly to initialize.
def createEmptyFile(file):
    for pageNumber in range(4):
        file.write("#" + str(pageNumber) + "#00000000\n")
        for recordNumber in range(8):
            file.write("$" + str(recordNumber) + "$")
            for i in range(12):
                file.write(" " * 20)
            file.write("\n")

# This function is for creating a type.
# It creates a type with empty files and trees as explained above.
# It also updates system catalog and file name count files.
def createType(stat):

    st = stat
    words = st.split()
   
    typeName = words[2]
    # Here we are checking whether the corresponding type exists or not.
    f = open("system_cat.txt","r")
    for x in f:
        try:
            line = x.split(",")
            if(line[1]==typeName):
                return ("Error: type exists")
            else:
                continue
        except:
            print("there is an error")
            continue
    f.close()

    # If the type does not exists in our database, we are taking its fields.
    numberOfField = words[3]
    primaryKeyOrder = words[4]
    fieldArray = []
    i=4
    while i<len(words)-1:
        i=i+1
        fieldName = words[i]
        i=i+1
        fieldType = words[i]
        fieldInfo = [fieldName,fieldType]
        fieldArray.append(fieldInfo)
    
            
    ## for system catalog. Updating the system catalog with relevant lines.
    file = open("system_cat.txt","a") 
    for a in range(int(numberOfField)):
        arg1 = fieldArray[a][0]
        arg2=""
        if fieldArray[a][1]=="str":
            arg2 = "s"
        else:
            arg2 = "i"
        position = str(a).zfill(2)
        typeToWrite = typeName
        pKey = 0
        if(a==int(primaryKeyOrder)-1):
            pKey=1 
        file.write(arg1+","+typeToWrite+","+arg2+","+position+","+str(pKey)+"\n")

    # These lines of codes is for initializing the empty files.
    fileObject = open(f"000_{typeName}.txt","x")
    primaryKeyToWrite = str(int(primaryKeyOrder) - 1).zfill(2)
    fileObject.write("!000!" + "aaaaa" + "!" + primaryKeyToWrite + "!00!0000\n")
    createEmptyFile(fileObject)
    createEmptyTreeFile(typeName)
    countFileObject = open("file_name_count.txt","a")
    countFileObject.write(typeName+","+"1"+"\n")
    countFileObject.close()
    fileObject.close()
    file.close()
    # We return success if the creation of the type successful.
    return "Success"

# This is just a helper function that deletes the type from the count file.txt
def deleteFromCountFile(typeName):
    try:
        f = open("file_name_count.txt", "r")
    except:
        return("File could not be opened (file_name_count)")

    lines = f.readlines()
    x = 0

    while x < len(lines):
        line = lines[x].split(",")
        if(line[0] == typeName):
            del lines[x]
            continue
        else:
            x += 1
    f.close()

    try:
        new_file = open("file_name_count.txt", "w")     # This time opening with "w"
    except:
        return("New file could not be opened (file_name_count)")
    
    for line in lines:
        new_file.write(line)
    new_file.close()

# Again, this is just a helper method that deletes corresponding lines from the system catalog.
def deleteFromCatalogFile(typeName):
    try:
        f = open("system_cat.txt","r")
    except:
        return("File could not be opened (system_cat)")

    lines = f.readlines()
    x=0
    while x < len(lines):
        line = lines[x].split(",")
        
        if(line[1]==typeName):
            del lines[x]
            continue
        else:
            x=x+1
    f.close()

    try:
        new_file = open("system_cat.txt", "w")  # Again, this time opening with "w"
    except:
        return("File could not be opened (system_cat)")
    for line in lines:
        new_file.write(line)

    new_file.close()

# This is for deleting all files of a given type. It is as simple as it is.
def deleteAllDataFiles(typeName):
    for i in range(1000):
        indexToCheck = str(i).zfill(3)
        try:
            os.remove(indexToCheck + "_" + typeName + ".txt")
        except:
            continue

# This function is for deleting a type. 
# It also calls the helper functions in order to delete corresponding files and updating system catalog and filecount file.
def deleteType(stat):
    st = stat
    words = stat.split()
    typeName = words[2]
    try:
        os.remove(typeName + "_tree.txt")
    except:
        return ("Error: tree file does not exists")
    # Calling helper functions
    deleteFromCatalogFile(typeName)
    deleteFromCountFile(typeName)
    deleteAllDataFiles(typeName)
    if(typeName in trees):
        del trees[typeName]
    return "Success"

# This function is for listing the types.
# It takes the output file object as the argument.
# It checks for the file_name_count and prints its lines.
# Since every type is in the file_name_count
def listTypes(output):
    try:
        f = open("file_name_count.txt","r")
    except:
        print("File could not be opened (file_name_count)")
        return("Error: file could not be opened.")
    
    lines = f.readlines()
    if(len(lines) == 0):
        return ("Error: No type exists")
    for line in lines:
        output.write(line.split(",")[0])
        output.write("\n") # For windows maybe we can use \r
    return "Success"

# This function is for creating a record.
# It takes the statement as it is and make the manipulations inside of the function.
# If the file did not created before or somehow reached to the end of the file (the file is full in other words),
# It creates another new file and updates file_count file and recalls the function itself.
def createRecord(statement):
    array = statement.split()
    typeName = array[2]
    fields = []
    global trees
    try:
        f = open("system_cat.txt","r")
    except:
        #print("File could not be opened (system_cat)")
        return("Error: catalog could not be opened")
    
    # In here we are checking that whether the type exists in our database or not.
    lines = f.readlines()
    f.close()
    numberOfFields = 0
    primaryKey = 0
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            numberOfFields += 1
            if(elements[4] == 1):
                primaryKey = elements[3]
    if(numberOfFields == 0):
        return ("Error: no type exists")
    
    # If the type exists, we are creating the line that we are going to insert.
    valueToInsert = ""
    for i in range(numberOfFields):
        element = array[i + 3]
        fields.append(element)
        element = element.ljust(20)
        valueToInsert += element
    valueToInsert = valueToInsert.ljust(240)

    primaryValue = fields[int(primaryKey)]
   
   # We are checking whether the given primary key is in our database or not.
    tree = trees[typeName]
    if(tree.retrieve(primaryValue) != None):
        return ("Error: key already exists")

    try:
        f = open("file_name_count.txt","r")
    except:
        return("Error: file could not be opened, count file.")
    
    lines = f.readlines()
    f.close()
    numberOfFiles = 0
    
    for line in lines:
        if(line.split(",")[0] == typeName):
            numberOfFiles = line.split(",")[1] # line.split(",")[1][:-1] For windows
    # In here, we are opening the file that we are going to write into.
    # In the inner loop, we are finding the page that we are going to write into, just by looking at the file header.
    for i in range(int(numberOfFiles)):
        position = str(i).zfill(3)
        fileName = position + "_" + typeName + ".txt"
        try:
            f = open(fileName,"r+")
        except:
            return("Error: file could not be opened.")
        fileHeader = f.readline()
        all = f.readline()
        emptyPlaces = fileHeader.split("!")[4]
        if(len(emptyPlaces) != 4):
            emptyPlaces = fileHeader.split("!")[5]
        
        # Here, we are looking at the file header that contains the value of the emptyness of the pages.
        for j in range(4):
            if(emptyPlaces[j] == "0"):
                f.seek( 22 + 1964* j) #22+1964 for MacOS // 23 + 1973 * j For windows
                emptyPageHeader = f.readline()
                emptyRecords = emptyPageHeader.split("#")[1]
                if(len(emptyRecords) != 8):
                    emptyRecords = emptyPageHeader.split("#")[2]
                # In here we have found the page,
                # We are looking for the empty record place just by looking at the page header.
                for k in range(8):
                    if(emptyRecords[k] == "0"):
                        index = (22 + 1964 * j + 12 + 244 * k) # 22 + 1964 * j + 12 + 244 * k for MacOS  // 23 + 1973 * j + 13 + 245 * k For Windows
                        f.seek(index)
                        value = "$" + str(k) + "$" + valueToInsert + "\n"
                        f.write(value)
                        indexPageHeader = (22 + 1964 * j + 3 + k) #22 + 1964 * j + 3 + k for MacOS  // 23 + 1973 * j + 3 + k For windows
                        f.seek(indexPageHeader)
                        f.write("1")
                        indexPageHeader = (22 + 1964 * j + 3) #22 + 1964 * j + 3 for MacOS // 23 + 1973 * j + 3 for windows
                        f.seek(indexPageHeader)
                        emptyRecordsAfter = f.read(8)
                        Full = True
                        # If all the records are full, we check for the another page.
                        # Note that we are only looking for the headers not all of the data of the pages.
                        for l in range(len(emptyRecordsAfter)):
                            if(emptyRecordsAfter[l] == "0"):
                                Full = False
                                break
                        if(Full):
                            indexFileHeader = (17 + j)
                            f.seek(indexFileHeader)
                            f.write("1")

                        # If a record place found empty, we write into it.
                        recordNumberFileHeader = 14
                        f.seek(14)
                        recordNumber = int(f.read(2)) + 1
                        f.seek(14)
                        f.write(str(recordNumber).zfill(2))

                        # Insert to tree
                        tree = trees[typeName]
                        tree.insert(primaryValue , position + str(j) + str(k))
                        f.close()
                        return "Success"
    # If we cannot find any place to insert the record.
    # We create another file into our database.
    # Then we recall the function itself.
    newNumOfFiles = str(int(numberOfFiles))
    NewFile = newNumOfFiles.zfill(3)+"_"+typeName+".txt"
    new = open(NewFile,"x")
    new.close()
    newWrite = open(NewFile,"w")
    newFileHeader ="!"+newNumOfFiles.zfill(3)+"!"+"aaaaa"+"!"+ str(primaryKey).zfill(2) + "!00!0000\n"  ##Record number is initialized as "00" but after creating it must be updated
    newWrite.write(newFileHeader)
    createEmptyFile(newWrite)
    newWrite.close()

    # Updating the file name count file. By 1.
    countFile = open("file_name_count.txt","r")
    lines = countFile.readlines()
    countFile.close()
    lineCount = 0
    while(lineCount<len(lines)):
        if(lines[lineCount].split(",")[0] == typeName):
            lines[lineCount]=typeName+","+str(int(newNumOfFiles) + 1)
        lineCount = lineCount+1
    countWrite = open("file_name_count.txt","w")
    for line in lines:
        countWrite.write(line)
    countWrite.close()

    # Recall the function itself with the new page.
    return createRecord(statement)

# This function is for deleting a specific record.
# It checks whether the type exists or not.
# Second, it finds where the record is by checking the tree.
# If the record does not exist in the tree, it means it does not exist in the database.
# If it can find successully in the tree, it finds its location by retrieving the value, then deletes it.
def deleteRecord(statement):
    array = statement.split()
    typeName = array[2]
    primaryKey = array[3]
    try:
        f = open("system_cat.txt","r")
    except:
        return ("Error: file could not be opened catalog.")
   
    # Checking whether the type exists or not.
    lines = f.readlines()
    f.close()
    hasType=False
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            hasType = True
    if(hasType==False):
        return ("Error: no type exists")
    tree = trees[typeName]
    value = tree.retrieve(primaryKey)

    # If the key does not exists in the tree, we return false.
    if(value == None):
        return ("Error: key doesn't exists")
    value = tree.retrieve(primaryKey)[0]

    file = str(value[0:3])+"_"+typeName+".txt"
    page = int(value[3:4])
    record = int(value[4:5])
    try:
        f = open(file,"r+")
    except:
        return ("Error: can not open file to delete record.")
    
    # From here, we are finding the corresponding index of  the record.
    index = (22 + 1964 * page + 12 + 244 * record) # 22 + 1964 * page + 12 + 244 * record for MacOS // 23 + 1973 * page + 13 + 245 * record for windows
    f.seek(index)
    valueToInsert=""
    value = "$" + str(record) + "$" + valueToInsert.ljust(240) + "\n"
    f.write(value)
    indexPageHeader = (22 + 1964 * page + 3 + record) #22 + 1964 * j + 3 + k for MacOS // 23 + 1973 * page + 3 + record for Windows
    f.seek(indexPageHeader)
    f.write("0")      
    
    indexFileHeader = (22 + 1964 * page + 3 ) #22 + 1964 * j + 3 for MacOS // 23 + 1973 * page + 3 for Windows
    f.seek(indexFileHeader)
    emptyRecordsAfter = f.read(8)
    Full = True
    # If the page becomes empty after the deletion, we change the file header. Make the corresponding pages emptyness to 0.
    for l in range(len(emptyRecordsAfter)):
        if(emptyRecordsAfter[l] == "1"):
            Full = False
            break
    if(Full):
        indexFileHeader = (17 + page)
        f.seek(indexFileHeader)
        f.write("0")
    f.seek(14)
    numberOfEntries = f.read(2)
    newNumberOfEntries = int(numberOfEntries) - 1
    numberOfEntriesToWrite = str(newNumberOfEntries).zfill(2)
    f.seek(14)
    f.write(numberOfEntriesToWrite)
    f.seek(14)
    numberOfEntries = f.read(2)
    # In here, we are checking whether the whole file is empty or not.
    # If the file is empty, we delete the file.
    # Then update file name count file.
    if(numberOfEntries=="00"):
        f.close()
        os.remove(file)
        countFile = open("file_name_count.txt","r")
        lines = countFile.readlines()
        countFile.close()
        lineCount = 0
        
        numberOfFiles = 0
        for line in lines:
            if(line.split(",")[0] == typeName):
                numberOfFiles = line.split(",")[1]
        #print(numberOfFiles)
        newNumOfFiles = int(numberOfFiles)-1

        lineCount = 0
        while(lineCount<len(lines)):
            if(lines[lineCount].split(",")[0] == typeName):
                lines[lineCount]=typeName+","+str(newNumOfFiles)+"\n"
            lineCount = lineCount+1
        countWrite = open("file_name_count.txt","w")
        for line in lines:
            countWrite.write(line)
        countWrite.close()

    # If we can do these operations successfully without returning an error, we return success.
    tree.delete(primaryKey)
    return "Success"

# This function is for updating a record.
# It first checks for the type and the record again,
# If it can find the record, it just changes corresponding fields.
def updateRecord(statement):
    array = statement.split()
    typeName = array[2]
    primaryKey = array[3]
    fields = []
    global trees
    try:
        f = open("system_cat.txt","r")
    except:
        print("File could not be opened (system_cat)")
        return("Error: file could not be opened, catalog.")
    
    # We are checking whether the type exists or not.
    lines = f.readlines()
    f.close()
    numberOfFields = 0
    hasType=False
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            numberOfFields += 1
            hasType = True
    if(hasType==False):
        return ("Error: no type exists")
    if(numberOfFields!=(len(array)-4)):
        return ("Error: fields not enough")
    valueToInsert = ""
    for i in range(numberOfFields):
        element = array[i + 4]
        fields.append(element)
        element = element.ljust(20)
        valueToInsert += element
    valueToInsert = valueToInsert.ljust(240)

    # We are checking whether the key exists or not.
    tree = trees[typeName]
    value = tree.retrieve(primaryKey)
    if(value == None):
        return ("Error: key doesn't exists")
    value = tree.retrieve(primaryKey)[0]
    file = str(value[0:3])+"_"+typeName+".txt"
    page = int(value[3:4])
    record = int(value[4:5])
    try:
        f = open(file,"r+")
    except:
        print("Can not open to file to update record")
        return ("Error: can not open file to update record.")
    
    # We go to the corresponding index by seek function, then write on to it.
    index = (22 + 1964 * page + 12 + 244 * record) # 22 + 1964 * j + 12 + 244 * k for MacOS // 23 + 1973 * page + 13 + 245 * record for Windows
    f.seek(index)
 
    value = "$" + str(record) + "$" + valueToInsert.ljust(240) + "\n"
    f.write(value)
    f.close()
    return "Success"

# This function is for searching a record.
# It again checks for the type and the key.
# Then it returns the value as a string.
def searchRecord(statement):
    array = statement.split()
    typeName =  array[2]
    primaryKey = array[3]
    global trees
    try:
        f = open("system_cat.txt","r")
    except:
        return ("Error: File could not be opened (system_cat)")
    
    # Check the types.
    lines = f.readlines()
    f.close()
    numberOfFields = 0
    hasType=False
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            numberOfFields += 1
            hasType = True
    if(hasType==False):
        return ("Error: No Type")
    tree = trees[typeName]
    value = tree.retrieve(primaryKey)

    # Check the key exists or not.
    if(value==None):
        return ("Error: Key doesn't exist to search record ")
    value = value[0]
    file = str(value[0:3])+"_"+typeName+".txt"
    page = int(value[3:4])
    record = int(value[4:5])
    try:
        f = open(file,"r")
    except:
        return ("Error: Can not open to file to search record")
    
    index = (22 + 1964 * page + 12 + 244 * record ) # 22 + 1964 * j + 12 + 244 * k for MacOS // 23 + 1973 * page + 13 + 245 * record for windows
    f.seek(index+3)
    
    
    returnString = ""
  
    for i in range(numberOfFields-1):
        field = f.read(20).strip()
        returnString = returnString + field + " "
        
    field = f.read(20).strip()
    returnString = returnString + field + " "
    return returnString

# This function is for listing all records of a type.
# It checks for the type, then finds all the keys in the tree of the corresponding type.
def listRecord (typeName):
    records = []
    try:
        f = open("system_cat.txt","r")
    except:
        return ("Error: file could not be opened")
    
    # Again, check for the type exists.
    lines = f.readlines()
    f.close()
    numberOfFields = 0
    hasType=False
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            numberOfFields += 1
            hasType = True 
    if(hasType==False):
        return ("Error: No type exists")
    
    global trees
    try:
        tree = trees[typeName]
    except:
        return("Error: no type exists")
    
    # We take the left most key of the tree,
    # Then iteratively, get all the values of keys.
    # Then find their location and return the values and fields as an array of array.
    node = tree.getLeftmostLeaf()
    while node:
        keys = node.keys
        for key in keys:
            values = []
            place = tree.retrieve(key)[0]
            fileNumber = place[0:3]
            page = int(place[3])
            record = int(place[4])
            file = fileNumber+"_"+typeName+".txt"
            try: 
                f = open(file,"r")
            except:
                return("Error: can not open file to list record")
            index = (22 + 1964 * page + 12 + 244 * record)
            f.seek(index+3)
            returnString = ""
            for i in range(numberOfFields-1):
                field = f.read(20).strip()
                values.append(field)
                returnString = returnString + field + " "
                
            field = f.read(20).strip()
            values.append(field)
            returnString = returnString + field + " "
            records.append(values)
            f.close()
        node = node.nextLeaf
    return records

# This is just a helper function
# It just finds the index of a field by checking its name from the system catalog.
def findFieldIndexWithName(name, typeName):
    try:
        f = open("system_cat.txt","r")
    except:
        return("Error: File could not be opened (system_cat)")
    lines = f.readlines()
    f.close()
    numberOfFields = 0
    hasType=False
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            numberOfFields += 1
            hasType = True 
            if(elements[0] == name):
                return ([elements[3], elements[2]])
    if(hasType==False):
        return ("Error: no type exists.")

# This function is for filtering the records.
# It has 3 ifs in it, respectively for = < > signs.
# It first finds the type.
def filterRecord(typeName, condition):
    global trees
    try:
        tree = trees[typeName]
    except:
        return ("Error: no type found for filtering")
    results = []
    fieldToCheckFor = ""
    conditionToCheckFor = ""

    # For the equality, it is the same as search record function, therefore we call searchRecord function inside of this code.
    if("=" in condition):
        fieldToCheckFor = condition[0:condition.index("=")]
        conditionToCheckFor = condition[condition.index("=")+1:]
        findedField = findFieldIndexWithName(fieldToCheckFor, typeName)
        if("Error" in findedField):
            return("Error: There is no such field for that type filtering")
        indexToCheck = int(findedField[0])
        result = searchRecord("search record " + typeName + " " + conditionToCheckFor)
        if("Error" in result):
            return result
        else:
            results.append([result])
            return results
    # For < sign, first, we take the leftmost node in the tree.
    # Then up until the value is reached in the condition, we take the data from the database.
    # Since every node in the tree is linked to each other, we go one by one from the left most node.
    elif("<" in condition):
        fieldToCheckFor = condition[0:condition.index("<")]
        conditionToCheckFor = condition[condition.index("<")+1:]
        findedField = findFieldIndexWithName(fieldToCheckFor, typeName)
        if("Error" in findedField):
            return("Error: There is no such field for that type filtering")
        indexToCheck = int(findedField[0])
        isInteger = False
        if(findedField[1] == "i"):
            isInteger = True
        # If the field is an integer, it changes the comparison method.
        # We cast into int to compare.
        if(isInteger):
            leftMost = tree.getLeftmostLeaf()
            ended = False
            while leftMost:
                for key in leftMost.keys:
                    if(key >= int(conditionToCheckFor)):
                        ended = True
                        break
                    result = searchRecord("search record " + typeName + " " + str(key))
                    if("Error" in result):
                        return result
                    else:
                        results.append([result])
                if(ended):
                    break
                leftMost = leftMost.nextLeaf
        # If the field to check for is not integer, we make string comparison.
        else:
            leftMost = tree.getLeftmostLeaf()
            ended = False
            while leftMost:
                for key in leftMost.keys:
                    if(key >= conditionToCheckFor):
                        ended = True
                        break
                    result = searchRecord("search record " + typeName + " " + key)
                    if("Error" in result):
                        return result
                    else:
                        results.append([result])
                if(ended):
                    break
                leftMost = leftMost.nextLeaf
    # This has the same mechanics as < sign.
    # The only difference is that we are starting from the right most node and come to the left one by one.
    elif(">" in condition):
        fieldToCheckFor = condition[0:condition.index(">")]
        conditionToCheckFor = condition[condition.index(">")+1:]
        findedField = findFieldIndexWithName(fieldToCheckFor, typeName)
        if("Error" in findedField):
            return("Error: There is no such field for that type filtering")
        indexToCheck = int(findedField[0])
        isInteger = False
        if(findedField[1] == "i"):
            isInteger = True
        if(isInteger):
            rightMost = tree.getRightmostLeaf()
            ended = False
            while rightMost:
                for key in rightMost.keys[::-1]:
                    if(key <= int(conditionToCheckFor)):
                        ended = True
                        break
                    result = searchRecord("search record " + typeName + " " + str(key))
                    if("Error" in result):
                        return result
                    else:
                        results.append([result])
                if(ended):
                    break
                rightMost = rightMost.prevLeaf
        else:
            rightMost = tree.getRightmostLeaf()
            ended = False
            while rightMost:
                for key in rightMost.keys[::-1]:
                    if(key <= conditionToCheckFor):
                        ended = True
                        break
                    result = searchRecord("search record " + typeName + " " + key)
                    if("Error" in result):
                        return result
                    else:
                        results.append([result])
                if(ended):
                    break
                rightMost = rightMost.prevLeaf
    # In order to write in sorted order, we reverse if the operation is > .
    if(">" in condition):
        return results[::-1]
    return results

# This is the main function,
# It just manipulates input and output operations.
# Calls the necessary functions for corresponding inputs.
def main():

    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    try:
        systemcatFile = open("system_cat.txt", mode="x")
        fileCountFile = open("file_name_count.txt", mode="x")
        systemcatFile.close()
        fileCountFile.close()
    except:
        pass
    try:
        f = open('horadrim-Log.csv', mode='a')
    except:
        print("File could not be opened log.")
    
    cswwriter = csv.writer(f, delimiter=',', quotechar = "'", escapechar="'", quoting = csv.QUOTE_NONE)

    try: 
        inputFile = open(inputFileName, mode = "r")
    except:
        print("Input file could not be opened,")
        return
    
    try:
        outputFile = open(outputFileName, mode = "w")
    except:
        print("Output file could not be opened")
        return
    lines = inputFile.readlines()
    inputFile.close()

    # We are initializing the database.
    initializeDatabase()

    # In here, for each operation we print success or failure.
    # Since in every error, we return "Error" keyword in the error statement.
    # Therefore, we can understand whether the function operates succesfully or not.
    for inp in lines:
        inp = inp.strip()
        fields = inp.split()
        numberOfFields = len(fields)
        operation = fields[0]+fields[1]
        # Call createType.
        if(operation == "createtype"):
            if(numberOfFields < 7):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            a = createType(inp)
            if("Success" in a):
                cswwriter.writerow([int(time.time()), inp, "success"])
            else:
                cswwriter.writerow([int(time.time()), inp, "failure"])
        # Call DeleteType
        elif(operation == "deletetype"):
            if(numberOfFields != 3):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            a = deleteType(inp)
            if("Success" in a):
                cswwriter.writerow([int(time.time()), inp, "success"])
            else:
                cswwriter.writerow([int(time.time()), inp, "failure"])
        # Call List type
        elif(operation == "listtype"):
            if(numberOfFields != 2):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            a = listTypes(outputFile)
            if("Success" in a):
                cswwriter.writerow([int(time.time()), inp, "success"])
            else:
                cswwriter.writerow([int(time.time()), inp, "failure"])
        # Call create record.
        elif(operation == "createrecord"):
            if(numberOfFields < 4):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            a = createRecord(inp)
            if("Success" in a):
                cswwriter.writerow([int(time.time()), inp, "success"])
            else:
                cswwriter.writerow([int(time.time()), inp, "failure"])
        # Call delete record.
        elif(operation == "deleterecord"):
            if(numberOfFields != 4):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            a = deleteRecord(inp)
            if("Success" in a):
                cswwriter.writerow([int(time.time()), inp, "success"])
            else:
                cswwriter.writerow([int(time.time()), inp, "failure"])
        # Call update record
        elif(operation == "updaterecord"):
            if(numberOfFields < 4):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            a = updateRecord(inp)
            if("Success" in a):
                cswwriter.writerow([int(time.time()), inp, "success"])
            else:
                cswwriter.writerow([int(time.time()), inp, "failure"])
        # Call search record
        elif(operation == "searchrecord"):
            if(numberOfFields != 4):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            result = searchRecord(inp)
            if("Error" in result):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            else:
                cswwriter.writerow([int(time.time()), inp, "success"])
            outputFile.write(result)
            outputFile.write("\n")
        # Call list record.
        elif(operation == "listrecord"):
            if(numberOfFields != 3):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            typeName = fields[2]
            records = listRecord(typeName)
            if("Error" in records):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            else:
                if(records == None):
                    cswwriter.writerow([int(time.time()), inp, "failure"])
                    continue
                if(len(records) == 0):
                    cswwriter.writerow([int(time.time()), inp, "failure"])
                    continue
                for entry in records:
                    for field in entry:
                        outputFile.write(field + " ")
                    outputFile.write("\n")
                cswwriter.writerow([int(time.time()), inp, "success"])
        # Call filter record.
        elif(operation == "filterrecord"):
            if(numberOfFields != 4):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            typeName = fields[2]
            condition = fields[3]
            records = filterRecord(typeName, condition)
            if("Error" in records):
                cswwriter.writerow([int(time.time()), inp, "failure"])
                continue
            else:
                if(records == None):
                    cswwriter.writerow([int(time.time()), inp, "failure"])
                    continue
                if(len(records) == 0):
                    cswwriter.writerow([int(time.time()), inp, "failure"])
                    continue
                for entry in records:
                    for field in entry:
                        outputFile.write(field + " ")
                    outputFile.write("\n")
                cswwriter.writerow([int(time.time()), inp, "success"])
        else:
            cswwriter.writerow([int(time.time()), inp, "failure"])
            continue

    f.close()
    # After the program ends, we close the database.
    # Save the tree files.
    closeDatabase()
if __name__ == "__main__":
    main()
