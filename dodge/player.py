from helpers import *


# Key 입력을 받아서 Player를 움직이는 부분은 추후 신경망 출력값으로 결정해야 하기 때문에 수정 대상


class Player():
    def __init__(self):
        self.px = WIDTH / 2 - PLAYER_SIZE / 2
        self.py = HEIGHT / 2 - PLAYER_SIZE / 2
        self.pos = [self.px, self.py]  # player 초기 위치는 화면 가운데로 설정
        self.isMove_up = False
        self.isMove_down = False
        self.isMove_right = False
        self.isMove_left = False

        self.fitness = 0

    

    def limit_x(self, px):  # x 좌표가 유효한 값인지 검사
        if (px <= 0):
            px = 0
        elif (px >= WIDTH - PLAYER_SIZE):
            px = WIDTH - PLAYER_SIZE
        return px

    def limit_y(self, py):  # y 좌표가 유효한 값인지 검사
        if (py >= HEIGHT - PLAYER_SIZE):
            py = HEIGHT - PLAYER_SIZE
        elif (py <= 0):
            py = 0
        return py

    def update(self):
        if self.collision_check():
            # The font will be printed in "red"
            label2 = self.endFont.render(final_score, 1, RED)
            label3 = self.endFont.render(msg, 1, (0, 255, 0))
            # It updates text to the specific part(position) of the screen
            self.screen.blit(label2, (250, 250))
            self.screen.blit(label3, (250, 300))
            game_over = True

        if self.isMove_down:
            self.move_down()
        elif self.isMove_left:
            self.move_left()
        elif self.isMove_right:
            self.move_right()
        elif self.isMove_up:
            self.move_up()

    def move_up(self):  # 방향키 위 동작
        self.py -= MOVE_SPEED
        self.py = self.limit_y(self.py)
        self.pos = [self.px, self.py]

    def move_down(self):  # 방향키 아래 동작
        self.py += MOVE_SPEED
        self.py = self.limit_y(self.py)
        self.pos = [self.px, self.py]

    def move_right(self):  # 방향키 오른쪽 동작
        self.px += MOVE_SPEED
        self.px = self.limit_x(self.px)
        self.pos = [self.px, self.py]

    def move_left(self):  # 방향키 왼쪽 동작
        self.px -= MOVE_SPEED
        self.px = self.limit_x(self.px)
        self.pos = [self.px, self.py]
