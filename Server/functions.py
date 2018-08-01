def cliInterpretor(string):
    keywords = []
    currentWord = ''
    isInWord = False
    isInString = False
    for char in string:
        if isInString:
            if char == "\"" or char == "\'":
                keywords.append(currentWord)
                currentWord = ''
                isInString = False
            else:
                currentWord += char
        elif isInWord:
            if char == ' ':
                keywords.append(currentWord)
                currentWord = ''
                isInWord = False
            else:
                currentWord += char
        else:
            if char == "\"" or char == "\'":
                isInString = True
            elif char != ' ':
                isInWord = True
                currentWord += char
    if currentWord != '':
        keywords.append(currentWord)
    return keywords


def clearSpaces(string):
    leftClearedString = ""
    isInString = False
    for char in string:
        if isInString:
            leftClearedString += char
        else:
            if char != " ":
                isInString = True
                leftClearedString += char
    isInString = False
    clearedString = ""
    for char in leftClearedString[::-1]:
        if isInString:
            clearedString += char
        else:
            if char != " ":
                isInString = True
                clearedString += char
    return clearedString[::-1]