import os
import sys




def this_file():
    current_path = os.getcwd()
    python_path = '/'.join(sys.argv[0].split('/')[:-1])
    return os.path.join(current_path, python_path).rstrip('/')

def get_save_votids():
    path_data = f'tmp/html'
    filenames = os.listdir(path_data)
    votids = [filename.split('.')[0] for filename in filenames if filename.split('.')[0]]
    votids.sort()
    return votids

def get_gen_votids():
    path_data = f'tmp/visualizaciones'
    filenames = os.listdir(path_data)
    names = [filename.split('.')[0] for filename in filenames if filename.split('.')[0]]
    names = filter(lambda name: name.split('_')[1] == "partidos", names)
    votids = [name.split('_')[0] for name in names]
    votids.sort()
    return votids

def create_file(path, abspath=False):
    dirs = path.strip('/').split('/')[:-1]
    for i in range(len(dirs)):
        semipath = '/'.join(dirs[:i+1])
        if abspath:
            semipath = '/'+semipath
        if not os.path.exists(semipath):
            os.mkdir(semipath)
    open(path, 'a').close()

def create_dirs(path, abspath=False):
    dirs = path.strip('/').split('/')
    for i in range(len(dirs)):
        semipath = '/'.join(dirs[:i+1])
        if abspath:
            semipath = '/'+semipath
        if not os.path.exists(semipath):
            os.mkdir(semipath)