class Account:
    def __init__(self, name, no, amount, limit):
        self.name = name
        self.number = no
        self.amount = amount
        self.limit = limit

    def isValid(self):
        sum = 0
        i=0
        while i <=14:
            if (i == 3 or i == 4):
                sum += ord('0')
            else:
                sum += ord(self.number[i])
            i+=1
        checksum = int(98 - (sum%97))
        str = ""
        str += self.number[3]
        str += self.number[4]
        numb = int(str)
        str1 = 0

        if checksum != numb:
            print("checksum not ok")
            print(checksum, numb)
            return False
        lowerF = []
        upperF = []
        for i in range(0,27):
            lowerF.append(0)
            upperF.append(0)

        i = 5
        while i<=14:
            letterCode = ord(self.number[i])
            if 65<=letterCode<=90:
                lowerF[letterCode - 65] += 1
            else:
                if 97 <= letterCode<=122:
                    upperF[letterCode-97] += 1
            i +=1
        for i in range(0,25):
            if lowerF[i] != upperF[i]:
                return False
        return True



class Transaction:
    def __init__(self, persFrom, persTo, amount, time):
        self.persFrom = persFrom
        self.persTo = persTo
        self.amount = amount
        self.time = time

class Repo:
    def __init__(self):
        self.transactions = []
        self.accounts = []
        self.okTransactions = 0

    def addTransaction(self, f, t, a, ti):
        self.transactions.append(Transaction(f,t,a,ti))

    def addAccount(self,n,a,b,c):
        self.accounts.append(Account(n,a,b,c))

    def readFromFile(self):

        f = open("input.txt", 'r')
        nr = int(f.readline())
        i = 0
        line = f.readline().strip()
        while i < nr :
            args = line.split(" ")
            self.addAccount(args[0], args[1], int(args[2]), int(args[3]))
            line = f.readline().strip()
            i+=1

        # nr = int(f.readline())
        nr = int(line)
        i = 0
        line = f.readline().strip()
        while i < nr:
            args = line.split(" ")
            self.addTransaction(args[0], args[1], int(args[2]), int(args[3]))
            line = f.readline().strip()
            i += 1

    def showTransactions(self):
        for i in self.transactions:

            print(i.persFrom, i.persTo, i.amount, i.time)

    def showAccounts(self):
        nr = 0
        for i in self.accounts:
            if i.isValid():
                nr += 1
        print(nr)
        for i in self.accounts:
            if i.isValid():
                print(i.name, i.amount)

    def doTransaction(self, t):
        for i in self.accounts:
            if i.number == t.persTo and i.isValid():
                for j in self.accounts:
                    if j.number == t.persFrom and j.isValid() and t.amount< j.amount+j.limit:
                        j.amount -= t.amount
                        i.amount += t.amount
                        return 1
        return 0

    def doTransactions(self):
        ok = 0
        while ok == 0:
            for i in range(0, len(self.transactions)-1):
                ok = 1
                for j in range(i+1, len(self.transactions)):
                    if self.transactions[i].time > self.transactions[j].time:
                        ok = 0
                        self.transactions[i], self.transactions[j] = self.transactions[j], self.transactions[i]
        #self.showTransactions()
        for i in self.transactions:
            if self.doTransaction(i) == 1:
                self.okTransactions += 1


class NewTransaction:
    def __init__(self, transID, noInputs, inputs:list, nrOutputs ,outputs:list, timeStamp ):
        self.transID = transID
        self.nrOutputs = nrOutputs
        self.noInputs = noInputs
        self.inputs = inputs
        self.outputs = outputs
        self.timeStamp = timeStamp

    def isValid(self, transList):
        for i in self.inputs:
            if i.amount <= 0:
                return False
        for i in self.outputs:
            if i.amount <= 0:
                return False

        sumin=0
        sumout=0
        for i in self.inputs:
            sumin += i.amount
        for i in self.outputs:
            sumout += i.amount
        if sumin!=sumout:
            return False

        for i in self.inputs:
            for j in range(len(transList)):
                if transList[j].id == self.transID:
                    pos = j
            isOutput=0
            for e in range(pos):
                for t in transList[e].outputs:
                    if t.owner == e.owner and t.amount == e.amount:
                        isOutput = 1
            if isOutput == 0:
                return False

        for o in range(len(self.outputs)-1):
            for op in range(o+1, len(self.outputs)):
                if self.outputs[o].owner == self.outputs[op].owner:
                    return False
        for o in range(len(self.outputs)):
            noUses=0
            for i in range(o+1, len(self.inputs)):
                if self.inputs[i].owner==self.outputs[o].owner:
                    noUses+=1
            if noUses>1:
                return False
        return True


class Input:
    def __init__(self, id, owner, amount ):
        self.id = id
        self.owner = owner
        self.amount = amount


class Output:
    def __init__(self, owner, amount):
        self.owner = owner
        self.amount = amount


class TransRepo:
    def __init__(self):
        self.transactions = []

    def add(self, t):
        self.transactions.append(t)
        ok = 0
        while ok == 0:
            for i in range(0, len(self.transactions) - 1):
                ok = 1
                for j in range(i + 1, len(self.transactions)):
                    if self.transactions[i].timeStamp > self.transactions[j].timeStamp:
                        ok = 0
                        self.transactions[i], self.transactions[j] = self.transactions[j], self.transactions[i]
            break


    def readFromFile(self):
        f = open("input.txt", 'r')
        nr = int(f.readline())
        i = 0
        line = f.readline().strip()
        while i < nr and line != "":
            args = line.split(" ")
            tID = args[0]
            noInputs = int(args[1])
            k = 2
            inputs =[]
            for i in range(noInputs):
                inputs.append(Input(args[k], args[k+1], int(args[k+2])))
                k+=3
            nrOutputs = int(args[k])
            k+=1
            outputs = []
            for i in range(nrOutputs):
                outputs.append(Output(args[k], int(args[k+1])))
                k+=2
            t = args[k]
            self.add(NewTransaction(tID, noInputs, inputs, nrOutputs, outputs, t ))
            line = f.readline().strip()

            i += 1



    def printTransactions(self):
        for i in self.transactions:
            str1 = ""
            for j in i.inputs:
                str1 += j.id
                str1 += " "
                str1 += j.owner
                str1 += " "
                str1 += str(j.amount)

            str2 = ""
            for j in i.outputs:
                str2 += j.owner
                str2 += " "
                str2 += str(j.amount)
            if i.isValid:
                print(i.transID, i.noInputs, str1, i.nrOutputs , str2, i.timeStamp)

repo = TransRepo()
repo.readFromFile()
repo.printTransactions()
