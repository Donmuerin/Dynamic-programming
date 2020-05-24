f = open("outputTask1.txt",'w')
def main(m, n):
    if m < 2 or m > 5 or n < 2 or n > 3:
        raise ValueError("Out of range")

    else:
        return m, n

m = int(input("m: "))
n = int(input("n: "))
alp, num = main(m, n)#accept m,n as arguments

#find letters of English alphabets
#eg = {A,B}
storeAlp = ''
for i in range(alp):
    storeAlp += (chr(65+i))#Upper one

#find all eg. 2^3 = 8 possible  
allList = []
def findPossible(astring,alist,size):
    if len(astring) == size:
        allList.append(astring)
    else:
        for i in range(len(alist)):
            findPossible(astring+alist[i],alist,size)

findPossible('',storeAlp,num)

#create Adjacency List
tmp2 = []
for i in range(len(allList)):
    tmp = []
    for j in range(len(allList)):
        if allList[i][1:] == allList[j][:len(allList[j])-1]:
            tmp.append(allList.index(allList[j]))#maybe can save memory
    tmp2.append(tmp)

#---test eulerian path------
#tmp3 = [[1],[2],[0,3],[1]]
#tmp3 = [[1],[3,4],[1],[2],[0,3]]
    
def inner(path,tmp,curr):
    while True:
        path.append(tmp[curr][0])
        del tmp[curr][0]#keep [] to check
        #if the element we looking for is not empty
        if tmp[path[len(path)-1]] != []:
            curr = path[len(path)-1]
        else:
            return path
           
#only accept eulerian cycle            
def eulerian_aux(tmp):
    """
    For a graph G(V, E) containing an Eulerian cycle(!!), Carl Hierholzer in 1873 proposed a simple
    algorithm to find such a cycle that can be implemented to run in O(|E|)-time.
    Complexity = O(|E|)
    """
    curr = tmp[0][0]
    path = [curr]#init as list
    path = inner(path,tmp,curr)#find the first one
    #continue with other possible edges(still have edge)
    for i in range(len(path)):
        if tmp[path[i]] != []:#if the one we looking for not empty - still have edge
            curr = path[i]
            another = [curr]#init as list
            another = inner(another,tmp,curr)#find another cycle
            path = path[:i] + another + path[i+1:]#merge
    #if all empty eg: [[],[],...]           
    return path

#Not really need - Not likely to happen neh!    
#accept both - check if cycle or path
def eulerian_main(tmp2):
    """
    O(N^2)
    """
    goIn = {}
    goOut = {}
    a = 0
    b = 0
    #Calculating the inbalance of the in and out edge of each vertex
    for i in range(len(tmp2)):
        goOut[i] = len(tmp2[i])#easy: len of adjacency list item
        for kk in tmp2[i]:#get the vertices that adjacent to each vertex
            #count freq, if the vertices not in dict
            if kk not in goIn:
                goIn[kk] = 1#init
            else:
                goIn[kk] += 1#freq increment

    #Algorithm credit to: Sandbox/bioinformatic
    last = []
    first = []
    for key ,val in goIn.items():
        #eg. goIn -> 3:2, goOut -> 3:1
        if val > goOut.get(key,0):#if bigger(inbalance)
            #get differences
            #must be the last vertex-(key, its difference)
            last.append((key,val - goOut.get(key,0)))

    for key ,val in goOut.items():
        #eg. goOut -> 4:2, goIn -> 4:1
        if val > goIn.get(key,0):#if bigger(inbalance)
            #get differences
            #must be the first vertex-(key, its difference)
            first.append((key,val - goIn.get(key,0)))
    #check if valid eulerian path, if has circuit will straightaway jump to below
    if (len(last) ==  1) and (last[0][1] == 1) and (len(first) ==  1) and (first[0][1] == 1):
        a = last[0][0]
        b = first[0][0]
    #it doesn't matter if cycle or path: will do the same anyway
    #but for cycle is more redundant
    #add the extra balancing edge
    #at position- (first) append (last)- vertex     
    tmp2[a].append(b)#if cycle will append to first to first
    path = eulerian_aux(tmp2)
    for i in range(len(path[:-1])):#skip the last one
        #go search the vertex that match first and last and reconstruct the path
        if (path[:-1][i] == a) and (path[i+1] == b):
            #eg. [1, 3, 4, 3, 2, 1, 4, 0, 1]
            # -> [1, 3| 4, 3, 2, 1, 4, 0   ]
            # -> [4, 3, 2, 1, 4, 0| 1, 3   ]
            path = path[i+1:] + path[1:i+1]
            return path
        
path = eulerian_main(tmp2)
#Make it become string again
for i in range(len(path)):
    path[i] = allList[path[i]]

#AAA....
# AAB...
#-------
#AAAB...
toString = str(path[0])#add first one
for i in range(len(path[1:])):#start from second
    toString += path[1:][i][-1]#add last letter
f.write('path: ' + str(toString))
f.close()
