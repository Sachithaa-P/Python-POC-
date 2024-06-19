1.word count. (single function pass file.read file and count each words count, make the output in the same location in csv format).
import os	
def fileread():
    #create an file called practise
    file=open("practise.csv","w")
    file.write('uwckwuckuh')
    file.close()
    #append the file
    file=open("practise.csv","a")
    file.write("iksdhncwi\n cat and dog \n mouse and cat\n")
    file.close()
    # read the file
    #count the no of words in the file
    file=open("practise.csv","r")
    content=file.read()
    word=content.split()
    num_of_words=len(word)
    print("num_of_words",num_of_words)
    file.close() 
fileread()

2.ip validation( ipv4 and ipv6 have different function and validate).
Ipv4 validation:
def validate_ipv4(ipv4):
    parts = ipv4.split('.')
    if len(parts) != 4: 
        return False

    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:  
            return False

    return True

ipv4 = input("Enter the IPv4 address: ")
print(validate_ipv4(ipv4))
ipv6 validation:
def validate_ipv6(ipv6):
    parts = ipv6.split(':')

    if len(parts) != 8:
        return False
    for part in parts:
        if not (1 <= len(part) >=4):
            return False
        try:
            int(part,16)
        except ValueError:
            return False
        
    return True
ipv6=input("Enter the ipv6 :")
print(validate_ipv6(ipv6))

3.String validation= c6*Dwu35ae2024 ( String should have last 4 digit as number, 
3rd character should be *, 4th character should be uppercase, from last 5th character should be alphabet, total char should be <=14). if failure each validation should be printed which dont obey. if success return success.
def validate_string(strr):
    if len(strr) > 14:
        return "Failure: The length should be less than or equal to 14"
    if strr[2] != '*':
        return "Failure :The 3rd character should be *"
    if not strr[3].isupper():
        return "Failure: 4th character should be uppercase"
    if not strr[-5].isalpha():
        return "Failure: last 5th character should be alphabet"
    if not strr[-4:].isdigit():
        return "Failure: The last four digit should be numbers"
    else:
        return "Success"

strr=input("Enter the string: ")
print(validate_string(strr))

4.find and replace. take file path as input, what word , which word is used to replace.
import os

def replace_word_in(file_path, search_word, replace_word):
    with open(file_path, "r") as file:
        contents = file.read()
        ucontents = contents.replace(search_word, replace_word)
    with open(file_path, "w") as file:
        file.write(ucontents)

file_path = "practise.csv"
search_word = "mouse"
replace_word = "lion"
replace_word_in(file_path, search_word, replace_word)

5.Find the next highest number by swapping the digit of the input given. ex 364179 -> 364197 swap two numbers to get next greater number.  
def validate_num(num):
    lst=list(str(num))
    for i in range(len(lst)-1, 0, -1):
        if lst[i]>lst[i-1]:
            lst[i-1],lst[i]=lst[i],lst[i-1]
            return int("".join(lst))
    return -1

num = int(input("Enter the number :"))
result=validate_num(num)
if result == -1 :
          print("In the given number we cant find the highest number")     
else:
    print("The next highest number is",result)

