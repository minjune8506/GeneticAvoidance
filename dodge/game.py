from matplotlib import pyplot as plt
import numpy as np
from helpers import *
from enemy import Enemy
from player import Player
import pygame
import time
import sys
from math import *

class Game() :
    def __init__(self) :
        pygame.init()  # To initialize pygame
        # set screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # We have a screen of WIDTH 800 and HEIGHT 600
        self.clock = pygame.time.Clock() # It defines a clock
        self.myFont = pygame.font.SysFont("monospace", 35)  # Defining the font in pygame (Monospace is font and 35 is in pixels)
        self.endFont = pygame.font.SysFont("comicsansms", 40, True, False)
        self.scores = []
        self.cnt = 0
    
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
                enemy.px += enemy.x_speed * ENEMY_SPEED
                x_move = True
            if (0 <= enemy.py <= HEIGHT) :
                enemy.py += enemy.y_speed * ENEMY_SPEED
                y_move = True

            if not x_move or not y_move : # x, y좌표중 하나라도 화면 밖에 있다면
                self.enemylist.pop(idx) # enemy 제거
                self.score += 1 # score 점수 증가
            elif self.out_of_range(enemy) : # 유효한 애들만
                x_d, y_d = self.cal_real_distance(enemy)
                distance = sqrt(pow(x_d, 2) + pow(y_d, 2))
                enemy_distance_list.append([distance, enemy.x_speed, enemy.y_speed]) # distance, x_speed, y_speed
        
        enemy_distance_list.sort(key = lambda x:x[0]) # distance 가 가장 낮은 애를 정렬
        print(enemy_distance_list[0][0])
        self.player.inputs = [enemy_distance_list[0][1], enemy_distance_list[0][2]]
    
    def cal_real_distance(self, enemy) :    
        x_d = 0
        y_d = 0
        p_x = self.player.pos[0]
        p_y = self.player.pos[1]

        if enemy.px + ENEMY_SIZE < p_x : # 왼쪽에 있으면
            x_d = p_x - (enemy.px + ENEMY_SIZE)
        elif p_x + PLAYER_SIZE < enemy.px : # 오른쪽에 있으면
            x_d = enemy.px - (p_x + PLAYER_SIZE)

        if enemy.py + ENEMY_SIZE < p_y : # 위에 있으면
            y_d = p_y - (enemy.py + ENEMY_SIZE)
        elif p_y + PLAYER_SIZE < enemy.py : # 아래에 있으면
            y_d = enemy.py - (p_y + PLAYER_SIZE)        

        return x_d, y_d
    
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
    
    def prepare(self) :
        self.score = 0
        self.player = Player()
        self.enemylist = []
        self.enemyMax = 30
        
    def play(self) :
        game_over = False
        self.prepare()
        while not game_over :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    sys.exit()
                if event.type == pygame.KEYDOWN : # 키가 눌렸을떄
                    pass
            self.move() # Player Move (Key Event)
            self.screen.fill(BACKGROUND_COLOR) # 배경 설정
            self.create_enemies() # enemy들 생성 -> enemyMax만큼 Enemy 생성
            self.update_enemy_positions() # enemy 위치 update
            self.set_level() # level 설정 -> maxEnemy 값 변경
            print(self.get_inputs())
        
            scoreText = "Score:" + str(self.score)  # Storing our score to "text" variable
            scoreLabel = self.myFont.render(scoreText, 1, YELLOW)
            self.screen.blit(scoreLabel, (WIDTH - scoreLabel.get_width(), 0)) # Attaching our label to screen
            
            if self.collision_check() : # 충돌 감지
                final_score = "Final Score: " + str(self.score)
                endScoreLabel = self.endFont.render(final_score, 1, RED)  # The font will be printed in "red"
                endMsg = "Game Over!!"
                endLabel = self.endFont.render(endMsg, 1, (0, 255, 0))
                self.screen.blit(endScoreLabel, ((WIDTH - endScoreLabel.get_width()) / 2, (HEIGHT - endScoreLabel.get_height()) / 2))  # It updates text to the specific part(position) of the screen
                self.screen.blit(endLabel, ((WIDTH - endScoreLabel.get_width()) / 2, (HEIGHT + endScoreLabel.get_height()) / 2))
                game_over = True # Game Over
            
            self.draw_enemies() # enemy들을 화면에 그린다
            pygame.draw.rect(self.screen, RED, (self.player.px, self.player.py, PLAYER_SIZE, PLAYER_SIZE)) # player를 화면에 그린다.
            self.clock.tick(60) # 60 Frame
            pygame.display.update() # screen update
            
            if game_over :
                self.scores.append(self.score)
                time.sleep(1)
                break
        plt.plot(np.array(list(range(self.cnt + 1))),
                 np.array(self.scores)) # 그래프 값 추가
        plt.draw()
        self.cnt += 1
        self.play() # Play Again

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1,1,1)
ax.set_title("Dodge game")
ax.set(xlabel = 'Generation', ylabel='Score')
plt.show(block = False)
game = Game() # Game 객체 생성
game.play() # play
        
