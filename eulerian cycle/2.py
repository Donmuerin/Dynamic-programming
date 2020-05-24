#reference1: http://www.applied-math.org/subset.pdf
#reference2: https://en.wikipedia.org/wiki/Gray_code#Constructing_an_n-bit_Gray_code

f = open("outputTask2.txt",'w')
def main(n):
    if (n < 2 or n > 10):
        raise ValueError("Out of range")
    else:
        return n

def graycode(n):
    """
    O(2(n-1))
    """
    #wikipedia pics
    original=['0','1']
    for i in range(n-1):
        #blue line(1st): Reflect 
        reflect=original[::-1]
        k = len(original)#2->4->8->16
        for j in range(k):
            #red line: Add 0 in front
            original[j]= "0" + original[j] 
            #blue line(2nd): Add 1 in front
            reflect[j]= "1" + reflect[j]
        original = original+reflect#double the size
    return original

input_num = int(input("Please enter your number: "))
n = main(input_num)
a = graycode(n)

for i in range(len(a)):
    result = set()
    for j in range(len(a[i])):
        length = len(a[i])
        #ord(a)=97, ord(d)= number
        number = 97 + length - 1#count total alphabets
        if a[i] == '0'*length:#find the empty subset
            result.add(' ')#{}
        else:
            if a[i][j] == '1':#if contain 1
                result.add(chr(number - j))#add the index 1 alphabets
            else:
                continue
    f.write("subset "+str(i+1)+": "+str(result)+'\n')

f.close()
