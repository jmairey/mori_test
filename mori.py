#!/usr/bin/python
#
# compute all possible expression trees, with results for bruce @ mori. 
# sort list by result and print.
#
#

import sys, getopt

an_option      = 1

# option processing boilerplate
try:
   opts, args = getopt.getopt(sys.argv[1:],"ho:",["options="])
except getopt.GetoptError:
   print 'mori.py -o <options> '
   sys.exit(2)

for opt, arg in opts:
    if opt in ( "-h", "--help"):
        print 'mori.py -o <options> '
        sys.exit()
    elif opt in ("-o", "--options"):
        an_option = int(arg)


if False:   # some sample data used in development; scaffolding

    expressionTreeA = [ 
        [2,  'leaf'],                 # 0
        ['+','operator',0,2,[0,'']],  # 1
        [2,  'leaf'],                 # 2                 =
        ['-','operator',1,4,[0,'']],  # 3             -      3     
        [1,  'leaf'],                 # 4         +     1
        ['=','operator',3,6,[0,'']],  # 5       2   2
        [3,  'leaf']                  # 6  (((2+2)-1)=3) (final result is 1)    ()op()op)()op   #1

                                      #          +push +op -push -op =push =op   #1
    ]

    expressionTreeB = [ 
        [2,  'leaf'],                 # 0
        ['+','operator',0,3,[0,'']],  # 1         +
        [2,  'leaf'],                 # 2      2       -           
        ['-','operator',2,5,[0,'']],  # 3           2     =
        [1,  'leaf'],                 # 4               1   3
        ['=','operator',4,6,[0,'']],  # 5
        [3,  'leaf']                  # 6  (2+(2-(1=3))) (final result is 4)   ((()op)op)op    #5 

                                      #           +push -push =push =op -op +op  #5
    ]

    expressionTreeC = [ 
        [2,  'leaf'],                 # 0
        ['+','operator',0,3,[0,'']],  # 1                            
        [2,  'leaf'],                 # 2  ((2+(2-1))=3) (final result is 1)   (()op)op()op   #3
        ['-','operator',2,4,[0,'']],  # 3                =          
        [1,  'leaf'],                 # 4         +         3
        ['=','operator',1,6,[0,'']],  # 5       2    -
        [3,  'leaf']                  # 6          2   1

                                      #           +push -push -op +op =push =op    #3
    ]

    expressionTreeD = [ 
        [2,  'leaf'],                 # 0
        ['+','operator',0,5,[0,'']],  # 1         +
        [2,  'leaf'],                 # 2      2         =     
        ['-','operator',2,4,[0,'']],  # 3             -    3
        [1,  'leaf'],                 # 4           2   1   
        ['=','operator',3,6,[0,'']],  # 5
        [3,  'leaf']                  # 6  (2+((2-1)=3)) (final result is 2)   (()-()=)+

                                      #           +push -push -op =push =op +op    #4
    ]

    expressionTreeE = [ 
        [2,  'leaf'],                 # 0
        ['+','operator',0,2,[0,'']],  # 1                        
        [2,  'leaf'],                 # 2  ((2+2)-(1=3)) (final result is 4)    ()+((
        ['-','operator',1,5,[0,'']],  # 3                        
        [1,  'leaf'],                 # 4           -             
        ['=','operator',4,6,[0,'']],  # 5      +          =
        [3,  'leaf']                  # 6    2   2     1     3

                                      #           +push +op -push =push =op -op     #2
    ]

def evaluate_expression_tree (expressionTree,i):

#    print "evaluate expression tree called with ", i

    if expressionTree[i][1] == 'leaf':
#        print "evaluate_expression_tree: 'leaf'"
        result = expressionTree[i][0]
        result_str = str(result)
    elif expressionTree[i][1] == 'operator':
#        print "evaluate_expression_tree: 'operator'"
        left = evaluate_expression_tree(expressionTree,expressionTree[i][2])[0]
        right = evaluate_expression_tree(expressionTree,expressionTree[i][3])[0]
        left_str = evaluate_expression_tree(expressionTree,expressionTree[i][2])[1]
        right_str = evaluate_expression_tree(expressionTree,expressionTree[i][3])[1]
        if expressionTree[i][0] == '+':
            result = left + right
            result_str = '(' + left_str + ' + ' + right_str + ')'
        elif expressionTree[i][0] == '-':
            result = left - right
            result_str = '(' + left_str + ' - ' + right_str + ')'
        elif expressionTree[i][0] == '*':
            result = left * right
            result_str = '(' + left_str + ' * ' + right_str + ')'
        elif expressionTree[i][0] == '=':
            result_str = '(' + left_str + ' = ' + right_str + ')'
            result = left - right
            if result == 0:
                result = 1
            else:
                result = 0
        else:
            print "evaluate_expression_tree: bad operator"
        expressionTree[i][4] = [ result, result_str]
    else:
        print "evaluate_expression_tree: 'unknown'"
        result = -999 # XXX
        result_str = str(result)

    return [result, result_str]
# end evaluate_expression_tree

def gen_all_expression_strings(tag,depth,left, right, s, a):

    if False:
        leftstr = ' push '
        rightstr = ' pop-erate '
    else:
        leftstr = '('
        rightstr = ')'

#    print "gen: tag= ",tag,"depth=",depth," left=",left," right=",right," s=",s

    if left == 0 and right == 0:
        a.append([s,'a comment string'])
#        print "."
    else:
        if left > 0:
            sl = s + leftstr
            gen_all_expression_strings('left',depth+1,left-1,right+1, sl, a)

        if True:
            if right > 0:
                sr = s + rightstr
                gen_all_expression_strings('right',depth+1,left,right-1, sr, a)
        else:
            while right > 0:
                right -= 1;

    return
# end

print "\nmori take home test"

argc = len(sys.argv)
#print "argc = ", argc

#sample_input = '2 + 2 - 1 = 3'
sample_input = '2 * 3 - 4 * 5'

if argc == 2:
    input = sys.argv[1]
else:
    input = sample_input

eT = []

numOperators = 0

for i in range(len(input)): 
    c = input[i]
    if   (c == '+' or c == '-' or c == '*' or c == '='):
        eT.append([c,'operator',0,0,[0,'']])
        numOperators += 1
    elif (c != ' '):
        eT.append([int(c), 'leaf'])

#for item in eT:
#    print item
    
# 

if False: # scaffolding
    result = evaluate_expression_tree(expressionTreeA,5)  
    print "evaluate_expression_tree result when passed tree A and root at index 5 is", result
    assert (result[0] == 1), "error in test A"
    result_list = [result]

    result = evaluate_expression_tree(expressionTreeB,1)
    print "evaluate_expression_tree result when passed tree B and root at index 1 is", result
    assert (result[0] == 4), "error in test B"
    result_list.append(result)

    result = evaluate_expression_tree(expressionTreeC,5)
    print "evaluate_expression_tree result when passed tree C and root at index 5 is", result
    assert (result[0] == 1), "error in test C"
    result_list.append(result)

    result = evaluate_expression_tree(expressionTreeD,1)
    print "evaluate_expression_tree result when passed tree D and root at index 1 is", result
    assert (result[0] == 2), "error in test D"
    result_list.append(result)

    result = evaluate_expression_tree(expressionTreeE,3)
    print "evaluate_expression_tree result when passed tree E and root at index 3 is", result
    assert (result[0] == 4), "error in test E"
    result_list.append(result)
    result_list.sort()

    for result in result_list:
        print result

else:

    # generate catalan sequences and use them to populate expression tree link members to construct expression trees for evaluation

    result_list = []

    if False:
        the_catalan_sequences = [
           ['()()()'," catalan#1 want  0,2  then 1,4  then 3,6, root 5 "]
          ,['((()))'," catalan#5 want  0,3  then 2,5  then 4,6, root 1 "]
          ,['(())()'," catalan#3 want  0,3  then 2,4  then 1,6, root 5 "]
          ,['(()())'," catalan#4 want  0,5  then 2,4  then 3,6, root 1 "]
          ,['()(())'," catalan#2 want  0,2  then 1,5  then 4,6, root 3 "]
        ]
    else:
        the_catalan_sequences = []
        gen_all_expression_strings('root',0,numOperators,0, "", the_catalan_sequences)

    for catalan_sequence_set in the_catalan_sequences:

        catalan_sequence = catalan_sequence_set[0];
#        print "\ncatalan sequence: ",catalan_sequence_set[0],catalan_sequence_set[1],"\n"

        operand_stack = []
        operand_index = 0
        operand_stack.append(operand_index)

        operator_stack = []
        operator_index = 1
        operator_stack.append(operator_index)

#        print 0,": ",catalan_sequence[0],"operand_stack ", operand_stack, "operator_stack ", operator_stack

        for i in range(1,len(catalan_sequence)):
#            print "\n",i,": ",catalan_sequence[i],"operand_stack ", operand_stack, "operator_stack ", operator_stack
            if catalan_sequence[i] == '(':

                operand_index += 2
                operator_index += 2

                if catalan_sequence[i-1]=='(':
                    operand_stack.append(operand_index)
#                    print "----","catalan_sequence[i-1]=",catalan_sequence[i-1]
#                else:
#                    print "????","catalan_sequence[i-1]=",catalan_sequence[i-1]

                operator_stack.append(operator_index)    

            elif catalan_sequence[i] == ')':

                if catalan_sequence[i-1] == '(':
#                    print "inner expression"
                    popped_left_operand_index = operand_stack.pop()
                    popped_operator_index = operator_stack.pop()
                    popped_right_operand_index = popped_operator_index+1

                else:
#                    print "outer expression"
                    popped_right_operand_index = operand_stack.pop()
                    popped_left_operand_index = operand_stack.pop()
                    popped_operator_index = operator_stack.pop()

#                print " popped_left_operand_index=",popped_left_operand_index, "popped_operator_index=",popped_operator_index

                eT[popped_operator_index][2] = popped_left_operand_index
                eT[popped_operator_index][3] = popped_right_operand_index

                operand_stack.append(popped_operator_index)

            else:
                print "error"

#        print "--"
#        print "done","operand_stack ", operand_stack, "operator_stack ", operator_stack
#        i = 0
#        for item in eT:
#            print i, item
#            i+=1

        if True:
            result = evaluate_expression_tree(eT,operand_stack[-1])  
#            print "evaluate_expression_tree result when passed tree A and root at index 5 is", result
#            print "evaluate_expression_tree result when passed eT and root at index ",operand_stack[-1]," is", result
            result_list.append(result)

#        print "--------------------------------------------------------------"
    result_list.sort()
    for result in result_list:
        print result

