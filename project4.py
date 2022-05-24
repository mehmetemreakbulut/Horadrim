import os

## create type

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
    try:
        fileObject = open(f"000_{typeName}.txt","x")
        # update File Object Header.
        primaryKeyToWrite = str(int(primaryKeyOrder) - 1).zfill(2)
        fileObject.write("!000!" + typeName + "!" + primaryKeyToWrite + "!00!0000\n")
        createEmptyFile(fileObject)
        countFileObject = open("file_name_count.txt","a")
        countFileObject.write(typeName+","+"1")
        countFileObject.close()
    except:
        print("Burada hata var, initial file olusturma")
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
    print("Successfully deleted")

def ListTypes():
    try:
        f = open("file_name_count.txt","r")
    except:
        print("File could not be opened (file_name_count)")
    
    lines = f.readlines()
    for line in lines:
        print(line.split(",")[0])

### run the file
def main():
    create = "create type angel 3 1 name str alias str affiliation str"
    #createType(create)
    #deleteType("delete type angel")
    ListTypes()
if __name__ == "__main__":
    main()