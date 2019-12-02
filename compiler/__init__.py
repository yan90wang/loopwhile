from compiler.loopwhile_compiler import *

'''
         Loop/While compiler usage: 
         -Put Loop/While programs as text files into folder input
         -if input parameters exist, specify them as a list, for example : parameters = [1, 2, 3]
         -run one specific program by changing: txt_file = 'yourprogram.txt' 
         -run main 
'''
if __name__ == '__main__':
    compiler = LoopWhileCompiler()
    parameters = [1, 2]
    txt_file = 'addition.txt'
    compiler.compile('input/' + txt_file, parameters)
