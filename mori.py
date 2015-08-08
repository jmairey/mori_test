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

# evaluate a binary expression tree, rooted at 'i' and put the results, numerical and string, back in the tree
def evaluate_expression_tree (expressionTree,i):

    if expressionTree[i][1] == 'leaf':
        result = expressionTree[i][0]
        result_str = str(result)
    elif expressionTree[i][1] == 'operator':
        left = evaluate_expression_tree(expressionTree,expressionTree[i][2])[0]          # XXX recursion
        right = evaluate_expression_tree(expressionTree,expressionTree[i][3])[0]          # XXX recursion
        left_str = evaluate_expression_tree(expressionTree,expressionTree[i][2])[1]          # XXX recursion
        right_str = evaluate_expression_tree(expressionTree,expressionTree[i][3])[1]          # XXX recursion
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

# generate all the catalan strings of order 'left'.
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
        if left > 0:            # could have our own stack and get rid of recursion
            sl = s + leftstr
            gen_all_expression_strings('left',depth+1,left-1,right+1, sl, a)

        if True:                # could get rid of this by just iterating
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

#sample_input = '2 + 2 - 1 = 3'
sample_input = '2 * 3 - 4 * 5'

if argc == 2:
    input = sys.argv[1]
else:
    input = sample_input

eT = []              # global expression tree (array with index links)
numOperators = 0     # order of catalan number generation 

for i in range(len(input)): 
    c = input[i]
    if   (c == '+' or c == '-' or c == '*' or c == '='):
        eT.append([c,'operator',0,0,[0,'']])
        numOperators += 1
    elif (c != ' '):
        eT.append([int(c), 'leaf'])

# generate catalan string sequences and use them to populate expression tree link members to construct expression trees for evaluation
# the mapping between the two is the only tricky thing here, other than maybe the catalan string generation?

result_list = []

the_catalan_sequences = []

gen_all_expression_strings('root',0,numOperators,0, "", the_catalan_sequences)

for catalan_sequence_set in the_catalan_sequences:

    catalan_sequence = catalan_sequence_set[0];

    operand_stack = []
    operand_index = 0
    operand_stack.append(operand_index)

    operator_stack = []
    operator_index = 1
    operator_stack.append(operator_index)

    for i in range(1,len(catalan_sequence)):
        if catalan_sequence[i] == '(':

            operand_index += 2
            operator_index += 2

            if catalan_sequence[i-1]=='(':
                operand_stack.append(operand_index)

            operator_stack.append(operator_index)    

        elif catalan_sequence[i] == ')':

            if catalan_sequence[i-1] == '(':
                popped_left_operand_index = operand_stack.pop()
                popped_operator_index = operator_stack.pop()
                popped_right_operand_index = popped_operator_index+1

            else:
                popped_right_operand_index = operand_stack.pop()
                popped_left_operand_index = operand_stack.pop()
                popped_operator_index = operator_stack.pop()


            eT[popped_operator_index][2] = popped_left_operand_index
            eT[popped_operator_index][3] = popped_right_operand_index

            operand_stack.append(popped_operator_index)

        else:
            print "error"


    result = evaluate_expression_tree(eT,operand_stack[-1])  
    result_list.append(result)

result_list.sort()
for result in result_list:
        print result

