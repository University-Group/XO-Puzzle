from termcolor import colored

class State :
    def __init__(self, cells, played) :
        self.cells = cells
        self.countOfNextStats = 0
        self.played = played
        self.weight = None

    def nextState(self, Me = False):
        if(self.played == 1):
            who = 0
        elif(self.played == 0):
            who = 1
        states = []
        for i,row in enumerate(self.cells):
            for j,col in enumerate(row):
                if(col == -5):
                    item = self.move(i,j,who)
                    self.countOfNextStats = self.countOfNextStats + 1
                    states.append(item)
                    if(Me):
                        print(colored(f"{self.countOfNextStats} - Put O in ({i+1}, {j+1}).", 'cyan'))             
        return states

    def move(self, i, j, who):
        newArr = self.copy()
        newArr[i][j] = who
        return State(newArr, who)

    def displayXO(self):
        print(chr(27) + "[2J")
        print("\n")
        print(colored("*" * 50, "cyan"))
        for row in self.cells:
            for col in row :
                if(col == 1) :
                    print(colored('X', 'blue'), end="")
                elif(col == 0) :
                    print(colored('O', 'yellow'), end="")
                else:
                    print('-', end="")
                print("\t", end="")
            print("\n")
        print(colored("*" * 50, "cyan"))
        print("\n")

    def isFull(self):
        full = True
        for row in self.cells :
            for col in row :
                if(col == -5):
                    full = False
        if(full == True):
            return 1
        else:
            return -1

    def isGoal(self):
        counterOfMainDianeter = 0
        counterOfSecondaryDianeter = 0
        countersOfCol = [0, 0, 0, 0, 0]
        for i,row in enumerate(self.cells) :
            counter = 0
            for j,col in enumerate(row) :
                countersOfCol[j] = countersOfCol[j] + col
                counter = counter + col
                if(i == j):
                    counterOfMainDianeter = counterOfMainDianeter + col
                if(i + j == 4):
                    counterOfSecondaryDianeter = counterOfSecondaryDianeter + col
            if(counter == 5):
                return 1
            elif(counter == 0):
                return 0

        for val in countersOfCol:
            if(val == 5):
                return 1
            elif(val == 0):
                return 0

        if(counterOfMainDianeter == 5 or counterOfSecondaryDianeter == 5):
            return 1
        elif(counterOfMainDianeter == 0 or counterOfSecondaryDianeter == 0):
            return 0

        return -1

    def horisticOfXO(self):
        countOfrowsOfX = 0
        countOfrowsOfY = 0
        countOfColsOfX = 0
        countOfColsOfY = 0
        countOfDiameterOfX = 0
        countOfDiameterOfY = 0

        chseckXInMainDiameter = False
        chseckXInSecondaryDiameter = False
        chseckYInMainDiameter = False
        chseckYInSecondaryDiameter = False

        chseckXIncols = [False, False, False, False, False]
        chseckYIncols = [False, False, False, False, False]
        for i,row in enumerate(self.cells) :
            chseckX = False
            chseckY = False
            for j,col in enumerate(row) :
                if(col == 1) :
                    chseckX = True
                    chseckXIncols[j] = True
                elif(col == 0) :
                    chseckY = True
                    chseckYIncols[j] = True

                if(i == j and col == 1):
                    chseckXInMainDiameter = True
                elif(i == j and col == 0):
                    chseckYInMainDiameter = True

                if(i + j == 4 and col == 1):
                    chseckXInSecondaryDiameter = True
                elif(i + j == 4 and col == 0):
                    chseckYInSecondaryDiameter = True        
            if(chseckX != True):
                countOfrowsOfY = countOfrowsOfY + 1
            if(chseckY != True):
                countOfrowsOfX = countOfrowsOfX + 1

        for val1,val2 in zip(chseckXIncols,chseckYIncols):
            if(val1 != True):
                countOfColsOfY = countOfColsOfY + 1
            if(val2 != True):
                countOfColsOfX = countOfColsOfX + 1

        if(chseckXInMainDiameter != True):
            countOfDiameterOfY = countOfDiameterOfY + 1
        if(chseckYInMainDiameter != True):
            countOfDiameterOfX = countOfDiameterOfX + 1

        if(chseckXInSecondaryDiameter != True):
            countOfDiameterOfY = countOfDiameterOfY + 1
        if(chseckYInSecondaryDiameter != True):
            countOfDiameterOfX = countOfDiameterOfX + 1
            
        result = (countOfrowsOfX + countOfColsOfX + countOfDiameterOfX) - (countOfrowsOfY + countOfColsOfY + countOfDiameterOfY)
        if(self.played == 0):
            self.weight = result
            return result
        elif(self.played == 1):
            self.weight = -1 * result
            return -1 * result

    def copy(self) :
        listall = []
        for row in self.cells :
            listall.append(row.copy())
        return listall

class Logic:

    @staticmethod
    def startGame(init):
        print(chr(27) + "[2J")
        inp = input(colored("\nChoose The Level Of Game:\n 1.Easy\n 2.Hard\n", 'green'))
        while inp.isnumeric() != True or int(inp) < 1 or int(inp) > 2 :
            inp = input(colored("\nChoose The Level Of Game:\n 1.Easy\n 2.Hard\n", 'green'))

        if(int(inp) == 1):
            Logic.playGame(init, 2)
        elif(int(inp) == 2):
            Logic.playGame(init, 5)

    @staticmethod
    def playGame(state, Level):
        while state.isGoal() == -1 and state.isFull() == -1:
            state.displayXO()
            if(state.played == 1):
                state = State(Logic.Me(state).copy(), 0)
            elif(state.played == 0):
                state = State(Logic.Software(state, Level).copy(), 1)
        
        state.displayXO()
        Logic.checkEndOfTheGame(state)

    @staticmethod
    def Me(state):
        states = state.nextState(True)
        inp = input(colored("\nWhat's The Movement Would You Want: ", 'green'))
        while inp.isnumeric() != True or int(inp) < 1 or int(inp) > len(states) :
            inp = input(colored("\nWhat's The Movement Would You Want: ", 'green'))
        state = states[int(inp) - 1]
        return state

    @staticmethod
    def Software(state, Level):
        return Logic.Max(state, Level, None)

    @staticmethod
    def Max(state, Level, Beta):
        if(Level == 0 or state.isFull() == 1):
            state.horisticOfXO()
            return state

        list = []
        states = state.nextState()
        for st in states:
            Logic.Min(st, Level - 1, state.weight)
            list.append(st.weight)
            if(state.weight == None):
                state.weight = st.weight
            else:
                state.weight = max(state.weight, st.weight)

            if(Beta and Beta <= st.weight):
                # print("*************************************************Hello From Beta Cut")
                break

        return states[list.index(state.weight)]

    @staticmethod
    def Min(state, Level, Alpha):
        if(Level == 0 or state.isFull() == 1):
            state.horisticOfXO()
            return state
        list = []
        states = state.nextState()
        for st in states:
            Logic.Max(st, Level - 1, state.weight)
            list.append(st.weight)
            if(state.weight == None):
                state.weight = st.weight
            else:
                state.weight = min(state.weight, st.weight)
                
            if(Alpha and Alpha >= st.weight):
                # print("*************************************************Hello From Alpha Cut")
                break

        return states[list.index(state.weight)]

    @staticmethod
    def checkEndOfTheGame(state):
        if(state.isFull() == 1):
            Logic.noOneWon()
        else:
            Logic.someOneWon(state.isGoal())

    @staticmethod
    def noOneWon():
        print("\n\t\t\t\t\t", end="")
        print(colored("# "*22, 'cyan'))
        print(colored("\n\t\t\t\t\t#\t     T R Y - A G A I N            #", 'cyan'))
        print("\n\t\t\t\t\t", end="")
        print(colored("# "*22, 'cyan'))

    @staticmethod
    def someOneWon(who):
        print("\n\t\t\t\t\t", end="")
        print(colored("# "*22, 'cyan'))
        print(colored("\n\t\t\t\t\t#\tC o n g r a t u l a t i o n       #", 'cyan'))
        print("\n\t\t\t\t\t", end="")
        print(colored("# "*22, 'cyan'))
        if(who == 1):
            team = 'X'
        elif(who == 0):
            team = 'O'
        print(f"\n\t\t\t\t\t\t      The {team} Team Is Won")

############################### Main ###############################

init = State([[1,0,0,0,0],
        [-5,1,-5,-5,-5],
        [-5,-5,1,-5,-5],
        [-5,-5,-5,-5,-5],
        [-5,-5,-5,-5,-5]], 0) # 1 For X , 0 For O , -5 For Empty

Logic.startGame(init)
