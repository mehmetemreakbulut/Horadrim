
## create type
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
    print("aa")
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
        createF = open(f"000_{typeName}.txt","x")
        count = open("file_name_count.txt","w")
        count.write(typeName+","+"1")
        count.close()
    except:
        pass
    createF.close()
    print("creating process is done")
    file.close()
## delete type
def deleteType(stat):
    st = stat
    words = stat.split()
    typeName = words[2]
    f = open("system_cat.txt","r")
    lines = f.readlines()
    
    print(len(lines))
    x=0
    while x < len(lines):
            print(x)
            print(lines)
            line = lines[x].split(",")
         
            if(line[1]==typeName):
                print("Field of Type")
                del lines[x]
                
                continue
            else:
                x=x+1
                continue
  

    f.close()

    new_file = open("system_cat.txt", "w")
    for line in lines:
        new_file.write(line)

    new_file.close()


### run the file
def main():
    create = "create type angel 3 1 name str alias str affiliation str"
    createType(create)
    #deleteType("delete type angel")
if __name__ == "__main__":
    main()