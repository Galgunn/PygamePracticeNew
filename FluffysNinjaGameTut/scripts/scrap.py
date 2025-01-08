
class main:
    def __init__(self):
        neighbor = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        print(tuple(sorted([(1, 0), (0, -1), (-1, 0), (0, 1)])))
        print(tuple(sorted([(-1, 0), (1, 0), (0, -1), (0, 1)])))
        a_set = set()

        for x in neighbor:
            a_set.add(x)

        print(a_set)
    
main()