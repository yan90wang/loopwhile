from compiler.loopwhile_compiler import *

'''
         Loop/While compiler usage: 
         -Put Loop/While programs as text files into folder input
         -if input parameters exist, specify them as a list, for example : parameters = [1, 2, 3]
         -run one specific program by changing: txt_file = 'yourprogram.txt' 
         -run main 
         
         In order to define a function use: 
                def your_function(x1, x2):
         In order to use a while loop the syntax is: 
                WHILE x1 not 0 DO
                  ...
                END
        
        Note: as defined by the LOOP/WHILE language initially all variables are set to 0, therefore a variable does not 
        need to be defined before usage 
'''
if __name__ == '__main__':
    compiler = LoopWhileCompiler()
    parameters = [3, 1]
    txt_file = 'addition.txt'
    compiler.compile('input/' + txt_file, parameters)
