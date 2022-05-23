import random
import copy
from network import Network

class Generation():
    def __init__(self):
        self.population = 50  # 한 세대에 공룡 50마리
        self.keep_best = 10  # 몇개를 살릴건지?
        self.genomes = self.set_initial_genomes() # 유전자 초기화
        self.chance_of_mutation = 0.1  # 돌연변이 확률

    def set_initial_genomes(self):  # 0세대 유전자들 초기값 설정
        genomes = []
        for i in range(self.population):  # 인구수만큼 -> 50만큼 반복문
            genomes.append(Network())  # 신경망 객체 생성
        return genomes  # 50개 초기 신경망 셋팅 후 리턴

    def set_genomes(self, genomes):
        self.genomes = genomes

    def keep_best_genomes(self):  # 적합도가 가장 잘 나온 10마리를 살린다.
        self.genomes.sort(key=lambda x: x.fitness, reverse=True)  # 적합도 기준으로 정렬
        self.best_genomes = self.genomes[:self.keep_best]  # 잘라서 가지고 있는다.
        self.genomes = copy.deepcopy(self.best_genomes[:])

    def mutations(self):  # 돌연변이
        # 40보다 작을 때까지? 이미 고른 우수한 유전자 10개를 가지고 40개를 교배 & 돌연변이 생성
        while len(self.genomes) < self.keep_best * 5:
            # 가장 적합도가 높은 10마리 중 하나를 랜덤하게 선택
            genome1 = random.choice(self.best_genomes)
            # 가장 적합도가 높은 10마리 중 하나를 랜덤하게 선택
            genome2 = random.choice(self.best_genomes)
            self.genomes.append(self.mutate(self.cross_over(genome1, genome2)))  # 교배 -> 돌연변이
        random.shuffle(self.genomes)  # 유전자 리스트 항목 섞기
        return self.genomes

    def cross_over(self, genome1, genome2):  # 우수한 유전자들 교배
        new_genome = copy.deepcopy(genome1)  # 가져온 두개의 우수한 유전자들 deep copy
        other_genome = copy.deepcopy(genome2)

        # random.uniform(a, b) : a ~ b 사이의 랜덤 실수를 리턴한다.
        # 얼만큼 자를 것인지? 랜덤하게 선택
        cut_location = int(len(new_genome.W1) * random.uniform(0, 1))
        for i in range(cut_location):  # W1 교배
            # 자른 만큼 W 값을 가져온다.
            new_genome.W1[i], other_genome.W1[i] = other_genome.W1[i], new_genome.W1[i]
            # 0 ~ cut_location까지 섞어준다.

        # cut_location = int(len(new_genome.W2) * random.uniform(0, 1))  # W2 교배
        # for i in range(cut_location):
        #     new_genome.W2[i], other_genome.W2[i] = other_genome.W2[i], new_genome.W2[i]

        cut_location = int(len(new_genome.W3) * random.uniform(0, 1))  # W3 교배
        for i in range(cut_location):
            new_genome.W3[i], other_genome.W3[i] = other_genome.W3[i], new_genome.W3[i]
        return new_genome

    def mutate_weights(self, weights):
        # print(weights)
        # chance_of_mutation = 0.1 랜덤으로 뽑은 확률이 0.1보다 작으면
        if random.uniform(0, 1) < self.chance_of_mutation:
            # 돌연변이 생성 (이상한 값)
            return weights * (random.uniform(0, 1) - 0.5) * 3 + (random.uniform(0, 1) - 0.5)
        else:
            return 0

    def mutate(self, genome):  # 돌연변이
        new_genome = copy.deepcopy(genome)  # 교배를 끝난 유전자를 가져온다.
        new_genome.W1 += self.mutate_weights(new_genome.W1)
        # new_genome.W2 += self.mutate_weights(new_genome.W2)
        new_genome.W3 += self.mutate_weights(new_genome.W3)
        return new_genome
