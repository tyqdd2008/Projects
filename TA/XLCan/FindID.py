#Find the count number of id is 4

path = r"D:\Temp\TA\XLCan\receive.txt"
fp = open(path,"r")
id = []
result = []
for line in fp.readlines():
    id.append(line[line.find("id=") + 3:line.find("l=") -1])
print set(id)
#print id
for i in range(len(id)):
    count = 0
    j = 0
    while j < len(id):
        if id[i] == id[j]:
            #print id[i]
            count = count + 1
        j = j + 1
    if count == 16:
        result.append(id[i])
        #print "\n"
print set(result)
    
    
