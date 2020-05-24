#(Reference1)
#https://www.cs.helsinki.fi/u/tpkarkka/teach/15-16/SPA/lecture10-2x4.pdf
#(Reference2)
#https://web.stanford.edu/class/cs262/archives/notes/lecture4.pdf

def mergeSort(alist):
    """
    param: alist - list
    return: alist(sorted) - list
    To sort a list
    time complexity: O(n logn)
    """
    tmp = [None]*len(alist)
    start = 0
    end = len(alist) -1
    merge_aux(alist, start,end,tmp)

def merge_aux(alist,start,end,tmp):
    if start < end:
        mid = (start+end)//2
        merge_aux(alist,start,mid,tmp)
        merge_aux(alist,mid+1,end,tmp)
        merge_array(alist,start,mid,end,tmp)
        for i in range(start,end+1):
            alist[i] = tmp[i]

def merge_array(alist,start,mid,end,tmp):
    i = start
    j = mid + 1
    for k in range(start,end+1):
        if i > mid:
            tmp[k]= alist[j]
            j += 1
        elif j > end:
            tmp[k]= alist[i]
            i += 1
        elif alist[i]<= alist[j]:
            tmp[k]=alist[i]
            i += 1
        else:
            tmp[k]=alist[j]
            j += 1
   
w = []
def suffix_array(tx):
    """
    param: tx- string
    return: sa - list
    time complexity: O(n log^2 n)
    
    Below understanding based on cs.helsinki lecture note
    For prefix doubling for T = banana$
    We know that
    N1 N2  N4    N8
    b  ba  bana  banana$
    a  an  anan  anana$
    n  na  nana  nana$
    a  an  ana$  ana$
    n  na  na$   na$
    a  a$  a$    a$
    $  $   $     $
    
    Where we can actually found a pattern in N8, that
    1st: |banana$ --> 0
    2nd: b|anana$ --> 1
    3rd: ba|nana$ --> 2
    4th: ban|ana$ --> 3
    5th: bana|na$ --> 4
    6th: banan|a$ --> 5
    7th: banana|$ --> 6
    where len(banana$) = 7
    """
    size = len(tx)
    #cannot directly use size tho
    step = 100#smtg deal with memory and characters bytes
    sa = [i for i in range (size)]
    
    #need to add i + step else q3 MemoryError!!!
    tmp = [(tx[i:i + step], i) for i in sa]
    #print([(tx[0:0+100],0)])--> [('banana$', 0)]
    #print([(tx[1:1+100],1)])--> [('anana$', 1)]
    # .....
    
    mergeSort(tmp)#sort them by aphabets
    sa = [i for (key, i) in tmp]
    #you sort by alphabets and retrieve their corresponding
    #value, which:
    #[('banana$', 0), ('anana$', 1), ('nana$', 2),('ana$', 3), ('na$', 4), ('a$', 5), ('$', 6)]
    #-->[('$', 6), ('a$', 5), ('ana$', 3), ('anana$', 1), ('banana$', 0), ('na$', 4), ('nana$', 2)]
    #-->[6, 5, 3, 1, 0, 4, 2]
    for i in range(len(sa)):
        st = tx[sa[i]:sa[i] + step]
        #to get the key:
        #['$', 'a$', 'ana$', 'anana$', 'banana$', 'na$', 'nana$']
        w.append(st)
        sa[i] = sa[i]#no need plus 1 if u wanna match sample output 
    
    return sa, w
    
def exactMatching(bw, p):
    """
    param:bw, p - string
    return: result - int
    time complexity: O(M), M is the length of pattern
    Supplementary Note Week7
    """
    alist = {}
    numOcc = {}
    rank = {}
    rankSec = {}
    last = p[-1]
    x = 0
    
    for i in range (len(bw)):
        if bw[i] not in alist:#find all the distinct alphabets
            #banana example: a,n,b,$
            alist[bw[i]] = 0#init
            numOcc[bw[i]] = []#init
           
    for i in range(len(bw)):
        alist[bw[i]] += 1#add the frequency while first alphabets is same
        #alist is a collection of the first alphabets and its frequency
        #annb$aa --> {'n': 2, 'a': 3, '$': 1, 'b': 1}
        #So basically alist is a collection of evey iteration
        #a:{'a': 1, 'b': 0, '$': 0, 'n': 0}
        #an:{'a': 1, 'b': 0, '$': 0, 'n': 1}
        #ann:{'a': 1, 'b': 0, '$': 0, 'n': 2}
        #...
        for j in alist:
            #append its corresponding list
            #eg. a ->[1, 1, 1, 1, 1, 2, 3]
            #gonna use append as:
            #{'a': [1], '$': [0], 'n': [0], 'b': [0]}
            #{'a': [1, 1], '$': [0, 0], 'n': [0, 1], 'b': [0, 0]}
            #{'a': [1, 1, 1], '$': [0, 0, 0], 'n': [0, 1, 2], 'b': [0, 0, 0]}
            #...   
            numOcc[j].append(alist[j])
            
    #since we can't use sorted to sort dict
    #append into list
    tmp = [i for i in alist.items()]
    #[('n', 2), ('$', 1), ('b', 1), ('a', 3)]
    #sort by alphabets
    mergeSort(tmp)
    #[('$', 1), ('a', 3), ('b', 1), ('n', 2)]
    
    for key, i in tmp:
        #$aaabnn -> |$aaabnn(0) -> $|aaabnn(1) -> $aaa|bnn(4) -> $aaab|nn(5)
        #$ -> 0
        #0 += 1 -> 1
        #a -> 1
        #1 += 3 -> 4
        #b -> 4
        #...
        rank[key] = x#{'a': 1, '$': 0, 'n': 5, 'b': 4}
        #Now we need to consider the last position of that distinct alphabets
        #$aaabnn -> $|aaabnn(1) -> $aaa|bnn(4) -> $aaab|nn(5) -> $aaabnn|(7)
        #Same here, you can actually see:
        #$ -> 0+1 = (1)
        #a -> 3+(1) = [4]
        #b -> 1+[4] = {5}
        #n -> 2+{5} = 7
        rankSec[key] = x + i
        x += i
        
    start = rank[last]
    end = rankSec[last]
    i = len(p)- 2#for example if we are comparing 'ana'
    #from Supplementary note 7
    while i >= 0 and end > start:
        start = rank[p[i]] + numOcc[p[i]][start-1]
        end = rank[p[i]] + numOcc[p[i]][end-1]
        i -= 1
    result = end - start#if no difference between,
    #equal to zero, mean the character does not occur
    return result

f = open("outputTask3.txt","w")

#bwt1001
infile = open("bwt1000001.txt","r")
b = infile.read()

#pattern
infile1 = open("shortpatterns.txt","r")
b1 = infile1.readlines()

infile2 = open("originalstring.txt","r")
a = infile2.read()

x,y = suffix_array(a)


for i in range(len(b1)):
    c = b1[i].rstrip()#each patterns, rstrip'\n'
    bw = exactMatching(b,c)#pattern appears times
    length = len(c)
    f.write("Pattern "+ str(c) + " appears " + str(bw)+" times")
    
    if bw ==0:
        f.write("\n")
    else:
        why = []
        f.write("\n")
        f.write("Its positions in the original string in SORTED ORDER: \n")
        for i in range(len(y)):
            #since y is a collection of every suffix array
            if y[i][0:length] == c:#compare every first N(len(c)) item if match pattern
                #if match append the position
                why.append(x[i])#since it want sort
            else:
                continue
        mergeSort(why)#sort list
        for i in range(len(why)):
            f.write(str(why[i]))#then only write out
            f.write("\n")
    f.write("\n")
        
f.close()
infile.close()
infile1.close()
infile2.close()
