from nltk.corpus import wordnet as wn


def getresult(text):
    action, data = extractInfo(text)
    if action == 1:
        return getMeaning(data)

    elif action == 2:
        syn = getSynonyms(data)
        if not syn:
            return "No synonyms found"
        else:
            if len(syn) > 1:
                for i in range(2):
                    return syn[i]
            else:
                return syn[0]

    elif action == 3:
        ant = getAntonyms(data)
        if not ant:
            return "No antonyms found"
        else:
            if len(ant) > 1:
                for i in range(2):
                    return ant[i]
            else:
                return ant[0]


def extractInfo(com):
    x = com.split()
    i = 0

    if "meaning" or "Meaning" in x:
        while x[i] != "of":
            i = i + 1
        return 1, x[i + 1]

    if "antonyms" in x:
        while x[i] != "of":
            i = i + 1
        return 3, x[i + 1]

    if "antonym" in x:
        while x[i] != "of":
            i = i + 1
        return 3, x[i + 1]

    if "synonyms" in x:
        while x[i] != "of":
            i = i + 1
        return 2, x[i + 1]

    if "synonym" in x:
        while x[i] != "of":
            i = i + 1
        return 2, x[i + 1]

    if "exit" in x:
        return 4, None

    if "quit" in x:
        return 4, None

    if "hello" in x:
        msg = ("Hello. Welcome to Wordbot. \nWordbot can help you find meanings, synonyms, antonyms for any word.\n")
        return 6, None

    if "hi" in x:
        msg = ("Hello. Welcome to Wordbot. \nWordbot can help you find meanings, synonyms, antonyms for any word.\n")
        return 6, None

    # else:
    return 5, None


def getMeaning(data):
    syn = wn.synsets(data)
    try:
        m = syn[0].definition()
    except IndexError:
        m = "No meaning found"
    # msg = ("\n Some examples of '", data, "' in a sentence are\n")
    # msg = (syn[0].examples())
    return m


def getSynonyms(data):
    synonyms = []
    for syn in wn.synsets(data):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms


def getAntonyms(data):
    antonyms = []
    for syn in wn.synsets(data):
        for l in syn.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    return antonyms


def execute(action, data):
    if action == 1:
        msg = getMeaning(data)

    elif action == 2:
        syn = getSynonyms(data)
        if syn == []:
            msg = "No synonyms found"
        else:
            if len(syn) > 1:
                for i in range(2):
                    msg = (syn[i])
            else:
                msg = syn[0]

    elif action == 3:
        ant = getAntonyms(data)
        if ant == []:
            msg = "No antonyms found"
        else:
            if len(ant) > 1:
                for i in range(2):
                    msg = ant[i]
            else:
                msg = ant[0]

    elif action == 4:
        exit(0)

    elif action == 5:
        msg = "Error in input"

    elif action == 6:
        pass

    else:
        msg = "**error in logic**"

    return msg
