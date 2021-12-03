
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

class Cell:
    def __init__(self, is_alive, index, x_field_dimension, y_field_dimension = 0):
        self.is_alive = is_alive
        self.index = index

        if y_field_dimension == 0:
            y_field_dimension = x_field_dimension

        self.y = index // y_field_dimension
        self.x = index - self.y * x_field_dimension


class SquadField:
    __startPopulationList = []
    __dimension = 0
    __alives = 0
    __hash = 0
    cells = []

    def __init__(self, dimension):
        self.__dimension = dimension
        for i in range(dimension*dimension):
            self.cells.append(Cell(False, i, dimension))
    #end def

    def get_dimension(self):
        return self.__dimension
    def get_alives(self):
        return self.__alives
    def get_cells(self):
        return self.cells
    def get_hash(self):
        return self.__hash

    # return array of indexes 
    def get_neighbors(self, x, y):
        fieldDimension = self.get_dimension()
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

    def calc_state(self):
        self.__alives = 0
        stateForHash = []
        for cell in self.cells:
            neighbors = self.get_neighbors(cell.x, cell.y)

            neighborsCount = 0
            for neighbor in neighbors:
                if self.cells[neighbor].is_alive:
                    neighborsCount = neighborsCount + 1

            if cell.is_alive:
                if not neighborsCount in [2,3]:
                    cell.is_alive = False
            else:
                if neighborsCount == 3:
                    cell.is_alive = True

            if cell.is_alive: self.__alives = self.__alives + 1
            stateForHash.append(cell.is_alive)

        self.__hash = hash(tuple(stateForHash))
        return self.__alives, self.__hash
        pass
    #end def

    def print(self):
        field = self
        if field.get_dimension() != 0:
            for i in field.cells:
                if i.is_alive:
                    print('+', end=' ')
                else:
                    print('0', end=' ')

                if (i.index + 1) % (field.get_dimension()) == 0:
                    print(end = '\n')
        pass
    #end def

    def populate(self, populationList):
        for populationIndex in populationList:
            #print(populationIndex)
            self.cells[populationIndex].is_alive = True
        pass
    #end def

    def populate_all(self):
        for cell in self.cells:
            cell.is_alive = True
        pass
    #end def

if __name__ == '__main__':

    fieldDimension = 5
    startPopulationList = [2,5,6,7,9,10,12,17,18,20]

    print('init life')

    field = SquadField(fieldDimension)
    print(field.get_dimension())
    field.print()
    
    print('populate field')
    field.populate(startPopulationList)
    field.print()

    #print(life.field.cells[2].x,life.field.cells[2].y)

    '''
    print(get_neighbors(0,0, field))
    print(get_neighbors(2,2, field))
    print(get_neighbors(0,2, field))
    print(get_neighbors(2,0, field))
    '''
    
    print("state 0")
    field.populate(startPopulationList)
    field.print()

    states = []
    circleOfLife = True

    while circleOfLife:
        alives, hashValue = field.calc_state()
        print('----------')
        print(alives, hashValue)
        field.print()
        if not (alives > 0 and states.count(hashValue) == 0):
            circleOfLife = False

        states.append(hashValue)
        pass

    print('----------')
    print('Count od states: ', len(states))
    print('Population: ', alives)

