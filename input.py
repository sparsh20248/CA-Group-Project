inputFile = open("input.txt", "r")
inputFile = inputFile.read()
list_of_instructions = []
temp = ""
for i in inputFile:
    if i != '\n':
        temp += i
    else:
        list_of_instructions.append(temp)
        temp=""
