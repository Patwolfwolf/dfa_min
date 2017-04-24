
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


delta = {
    ("A", "0") : "B", ("A", "1") : "E",
    ("B", "0") : "C", ("B", "1") : "F",
    ("C", "0") : "D", ("C", "1") : "H",
    ("D", "0") : "E", ("D", "1") : "H",
    ("E", "0") : "F", ("E", "1") : "I",
    ("F", "0") : "G", ("F", "1") : "B",
    ("G", "0") : "H", ("G", "1") : "B",
    ("H", "0") : "I", ("H", "1") : "C",
    ("I", "0") : "A", ("I", "1") : "E",
    }
states= {"A", "B", "C", "D", "E", "F", "G", "H", "I"}
q0 = "A"
accepting = set(["C", "F", "I"])
save_dfa(states, delta, q0, accepting, "problem1")