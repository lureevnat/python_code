def lex_dominate(obj1, obj2):

    a_dom_b = 0;
    b_dom_a = 0;


    sz = obj1.shape[2];
    for i in range( 1,sz ):
        if obj1(i) > obj2(i):
            b_dom_a = 1;
        elif(obj1(i) < obj2(i)):
            a_dom_b = 1;

    if(a_dom_b==0 and b_dom_a==0):
        d = 2;
    elif(a_dom_b==1 and b_dom_a==1):
       d = 2;
    else:
        if a_dom_b==1:
            d = 1;
        else:
            d = 3;
    return [d]
