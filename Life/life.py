
'''
в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; в противном случае, если соседей меньше двух или больше трёх, клетка умирает («от одиночества» или «от перенаселённости»)
Игра прекращается, если
на поле не останется ни одной «живой» клетки
конфигурация на очередном шаге в точности (без сдвигов и поворотов) повторит себя же на одном из более ранних шагов (складывается периодическая конфигурация)
при очередном шаге ни одна из клеток не меняет своего состояния (складывается стабильная конфигурация; предыдущее правило, вырожденное до одного шага назад)
'''

class Figures:
    pentamino = {0:(0,1,0), 1:(0,1,1), 2:(1,1,0)}
    glider = {0:(0,1,0), 1:(0,0,1), 2:(1,1,1)}
    galactic = {0:(1,1,0,1,1,1,1,1,1),
                1:(1,1,0,1,1,1,1,1,1),
                2:(1,1,0,0,0,0,0,0,0),
                3:(1,1,0,0,0,0,0,1,1),
                4:(1,1,0,0,0,0,0,1,1),
                5:(1,1,0,0,0,0,0,1,1),
                6:(0,0,0,0,0,0,0,1,1),
                7:(1,1,1,1,1,1,0,1,1),
                8:(1,1,1,1,1,1,0,1,1)}

class Cell:
    def __init__(self, is_alive, index, x_field_dimension, y_field_dimension = 0, properties = None):
        self.is_alive = is_alive
        self.index = index
        
        if y_field_dimension == 0:
            y_field_dimension = x_field_dimension

        self.y = index // y_field_dimension
        self.x = index - self.y * x_field_dimension

        #self.alive_neighbors = 0

        #tuple of some properties
        self.properties = properties if properties else {}

        self.neighbors = self.get_neighbors_by_index(index, x_field_dimension, y_field_dimension)
    #end def

    def copy(self):
        copy = Cell(self.is_alive, 0, 1, 1)
        copy.index = self.index
        copy.y = self.y
        copy.x = self.x
        copy.properties = self.properties.copy()
        copy.neighbors = self.neighbors.copy()
        return copy
    #end def

    @staticmethod 
    def get_xy_by_index(index, x_field_dimension, y_field_dimension = 0):       
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
        
        x, y = Cell.get_xy_by_index(index, x_field_dimension, y_field_dimension)

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

class SquareField:
    __dimension = 0
    __alives = 0
    __hash = 0

    # list of alive indexes, need to calc hash, keep sorted
    __alive_indexes = []

    # tuple {index(int) : alives_count(int))}
    # for each index alives must be calculated, includes neighbors and alive cells
    __calculated_cells = {}
 
    # tuple {index : Cell} # old redaction, only alives
    #__cells = {}
    cells = {}

    def __init__(self, dimension, start_position = []):
        self.__dimension = dimension
        # we'll store only alives
        self.populate(start_position)
    #end def

    def __hash__(self):
        self.__alive_indexes.sort()
        self.__hash = hash(tuple(self.__alive_indexes))
    #end def
            
    def __update_calculated_cells_by_index__(self, index):
        for i in self.get_neighbors_by_index(index, True):
            self.__calculated_cells[i] = self.__calculated_cells.get(i, 0) + (1 if i != index else 0)
    #end def

    def get_dimension(self):
        return self.__dimension
    def get_alives(self):
        return self.__alives
    def get_alive_indexes(self):
        return self.__alive_indexes
    def get_cells(self):
        return self.cells
    def get_hash(self):
        return self.__hash

    # return set of neighbors indexes by (x,y)
    def get_neighbors_by_xy(self, x, y):
        field_dimension = self.__dimension
        index = y * field_dimension + x
        neighbors = self.get_neighbors_by_index(self, index)

        return neighbors
    #end def

    # return value - set - of neighbors indexes by (index)
    def get_neighbors_by_index(self, index, include_index = False):
        neighbors = set(Cell.get_neighbors_by_index(index, self.__dimension))
        if include_index:
            neighbors.add(index)

        return neighbors
    #end def

    def calc_figure_indexes(self, figure, start_x, start_y):      
        indexes = []
        for y, row in figure.items():
            for x in range(len(row)):
                if row[x] == 1:
                    # TO DO add calculation for tor field coords
                    index = (start_y + y) * self.__dimension + start_x + x
                    indexes.append(index)
        return indexes
        pass
    #end def

    # return value - dict - {index : cell}
    def calc_state(self):

        new_state_cells = {}
        for index, alive_neighbors_count in self.__calculated_cells.items():
            cell = self.cells.get(index, None)
            old_state = False if cell == None else cell.is_alive
            new_state = old_state
            if (new_state and not alive_neighbors_count in [2,3]) or (not new_state and alive_neighbors_count == 3):
                new_state = not new_state

            # TO DO 
            # add other conditions
            if new_state:
                new_state_cells[index] = Cell(True, index, self.__dimension, self.__dimension, {}) if cell == None else cell.copy()            

        return new_state_cells
        pass
    #end def

    # return value - set - indexes that was changed
    def apply_state(self, new_state_cells):

        self.__alive_indexes = list(new_state_cells.keys())
        self.__alives = self.__alive_indexes.__len__()

        new_state_keys = set(self.__alive_indexes)
        current_state_keys = set(self.cells.keys())

        changed_keys = (current_state_keys | new_state_keys)

        self.cells.clear()
        self.__calculated_cells.clear()
        
        for i, cell in new_state_cells.items():
            self.cells[i] = cell
            self.__update_calculated_cells_by_index__(i)

        self.__hash__()

        return changed_keys
    #end def

    # TO DO statements of population set some properties of cells
    def populate(self, population_list, properties = None):
        for i in population_list:

            # if such index already was filled by another cell we leave old assignment
            if self.cells.get(i, None): 
                continue

            self.cells[i] = Cell(True, i, self.__dimension, self.__dimension, properties)
            self.__alive_indexes.append(i)

            self.__update_calculated_cells_by_index__(i)

        self.__alives = len(self.__alive_indexes)
        self.__hash__()
        pass
    #end def

    def repopulate(self, population_list, properties = None):
        self.cells.clear()
        self.__alive_indexes.clear()
        self.__calculated_cells.clear()
        self.__alives = 0
        self.__hash = 0
        self.populate(self, population_list, properties)
    #end def

    # return value - int
    def calc_state_hash(self):
        # to get correct hash sort is needed 
        # hash is calculating only for property 'is_alive'
        state_keys = list(self.cells.keys())
        state_keys.sort()
        return tuple(state_keys).__hash__()
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
                    print('0' if field.cells.get(i) == None else '+', end=' ')

                if (i + 1) % (dimension) == 0:
                    print(end = '\n')
        pass
    #end def

#end class

if __name__ == '__main__':

    t = {0:{0: 0, 1: 0, 2: 0}, 1:{0: 0, 1: 0, 2: 0}, 2:{0: 0, 1: 0, 2: 0}}
    '''
    for (i, item) in t.items():
        #for j in i.items():
        print(i)
        #for j in i.values():
        #    print(j)
    '''


    field_dimension = 10
    #start_population_list = [2,5,6,7,9,10,12,17,18,20]

    # R - pentamino for dimension 10
    start_population_list = [34,44,45,53,54]
    # R - glider for dimension 10
    start_population_list = [1,12,20,21,22]

    print('init life')

    field = SquareField(field_dimension)
    print('dimension: ' , field.get_dimension())
    field.print(True) 
    print('populate field')
     
    print("state 0")
    field.populate(start_population_list)
    field.print()
    print(field.get_alives(), field.get_hash())

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

