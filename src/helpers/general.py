'''
	Some general helper functions 
'''

def print_full(df):
    '''Prints dataframe, displays all data
    '''
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


def create_dir(directory):
    '''
    Creates a directory if it does not already exist.
    
    '''

    if not os.path.exists(directory):
        os.makedirs(directory)

def save_obj(obj, name):
    '''
    Pickle an object to file
    Saves picked object in the ./pickle folder
    
    '''
    create_dir('pickle')
    file_handler = open('./pickle/' + name + '.obj', 'wb')
    pickle.dump(obj, file_handler)

def read_obj(name):
    '''
    Retrieves object from pickled file
    Returns object

    '''
    file_handler = open('./pickle/' + name + '.obj', 'rb')
    obj = pickle.load(file_handler)

    return obj
 