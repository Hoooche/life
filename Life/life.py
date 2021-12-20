
'''
в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить; в противном случае, если соседей меньше двух или больше трёх, клетка умирает («от одиночества» или «от перенаселённости»)
Игра прекращается, если
на поле не останется ни одной «живой» клетки
конфигурация на очередном шаге в точности (без сдвигов и поворотов) повторит себя же на одном из более ранних шагов (складывается периодическая конфигурация)
при очередном шаге ни одна из клеток не меняет своего состояния (складывается стабильная конфигурация; предыдущее правило, вырожденное до одного шага назад)
'''
from datetime import datetime

class Figures:
    pentamino = {0:(0,1,0), 1:(0,1,1), 2:(1,1,0)}
    glider = {0:(0,1,0), 1:(0,0,1), 2:(1,1,1)}
    koks_galaxy = {0:(1,1,0,1,1,1,1,1,1),
                1:(1,1,0,1,1,1,1,1,1),
                2:(1,1,0,0,0,0,0,0,0),
                3:(1,1,0,0,0,0,0,1,1),
                4:(1,1,0,0,0,0,0,1,1),
                5:(1,1,0,0,0,0,0,1,1),
                6:(0,0,0,0,0,0,0,1,1),
                7:(1,1,1,1,1,1,0,1,1),
                8:(1,1,1,1,1,1,0,1,1)}
    cross = {0:(0,0,1,1,1,1,0,0),
             1:(0,0,1,0,0,1,0,0),
             2:(1,1,1,0,0,1,1,1),
             3:(1,0,0,0,0,0,0,1),
             4:(1,0,0,0,0,0,0,1),
             5:(1,1,1,0,0,1,1,1),
             6:(0,0,1,0,0,1,0,0),
             7:(0,0,1,1,1,1,0,0)}
    pentadecathlon = {0:(0,0,1,0,0,0,0,1,0,0),
                      1:(1,1,0,1,1,1,1,0,1,1),
                      2:(0,0,1,0,0,0,0,1,0,0)}
    lock =  {0:(0,1),
             1:(1,1),
             2:(1,1),
             3:(1,0)}
             
    block = {0:(0,0,0,0),
             1:(0,1,1,0),
             2:(0,1,1,0),
             3:(0,0,0,0)}
    blinker = {0:(0,0,0),
               1:(0,1,0),
               2:(0,1,0),
               3:(0,1,0),
               4:(0,0,0)}             
    tub =   {0:(0,0,0,0,0),
             1:(0,0,1,0,0),
             2:(0,1,0,1,0),
             3:(0,0,1,0,0),
             4:(0,0,0,0,0)}
    ship =  {0:(0,0,0,0,0),
             1:(0,1,1,0,0),
             2:(0,1,0,1,0),
             3:(0,0,1,1,0),
             4:(0,0,0,0,0)}
    boat =  {0:(0,0,0,0,0),
             1:(0,1,1,0,0),
             2:(0,1,0,1,0),
             3:(0,0,1,0,0),
             4:(0,0,0,0,0)}
    hive =  {0:(0,0,0,0,0),
            1:(0,0,1,0,0),
            2:(0,1,0,1,0),
            3:(0,1,0,1,0),
            4:(0,0,1,0,0),
            5:(0,0,0,0,0)}
    pond = {0:(0,0,0,0,0,0),
            1:(0,0,1,1,0,0),
            2:(0,1,0,0,1,0),
            3:(0,1,0,0,1,0),
            4:(0,0,1,1,0,0),
            5:(0,0,0,0,0,0)}
    loaf = {0:(0,0,0,0,0,0),
            1:(0,0,0,1,0,0),
            2:(0,0,1,0,1,0),
            3:(0,1,0,0,1,0),
            4:(0,0,1,1,0,0),
            5:(0,0,0,0,0,0)}
    double_loaf = {0:(0,0,0,0,0,0,0,0,0),
                   1:(0,0,0,0,0,0,1,0,0),
                   2:(0,0,0,0,0,1,0,1,0),
                   3:(0,0,0,0,1,0,0,1,0),
                   4:(0,0,0,1,0,1,1,0,0),
                   5:(0,0,1,0,1,0,0,0,0),
                   6:(0,1,0,0,1,0,0,0,0),
                   7:(0,0,1,1,0,0,0,0,0),
                   8:(0,0,0,0,0,0,0,0,0)}

class Cell:
    def __init__(self, is_alive, index, x_field_dimension, y_field_dimension = 0, properties = None):
        self.is_alive = is_alive
        self.index = index
        
        if y_field_dimension == 0:
            y_field_dimension = x_field_dimension

        self.y = index // y_field_dimension
        self.x = index - self.y * x_field_dimension

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
    __keep_history = True
    # history of field`s cells activity
    __history = []

    # tuple {index(int) : alives_count(int))}
    # for each index alives must be calculated, includes neighbors and alive cells
    __calculated_cells = {}
 
    # tuple {index : Cell} # old redaction, only alives
    cells = {}

    def __init__(self, dimension, start_position = []):
        self.__dimension = dimension
        # we'll store only alives
        self.populate(start_position)
    #end def

    # for internal use only - very slow
    def __hash__(self):
        __alive_indexes = list(self.cells.keys())
        __alive_indexes.sort()
        return tuple(__alive_indexes).__hash__()
    #end def
            
    def __update_calculated_cells_by_index__(self, index):
        for i in self.get_neighbors_by_index(index, True):
            self.__calculated_cells[i] = self.__calculated_cells.get(i, 0) + (1 if i != index else 0)
    #end def

    def get_dimension(self):
        return self.__dimension
    def get_alives(self):
        return self.__alives
    def get_history(self):
        return self.__history
    def get_history_count(self):
        return len(self.__history)
    def get_cells(self):
        return self.cells

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
    # old version (calculated pentamo at 360*360 for 53 seconds)
    def apply_state_old(self, new_state_cells):

        new_state_keys = set(new_state_cells.keys())
        current_state_keys = set(self.cells.keys())

        changed_keys = (current_state_keys | new_state_keys)
 
        self.cells.clear()
        self.__calculated_cells.clear()
        
        for i, cell in new_state_cells.items():
            self.cells[i] = cell
            self.__update_calculated_cells_by_index__(i)

        self.__alives = new_state_keys.__len__()

        if self.__keep_history:
            self.__history.append(new_state_keys)

        return changed_keys
    #end def

    # new version (calculated pentamo at 360*360 for 36 seconds)
    def apply_state(self, new_state_cells):

        new_state_keys = set(new_state_cells.keys())
        current_state_keys = set(self.cells.keys())

        new_keys = (new_state_keys - current_state_keys)
        #add new keys to cells
        for i, cell in new_state_cells.items():
            self.cells[i] = cell
            if i in new_keys:
                self.__calculated_cells[i] = self.__calculated_cells.get(i, 0)
                for key in cell.neighbors:
                    self.__calculated_cells[key] = self.__calculated_cells.get(key, 0) + 1

        # delete keys from cells
        # find __calculatetd_cells for delete 
        delete_calculated_cells = set()
        for i in (current_state_keys - new_state_keys):
            cell = self.cells.pop(i)
            #cell_neighbors = cell.neighbors.copy()
            #cell_neighbors.append(i)
            cell.neighbors.append(i)
            for key in cell.neighbors:
                key_value = self.__calculated_cells.get(key, 0) - (1 if key != i else 0)
                self.__calculated_cells[key] = key_value
                if key_value == 0:
                    delete_calculated_cells.add(key)

        for i in (delete_calculated_cells - new_state_keys):
            self.__calculated_cells.pop(i)

        self.__alives = new_state_keys.__len__()

        if self.__keep_history:
            self.__history.append(new_state_keys)

        return (new_state_keys | current_state_keys)
                    
    #end def

    def applyable_state(self, new_state_cells):
        new_state_keys = set(new_state_cells.keys())
        applyable = len(new_state_keys) > 0 and new_state_keys not in self.__history
        return applyable
        pass
    #end def

    # TO DO statements of population set some properties of cells
    def populate(self, population_list, properties = None):
        for i in population_list:

            # if such index already was filled by another cell we leave old assignment
            if self.cells.get(i, None): 
                continue

            self.cells[i] = Cell(True, i, self.__dimension, self.__dimension, properties)

            self.__update_calculated_cells_by_index__(i)

        self.__alives = len(self.cells.keys())
        pass
    #end def

    def repopulate(self, population_list, properties = None):
        self.cells.clear()        
        self.__calculated_cells.clear()
        self.__history.clear()
        self.__alives = 0        
        self.populate(self, population_list, properties)
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
    
    start_time = datetime.now()

    s0 = set([9,2,5,6,7,8])
    s1 = set([5,2,6,1,7,3])

    print(s0-s1, s1-s0, s0|s1)

    print('Init life at', start_time)

    field_dimension = 10

    field = SquareField(field_dimension)
    print('dimension: ' , field.get_dimension())
    field.print(True) 
    print('populate field')

    # R - pentamino for dimension 10
    #[34,44,45,53,54]
    start_population_list = field.calc_figure_indexes(Figures.pentamino, field_dimension/2-1, field_dimension/2-1) 
    # R - glider for dimension 10
    #[1,12,20,21,22]
    start_population_list = field.calc_figure_indexes(Figures.glider, 0, 0)

    #start_population_list = field.calc_figure_indexes(Figures.block, 0, 0) + field.calc_figure_indexes(Figures.block, 3, 0)

    field.populate(start_population_list)
    print("age: 0", 'alives:', field.get_alives())
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

    circleOfLife = True

    while circleOfLife:
        new_state = field.calc_state()
        circleOfLife = field.applyable_state(new_state)
        if circleOfLife:
            field.apply_state(new_state)
            print('age: ', field.get_history_count(), 'alives:', field.get_alives())
            field.print()
       
        pass

    stop_time = datetime.now()
    print('Finished at ', stop_time)
    print('----------', (stop_time-start_time))
