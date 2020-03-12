import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import graphviz
#import anytree
#from myNode import MyNode


# terminals = [variables, constants, neg, connectors, eq, predicates, quan]
def elimWhite(formula, index):
    s=0
    while formula[index]==" ":
        index+=1
        s+=1
    return s
    
def expandFormula(formula, index, terminals):
    # case (term eq term) | (form connec form)
    nodes = []
    if formula[index] == "(":
        parenth = Node(str(index),distplay_name = "(")
        nodes.append(parenth)
        print("parenthesis")
        startInd = index
        index += 1
        aux = index

        index += elimWhite(formula,index)
        aux = index
        
        progress, newNode = expandTerm(formula,index, terminals)
        nodes.append(newNode)
        index += progress
        if aux != index:
            print("term")
            index += elimWhite(formula,index)
            aux = index
            progress, newNode = expandEqual(formula, index, terminals)
            nodes.append(newNode)
            index += progress
            if aux!= index:
                print("equal")
                index += elimWhite(formula,index)
                aux = index
                progress, newNode = expandTerm(formula,index, terminals)
                nodes.append(newNode)
                index += progress
                if aux!=index:
                    print("term")
                    index += elimWhite(formula,index)
                    aux = index
                    if formula[index] != ")":
                        print("error")
                        exit()
                    else:
                        closeParenth = Node(str(index),distplay_name = ")")
                        nodes.append(closeParenth)
                        form = Node(str(index),children = [i for i in nodes if i],distplay_name = "formula")
                        #setParent(form,nodes)
                        print("Connector (v=v) detected")
                        return index - startInd +1, form

        progress, newNode = expandFormula(formula,index, terminals)
        nodes.append(newNode)
        index += progress

        if aux != index:
            aux = index
            index += elimWhite(formula,index)
            if index!=aux:
                aux = index
                progress, newNode = expandConnec(formula,index, terminals)
                nodes.append(newNode)
                index += progress
                if aux!= index:
                    aux = index
                    index += elimWhite(formula,index)
                    if index != aux:
                        print("conn")
                        aux = index
                        progress, newNode = expandFormula(formula,index, terminals)
                        nodes.append(newNode)
                        index += progress
                        if aux!=index:
                            index += elimWhite(formula,index)
                            aux = index
                            if formula[index] !=")" :
                                print("error1")
                                exit()
                            else:
                                closeParenth = Node(str(index),distplay_name = ")")
                                nodes.append(closeParenth)
                                form = Node(str(index),children = [i for i in nodes if i],distplay_name = "formula")
                                #setParent(form,nodes)
                                print("Connector (formula conn formula) detected")
                                return index - startInd +1, form

    else:

        startInd = index
        aux = index
        progress, newNode = expandNeg(formula,index, terminals)
        nodes.append(newNode)
        index += progress

        if aux != index:
            print("neg")
            aux = index
            index += elimWhite(formula,index)
            if index!=aux:
                aux = index

                progress, newNode = expandFormula(formula,index, terminals)
                nodes.append(newNode)
                index += progress
                if aux== index:
                    print("error")
                    exit()
                else:
                    print("Connector (neg formula) detected")
                    form = Node(str(index),children = nodes,distplay_name = "formula")
                    #nt(form,nodes)
                    return index - startInd, form

        progress, newNode = expandPredicate(formula,index, terminals)
        nodes.append(newNode)
        index += progress
        if aux!= index:
            form = Node(str(index),children = [i for i in nodes if i],distplay_name = "formula")
            #setParent(form,nodes)
            print("Predicate detected")
            return index - startInd, form

        
        progress, newNode = expandQuantifier(formula,index, terminals)
        nodes.append(newNode)
        index += progress
        if aux != index:
            aux = index
            index += elimWhite(formula,index)
            if index!=aux:
                aux = index
                progress, newNode = expandTerm(formula,index, terminals)
                nodes.append(newNode)
                index += progress
                if aux != index:
                    aux = index
                    index += elimWhite(formula,index)
                    if aux != index:
                        aux = index
                        progress, newNode = expandFormula(formula,index, terminals)
                        nodes.append(newNode)
                        index += progress
                        if aux!=index:
                            print("quan found")
                            form = Node(str(index),children = [i for i in nodes if i],distplay_name = "formula")
                            #setParent(form,nodes)
                            print(form)
                            return index-startInd, form

        progress, newNode = expandTerm(formula,index, terminals)
        nodes.append(newNode)
        index += progress
        if aux!= index:
            form = Node(str(index),children = [i for i in nodes if i],distplay_name = "formula")
            #setParent(form,nodes)
            print("Term detected")
            return index - startInd, form


    return 0 , None

def expandTerm(formula, index, terminals):
    for term in terminals[0]+terminals[1]:
        if term == formula[index:index+len(term)]:
            print(term)
            trm = Node(str(index+len(term)), display_name=term)
            return len(term), trm
    return 0 , None

def expandEqual(formula, index, terminals):
    term = terminals[4]
    if term == formula[index:index+len(term)]:
        print(term)
        eq = Node(str(index+len(term)), display_name=term)
        return len(term), eq
    return 0 , None

def expandConnec(formula, index, terminals):
    for term in terminals[3]:
        if term == formula[index:index+len(term)]:
            print("hey")
            print(term)
            conn = Node(str(index+len(term)),display_name=term)
            return len(term),conn
    return 0, None

def expandNeg(formula, index, terminals):
    term = terminals[2]
    if term == formula[index:index+len(term)]:
        print(term)
        neg = Node(str(index+len(term)), display_name=term)
        return len(term), neg
    return 0 , None

def expandPredicate(formula, index, terminals):
    startind = index
    terminals[0].sort(key=len,reverse=True)
    predNodes = []
    newNode = None
    for term in terminals[5]:
        numVars = term.count("var")
        ind1 = term.find('[')
        ind2 = term.find(']')
        if term[:ind1] == formula[index:index+ind1]:
            index += ind1
            if formula[index]=="(":
                parenth = Node(str(index),distplay_name = "(")
                predNodes.append(parenth)
                index += 1
                #  pred(var   from   pred(var,var,var)
                index += elimWhite(formula,index)
                aux = index
                progress, newNode = expandTerm(formula,index,[terminals[0],[]])
                index += progress
                predNodes.append(newNode)
                if aux != index:
                    index += elimWhite(formula,index)
                    aux = index
                    # pred(var,var,var from pred(var,var,var)
                    for i in range(numVars-1):
                        index += elimWhite(formula,index)
                        if formula[index]==",":
                            index += 1
                            index += elimWhite(formula,index)
                            aux = index
                            progress, newNode = expandTerm(formula,index,[terminals[0],[]])
                            index += progress
                            predNodes.append(newNode)
                            if aux == index:
                                print(1)
                                return 0 
                    index += elimWhite(formula,index)
                    if formula[index]==')':
                        closeParenth = Node(str(index),distplay_name = ")")
                        predNodes.append(closeParenth)
                        prd = Node(str(index),children = [i for i in predNodes if i],distplay_name = term[:ind1])
                        #setParent(prd,predNodes)
                        print(formula[startind:index+1])

                        return index - startind + 1 ,prd

    return 0, None

def expandQuantifier(formula, index, terminals):
    for term in terminals[6]:
        if term == formula[index:index+len(term)]:
            print(term)
            quan = Node(str(index+len(term)), display_name=term)
            return len(term),quan
    return 0, None

def setParent(father, children):
    for child in children:
        if child!=None:
            child.parent = father
    
def readText(f):
    line = 1
    decList = []
    setDefinitions = []
    for char in f.read():
        if char == '\n':
            line += 1
        if char == ':':
            decList.append(line)
    f.close()

    f = open("example.txt", "r")
    for i in range(len(decList)):
        definition = ""
        if i < len(decList)-1:
            numLines = decList[i+1] - decList[i]
            for j in range(numLines):
                definition += f.readline()
            setDefinitions.append(definition)
        else:
            numLines = 1 + line - decList[i]
            for j in range(numLines):
                definition += f.readline()
            setDefinitions.append(definition)

    for i in range(len(setDefinitions)):
        setDefinitions[i] = setDefinitions[i].split()

    return setDefinitions

# labels = ["variables","constants","predicates","equality","connectives","quantifiers","formula"]

def constructGrammar(setDefinitions):
    print(setDefinitions)
    grammar = []
    # GET VARIABLES
    grammar.append(
        "form -> (form connec form) | not form | (term eq term) | predicate | quan var form | term")
    grammar.append("term -> var | cons")
    for definition in setDefinitions:
        # look for variables
        if definition[0] == 'variables:':
            line = "var -> "
            if len(definition) > 1:
                line += definition[1]
            if len(definition) > 2:
                for i in range(2, len(definition)):
                    line += (" | " + definition[i])
            #print(line)
            grammar.append(line)

    # GET CONSTANTS

    for definition in setDefinitions:
        # look for Cons
        if definition[0] == 'constants:':
            line = "cons -> "
            if len(definition) > 1:
                line += definition[1]
            if len(definition) > 2:
                for i in range(2, len(definition)):
                    line += (" | " + definition[i])
            #print(line)
            grammar.append(line)

    # GET connectives to build Expression and Form
    for definition in setDefinitions:
        # look for Cons
        if definition[0] == 'connectives:':
            form = "connec -> "
            if len(definition) == 6:
                form += definition[1]
                for i in range(2, len(definition)-1):
                    form += (" | " + definition[i])
                grammar.append("not -> " + definition[-1])
            grammar.append(form)

    # T -> (C=V) | (V=V) | (C=C) | (V=C)
    # T -> A

    #get T
    for definition in setDefinitions:
        # look for Cons
        if definition[0] == 'equality:':
            term = "eq -> " + definition[1]
            grammar.append(term)

    for definition in setDefinitions:
        # look for Cons
        if definition[0] == 'predicates:':
            atom = "predicates -> "
            for i in range(1, len(definition)):
                ind1 = definition[i].find('[')
                ind2 = definition[i].find(']')
                num = int(definition[i][ind1+1:ind2])
                atom += definition[i][:ind1+1] + "var"
                for i in range(num-1):
                    atom += ",var"
                atom += "] | "
            grammar.append(atom[:-3])

    for definition in setDefinitions:
        # look for Cons
        if definition[0] == 'quantifiers:':
            quan = "quan -> "
            quan += definition[1] + " | "
            quan += definition[2]
            grammar.append(quan)
    print()
    for g in grammar:
        print(g)
    return grammar


f = open("example.txt", "r")
setDefinitions = readText(f)

print(setDefinitions)
grammar = constructGrammar(setDefinitions)

variables = grammar[2][7:].split(" | ")
constants = grammar[3][8:].split(" | ")
neg = grammar[4][7:]
connectors = grammar[5][10:].split(" | ")
eq = grammar[6][6:]
predicates = grammar[7][14:].split(" | ")
quan = grammar[8][8:].split(" | ")

terminals = [variables, constants, neg, connectors, eq, predicates, quan]
terminals[0].sort(key=len,reverse=True)

print()
formula1 = "A price E cost1 ( Same(cost1, price) AND ( NOT Non_zero(price) IFF (cost1 == 30) ) )"
formula2 = "\\forall   x   (   \exists   y  ( (C=C) \implies   \\neg  (C=C)  )   \lor   \exists z ( ( (C = z) \land (C=C) ) \land (C=C) ) )"
formula3 = "((C=x) \implies (x=C))"
#node = Node("Start")
index , node = expandFormula(formula2, 0, terminals)
print(node)
print()
print(formula2)
print(RenderTree(node))
#DotExporter(node).to_picture("node.png")
