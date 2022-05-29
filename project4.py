import os
from bplustree import *
## create type

trees = {}

def closeDatabase():
    global trees
    for typeName in trees.keys():
        tree = trees[typeName]
        fileName = typeName + "_tree.txt"
        tree.writeFile(fileName)
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
def createEmptyTreeFile(typeName):
    global trees
    fileName = typeName + "_tree.txt"
    f = open(fileName, "x")
    f.write("LastNode")
    f.close()
    tree = BPlusTree(order = 4)
    tree.built(fileName)
    trees[typeName] = tree
def createEmptyFile(file):
    for pageNumber in range(4):
        file.write("#" + str(pageNumber) + "#00000000\n")
        for recordNumber in range(8):
            file.write("$" + str(recordNumber) + "$")
            for i in range(12):
                file.write(" " * 20)
            file.write("\n")
def createType(stat):

    st = stat
    words = st.split()
   
    typeName = words[2]
    print(f"creating of {typeName} has started")
    f = open("system_cat.txt","r")
    for x in f:
        try:
            line = x.split(",")
            #print(line[1])
            if(line[1]==typeName):
                print("Type exists")
                return
            else:
                continue
        except:
            print("there is an error")
            continue
    f.close()
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
    
            
    ## for system catalog
    file = open("system_cat.txt","a") 
    for a in range(int(numberOfField)):
        ##arg1= "{:<20}".format(fieldArray[a][0])  NO NEED TO FILL TO 20 FOR SYSTEM CATALOG
        arg1 = fieldArray[a][0]
        
        arg2=""
        if fieldArray[a][1]=="str":
            arg2 = "s"
        else:
            arg2 = "i"
        position = str(a).zfill(2)
        ##typeToWrite = "{:<20}".format(typeName)  NO NEED TO FILL TO 20 FOR SYSTEM CATALOG
        typeToWrite = typeName
        pKey = 0
        if(a==int(primaryKeyOrder)-1):
            pKey=1 
        file.write(arg1+","+typeToWrite+","+arg2+","+position+","+str(pKey)+"\n")
    #try:
    fileObject = open(f"000_{typeName}.txt","x")
    # update File Object Header.
    primaryKeyToWrite = str(int(primaryKeyOrder) - 1).zfill(2)
    fileObject.write("!000!" + "aaaaa" + "!" + primaryKeyToWrite + "!00!0000\n")
    createEmptyFile(fileObject)
    createEmptyTreeFile(typeName)
    countFileObject = open("file_name_count.txt","a")
    countFileObject.write(typeName+","+"1"+"\n")
    countFileObject.close()
    #except:
    #    print("Burada hata var, initial file olusturma")
    fileObject.close()
    print("creating process is done")
    file.close()
def deleteFromCountFile(typeName):
    try:
        f = open("file_name_count.txt", "r")
    except:
        print("File could not be opened (file_name_count)")

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
        print("New file could not be opened (file_name_count)")
    
    for line in lines:
        new_file.write(line)
    new_file.close()
def deleteFromCatalogFile(typeName):
    try:
        f = open("system_cat.txt","r")
    except:
        print("File could not be opened (system_cat)")

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
        print("File could not be opened (system_cat)")
    for line in lines:
        new_file.write(line)

    new_file.close()
def deleteAllDataFiles(typeName):
    for i in range(1000):
        indexToCheck = str(i).zfill(3)
        try:
            os.remove(indexToCheck + "_" + typeName + ".txt")
        except:
            continue
## delete type
def deleteType(stat):
    st = stat
    words = stat.split()
    typeName = words[2]
    deleteFromCatalogFile(typeName)
    deleteFromCountFile(typeName)
    deleteAllDataFiles(typeName)
    try:
        os.remove(typeName + "_tree.txt")
    except:
        print("Tree file does not exist")
    if(typeName in trees):
        del trees[typeName]
    print("Successfully deleted")
def listTypes():
    try:
        f = open("file_name_count.txt","r")
    except:
        print("File could not be opened (file_name_count)")
    
    lines = f.readlines()
    for line in lines:
        print(line.split(",")[0])

def createRecord(statement):
    array = statement.split()
    typeName = array[2]
    fields = []
    global trees
    try:
        f = open("system_cat.txt","r")
    except:
        print("File could not be opened (system_cat)")
    
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
    
    valueToInsert = ""
    for i in range(numberOfFields):
        element = array[i + 3]
        fields.append(element)
        element = element.ljust(20)
        valueToInsert += element
    valueToInsert = valueToInsert.ljust(240)

    primaryValue = fields[int(primaryKey)]
   
    tree = trees[typeName]
    if(tree.retrieve(primaryValue) != None):
        print("Key already exists")
        return

    try:
        f = open("file_name_count.txt","r")
    except:
        print("File could not be opened (file_name_count)")
    
    lines = f.readlines()
    f.close()
    numberOfFiles = 0
    
    for line in lines:
        if(line.split(",")[0] == typeName):
            numberOfFiles = line.split(",")[1] # line.split(",")[1][:-1] For windows
    #print(numberOfFiles)
    for i in range(int(numberOfFiles)):
        position = str(i).zfill(3)
        fileName = position + "_" + typeName + ".txt"
        #print(fileName)
        try:
            f = open(fileName,"r+")
        except:
            print("File could not be opened ()")
        fileHeader = f.readline()
        all = f.readline()
        #print(all)
        #print(fileHeader.split("!"))
        emptyPlaces = fileHeader.split("!")[4]
        if(len(emptyPlaces) != 4):
            emptyPlaces = fileHeader.split("!")[5]
        
        for j in range(4):
            
            if(emptyPlaces[j] == "0"):
                f.seek( 22 + 1964* j) #22+1964 for MacOS // 23 + 1973 * j For windows
                emptyPageHeader = f.readline()
                #print(emptyPageHeader)
                #print(emptyPageHeader.split("#"))
                emptyRecords = emptyPageHeader.split("#")[1]
                if(len(emptyRecords) != 8):
                    emptyRecords = emptyPageHeader.split("#")[2]
                #print(emptyRecords)
                for k in range(8):
                    if(emptyRecords[k] == "0"):
                        index = (22 + 1964 * j + 12 + 244 * k) # 22 + 1964 * j + 12 + 244 * k for MacOS  // 23 + 1973 * j + 13 + 245 * k For Windows
                        f.seek(index)
                        value = "$" + str(k) + "$" + valueToInsert + "\n"
                        #print(value)
                        f.write(value)
                        indexPageHeader = (22 + 1964 * j + 3 + k) #22 + 1964 * j + 3 + k for MacOS  // 23 + 1973 * j + 3 + k For windows
                        f.seek(indexPageHeader)
                        f.write("1")
                        indexPageHeader = (22 + 1964 * j + 3) #22 + 1964 * j + 3 for MacOS // 23 + 1973 * j + 3 for windows
                        f.seek(indexPageHeader)
                        emptyRecordsAfter = f.read(8)
                        Full = True
                        for l in range(len(emptyRecordsAfter)):
                            if(emptyRecordsAfter[l] == "0"):
                                Full = False
                                break
                        if(Full):
                            indexFileHeader = (17 + j)
                            f.seek(indexFileHeader)
                            f.write("1")

                        
                        recordNumberFileHeader = 14
                        f.seek(14)
                        recordNumber = int(f.read(2)) + 1
                        f.seek(14)
                        f.write(str(recordNumber).zfill(2))

                        # Insert to tree
                        tree = trees[typeName]
                        tree.insert(primaryValue , position + str(j) + str(k))
                        f.close()
                        return True
    # Open new file.
    newNumOfFiles = str(int(numberOfFiles))
    NewFile = newNumOfFiles.zfill(3)+"_"+typeName+".txt"
    new = open(NewFile,"x")
    new.close()
    newWrite = open(NewFile,"w")
    newFileHeader ="!"+newNumOfFiles.zfill(3)+"!"+"aaaaa"+"!"+ str(primaryKey).zfill(2) + "!00!0000\n"  ##Record number is initialized as "00" but after creating it must be updated
    newWrite.write(newFileHeader)
    createEmptyFile(newWrite)
    newWrite.close()



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

    return createRecord(statement)

def deleteRecord(statement):
    array = statement.split()
    typeName = array[2]
    primaryKey = array[3]
    try:
        f = open("system_cat.txt","r")
    except:
        print("File could not be opened (system_cat)")

    lines = f.readlines()
    f.close()
    hasType=False
    for line in lines:
        elements = line.split(",")
        if(elements[1] == typeName):
            hasType = True
    if(hasType==False):
        return False
    tree = trees[typeName]
    value = tree.retrieve(primaryKey)
    #print(value)
    if(value == None):
        print("Key doesn't exist")
        return
    value = tree.retrieve(primaryKey)[0]

    file = str(value[0:3])+"_"+typeName+".txt"
    page = int(value[3:4])
    record = int(value[4:5])
    try:
        f = open(file,"r+")
    except:
        print("Can not open to file to delete record")
        return
    
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

    tree.delete(primaryKey)

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
        print("No Type")
        return
    if(numberOfFields!=(len(array)-4)):
        print("fields not enough")
        return
    valueToInsert = ""
    for i in range(numberOfFields):
        element = array[i + 4]
        fields.append(element)
        element = element.ljust(20)
        valueToInsert += element
    valueToInsert = valueToInsert.ljust(240)

    
    tree = trees[typeName]
    value = tree.retrieve(primaryKey)
    if(value == None):
        print("Key doesn't exist")
        return
    value = tree.retrieve(primaryKey)[0]
    file = str(value[0:3])+"_"+typeName+".txt"
    page = int(value[3:4])
    record = int(value[4:5])
    try:
        f = open(file,"r+")
    except:
        print("Can not open to file to update record")
        return
    
    index = (22 + 1964 * page + 12 + 244 * record) # 22 + 1964 * j + 12 + 244 * k for MacOS // 23 + 1973 * page + 13 + 245 * record for Windows
    f.seek(index)
 
    value = "$" + str(record) + "$" + valueToInsert.ljust(240) + "\n"
    f.write(value)

def searchRecord(statement):
    array = statement.split()
    typeName =  array[2]
    primaryKey = array[3]
    #print(primaryKey)
    global trees
    try:
        f = open("system_cat.txt","r")
    except:
        #print("File could not be opened (system_cat)")
        return ("Error: File could not be opened (system_cat)")
    
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
    #print(tree.retrieve(primaryKey))
    value = tree.retrieve(primaryKey)
    if(value==None):
        #print("Key doesn't exist to search record")
        return ("Error: Key doesn't exist to search record ")
    value = value[0]
    file = str(value[0:3])+"_"+typeName+".txt"
    page = int(value[3:4])
    record = int(value[4:5])
    try:
        f = open(file,"r")
    except:
        #print("Can not open to file to search record")
        return ("Error: Can not open to file to search record")
    
    index = (22 + 1964 * page + 12 + 244 * record ) # 22 + 1964 * j + 12 + 244 * k for MacOS // 23 + 1973 * page + 13 + 245 * record for windows
    f.seek(index+3)
    
    
    returnString = ""
  
    for i in range(numberOfFields-1):
        field = f.read(20).strip()
        returnString = returnString + field + " "
        
    field = f.read(20).strip()
    returnString = returnString + field + " "
    #print(returnString)
    return returnString

def listRecord (typeName):
    records = []
    try:
        f = open("system_cat.txt","r")
    except:
        print("File could not be opened (system_cat)")
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
        print("No Type")
        return
    
    global trees
    try:
        tree = trees[typeName]
    except:
        print("There is no such type exists")
        return
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
                print("Can not open to file to list record")
                return
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
    #arr = []
    #print(tree.showAllData(arr))
    #print(arr)

def findFieldIndexWithName(name, typeName):
    try:
        f = open("system_cat.txt","r")
    except:
        print("File could not be opened (system_cat)")
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
        print("No Type")
        return

def filterRecord(typeName, condition):
    global trees
    tree = trees[typeName]
    results = []
    fieldToCheckFor = ""
    conditionToCheckFor = ""
    if("=" in condition):
        fieldToCheckFor = condition[0:condition.index("=")]
        conditionToCheckFor = condition[condition.index("=")+1:]
        findedField = findFieldIndexWithName(fieldToCheckFor, typeName)
        if(findedField == None):
            return("Error: There is no such field for that type filtering")
        indexToCheck = int(findedField[0])
        #isInteger = False
        #if(findedField[1] == "i"):
        #    isInteger = True
        result = searchRecord("search record " + typeName + " " + conditionToCheckFor)
        if("Error" in result):
            return result
        else:
            results.append([result])
            return results
    elif("<" in condition):
        fieldToCheckFor = condition[0:condition.index("<")]
        conditionToCheckFor = condition[condition.index("<")+1:]
        findedField = findFieldIndexWithName(fieldToCheckFor, typeName)
        if(findedField == None):
            return("Error: There is no such field for that type filtering")
        indexToCheck = int(findedField[0])
        isInteger = False
        if(findedField[1] == "i"):
            isInteger = True
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
    elif(">" in condition):
        fieldToCheckFor = condition[0:condition.index(">")]
        conditionToCheckFor = condition[condition.index(">")+1:]
        findedField = findFieldIndexWithName(fieldToCheckFor, typeName)
        if(findedField == None):
            return("Error: There is no such field for that type filtering")
        indexToCheck = int(findedField[0])
        isInteger = False
        if(findedField[1] == "i"):
            isInteger = True
        if(isInteger):
            rightMost = tree.getRightmostLeaf()
            ended = False
            while rightMost:
                #print(rightMost.keys)
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
                for key in rightMost.keys:
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
    return results
### run the file
def main():

    initializeDatabase()
    while True:
    #for i in range(0, 1):
        #inp = "create record angel Tyrael" + str(i) + " a a " + str(i)
        #inp = "create type angel 4 1 name str alias str affiliation str deneme int"
        #inp = "delete type angel"
        #inp = "filter record angel deneme<100"
        inp = input()
        if (inp == ""):
            break
        fields = inp.split()
        numberOfFields = len(fields)
        operation = fields[0]+fields[1]
        if(operation == "createtype"):
            if(numberOfFields < 7):
                print("Input cannot have less than 1 fields for create type")
                continue
            createType(inp)
        elif(operation == "deletetype"):
            if(numberOfFields != 3):
                print("Input is not in correct structure")
                continue
            deleteType(inp)
        elif(operation == "listtype"):
            if(numberOfFields != 2):
                print("Input is not in correct structure")
                continue
            listTypes()
        elif(operation == "createrecord"):
            if(numberOfFields < 4):
                print("Input cannot have less than 1 fields for create record")
                continue
            createRecord(inp)
        elif(operation == "deleterecord"):
            if(numberOfFields != 4):
                print("Input is not in correct structure")
                continue
            deleteRecord(inp)
        elif(operation == "updaterecord"):
            if(numberOfFields < 4):
                print("Input cannot have less than 1 fields for delete record")
                continue
            updateRecord(inp)
        elif(operation == "searchrecord"):
            if(numberOfFields != 4):
                print("Input is not in correct structure")
                continue
            result = searchRecord(inp)
            print(result)
        elif(operation == "listrecord"):
            if(numberOfFields != 3):
                print("Input is not in correct structure")
                continue
            typeName = fields[2]
            records = listRecord(typeName)
            if(records == None):
                continue
            for entry in records:
                for field in entry:
                    print(field, end = " ")
                print()
        elif(operation == "filterrecord"):
            if(numberOfFields != 4):
                print("Input is not in correct structure")
                continue
            typeName = fields[2]
            condition = fields[3]
            records = filterRecord(typeName, condition)
            if("Error" in records):
                print(records)
                continue
            for entry in records:
                for field in entry:
                    print(field, end = " ")
                print()

    closeDatabase()
    #create = "create type angel 3 1 name str alias str affiliation str"
    
    ##CREATE
    #createRecordString = "create record angel angelaa Archangkerkrce HighHeavens"
    #deleteRecordString = "delete record angel newFile"
    #updateRecordString = "update record angel newFile newFile AspectOfWisdom Horadrim"
    #searchRecordString = "search record angel newFile"
    #Created=createRecord(createRecordString)
    #if(not(Created)):
    #   createRecord(createRecordString)

    ##CREATE
    
    #createRecord(createRecordString)
    #closeDatabase()
    #createType(create)
    #deleteType("delete type angel")
    #updateRecord(updateRecordString)
    #searchRecord(searchRecordString)
    #deleteRecord(deleteRecordString)
    #print(listRecord("angel"))
    #ListTypes()
    #print(filterRecord("angel" , "affiliation=HighHeavens"))
    #print(findFieldIndexWithName("a", "eviaal"))
    #closeDatabase()
if __name__ == "__main__":
    main()
