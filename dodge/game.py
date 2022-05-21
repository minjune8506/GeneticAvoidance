from matplotlib import pyplot as plt
import numpy as np
import pygame
import time
import sys
import copy
from math import *
from helpers import *
from enemy import Enemy
from player import Player
from generation import Generation

class Game() :
    def __init__(self) :
        pygame.init()  # To initialize pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen 생성
        self.clock = pygame.time.Clock() # It defines a clock
        self.myFont = pygame.font.SysFont("monospace", 35)  # Defining the font in pygame (Monospace is font and 35 is in pixels)
        self.endFont = pygame.font.SysFont("comicsansms", 40, True, False)
        self.generation = Generation() # Generation 생성 (유전자 모음)
        self.genomes = copy.deepcopy(self.generation.genomes)
        self.gen = 0 # 세대
        self.scores = [] # Score 모음

    def set_level(self) :
        if self.score < 20:
            self.enemyMax = 30 # level 1
        elif self.score < 50:
            self.enemyMax = 50 # level 2
        elif self.score < 100:
            self.enemyMax = 70 # level 3
        else:
            self.enemyMax = 100 # level 4
    
    def create_enemies(self) :
        while len(self.enemylist) < self.enemyMax : # enemyMax 만큼 enemy 객체 생성
            self.enemylist.append(Enemy()) # 리스트에 추가
    
    def draw_enemies(self) :
        for enemy in self.enemylist : # enemylist에 있는 enemy객체들을 화면에 그린다.
            pygame.draw.rect(self.screen, BLUE, (enemy.px, enemy.py, ENEMY_SIZE, ENEMY_SIZE))

    def update_enemy_positions(self) : # enemy의 위치 update
        for idx, enemy in enumerate(self.enemylist) :
            x_move = False
            y_move = False
            if (0 <= enemy.px + enemy.x_speed * ENEMY_SPEED <= WIDTH) : # enemy가 화면 안에 있는지 검사
                enemy.px += enemy.x_speed * ENEMY_SPEED
                x_move = True
            if (0 <= enemy.py + enemy.y_speed * ENEMY_SPEED <= HEIGHT) :
                enemy.py += enemy.y_speed * ENEMY_SPEED
                y_move = True

            if not x_move or not y_move : # x, y좌표중 하나라도 화면 밖에 있다면
                self.enemylist.pop(idx) # enemy 제거
                self.score += 1 # score 점수 증가
            else :
                # print("(%d, %d)" %(enemy.px, enemy.py))
                for player in self.players :
                    if (player.dead == True) : # Player가 이미 죽은 경우 넘어간다.
                        continue
                    x_d, y_d = self.cal_real_distance(enemy, player)
                    distance = sqrt(pow(x_d, 2) + pow(y_d, 2)) # player와 enemy 거리 계산
                    player.distance = [min(player.distance[0], distance), enemy.x_speed, enemy.y_speed]
    
    def cal_real_distance(self, enemy, player) :
        # 위치 계산을 아예 enemy의 중심값, player의 중심값을 기준으로 계산해보는건 어떤지..?
        x_d = 0
        y_d = 0
        p_x = player.pos[0]
        p_y = player.pos[1]

        if enemy.px + ENEMY_SIZE < p_x : # 왼쪽에 있으면
            x_d = p_x - (enemy.px + ENEMY_SIZE)
        elif p_x + PLAYER_SIZE < enemy.px : # 오른쪽에 있으면
            x_d = enemy.px - (p_x + PLAYER_SIZE)

        if enemy.py + ENEMY_SIZE < p_y : # 위에 있으면
            y_d = p_y - (enemy.py + ENEMY_SIZE)
        elif p_y + PLAYER_SIZE < enemy.py : # 아래에 있으면
            y_d = enemy.py - (p_y + PLAYER_SIZE)        

        return x_d, y_d

    def collision_check(self, idx) : # player와 enemy가 충돌했는지 검사
        for enemy in self.enemylist :
            if self.detect_collision(self.players[idx], enemy) : # 충돌 검사
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
    
    def move(self, idx, output) : # 신경망 결과 값으로 방향 조정
        max_val = max(output)
        if max_val == output[UP] : # Up
            self.players[idx].move_up()
        elif max_val == output[DOWN] : # Down
            self.players[idx].move_down()
        elif max_val == output[LEFT] : # Left
            self.players[idx].move_left()
        elif max_val == output[RIGHT] : # Right
            self.players[idx].move_right()
        elif max_val == output[STAY] : # Stay
            pass
    
    def prepare(self) :
        self.score = 0 # score
        self.players = [] # Player 보관 리스트
        for i in range (self.generation.population) :
            self.players.append(Player()) # 세대의 인구 수만큼 플레이어 생성
        self.genomes = copy.deepcopy(self.generation.genomes) # generation의 유전자 값 복사
        self.enemylist = [] # 적들의 리스트
        self.enemyMax = 30 # 최대 적 갯수
    
    def print_end_msg(self) : # 게임이 끝나지 않고 진행되므로 안써도 되는 메소드
        final_score = "Final Score: " + str(self.score)
        endScoreLabel = self.endFont.render(final_score, 1, RED)  # The font will be printed in "red"
        endMsg = "Game Over!!"
        endLabel = self.endFont.render(endMsg, 1, (0, 255, 0))
        self.screen.blit(endScoreLabel, ((WIDTH - endScoreLabel.get_width()) / 2, (HEIGHT - endScoreLabel.get_height()) / 2))  # It updates text to the specific part(position) of the screen
        self.screen.blit(endLabel, ((WIDTH - endScoreLabel.get_width()) / 2, (HEIGHT + endScoreLabel.get_height()) / 2))
    
    def play(self) :
        game_over = False
        self.prepare()
        while not game_over :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    sys.exit()
                if event.type == pygame.KEYDOWN : # 키가 눌렸을떄
                    pass
            self.screen.fill(BACKGROUND_COLOR) # 배경 설정
            self.create_enemies() # enemy들 생성 -> enemyMax만큼 Enemy 생성
            self.update_enemy_positions() # enemy 위치 update
            self.set_level() # level 설정 -> maxEnemy 값 변경
            
            for i in range(self.generation.population) :
                if self.players[i].dead == True : # 이미 죽었으면 넘어간다.
                    continue
                output = self.genomes[i].decisionOutput(self.players[i].get_inputs()) # 신경망 계산
                self.move(i, output) # Player Move
                if self.collision_check(i) : # 충돌 검사
                    self.players[i].dead = True # dead
                    self.genomes[i].finess = self.score # 적합도 설정
        
            scoreText = "Score:" + str(self.score)  # Score 갱신
            scoreLabel = self.myFont.render(scoreText, 1, YELLOW)
            self.screen.blit(scoreLabel, (WIDTH - scoreLabel.get_width(), 0)) # Screen에 Label 추가
            
            self.draw_enemies() # enemy들을 화면에 그린다
            for player in self.players :
                if player.dead == True : # 죽었으면 패스
                    continue
                # 안죽은 플레이어만 화면에 그린다.
                pygame.draw.rect(self.screen, RED, (player.px, player.py, PLAYER_SIZE, PLAYER_SIZE))
            
            self.clock.tick(60) # 60 Frame
            pygame.display.update() # screen update
            
            # Player가 모두 죽었는지 확인
            game_over = True
            for i in range(self.generation.population) :
                if (self.players[i].dead == False) :
                    game_over = False

            if game_over : # Game Over
                self.scores.append(self.score)
                print("---------Generation %d Ends---------" %self.gen)
                print("Max Score : %d" %self.score)
                self.generation.genomes = copy.deepcopy(self.genomes)
                self.generation.keep_best_genomes() # 적합도가 높은 유전자 보존
                self.generation.mutations() # 유전자 교배
                time.sleep(1)
                break
        
        plt.plot(np.array(list(range(self.gen + 1))),
                 np.array(self.scores)) # 그래프 값 추가
        plt.draw()
        self.gen += 1
        self.play() # Play Again

# 그래프 그리기 위해 초기화
fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(1,1,1)
ax.set_title("Dodge game")
ax.set(xlabel = 'Generation', ylabel='Score')
plt.show(block = False)

game = Game() # Game 객체 생성
game.play() # play
        
