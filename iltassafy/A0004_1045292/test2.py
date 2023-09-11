import socket
import time
import math

# 닉네임을 사용자에 맞게 변경해 주세요.
NICKNAME = 'A0004_1045292'

# 일타싸피 프로그램을 로컬에서 실행할 경우 변경하지 않습니다.
HOST = '127.0.0.1'

# 일타싸피 프로그램과 통신할 때 사용하는 코드값으로 변경하지 않습니다.
PORT = 1447
CODE_SEND = 9901
CODE_REQUEST = 9902
SIGNAL_ORDER = 9908
SIGNAL_CLOSE = 9909

# 게임 환경에 대한 상수입니다.
TABLE_WIDTH = 254
TABLE_HEIGHT = 127
NUMBER_OF_BALLS = 6
HOLES = [[0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127]]

order = 0
balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]

sock = socket.socket()
print('Trying to Connect: %s:%d' % (HOST, PORT))
sock.connect((HOST, PORT))
print('Connected: %s:%d' % (HOST, PORT))

send_data = '%d/%s' % (CODE_SEND, NICKNAME)
sock.send(send_data.encode('utf-8'))
print('Ready to play!\n--------------------')

def path_find(x, y):
    # 이 함수는 수정해야 합니다.
    pass

while True:

    # Receive Data
    recv_data = (sock.recv(1024)).decode()
    print('Data Received: %s' % recv_data)

    # Read Game Data
    split_data = recv_data.split('/')
    idx = 0
    try:
        for i in range(NUMBER_OF_BALLS):
            for j in range(2):
                balls[i][j] = float(split_data[idx])
                idx += 1
    except:
        send_data = '%d/%s' % (CODE_REQUEST, NICKNAME)
        print("Received Data has been corrupted, Resend Requested.")
        continue

    # Check Signal for Player Order or Close Connection
    if balls[0][0] == SIGNAL_ORDER:
        order = int(balls[0][1])
        print('\n* You will be the %s player. *\n' % ('first' if order == 1 else 'second'))
        continue
    elif balls[0][0] == SIGNAL_CLOSE:
        break

    # Show Balls' Position
    print('====== Arrays ======')
    for i in range(NUMBER_OF_BALLS):
        print('Ball %d: %f, %f' % (i, balls[i][0], balls[i][1]))
    print('====================')

    angle = 0.0
    power = 0.0

    ##############################
    # 여기서부터 코드를 작성하세요.
    # 아래에 있는 것은 샘플로 작성된 코드이므로 자유롭게 변경할 수 있습니다.

    # 내 목적구에 대해서만
    for obj in objball:
        # 후보가 될 path들
        cand_path = []
        # 모든 홀에 대해서 (6개)
        for hole in Myholes:
            # obj이 hole에 가는 방법
            objtohole = path_find(obj, hole)
            # path_find 함수는 obj-hole 백터를 반환하며 공의 진행방향에 장애물이 있나 확인
            if not objtohole:
                print('not objtohole pass')
                continue
            # objtohole을 위해 수구의 도착 위치 계산
            objtohole_nv = objtohole / (objtohole.norm)
            # 목적구가 홀로 가려는 방향의 반대방향으로 
            # 공 크기만큼 이동한 점이 수구가 가야할 곳
            que = obj + Ball_R * -objtohole_nv
            # 수구 to que점을 가는 길 계산
            quetoobj = path_find(myball, que)
            if not quetoobj:
                print('no quetoobj pass')
                continue
            quetoobj_nv = quetoobj / (quetoobj.norm)
            # 두 백터의 각도 계산 (단위 백터끼리의 내적 cos(theta) 값임)
            # 영보다 작거나 음수면 안하고 진행
            if objtohole_nv.dot(quetoobj_nv) <= 0:
                continue
            # weights *= objtohole_nv.dot(quetoobj_nv)

            # 예측 힘의 값, objtohole 거리, quetoobj 거리에 비례하게 함

            mue = 5.5
            v1h = (55 + 2 * mue * objtohole.norm)
            v01 = (v1h + 2 * mue * quetoobj.norm) ** (1 / 2)
            inferF = quetoobj_nv * v01
            # 앞선 각도를 계산한 내적 값을 나눠주어 각도가 얇다면 더 쎄게 치도록 함
            inferF = inferF / (objtohole_nv.dot(quetoobj_nv) ** (1 / 2))
            # 완성된 패스를 등록
            # 등록할 때 각도가 두꺼운 것을 우선하도록
            # 하지만 적당히 두꺼운 각도면 수용하도록 각도를 integer화함
            cand_path.append([int(objtohole_nv.dot(quetoobj_nv) * 10), inferF.norm, inferF])
        # 모든 Hole에 대한 연산이 끝나면
        # cand_path를 정렬하여 가장 각도가 두껍고 힘이 약한 것을
        cand_path.sort(key=lambda x: (-x[0], x[1]))
        if cand_path:
            # Pathlist에 넣는다. cand_path는 한 목적구에 대한 계산임
            Pathlist.append(cand_path[0])

    # Pathlist는 모든 목적구에 대한 
    # 가장 일직선으로 만나는 것 + 다음으로 힘의 필요가 가장 작은 것을 쓰자
    Pathlist.sort(key=lambda x: (-x[0], x[1]))

    merged_data = '%f/%f/' % (angle, power)
    sock.send(merged_data.encode('utf-8'))
    print('Data Sent: %s' % merged_data)

sock.close()
print('Connection Closed.\n--------------------')
