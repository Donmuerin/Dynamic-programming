#(Reference1)
#https://www.cs.helsinki.fi/u/tpkarkka/teach/15-16/SPA/lecture10-2x4.pdf
#(Reference2)
#https://web.stanford.edu/class/cs262/archives/notes/lecture4.pdf

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
    
    #need to add i + step else MemoryError!!!
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
        sa[i] = sa[i] + 1#banana -> [7,6,4,2,1,5,3]
    
    return sa


def conBwt(x,a):
    """
    param: suffix array - list
    return: bwt - string
    Stanford Lecture Note 4 CS262:
    Go to the character in X pointed to by S[i], and move one spot to the left.
    If S[i]=1, take the last character of X(which is the $)
    BWT(X)[i] = X[S[i]-1] if S[i]>1 else X[len(X)]
    """
    bwt = ""
    for i in range(len(a)):
      if x[i] > 0:
        bwt += str(a[x[i]-2])
      else:
        bwt += str(a[len(a)-1])
    return bwt

def main(filename):
    infile = open(filename,"r")
    a = infile.read()
    f= open("outputbwt.txt","w")
    x = suffix_array(a)
    result = conBwt(x,a)
    f.write(str(result))
    infile.close()
    f.close()

main(filename)

