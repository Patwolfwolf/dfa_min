# CS301 Assignment 3
# DFA Minimization
# Ruiwen Fu
# Feb.15th 2017
import math



def save_dfa(states, delta, q0, accepting, filename):
    f = file(filename+".jff", "w")
    statesName = {}
    alpha = 360/len(states)
    print >> f, '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    print >> f, '<structure>'
    print >> f, '\t<type>fa</type>'
    print >> f, '\t<automaton>'
    print >> f, '\t\t<!--The list of states.-->'
    for i,c in enumerate(states):
        print >> f, '\t\t<state id="%d" name="%s">' % (i, c)
        print >> f, '\t\t\t<x>%f</x>' % (100 + 250 * math.cos(i*alpha))
        print >> f, '\t\t\t<y>%f</y>' % (100 + 250 * math.sin(i*alpha))
        if c in q0:
            print >> f, '\t\t\t<initial/>'
        if c in accepting:
            print >> f, '\t\t\t<final/>'
        print >> f, '\t\t</state>'
        statesName[c] = i
    for key, value in delta.iteritems():
        x,y = key
        print >> f, '\t\t<transition>'
        print >> f, '\t\t\t<from>%d</from>' % statesName[x]
        print >> f, '\t\t\t<to>%d</to>' % statesName[value]
        print >> f, '\t\t\t<read>%s</read>' % y
        print >> f, '\t\t</transition>'
    print >> f, '\t</automaton>'
    print >> f, '</structure>'
    f.close()


def build_table(states, alphabet, delta, accepting):
    table = {}
    for i in states:
        for j in states:
            table[i, j] = True
    for i in states:
        for j in states:
            if i in accepting and j not in accepting:
                table[i, j] = False
                table[j, i] = False
    temp = {}
    while temp != table:
        temp = table.copy()
        print temp
        for i in states:
            for j in states:
                for k in alphabet:
                    if table[delta[i, k], delta[j, k]] == False:
                        table[i, j] = False
                        table[j, i] = False
        print temp
    return table


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


def build_mindfa(states, alphabet, delta, q0, accepting, distinct):
    minDelta = {}
    minStates = set()
    minAccepting = set()
    minAlpha = set()
    minQ0 = set()
    equality = {}
    for i in states:
        for j in states:
            if distinct[i, j] == True and i != j:
                distinct[j, i] = False
                equality[i] = set([i, j])
                equality[j] = set([i, j])
                for k in equality:
                    if i in equality[k] or j in equality[k]:
                        equality[k].add(i)
                        equality[k].add(j)
                        for c in equality[k]:
                            equality[i].add(c)
                            equality[j].add(c)
    for k, v in delta.iteritems():
        x, y = k
        for e in equality:
            if x in equality[e]:
                x = e
            if v in equality[e]:
                v = e
        minDelta[x, y] = v
    for a in states:
        for e in equality:
            if a in equality[e]:
                a = e
        minStates.add(a)
    for a in accepting:
        for e in equality:
            if a in equality[e]:
                a = e
        minAccepting.add(a)
    for a in q0:
        for e in equality:
            if a in equality[e]:
                a = e
        minQ0.add(a)
    return minStates, minDelta, minQ0, minAccepting

def minimize(dfaFilename):
    states, delta, stateNames, alphabet, q0, accepting = read_dfa(dfaFilename)
    print accepting
    print q0
    distinct = build_table(stateNames, alphabet, delta, accepting)
    states, delta, q0, accepting = build_mindfa(stateNames, alphabet, delta, q0, accepting, distinct)
    print q0
    save_dfa(states, delta, q0, accepting, "min_"+dfaFilename[:-4])


minimize("gene_hunting2.jff")
print "success"
