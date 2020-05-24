keys = []
pFreq = []#probabilities frequency
oFreq=[]#original frequency
f = open("frequencies.txt","r")
string = f.read()
new = string.split()#split key and frequency by blank space

#As we know that key is always associate with its pFrequency,
#if first element is key, then it will come with its pFrequency
#Use this logic, we can know that even number is key,
#odd is frequency
for i in range(len(new)):
    if i % 2 == 1:
        oFreq.append(int(new[i]))
    else:
        keys.append(new[i])

#to count the total frequency            
totalFreq = 0    
for i in range(len(oFreq)):
    totalFreq += oFreq[i]

#append each corresponsding probabilities frequency into the list                     
for j in range(len(oFreq)):
    pFreq.append(float(int(oFreq[j])/totalFreq))

#Algorithm references:
#http://www.geeksforgeeks.org/dynamic-programming-set-24-optimal-binary-search-tree/
#http://www.radford.edu/~nokie/classes/360/dp-opt-bst.html
#http://software.ucv.ro/~cmihaescu/ro/laboratoare/SDA/docs/arboriOptimali_en.pdf
def optimalBST(keys, pFreq, n):#take in array->keys, array->pFreq, int->n
    #c[i, j], ∀0 ≤ i ≤ j ≤ n,storing the cost of the tree T(Ki+1, . . . , Kj )
    #r[i, j], ∀0 ≤ i<j ≤ n,storing the root of the tree T(Ki+1, . . . , Kj )
    #w[i, j], ∀0 ≤ i ≤ j ≤ n,storing the sum of probabilities of keys in T(Ki+1, . . . , Kj )

    #Initiate
    #For example if keys is 2, initiate c as [[0,0][0,0]]
    c = [[0 for x in range(n)] for y in range(n)]
    r = [[[None] for x in range(n)] for y in range(n)]
    w = [[0 for x in range(n)] for y in range(n)]

    for size in range(0, n): 
        for i in range(n-size):
            j = i + size 
            c[i][j] = float('inf')#initiate as INT_MAX
            root = None
            for k in range(i, j+1):
                s = 0
                s += pFreq[k]
                #for left side tree
                if k-1 < 0:
                    left = 0
                else:
                    #count the cost of left tree
                    #background info: (K1,...Kr-1)
                    #But we start as 0
                    left = c[i][k-1]

                #for right side tree
                if k+1 >= n:
                    right = 0
                else:
                    #count the cost of right tree
                    #background info: (Kr+1,...Kn)
                    #last is n-1, so = n is not acceptable
                    right = c[k+1][j]
    
                if i == j+1:
                    t = 0
                else:
                    w = s
                    t = left + right + w
           
                if t < c[i][j]:
                    #As said, c(i, j) store the minimum cost BST
                    c[i][j] = t
                    root = k         
            c[i][j] = c[i][j]#replace, this.c[i][j] = c[i][j]
            r[i][j] = root
            
    a = c[0][n-1]

    #initiate depth as 1
    depth = 1
    k = {}
    def findLevel(i,j,depth):
        if i <= j:
            node = r[i][j]#access root
            if node != None:
                #take each key as item, its depth(level)as value
                k[keys[node]]=depth
                #every recursive, depth+=1
                findLevel(i,node-1,depth+1)#left subtree
                findLevel(node+1,j,depth+1)#right subtree
    findLevel(0,n-1,depth)

    #Below code is for me to test if the output is correct
    #If based on radford.edu, output should be  [[k1] k2[[[k3] k4] k5] ]
    #Matched.
    """
    def printTree(i,j):
        if i <= j:
            node = r[i][j]
            if node != None:
                print("[",end='')
                printTree(i,node-1)#print left subtree
                print(keys[node],end='')
                printTree(node+1,j)#print right subtree
                print("] ",end='')

    printTree(0,n-1)
    """
    
    return a,k



n= len(keys)
a,b = optimalBST(keys, pFreq, n)

result = 0.0

writeFile = open("mincostbst.txt","w")
for i in range(len(keys)):
    #          pFrequency
    # sum =  ---------------- * its level + previous sum
    #        total pFrequency
    result += pFreq[i]*b[keys[i]]
    
    #to print as a required output, alignment to the right
    #toPrint = '%18s %10s %10s %.6f' %(keys[i],oFreq[i],b[keys[i]],result)
    
    writeFile.write(str(keys[i]).ljust(18)+'\t\t'+str(oFreq[i])+'\t\t'+str(b[keys[i]])+'\t'+str('%.6f'%(result))+'\n')

f.close()
writeFile.close()


