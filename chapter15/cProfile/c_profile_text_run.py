import random


def randomlist(n):
    lists = []
    l = [random.random() for i in range(n)]
    l.sort()
    for v in l:
        lists.append(v)
    return lists




if __name__ == "__main__":
    randomlist(20)