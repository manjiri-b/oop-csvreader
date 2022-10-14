"""
Add LabeledList and Table classes
"""

#LabeledList Class

class LabeledList():

    #data = values, index = key

    def __init__(self, data=None, index=None):

        self.values = data
        self.index = index

        #Note that if index is None then the labels should be from 0 to the length of the data - 1
        if index == None:
            self.index = [x for x in range(len(data))]

    def __str__(self):

        #Getting max width for formatting (dynamic width)
        max_width = max([len(str(x)) for x in self.index])

        string_output = ""
        
        for i in range(len(self.index)):
            string_output += format(self.index[i],">"+str(max_width)) + " " + str(self.values[i]) + "\n"

        return string_output.strip("\n") #Don't want the last line

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key_list):

        #1
        if isinstance(key_list, LabeledList):
            values = key_list.values
            
            #Need to return new LABELLED LISTTTT
            new_data = []
            new_index = []

            for key in values:
                #Find key in data
                for i in range(len(self.index)):
                    if self.index[i] == key:
                        new_index.append(self.index[i])
                        new_data.append(self.values[i])

            return LabeledList(new_data, new_index)

        #3
        elif isinstance(key_list, list) and all(isinstance(key, bool) for key in key_list):
            new_data = []
            new_index = []
            
            for i in range(len(key_list)):
                if key_list[i] == True:
                    new_index.append(self.index[i])
                    new_data.append(self.values[i])

            return LabeledList(new_data, new_index)
                    

        #2
        elif isinstance(key_list, list):
            
            #Need to return new LABELLED LISTTTT
            new_data = []
            new_index = []

            for key in key_list:
                #Find key in index
                for i in range(len(self.index)):
                    if self.index[i] == key:
                        new_index.append(self.index[i])
                        new_data.append(self.values[i])

            return LabeledList(new_data, new_index)


        #4   
        elif type(key_list) == str or type(key_list) == int:

            #4a
            if self.index.count(key_list) == 1:    
                return self.values[self.index.index(key_list)]

            #4b
            elif self.index.count(key_list) > 1:
                new_index = [key_list]*self.index.count(key_list)
                new_data = []

                for i in range(len(self.index)):
                    if self.index[i] == key_list:
                        new_data.append(self.values[i])

                return LabeledList(new_data, new_index) 

    #Equals
    def __eq__(self, scalar):

        #Comparison list would be the new data of the returned Labeled List
        comparison_list = [False if value == None else value == scalar for value in self.values]

        return LabeledList(comparison_list, self.index)
        
    

    #Not equal
    def __ne__(self, scalar):
        
        comparison_list = [False if value == None else value != scalar for value in self.values]

        return LabeledList(comparison_list, self.index)

    #Greater than
    def __gt__(self, scalar):

        comparison_list = [False if value == None else value > scalar for value in self.values]

        return LabeledList(comparison_list, self.index)
    
    #Less than
    def __lt__(self, scalar):

        comparison_list = [False if value == None else value < scalar for value in self.values]

        return LabeledList(comparison_list, self.index)

    #Map Function
    def map(self, f):
        return LabeledList([f(value) for value in self.values], self.index)

#Table Class
class Table():

    def __init__(self, data, index=None, columns=None):

        self.values = data
        self.index = index
        self.columns = columns

        if index == None:
            self.index = [x for x in range(len(data))]

        if columns == None:
            self.columns = [x for x in range(len(data[0]))]
    
    def __str__(self):

        string_output = ""

        #Getting max width for formatting row labels
        max_width_row = max([len(str(x)) for x in self.index]) + 2

        #Width of column depends on width of longest element in it /column name
        max_column_widths = []
        
        for r in range (len(self.index)):
            if len(self.values[r]) > 0:
                max_column_widths.append(max([len(str(x)) for x in self.values[r]]))

        max_column_width = max(max_column_widths)

        max_column_name = max([len(str(x)) for x in self.columns])

        if max_column_name > max_column_width:
            max_column_width = max_column_name + 1
        else:
            max_column_width += 1
        
        #Adding space to header
        string_output += format(" ", str(max_width_row))

        #Adding the header to the string
        for column_name in self.columns:
            string_output += format(column_name, ">"+str(max_column_width))

        string_output += "\n"
        
        #Adding each row
        for row in range(len(self.index)):
            string_output += format(self.index[row], '>' + str(max_width_row))

            for column_index in range(len(self.columns)):
                string_output += format(self.values[row][column_index], '>' + str(max_column_width))

            string_output += "\n"
        
        return string_output.strip("\n")
         
    def __repr__(self):
        return self.__str__()

    #Get Item Function
    def __getitem__(self, col_list):

        #1
        if isinstance(col_list, LabeledList):
            
            columns_included = col_list.values

            return self.__getitem__(columns_included)

        #3
        elif isinstance(col_list, list) and all(isinstance(key, bool) for key in col_list):

            new_data = []
            new_rows = []
            for i in range(len(col_list)):
                if col_list[i] == True:
                    new_data.append(self.values[i])
                    new_rows.append(self.index[i])

            return Table(new_data, new_rows, self.columns)

        #2
        elif isinstance(col_list, list):

            new_data = []

            #make a new col_list too
            new_col_list = []

            for key in col_list:

                #Counting number of times key appears in self.columns
                count = self.columns.count(key)

                new_col_list += [key]*count

            for row in self.values:

                row_data = []
                
                for key in col_list:

                    for c_index in range(len(self.columns)):

                        if self.columns[c_index] == key:
                            row_data.append(row[c_index])

                new_data.append(row_data)

            return Table(new_data, self.index, new_col_list)
                
                    
        #4   
        elif type(col_list) == str or type(col_list) == int:

            #4a
            if self.columns.count(col_list) == 1:
                col_data = []
                #
                index_list = []
                for row in self.values:
                    col_data.append(row[self.columns.index(col_list)])
                    #
                    index_list.append(self.columns.index(col_list))
                
                return LabeledList(col_data, self.index)

            
            #4b
            elif self.columns.count(col_list) > 1:
                new_columns = [col_list]

                return self.__getitem__([col_list])
            

    def head(self, n):
        #Showing first n rows (all columns kept)

        return Table(self.values[:n], self.index[:n], self.columns)

    def tail(self, n):
        #Showing last n rows (all columns kept) using negative indexing
        return Table(self.values[-n:], self.index[-n:], self.columns)


    def shape(self):
        return (len(self.values), len(self.values[0]))

def read_csv(fn):

    import csv

    with open(fn) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        
        #assume that the first row is the header (it can be treated as column names)
        column_names = csv_reader.__next__()
        
        #Getting list of tuples which has level as detail and the Occupation title contains either data or computer
        data_by_row = [x for x in csv_reader.__iter__() if len(x) > 0]
        
        #Converting numeric values to floats
        new_data = []
        
        for row in data_by_row:
            
            row_data = []
            
            for data in row:
                
                try:
                    row_data.append(float(data))
                except ValueError:
                    row_data.append(data)

            new_data.append(row_data)

        return Table(new_data, columns = column_names)

'''
TESTING
d = [[1000,10,100,1,1.0],[200,2,2.0,2000,20],[3,300,3000,3.0,30],[40,4000,4.0,400,4],[7,8,6,3,41]]
t = Table(d, ['foo', 'bar', 'bazzy', 'qux', 'quxx'], ['a', 'b', 'c', 'd', 'e'])
print(t)
print()
print(t[LabeledList(['a', 'b','b'])])
print()
print(t[['a', 'b','c','c']])


t = Table([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'a'])
print(t['b'])

t = Table([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'a'])
print(t[['a']])



t = Table([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'a'])
print(t)
print(t[['a', 'b','a']]) #Should give both a's first #currently only gives first one 'a'


t = Table([[15, 17, 19], [14, 16, 18]], columns=['x', 'x', 'z'])
print(t)
print(t[['x', 'x', 'z']])

t = Table([[1, 2, 3], [4, 5, 6], [7, 8 , 9]], columns=['x', 'y', 'z'])
print(t)
print(t[[True, False, True]])
'''

#t = Table([[1, 2], [3, 4], [5, 6], [7, 8]], columns=['x', 'y'])
'''
t = read_csv('fruitarians.csv')
print(t)
'''
