
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
    fieldDimension = 0
    
    def __init__(self, dimension):
        self.fieldDimension = dimension
        print('qq', dimension)
        print(self.fieldDimension)
        self.field = self.createField(dimension)

    class Cell:
        def __init__(self, isAlive, index):
            self.isAlive = isAlive
            self.index = index
            
            self.y = index // Life.fieldDimension
            self.x = index - self.y * Life.fieldDimension

    def createField(self, dimension):
        sequence = []
        for i in range(dimension*dimension):
            sequence.append(self.Cell(False, i))
        return sequence
    #end def
    
    # return array of indexes 
    def getNeighbors(self, x, y):
        fieldDimension = self.fieldDimension
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
        for cell in self.field:
            neighbors = self.getNeighbors(cell.x, cell.y)

            neighborsCount = 0
            for neighbor in neighbors:
                if field[neighbor].isAlive:
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

    def printField(field):
        for i in field:
            if i.isAlive:
                print('+', end=' ')
            else:
                print('0', end=' ')

            if (i.index + 1) % (field.fieldDimension) == 0:
                print(end = '\n')
        pass
    #end def

    def populateField(self, field, populationcount):
        field[2].isAlive = True
        field[5].isAlive = True
        field[6].isAlive = True
        field[9].isAlive = True
        field[10].isAlive = True
        pass
    #end def

if __name__ == '__main__':
    fieldDimension = 5
    startPopulationCount = 4

    field = Life(fieldDimension)
    
    '''
    print(getNeighbors(0,0, field))
    print(getNeighbors(2,2, field))
    print(getNeighbors(0,2, field))
    print(getNeighbors(2,0, field))
    '''

    print("state 0")
    Life.populateField(field, startPopulationCount)
    Life.printField(field)

    states = []
    circleOfLife = True

    while circleOfLife:
        alives, hashValue = Life.calcStateOfField()
        print('----------')
        print(alives, hashValue)
        Life.printField(field)
        if not (alives > 0 and states.count(hashValue) == 0):
            circleOfLife = False

        states.append(hashValue)
        pass

    print('----------')
    print('Count od states: ', len(states))
    print('Population: ', alives)
    #printField(field)
