
# 색종이 자르기

def ch(start, start2, end, end2):
    global result
    if end - start == 1:
        return 1
    else:
        for i in range(start, end- 1):
            for j in range(start2, end2 - 1):
                if arr[i][j] == arr[i][j+1] and arr[i][j] == arr[i + 1][j]:
                    continue
                else:
                    result = ch()



N = int(input())
arr = [list(map(int, input().split())) for _ in range(N)]
result = 0