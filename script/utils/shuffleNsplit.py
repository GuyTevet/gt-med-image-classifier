from random import shuffle

"""
def shuffleNsplit(a,b,c,splitIndex):
        [a,b,c] = shuffleLists(a,b,c)
        return splitLists(a,b,c,splitIndex)

def splitLists(a,b,c,splitIndex):
        
        a0 = []
        a1 = []

        b0 = []
        b1 = []

        c0 = []
        c1 = []

        assert splitIndex < len(a)

        for i in range(len(a)):
                if(i < splitIndex):
                        a0.append(a[i])
                        b0.append(b[i])
                        c0.append(c[i])
                else:
                        a1.append(a[i])
                        b1.append(b[i])
                        c1.append(c[i])

        return [[a0,b0,c0],[a1,b1,c1]]
""" 


def shuffleLists(a,b,c,d):
        new_a = []
        new_b = []
        new_c = []
        new_d = []
       
        assert len(a) == len(b) and len(a) == len(c) and len(a) == len(d)

        index_shuf = range(len(a))
        shuffle(index_shuf)
        for i in index_shuf:
                new_a.append(a[i])
                new_b.append(b[i])
                new_c.append(c[i])
                new_d.append(d[i])

        return [new_a,new_b,new_c,new_d]
