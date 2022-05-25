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
            print(line[1])
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
    file = open("system_cat.txt","w") 
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
    fileObject.write("!000!" + typeName + "!" + primaryKeyToWrite + "!00!0000\n")
    createEmptyFile(fileObject)
    createEmptyTreeFile(typeName)
    countFileObject = open("file_name_count.txt","a")
    countFileObject.write(typeName+","+"1")
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
def ListTypes():
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
            numberOfFiles = line.split(",")[1]

    for i in range(int(numberOfFiles)):
        position = str(i).zfill(3)
        fileName = position + "_" + typeName + ".txt"
        try:
            f = open(fileName,"r+")
        except:
            print("File could not be opened ()")
        fileHeader = f.readline()
        emptyPlaces = fileHeader.split("!")[5]
        for j in range(4):
            if(emptyPlaces[j] == "0"):
                f.seek(22 + 1964 * j)
                emptyPageHeader = f.readline()
                #print(emptyPageHeader)
                emptyRecords = emptyPageHeader.split("#")[2]
                #print(emptyRecords)
                for k in range(8):
                    if(emptyRecords[k] == "0"):
                        index = (22 + 1964 * j + 12 + 244 * k)
                        f.seek(index)
                        value = "$" + str(k) + "$" + valueToInsert + "\n"
                        print(value)
                        f.write(value)
                        indexPageHeader = (22 + 1964 * j + 3 + k)
                        f.seek(indexPageHeader)
                        f.write("1")
                        indexPageHeader = (22 + 1964 * j + 3)
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
                        # Insert to tree
                        tree = trees[typeName]
                        tree.insert(primaryValue , position + str(j) + str(k))
                        return
        # Open new file.





### run the file
def main():
    create = "create type angel 3 1 name str alias str affiliation str"
    createRecordString = "create record angel denemeler Archangkerkrce HighHeavens"
    initializeDatabase()
    createRecord(createRecordString)
    closeDatabase()
    #createRecord(createRecordString)
    #closeDatabase()
    #createType(create)
    #deleteType("delete type angel")


if __name__ == "__main__":
    main()

    #createType(create)
    #deleteType("delete type angel")
    #ListTypes()
    #deneme = BPlusTree(order = 4)
    #fileName = "b+tree.txt"
    #tree = deneme.built(fileName)
    #tree.insert("adanaa", "002")
    #tree.writeFile(fileName)