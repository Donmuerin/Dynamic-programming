#(Reference1)
#https://www.cs.helsinki.fi/u/tpkarkka/teach/15-16/SPA/lecture10-2x4.pdf
#(Reference2)
#https://web.stanford.edu/class/cs262/archives/notes/lecture4.pdf

#import timeit
filename = input("Please enter the file name: ")

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
   
def inverse(s):
    """
    param: take in the BWT of the string
    return: its original string
    O(N) time
    """
    freq = {} # letter count
    occ = {}
    x = 0
    alist = []
    for i in range(len(s)):
        if s[i] in freq:#if already exist
            freq[s[i]] += 1
        else:
            freq[s[i]] = 1
            #as I can't really sort dict key
            alist.append(s[i])
    #alist -> ['a', 'n', 'b', '$']
    mergeSort(alist)
    #alist -> ['$', 'a', 'b', 'n']
    for j in range (len(alist)):
        #now we wanna get the rank
        #$aaabnn -> |$aaabnn(0) -> $|aaabnn(1) -> $aaa|bnn(4) -> $aaab|nn(5)
        #$ -> 0
        #0 += 1 -> 1
        #a -> 1
        #1 += 3 -> 4
        #b -> 4
        #...
        occ[alist[j]] = x
        #plus the key frequency
        x += freq[alist[j]]
    #occ -> {'n': 5, 'a': 1, 'b': 4, '$': 0}
        
    #initiate first
    lfMapping = [0]* len(s)
    for i in range(len(s)):
        lfMapping[i]=occ[s[i]]+1#of that key
        #We know that if sort the alphabets:
        #Pos: 1|2|3|4|5|6|7
        #Alp: $|a|a|a|b|n|n
        #Use this as reference, assign value for annb$aa
        #a:[2, 0, 0, 0, 0, 0, 0]
        #n:[2, 6, 0, 0, 0, 0, 0]
        #n:[2, 6, 7, 0, 0, 0, 0]
        #...
        #>>lfMapping: [2, 6, 7, 5, 1, 3, 4]
        occ[s[i]] += 1
        
    r = ['']*(len(s)-1)#ignore the $ first
    i = 0
    k = 0
    string = ""
    while s[i] !="$":#ignore the $ first else $ will be the first
        #start from the last
        #Interesting part is:
        #Str:a|n|n|b|$|a|a
        #LFM:2|6|7|5|1|3|4
        #you can actually found a pattern that
        #look up string, a, its LFM value - 1 then use that value
        #to look up another character
        #eg. pos(0):a ->LFM(2) ->find 2-1=1 ->pos(1):n ->LFM(6)
        #->find 6-1=5 ->pos(5):a ->LFM(3) ->find 3-1=2 ->pos(2):n
        #->LFM(7) ->find 7-1=6 ->pos(6):a ->LFM(4) ->find 4-1=3 ->pos(3):b
        r[len(r)-k-1] = s[i]#a->n->a->n->a->b
        i  = lfMapping[i]-1
        k += 1#second last position and such
    for i in range(len(r)):
        #because you need to make it as a string and write
        string += r[i]
    return string + "$"#only add it afterward
    

#start = timeit.default_timer()
def main(filename):
    infile = open(filename,"r")
    a = infile.read()
    #less than 1 min for bwt1000001.txt
    f= open("originalstring.txt","w")
    f.write(str(inverse(a)))
    #taken = (timeit.default_timer() - start)
    #print(taken)
    infile.close()
    f.close()
    
main(filename)
