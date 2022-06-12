from this import d
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

class Dummy_Enemy : # 일단, detect collision 에다가 입력으로 넘겨야 하기 때문에 일단 dummy 로 만들자. (나중에 잘 되면 수정해도 괜찮을 듯)
    def __init__(self, px, py) :
        self.px = px
        self.py = py

class Dummy_Player : # 위와 동일
    def __init__(self, px, py) :
        self.px = px
        self.py = py

class Game() :
    def __init__(self) : # 초기화
        pygame.init()  # To initialize pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen 생성
        self.myFont = pygame.font.SysFont("monospace", 35)  # Defining the font in pygame (Monospace is font and 35 is in pixels)
        self.endFont = pygame.font.SysFont("comicsansms", 40, True, False)
        self.generation = Generation() # Generation 생성 (유전자 모음)
        self.genomes = copy.deepcopy(self.generation.genomes)
        self.gen = 0 # 세대
        self.scores = [] # Score 모음
        self.clock = pygame.time.Clock() # It defines a clock

    def set_level(self) : # level 당 enemy 개수
        if self.score < 20:
            self.enemyMax = 30 # level 1
        elif self.score < 50:
            self.enemyMax = 50 # level 2
        elif self.score < 100:
            self.enemyMax = 70 # level 3
        else:
            self.enemyMax = 100 # level 4

    def create_enemies(self) : # enemy 생성
        while len(self.enemylist) < self.enemyMax : # enemyMax 만큼 enemy 객체 생성
            self.enemylist.append(Enemy()) # 리스트에 추가
    
    def draw_enemies(self) : # enemy 그리기
        for enemy in self.enemylist : # enemylist에 있는 enemy객체들을 화면에 그린다.
            pygame.draw.rect(self.screen, BLUE, (enemy.px, enemy.py, ENEMY_SIZE, ENEMY_SIZE))

    def update_enemy_positions(self) : # enemy의 위치 update
        for idx, enemy in enumerate(self.enemylist) :
            x_move = False
            y_move = False
            if (-20 <= enemy.px + enemy.x_speed * ENEMY_SPEED <= WIDTH + 20) : # enemy가 화면 안에 있는지 검사
                enemy.px += enemy.x_speed * ENEMY_SPEED
                x_move = True
            if (-20 <= enemy.py + enemy.y_speed * ENEMY_SPEED <= HEIGHT + 20) :
                enemy.py += enemy.y_speed * ENEMY_SPEED
                y_move = True

            if not x_move or not y_move : # x, y좌표중 하나라도 화면 밖에 있다면
                self.enemylist.pop(idx) # enemy 제거
                self.score += 1 # score 점수 증가
            else :                
                for player in self.players : # 각 player 와 현재 적을 비교
                    self.append_player_list(enemy, player)
        
        for player in self.players :
            self.pull_input(player)

    def append_player_list(self, enemy, player) : # enemy, player 의 정보를 이용하여, 가장 가까운 장애물을 골라냄
        if (player.dead != True) : # Player가 이미 죽은 경우 넘어간다.
            distance = self.cal_distance(enemy, player)
            relative_x_d, relative_y_d = self.relative_position(enemy, player)
            if (distance < 100) :
                if distance < player.input[0] : # 현재 distance 가 더 낮은 경우에만 집어넣는다, 그렇지 않으면 그냥 넣지 않으니 무시
                    player.input = [distance, relative_x_d, relative_y_d, enemy.x_speed, enemy.y_speed]                

    def relative_position(self, enemy, player) : # 적과의 상대적 거리를 반환    
        relative_x_d = player.px - enemy.px
        relative_y_d = player.py - enemy.py
        
        return relative_x_d, relative_y_d

    def cal_distance(self, enemy, player) : # player 와 enemy 와의 거리를 계산
        x_d = player.px - enemy.px
        y_d = player.py - enemy.py
        distance = sqrt(pow(x_d, 2) + pow(y_d, 2)) # player와 enemy 거리 계산
        return distance

    def pull_input(self, player) : # 계산해놓은 player list 를 가지고 가장 가까운 적을 뽑아냄
        if player.dead != True :        
            player.input = player.input[1:5]

    def collision_check(self, idx) : # player와 enemy가 충돌했는지 검사
        for enemy in self.enemylist :
            if self.detect_collision(self.players[idx], enemy) : # 충돌 검사
                return True

        return False

    def detect_end_in_deadlock(self, player) : # 실질적인 사이즈를 고려하여, 벽에 부딪혀서 더 이상 움직이지 못하는지를 파악해야함, 벽에 부딪히는 경우도 계산하자.
        wall_list = [0, HEIGHT - PLAYER_SIZE, 0, WIDTH - PLAYER_SIZE] # 위, 아래, 왼쪽, 오른쪽 Player size 를 고려하여서 벽에 부딪히는지 안부딪히는지 계산하기 위함이다.
        p_x = player.px
        p_y = player.py

        if p_y < wall_list[0] or p_y > wall_list[1] or p_x < wall_list[2] or p_x > wall_list[3]:
            return True

        return False

    def detect_collision(self, player, enemy) : # enemy 와 player 가 충돌하는지를 판별
        p_x = player.px
        p_y = player.py
        e_x = enemy.px
        e_y = enemy.py
        if (e_x >= p_x and e_x < (p_x + PLAYER_SIZE)) or (p_x >= e_x and p_x < (e_x + ENEMY_SIZE)):  # Checks to see the x-overlap
            if (e_y >= p_y and e_y < (p_y + PLAYER_SIZE)) or (p_y >= e_y and p_y < (e_y + ENEMY_SIZE)):  # Checks to see the y-overlap
                return True
        return False  # False is returned only when the above if statements do not get run.
    
    def move(self, idx, output) : # 신경망 결과 값으로 방향 조정                
        if output == UP :
            self.players[idx].move_up()
        elif output == DOWN :
            self.players[idx].move_down()
        elif output == LEFT :
            self.players[idx].move_left()
        elif output == RIGHT :
            self.players[idx].move_right()
        elif output == UPLEFT :
            self.players[idx].move_up()
            self.players[idx].move_left()
        elif output == UPRIGHT :
            self.players[idx].move_up()
            self.players[idx].move_right()
        elif output == DOWNLEFT :
            self.players[idx].move_down()
            self.players[idx].move_left()
        elif output == DOWNRIGHT :
            self.players[idx].move_down()
            self.players[idx].move_right()
    
    def prepare(self) : # Game 을 시작하기 이전에 초기화
        self.score = 0 # score
        self.players = [] # Player 보관 리스트
        for i in range (self.generation.population) :
            self.players.append(Player()) # 세대의 인구 수만큼 플레이어 생성
            self.genomes[i].fitness = 0 # 새로 시작할 때마다, genome fitness 수정
        self.genomes = copy.deepcopy(self.generation.genomes) # generation의 유전자 값 복사
        self.enemylist = [] # 적들의 리스트
        self.enemyMax = 30 # 최대 적 갯수
        self.is_live = self.generation.population
    
    def print_end_msg(self) : # 게임이 끝나지 않고 진행되므로 안써도 되는 메소드
        final_score = "Final Score: " + str(self.score)
        endScoreLabel = self.endFont.render(final_score, 1, RED)  # The font will be printed in "red"
        endMsg = "Game Over!!"
        endLabel = self.endFont.render(endMsg, 1, (0, 255, 0))
        self.screen.blit(endScoreLabel, ((WIDTH - endScoreLabel.get_width()) / 2, (HEIGHT - endScoreLabel.get_height()) / 2))  # It updates text to the specific part(position) of the screen
        self.screen.blit(endLabel, ((WIDTH - endScoreLabel.get_width()) / 2, (HEIGHT + endScoreLabel.get_height()) / 2))
    
    def play(self) : # 게임 시작
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
                player_input = self.players[i].get_inputs()
                if not (player_input[0] == 0 and player_input[1] == 0) : # 처음에 적을 감지하지 못하였는데, 움직이는 현상을 해결
                    output = np.argmax(self.genomes[i].decisionOutput(self.players[i].get_inputs())) # 신경망 계산
                    self.move(i, output) # Player Move            
                self.players[i].input = [INIT_DISTANCE, 0, 0, 0, 0]
                if self.collision_check(i) : # 충돌 검사
                    self.players[i].dead = True # dead
                    self.is_live -= 1
                    self.genomes[i].fitness = self.score # 적합도 설정
        
            scoreText = "Score:" + str(self.score)  # Score 갱신
            scoreLabel = self.myFont.render(scoreText, 1, YELLOW)
            self.screen.blit(scoreLabel, (WIDTH - scoreLabel.get_width(), 0)) # Screen에 Label 추가
            
            isLiveText = "Player:" + str(self.is_live)
            liveLabel = self.myFont.render(isLiveText, 1, YELLOW)
            self.screen.blit(liveLabel, (0, 0)) # 플레이어 얼마나 살아있는지 정보 표시
            
            self.draw_enemies() # enemy들을 화면에 그린다
            for player in self.players :
                if player.dead == True : # 죽었으면 패스
                    continue
                # 안죽은 플레이어만 화면에 그린다.
                pygame.draw.rect(self.screen, RED, (player.px, player.py, PLAYER_SIZE, PLAYER_SIZE))
            
            self.clock.tick(60) # 120 Frame
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
                self.fitness_list.append(self.generation.genomes[0].fitness) # keep_best_genomes 에서 정렬을 해주니까 여기서 넣어줌
                self.generation.mutations() # 유전자 교배
                time.sleep(1)
        plt.plot(np.array(list(range(self.gen + 1))),
			np.array(self.scores)) # 그래프 값 추가
        plt.draw()
        self.gen += 1
        self.play() # Play Again

# 그래프 그리기 위해 초기화
fig = plt.figure(figsize=(6,4))
ax = fig.add_subplot(1,1,1)
ax.set_title("Dodge game")
ax.set(xlabel = 'Generation', ylabel='Fitness')
plt.show(block = False)

game = Game() # Game 객체 생성
game.play() # play
        
