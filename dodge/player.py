from helpers import *

class Player() :
    def __init__(self) :
        self.px = (WIDTH - PLAYER_SIZE) / 2
        self.py = (HEIGHT - PLAYER_SIZE) / 2
        self.pre_pos = [self.px, self.py]
        self.pos = [self.px, self.py] # player 초기 위치는 화면 가운데로 설정
        self.pre_distance = 0
        self.distance = [0, 0, 0, 0, 0] # 가장 가까운 장애물과의 거리, x_speed, y_speed, 적과의 방향, 벽이랑 가까워지는지 멀어지는지
        self.score = 0
        self.dead = False
        
    def get_inputs(self) : # 지금 껏 계산된 player input 을 반환
        # print(self.distance)
        return self.distance # Input Layer 입력값
    
    def limit_x(self, px) : # x 좌표가 유효한 값인지 검사
        if (px <= 30) :
            px = 30
        elif (px >= WIDTH - PLAYER_SIZE - 30) :
            px = WIDTH - PLAYER_SIZE - 30
        return px
        
    def limit_y(self, py) : # y 좌표가 유효한 값인지 검사
        if (py >= HEIGHT - PLAYER_SIZE - 30) :
            py = HEIGHT - PLAYER_SIZE - 30
        elif (py <= 30) :
            py = 30
        return py
    
    def move_up(self) : # 방향키 위 동작
        self.py -= MOVE_SPEED
        self.py = self.limit_y(self.py)
        self.pos = [self.px, self.py]
    
    def move_down(self) : # 방향키 아래 동작
        self.py += MOVE_SPEED
        self.py = self.limit_y(self.py)
        self.pos = [self.px, self.py]
    
    def move_right(self) : # 방향키 오른쪽 동작
        self.px += MOVE_SPEED
        self.px = self.limit_x(self.px)
        self.pos = [self.px, self.py]
    
    def move_left(self) : # 방향키 왼쪽 동작
        self.px -= MOVE_SPEED
        self.px = self.limit_x(self.px)
        self.pos = [self.px, self.py]
