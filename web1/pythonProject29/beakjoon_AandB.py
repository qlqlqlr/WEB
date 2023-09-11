# A와 B

S = list(input())
T = list(input())


def ch(S, T):

    while len(S) != len(T):
        n = len(T)
        if T[n-1] == 'A':
            T = T[:n - 1]

        elif T[n-1] == 'B':
            T = T[:n - 1]
            T = T[::-1]

        else:
            if S == T:
                print(1)
                exit()
            else:
                print(0)
                exit()
        if len(S) == len(T):
            if S != T:
                print(0)
                exit()
    print(1)

ch(S, T)