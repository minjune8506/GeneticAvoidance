from xml.sax.xmlreader import InputSource

from numpy import true_divide
import outcome
from helpers import *
from enemy import Enemy
from player import Player
import pygame
import sys
from math import *

class Game() :
    def __init__(self) :
        pygame.init()  # To initialize pygame
        # set screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # We have a screen of WIDTH 800 and HEIGHT 600
        self.player = Player() # Player 객체 생성
        self.score = 0 # 점수
        self.clock = pygame.time.Clock() # It defines a clock
        self.myFont = pygame.font.SysFont("monospace", 35)  # Defining the font in pygame (Monospace is font and 35 is in pixels)
        self.endFont = pygame.font.SysFont("comicsansms", 40, True, False)
        self.enemylist = [] # 적들을 담는 리스트
        self.enemyMax = 10 # 적들의 최대 개수    
    
    def get_inputs(self) : # 지금 껏 계산된 player input 을 반환
        return self.player.inputs

    def set_level(self) :
        if self.score < 20:
            self.enemyMax = 30 # level 1
        elif self.score < 50:
            self.enemyMax = 50 # level 2
        elif self.score < 100:
            self.enemyMax = 100 # level 3
        else:
            self.enemyMax = 200 # level 4
    
    def create_enemies(self) :
        while len(self.enemylist) < self.enemyMax : # enemyMax 만큼 enemy 객체 생성
            self.enemylist.append(Enemy()) # 리스트에 추가
    
    def draw_enemies(self) :
        for enemy in self.enemylist : # enemylist에 있는 enemy객체들을 화면에 그린다.
            pygame.draw.rect(self.screen, BLUE, (enemy.px, enemy.py, ENEMY_SIZE, ENEMY_SIZE))
        
    def update_enemy_positions(self) : # enemy의 위치 update
        enemy_distance_list = []
        for idx, enemy in enumerate(self.enemylist) :
            x_move = False
            y_move = False
            # print("(%d, %d)" %(enemy.px, enemy.py))
            if (0 <= enemy.px <= WIDTH) : # enemy가 화면 안에 있는지 검사
                enemy.px += enemy.x_speed
                x_move = True
            if (0 <= enemy.py <= HEIGHT) :
                enemy.py += enemy.y_speed
                y_move = True

            if not x_move or not y_move : # x, y좌표중 하나라도 화면 밖에 있다면
                self.enemylist.pop(idx) # enemy 제거
                self.score += 1 # score 점수 증가

            elif self.out_of_range(enemy) : # 유효한 애들만
                x_y_distance = self.cal_real_distance(enemy)
                distance = sqrt(pow(x_y_distance[1], 2) + pow(x_y_distance[0], 2))
                enemy_distance_list.append([distance, enemy.x_speed, enemy.y_speed]) # distance, x_speed, y_speed
        
        enemy_distance_list.sort(key = lambda x:x[0]) # distance 가 가장 낮은 애를 정렬
        print(enemy_distance_list[0][0])
        self.player.inputs = [enemy_distance_list[0][1], enemy_distance_list[0][2]]
    
    def cal_real_distance(self, enemy) :    
        x_y_distance = [0, 0] # 아래 조건에 걸리지 않는 경우는 x 혹은 y 가 겹쳐있는 상태를 의미하기에 0으로 설정이 되어야 한다.
        x = self.player.pos[0]
        y = self.player.pos[1]

        if enemy.px + ENEMY_SIZE < x : # 왼쪽에 있으면
            x_y_distance[0] = x - (enemy.px + ENEMY_SIZE)
        elif x + PLAYER_SIZE < enemy.px : # 오른쪽에 있으면
            x_y_distance[0] = enemy.px - (x + PLAYER_SIZE)

        if enemy.py + ENEMY_SIZE < y : # 위에 있으면
            x_y_distance[1] = y - (enemy.py + ENEMY_SIZE)
        elif y + PLAYER_SIZE < enemy.py : # 아래에 있으면
            x_y_distance[1] = enemy.py - (y + PLAYER_SIZE)        

        return x_y_distance 
    
    def out_of_range(self, enemy) :
        if ((enemy.py < 0 or enemy.py > HEIGHT) or (enemy.px < 0 or enemy.px > WIDTH)) : # 범위를 벗어나는 경우 False
            return False
        else : # 범위를 벗어나지 않는 경우 검사
            return True

    def collision_check(self) : # player와 enemy가 충돌했는지 검사
        for enemy in self.enemylist :
            if self.detect_collision(self.player, enemy) : # 충돌 검사
                return True
        return False        

    def detect_collision(self, player, enemy) :
        p_x = player.px
        p_y = player.py
        e_x = enemy.px
        e_y = enemy.py
        if (e_x >= p_x and e_x < (p_x + PLAYER_SIZE)) or (p_x >= e_x and p_x < (e_x + ENEMY_SIZE)):  # Checks to see the x-overlap
            if (e_y >= p_y and e_y < (p_y + PLAYER_SIZE)) or (p_y >= e_y and p_y < (e_y + ENEMY_SIZE)):  # Checks to see the y-overlap
                return True
        return False  # False is returned only when the above if statements do not get run.
    
    def move(self) : 
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] :
            self.player.move_left()
        elif key_pressed[pygame.K_RIGHT] :
            self.player.move_right()
        elif key_pressed[pygame.K_DOWN] :
            self.player.move_down()
        elif key_pressed[pygame.K_UP] :
            self.player.move_up()
    
    def play(self) :
        game_over = False
        while not game_over :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    sys.exit()
                if event.type == pygame.KEYDOWN : # 키가 눌렸을떄
                    pass
            self.move()
            self.screen.fill(BACKGROUND_COLOR) # 배경 설정
            self.create_enemies() # enemy들 생성 -> enemyMax만큼 개수를 맞춘다.
            self.update_enemy_positions() # enemy 위치 update
            self.set_level() # level 설정 -> maxEnemy 값 변경
            print(self.get_inputs())
        
            scoreText = "Score:" + str(self.score)  # Storing our score to "text" variable
            final_score = "Final Score: " + str(self.score)
            msg = "Game Over!!"
            label1 = self.myFont.render(scoreText, 1, YELLOW)
            self.screen.blit(label1,  (WIDTH - 200, HEIGHT - 50)) # Attaching our label to screen
            
            if self.collision_check() : # 충돌 감지
                label2 = self.endFont.render(final_score, 1, RED)  # The font will be printed in "red"
                label3 = self.endFont.render(msg, 1, (0, 255, 0))
                self.screen.blit(label2, (250, 250))  # It updates text to the specific part(position) of the screen
                self.screen.blit(label3, (250, 300))
                game_over = True # Game Over
            
            self.draw_enemies() # enemy들을 화면에 그린다
            pygame.draw.rect(self.screen, RED, (self.player.px, self.player.py, PLAYER_SIZE, PLAYER_SIZE)) # player를 화면에 그린다.
            self.clock.tick(60) # 60 Frame
            pygame.display.update() # screen update
            
            if game_over :
                pygame.time.wait(1000) # game_over일 경우 1초 대기후 종료 -> 다시 플레이 하게 만들면 된다.
                # 다시 플레이 하기 전에 matplot으로 세대별 점수 그래프를 그리면 될듯하다.

game = Game() # Game 객체 생성
game.play() # play
        
