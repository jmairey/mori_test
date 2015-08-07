


def gen_all_expression_strings(tag,depth,left, right, s, a):


    if False:
        leftstr = ' push '
        rightstr = ' pop-erate '
    else:
        leftstr = '('
        rightstr = ')'


    print "gen: tag= ",tag,"depth=",depth," left=",left," right=",right," s=",s

    if left == 0 and right == 0:
        a.append(s)
        print "."

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


if False:
    print "\nn = 1"
    a = []
    gen_all_expression_strings('root',0,1,0, "",a)
    print "---"
    i = 1
    for e in a:
        print i,": ",e
        i+=1

    print "\nn = 2"
    a = []
    gen_all_expression_strings('root',0,2,0, "",a)
    print "---"
    i = 1
    for e in a:
        print i,": ",e
        i+=1

print "\nn = 3"
a = []
gen_all_expression_strings('root',0,3,0, "",a)
print "---"
i = 1
for e in a:
    print i,": ",e
    i+=1
