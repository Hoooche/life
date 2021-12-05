
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

        self.neighbors = self.get_neighbors_by_index(index, x_field_dimension, y_field_dimension)
    #end def

    @staticmethod 
    def get_coords_by_index(index, x_field_dimension, y_field_dimension = 0):       
        if y_field_dimension == 0:
            y_field_dimension = x_field_dimension

        y = index // y_field_dimension
        x = index - y * x_field_dimension
        return x, y
    #end def

    @staticmethod 
    def get_neighbors_by_index(index, x_field_dimension, y_field_dimension = 0):       
        if y_field_dimension == 0:
            y_field_dimension = x_field_dimension
        
        x, y = Cell.get_coords_by_index(index, x_field_dimension, y_field_dimension)

        x_left = x - 1
        if x_left < 0:
            x_left = x_field_dimension-1

        x_right = x + 1
        if x_right == x_field_dimension:
            x_right = 0

        y_up = y - 1
        if y_up < 0:
            y_up = y_field_dimension-1

        y_down = y + 1
        if y_down == y_field_dimension:
            y_down = 0

        neighbors = []
        neighbors.append(y_up * y_field_dimension + x_left)
        neighbors.append(y_up * y_field_dimension + x)
        neighbors.append(y_up * y_field_dimension + x_right)

        neighbors.append(y * y_field_dimension + x_left)
        neighbors.append(y * y_field_dimension + x_right)

        neighbors.append(y_down * y_field_dimension + x_left)
        neighbors.append(y_down * y_field_dimension + x)
        neighbors.append(y_down * y_field_dimension + x_right)

        return neighbors
    #end def
#end class

class SquadField:
    __startPopulationList = []
    __dimension = 0
    __alives = 0
    __hash = 0
    # alive cells
    cells = {}
    tuple_cells = []
    def __init__(self, dimension, start_position = []):
        self.__dimension = dimension
        #for i in range(dimension*dimension):
        #    self.cells.append(Cell(False, i, dimension))

        # we'll store only alives
        for i in start_position:
            self.cells[i] = Cell(True, i, dimension)    
    #end def

    def get_dimension(self):
        return self.__dimension
    def get_alives(self):
        return self.__alives
    def get_cells(self):
        return self.cells
    def get_hash(self):
        return self.__hash

    # return array of neighbors indexes by (x,y)
    def get_neighbors(self, x, y):

        field_dimension = self.get_dimension()
        index = y * field_dimension + x
        neighbors = self.get_neighbors_by_index(self, index)

        return neighbors
    #end def

    # return array of neighbors indexes by (index)
    def get_neighbors_by_index(self, index):
        neighbors = []
        cell = self.cells.get(index, None)
        if cell == None:
            neighbors = Cell.get_neighbors_by_index(index, self.__dimension)
        else:
            neighbors = cell.neighbors
        
        return neighbors
    #end def

    def calc_state(self):

        new_state_cells = {}
        calculated_cells = []

        current_state_keys = self.cells.keys()

        for i, cell in self.cells.items():

            cell_indexes = self.get_neighbors_by_index(i).copy()
            cell_indexes.append(i)

            for index in cell_indexes:

                if index in calculated_cells:
                    continue
  
                neighbors = self.get_neighbors_by_index(index)

                # lets count alive neighbors
                alive_neighbors_count = list(set(neighbors) & set(current_state_keys)).__len__()
            
                # checking conditions to get new cell statement            
                new_state = index in current_state_keys

                if (new_state and not alive_neighbors_count in [2,3]) or (not new_state and alive_neighbors_count == 3):
                    new_state = not new_state

                if new_state:
                    # create new object Cell with new statements, here we can modify values of some properties 
                    new_state_cells[index] = Cell(True, index, self.__dimension)

                calculated_cells.append(index)

        return new_state_cells
        pass
    #end def

    def calc_state_hash(self):
        # to get correct hash sort is needed 
        # hash is calculating only for property 'is_alive'
        state_keys = list(self.cells.keys())
        state_keys.sort()
        return tuple(state_keys).__hash__()
    #end def

    def apply_state(self, new_state_cells):
        changed_keys = []

        old_hash = self.__hash
        self.__hash = self.calc_state_hash()
        
        if old_hash != self.__hash:
            new_state_keys = list(new_state_cells.keys())
            self.__alives = new_state_keys.__len__()

            current_state_keys = list(self.cells.keys())
            changed_keys = list(set(current_state_keys + new_state_keys))

            # delete cells 
            for i in list(set(current_state_keys) - set(new_state_keys)):
                self.cells.pop(i)

            for i, cell in new_state_cells.items():
                # TO DO: no need to use new cell ref if cell already exists, check needed
                self.cells[i] = cell

        return changed_keys
    #end def

    def print(self, show_index = False):
        field = self
        dimension = field.get_dimension()
        dimension_str_len = len(str(dimension))
        if dimension != 0:
            for i in range(dimension*dimension):
                if show_index:
                    print('{0:0{width}}'.format(i, width=dimension_str_len), end=' ')
                else:
                    # if we found any cell in cells by index, that means it is alive
                    alive_cell = field.cells.get(i) 
                    if alive_cell == None:
                        print('0', end=' ')
                    else:
                        print('+', end=' ')

                if (i + 1) % (dimension) == 0:
                    print(end = '\n')
        pass
    #end def

    def populate(self, population_list):
        dimension = self.get_dimension()
        self.cells.clear()
        for i in population_list:
            self.cells[i]= Cell(True, i, dimension)
        pass
    #end def
#end class

if __name__ == '__main__':
    
    field_dimension = 10
    #start_population_list = [2,5,6,7,9,10,12,17,18,20]

    # R - pentamino for dimension 10
    start_population_list = [34,44,45,53,54]
    # R - glider for dimension 10
    start_population_list = [1,12,20,21,22]

    print('init life')

    field = SquadField(field_dimension)
    print('dimension: ' , field.get_dimension())
    field.print(True) 
    print('populate field')
     
    print("state 0")
    field.populate(start_population_list)
    field.print()

    #print(field.get_neighbors(0,0))
    #print(field.get_neighbors(1,0))    
    #print(field.get_neighbors(2,2))    
    #print(field.get_neighbors(0,1))    
    #print(field.get_neighbors(0,2))    

    '''
    [99, 90, 91, 9, 1, 19, 10, 11]
    [90, 91, 92, 0, 2, 10, 11, 12]
    [11, 12, 13, 21, 23, 31, 32, 33]
    [9, 0, 1, 19, 11, 29, 20, 21]
    [19, 10, 11, 29, 21, 39, 30, 31]
    '''

    states = []
    circleOfLife = True

    while circleOfLife:
        new_state = field.calc_state()
        field.apply_state(new_state)        
        print('----------')
        print(field.get_alives(), field.get_hash())
        field.print()
        if not (field.get_alives() > 0 and states.count(field.get_hash()) == 0):
            circleOfLife = False

        states.append(field.get_hash())
        pass

    print('----------')
    print('Count od states: ', len(states))
    print('Population: ', field.get_alives())

