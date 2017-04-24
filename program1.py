# CS301 Assignment 3
# DFA Minimization
# Ruiwen Fu
# Feb.15th 2017


# search for the index of reaching a final state for some string
# w - the string to search
# delta - transition function
# q0 - starting state
# accepting - set of accepting state
def dfa_search_string(w, delta, begin, accepting):
    currState = begin.pop()
    for i, c in enumerate(w):
        currState = delta[currState, c]
        print "s"
        if currState in accepting:
            print "match found, ending at index", i


#read dfa from .jff
def read_dfa(filenames):
    state = {}
    transition = {}
    stateNames = set()
    alphabet = set()
    accepting = set()
    init = set()
    f = file(filenames)
    line = f.readline()
    while line != "":
        line = line.strip()  # remove initial/trailing whitespace
        if line.startswith("<state"):
            line = line.replace("<state", "")
            line = line.replace(" id=", "")
            line = line.replace("name=", "")
            line = line.replace(">", "")
            line = line.replace('"', "")
            line.strip()
            ind = line.find(" ")
            id = line[0: ind]
            name = line[ind+1:]
            stateNames.add(name)
            state[id] = name
        if line.startswith("<from>"):
            line = line.replace("<from>", "")
            line = line.replace("</from>", "")
            fromState = line
            line = f.readline()
            line = line.strip()
            line = line.replace("<to>", "")
            line = line.replace("</to>", "")
            toState = line
            line = f.readline()
            line = line.strip()
            line = line.replace("<read>", "")
            line = line.replace("</read>", "")
            func = line
            alphabet.add(func)
            transition[state[fromState], func] = state[toState]
        if line.startswith("<initial/>"):
                init.add(name)
        if line.startswith("<final/>"):
                accepting.add(name)

        line = f.readline()
    f.close()
    return state, transition, stateNames, alphabet, init, accepting


#search file method
def dfa_search_file(dataFilename, dfaFilename):
    state, transition, stateNames, alphabet, init, accepting = read_dfa(dfaFilename)
    f = file(dataFilename)
    chars = f.read()
    dfa_search_string(chars, transition, init, accepting)
    f.close()


#Main Method
dfa_search_file("ecoli.fasta", "min_gene_hunting2.jff.jff")

















