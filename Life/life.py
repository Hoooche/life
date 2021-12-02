
'''
в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; в противном случае, если соседей меньше двух или больше трёх, клетка умирает («от одиночества» или «от перенаселённости»)
Игра прекращается, если
на поле не останется ни одной «живой» клетки
конфигурация на очередном шаге в точности (без сдвигов и поворотов) повторит себя же на одном из более ранних шагов (складывается периодическая конфигурация)
при очередном шаге ни одна из клеток не меняет своего состояния (складывается стабильная конфигурация; предыдущее правило, вырожденное до одного шага назад)
'''

'''
Характеристика "Желание жить" 
2 из 3 клеток получают опыт увеличивающий эту характеристику (опыт рождения)
Все клетки получают опыт уменьшающий эту харктеристику (опыт смерти)
Есть минимальное значение характеристики, при достижении которого в случае когда вокруг анализируемой клетки есть только 1 клетка, 
то умирают обе, одна от "одиночества", а другая от "депрессии".
'''
'''
Порядок обхода клеток имеет значение. 
Обдумать возможность альтернативного порядка обхода. 
Например, случайного, или сначала все клетки с наибольшим количеством соседей или сначала все клетки с наименьшим...
'''


class Life:
    __startPopulationList = []
    def __init__(self, dimension):
        self.createField(dimension)

    def createField(self, dimension):

        class Cell:
            def __init__(self, isAlive, index):
                self.isAlive = isAlive
                self.index = index
                
                self.y = index // dimension
                self.x = index - self.y * dimension

        class Field:
            def __init__(self, fieldDimension):
                self.__dimension = fieldDimension
                self.__alives = 0

                self.cells = []

            def fieldDimension(self):
                return self.__dimension
            def fieldAlives(self):
                return self.__alives
            def fieldCells(self):
                return self.cells

        self.field = Field(dimension)
        for i in range(dimension*dimension):
            self.field.cells.append(Cell(False, i))

        return self.field
    #end def

    def fieldDimension(self):
        return self.field.fieldDimension()

    # return array of indexes 
    def getNeighbors(self, x, y):
        fieldDimension = self.fieldDimension()
        neighbors = []

        xLeft = x - 1
        if xLeft < 0:
            xLeft = fieldDimension-1

        xRight = x + 1
        if xRight == fieldDimension:
            xRight = 0

        yUp = y - 1
        if yUp < 0:
            yUp = fieldDimension-1

        yDown = y + 1
        if yDown == fieldDimension:
            yDown = 0

        neighbors.append(yUp * fieldDimension + xLeft)
        neighbors.append(yUp * fieldDimension + x)
        neighbors.append(yUp * fieldDimension + xRight)

        neighbors.append(y * fieldDimension + xLeft)
        neighbors.append(y * fieldDimension + xRight)

        neighbors.append(yDown * fieldDimension + xLeft)
        neighbors.append(yDown * fieldDimension + x)
        neighbors.append(yDown * fieldDimension + xRight)

        return neighbors
    #end def

    def calcStateOfField(self):
        aliveCount = 0
        stateForHash = []
        for cell in self.field.cells:
            neighbors = self.getNeighbors(cell.x, cell.y)

            neighborsCount = 0
            for neighbor in neighbors:
                if self.field.cells[neighbor].isAlive:
                    neighborsCount = neighborsCount + 1

            if cell.isAlive:
                if not neighborsCount in [2,3]:
                    cell.isAlive = False
            else:
                if neighborsCount == 3:
                    cell.isAlive = True

            if cell.isAlive: aliveCount = aliveCount + 1
            stateForHash.append(cell.isAlive)

        hashValue = hash(tuple(stateForHash))
        return aliveCount, hashValue
        pass
    #end def

    def printField(self, field):
        for i in field.cells:
            if i.isAlive:
                print('+', end=' ')
            else:
                print('0', end=' ')

            if (i.index + 1) % (field.fieldDimension()) == 0:
                print(end = '\n')
        pass
    #end def

    def populateField(self, populationList):
        for populationIndex in populationList:
            #print(populationIndex)
            self.field.cells[populationIndex].isAlive = True
        pass
    #end def

    def populateAllField(self):
        for cell in self.field.cells:
            cell.isAlive = True
        pass
    #end def

if __name__ == '__main__':

    fieldDimension = 5
    startPopulationList = [2,5,6,9,10]

    print('init life')

    life = Life(fieldDimension)
    print(life.fieldDimension())
    life.printField(life.field)
    
    print('populate field')
    life.populateField(startPopulationList)
    life.printField(life.field)

    #print(life.field.cells[2].x,life.field.cells[2].y)

    '''
    print(getNeighbors(0,0, field))
    print(getNeighbors(2,2, field))
    print(getNeighbors(0,2, field))
    print(getNeighbors(2,0, field))
    '''
    '''
    print("state 0")
    Life.populateField(Life.field, startPopulationList)
    Life.printField(Life.field)

    exit

    states = []
    circleOfLife = True

    while circleOfLife:
        alives, hashValue = Life.calcStateOfField()
        print('----------')
        print(alives, hashValue)
        Life.printField(Life.field)
        if not (alives > 0 and states.count(hashValue) == 0):
            circleOfLife = False

        states.append(hashValue)
        pass

    print('----------')
    print('Count od states: ', len(states))
    print('Population: ', alives)
    #printField(Life.field)
    '''