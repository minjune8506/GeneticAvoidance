from helpers import *
import pygame

# Key 입력을 받아서 Player를 움직이는 부분은 추후 신경망 출력값으로 결정해야 하기 때문에 수정 대상
class Player() :
    def __init__(self) :
        self.px = WIDTH / 2 - PLAYER_SIZE / 2
        self.py = HEIGHT / 2 - PLAYER_SIZE / 2
        self.pos = [self.px, self.py] # player 초기 위치는 화면 가운데로 설정
        self.inputs = [0, 0] # 가장 가까운 장애물의 이동방향
        
    def limit_x(self, px) : # x 좌표가 유효한 값인지 검사
        if (px <= 0) :
            px = 0
        elif (px >= WIDTH - PLAYER_SIZE) :
            px = WIDTH - PLAYER_SIZE
        return px
        
    def limit_y(self, py) : # y 좌표가 유효한 값인지 검사
        if (py >= HEIGHT - PLAYER_SIZE) :
            py = HEIGHT - PLAYER_SIZE
        elif (py <= 0) :
            py = 0
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
    