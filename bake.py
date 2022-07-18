
import os
import subprocess

# General compile options

platform = 'win'

definitions = []
inc_folders = ['ryu']


# Compiler-specific options

clang_dbg_flags    = ['-g', '-gcodeview']
clang_common_flags = ['-c', '-nodefaultlibs', '-mfma']

#----------------------------------------------------------------------------#
# Map lists to lists of options
inc_flags = []
def_flags = []
def compile(root, cmap):
    global inc_flags
    global def_flags
    inc_flags = list(map(lambda p: '-I '+ p, inc_folders))
    def_flags = list(map(lambda d: '-D' + d, definitions))
    for path, subdirs, files in os.walk(root):
        for file_name in files:
            file_path = os.path.join(path, file_name)
            short_name, ext = os.path.splitext(file_path)
            if ext in cmap.keys():
                func = cmap[ext]
                func(file_path)

def get_bin_path(file_path):
    rel_path = os.path.normpath(file_path).split(os.path.sep)[1:]
    name, ext = os.path.splitext(os.path.sep.join(rel_path))
    bin_path = os.path.join('bin', name+'.obj')
    os.makedirs(os.path.dirname(bin_path), exist_ok=True)
    return bin_path

def clang_compile(file_name):
    bin_path = get_bin_path(file_name)
    dbg_flags = clang_dbg_flags
    cmn_flags = clang_common_flags
    flags     = dbg_flags + cmn_flags + inc_flags + def_flags
    command   = ' '.join(["clang", file_name, '-o', bin_path] + flags)
    subprocess.run(command.split(' '))
    print(file_name, '=>', bin_path)

def nasm_compile(file_name):
    bin_path = get_bin_path(file_name)
    subprocess.run(['nasm', file_name, '-f', 'win64', '-o', bin_path])
    print(file_name, '=>', bin_path)

#-----------------------------------------------------------------------------#

# Compile the object files
compile_map = {}
compile_map['.c']   = clang_compile
compile(os.path.normpath('ryu'), compile_map)

# Make an archive of all object files
obj_paths = []
for dir, _, f in os.walk('bin'):
    if len(f) != 0:
        obj_paths.append(os.path.join(dir, '*.obj'))
subprocess.run(['llvm-ar', 'rc', 'ryu.lib'] + obj_paths)
