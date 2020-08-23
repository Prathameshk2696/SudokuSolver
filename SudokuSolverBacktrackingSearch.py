# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 12:27:45 2020

@author: Prthamesh
"""

def displayBoard(board):
    for ri,row in enumerate(board):
        print("\t",end="")
        if ri>0 and (ri%3)==0:
            print("-"*19)
            print("\t",end="")
        for rc,num in enumerate(row):
            if rc>0 and (rc%3)==0:
                print('|',end='')
            print(num,end=' ')
        print()

# inserts all keys. values are lists
def initializeNeighbours():
    for row in range(9):
        for col in range(9):
            key = (row,col)
            neighbours[key] = []

# put all constraints in a queue
def initializeQueueForAC3():
    queue = []
    # all horizontal
    for row in range(9):
        for col in range(8):
            for k in range(col+1,9):
                constraint1 = (row,col,row,k)
                constraint2 = (row,k,row,col)
                queue.append(constraint1)
                queue.append(constraint2)
                if (row,k) not in neighbours[(row,col)]:
                    neighbours[(row,col)].append((row,k))
                if (row,col) not in neighbours[(row,k)]:
                    neighbours[(row,k)].append((row,col))
                                    
    # all vertical
    for col in range(9):
        for row in range(8):
            for k in range(row+1,9):
                constraint1 = (row,col,k,col)
                constraint2 = (k,col,row,col)
                queue.append(constraint1)
                queue.append(constraint2)
                if (k,col) not in neighbours[(row,col)]:
                    neighbours[(row,col)].append((k,col))
                if (row,col) not in neighbours[(k,col)]:
                    neighbours[(k,col)].append((row,col))
    # all box
    for row in range(3):
        for col in range(3):
            for row2 in range(3):
                for col2 in range(3):
                    if row!=row2 and col!=col2:
                            constraint1 = (row,col,row2,col2)
                            constraint2 = (row2,col2,row,col)
                        #if constraint1 not in queue and constraint2 not in queue:
                            for i in range(3):
                                for j in range(3):
                                    r1 = row+3*i
                                    c1 = col+3*j
                                    r2 = row2+3*i
                                    c2 = col2+3*j
                                    t = (r1,c1,r2,c2)
                                    queue.append(t)
                                    queue.append((r2,c2,r1,c1))
                                    if (r2,c2) not in neighbours[(r1,c1)]:
                                        neighbours[(r1,c1)].append((r2,c2))
                                    if (r1,c1) not in neighbours[(r2,c2)]:
                                        neighbours[(r2,c2)].append((r1,c1))
    queue = list(set(queue))
    return queue

# Make constraint t arc-consistent
def AC3Revise(t):
    i1,j1,i2,j2 = t
    domain1 = domains[i1][j1]
    domain2 = domains[i2][j2]
    for num in domain1:
        if len(domain2 - {num})==0:
            domains[i1][j1].remove(num) # revises domain
            return True
    return False

# achieves arc-consistentcy over whole constraint graph
def AC3(queue):
    while queue:
        #print(len(queue))
        t = queue.pop(0)
        i1,j1,i2,j2 = t
        isRevised = AC3Revise(t)
        if isRevised:
            for (ni1,nj1) in neighbours[(i1,j1)]:
                if (ni1,j1) == (i2,j2):
                    continue
                if (ni1,nj1,i1,j1) not in queue:# and (n1,n2,i1,j2) not in queue:
                    queue.append((ni1,nj1,i1,j1))
                
def applyDomain(board):
    for i in range(9):
        for j in range(9):
            board[i][j] = list(domains[i][j])[0]
            
def getNumberOfFilledSquares(board):
    count = 0
    for i in range(9):
        for j in range(9):
            if board[i][j]!=0:
                count += 1
    return count

def getNextUnassignedVariable(board,domains):
    for i in range(9):
        for j in range(9):
            if board[i][j]==0:
                return (i,j)

def isValueConsistent(board,value,vari,varj):
    neighboursList = neighbours[(vari,varj)]
    for (i,j) in neighboursList:
        if board[i][j]==value:
            return False
    return True
            
def backtrack(board,domains,count):
    if count == 81:
        return board
    vari,varj = getNextUnassignedVariable(board,domains)
    domain = domains[vari][varj]
    for value in domain:
        if isValueConsistent(board,value,vari,varj):
            board[vari][varj] = value
            result = backtrack(board,domains,count+1)
            if result != False:
                return result
        board[vari][varj] = 0
    return False

def areAllDomainsSingleton(domains):
    for i in range(9):
        for j in range(9):
            if len(domains[i][j])>1:
                return False
    return True
    
def backtrackingSearch(board):
    count = getNumberOfFilledSquares(board)
    solvedBoard = backtrack(board,domains,count)
    return solvedBoard

def initializeSudokuBoard():
    print("Type all digits in a row without seperator.")
    print("Type 0 for blank square")
    print("Hit Enter when done")
    #s9 = [None]*9
    for i in range(9):
        #s = x[i*9:i*9+9]
        s = input("Row {} : ".format(i+1))
        s9 = [int(letter) for letter in s]
        for j in range(9):
            num = s9[j]
            if num!=0:
                board[i][j] = s9[j]
                domains[i][j] = {s9[j]}

def solveSudoku(board):
    print("\nInitial stage")
    displayBoard(board)
    initializeNeighbours()
    queue = initializeQueueForAC3()
    AC3(queue)
    if areAllDomainsSingleton(domains): # AC3 was enough
        applyDomain(board)
        solvedBoard = board
    else:
        solvedBoard = backtrackingSearch(board) # AC3 wasn't enough
    print("\nSolution")
    displayBoard(solvedBoard)
    
domains = [[{1,2,3,4,5,6,7,8,9} for i in range(9)] for j in range(9)]
neighbours = {}
board = [[0 for i in range(9)] for j in range(9)]
initializeSudokuBoard()
solveSudoku(board)

# Example sudokus

easy = ("006031070"
         "437005000"
         "010467008"
         "029178300"
         "000000026"
         "300050000"
         "805004910"
         "003509087"
         "790086004")

medium = ("000000609"
          "100004000"
          "005306821"
          "004670050"
          "007000900"
          "000540000"
          "370405206"
          "000000510"
          "060020037")

hard = ("586070000"
        "000901600"
        "000600000"
        "007000000"
        "902010305"
        "005090000"
        "090040008"
        "003500060"
        "000020470")

expert = ("800200000"
          "000009010"
          "345000000"
          "000100050"
          "060000003"
          "038700290"
          "010000006"
          "007900020"
          "000003000"
          )
