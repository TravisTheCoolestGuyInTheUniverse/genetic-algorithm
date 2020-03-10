import random
from random import randrange
import sys

class individual:
    def __init__(self, Q, D, N, P):
        self.genes = {"Q": Q, "D": D, "N": N, "P": P}

class evolution:
    def __init__(self, popSize, dollarAmount):
        self.population = []
        self.popSize = int(popSize)
        self.dollarAmount = float(dollarAmount)
        self.generationNumber = 1
        self.fitness = -1
        self.optimalCoinCount = self.getOptimalSolution()
        self.bestIndividual = None
        self.secondBestIndividual = None

    def generatePopulation(self):
        for i in range(self.popSize):
            popMember = self.generateIndividual()
            while self.coinSum(popMember) != self.dollarAmount:
                popMember = self.generateIndividual()
            self.population.append(popMember)
        self.calculateFitness()


    def generateIndividual(self):
        Q = randrange(0, self.dollarAmount*100//25+1)
        D = randrange(0, self.dollarAmount*100//10+1)
        N = randrange(0, self.dollarAmount*100//5+1)
        P = randrange(0, self.dollarAmount*100//1+1)
        return individual(Q, D, N, P)

    def coinSum(self, individual):
        return 0.25*individual.genes["Q"] + 0.1*individual.genes["D"] + 0.05*individual.genes["N"] + 0.01*individual.genes["P"]

    def getOptimalSolution(self):
        Q = round(self.dollarAmount*100, 0)//25
        D = round(self.dollarAmount*100, 0)%25//10
        N = round(self.dollarAmount*100, 0)%25%10//5
        P = round(self.dollarAmount*100, 0)%25%10%5
        #print(f'Q: {Q}, D: {D}, N: {N}, P: {P}')
        return int(Q + D + N + P)

    def printPopulation(self):
        for individual in self.population:
            print(f'S:{individual.genes}')
        print(f'Fitness: {self.fitness}')

    def printGeneration(self):
        for i in range(len(self.population)):
            print(f'{i+1}: {self.population[i].genes}')
        print(f'Generation number: {self.generationNumber}')
        print(f'Fitness: {self.fitness}')


    def calculateFitness(self):
        self.fitness = secondFitness = sys.maxsize
        firstBest = secondBest = self.population[0]
        for individual in self.population:
            currentFitness = self.individualFitness(individual)
            if currentFitness < self.fitness:
                self.fitness = currentFitness
                firstBest = individual
            elif currentFitness < secondFitness:
                secondFitness = currentFitness
                secondBest = individual
        self.bestIndividual = firstBest
        self.secondBestIndividual = secondBest
        return (firstBest, secondBest)

    def individualFitness(self, individual):
        return self.countCoins(individual) - self.optimalCoinCount

    def countCoins(self, individual):
        count = 0
        for coin in individual.genes:
            count += individual.genes[coin]
        return count

    def crossover(self, parent1, parent2):
        Q1 = random.choice([True, False])
        D1 = random.choice([True, False])
        N1 = random.choice([True, False])
        P1 = random.choice([True, False])
        Q = D = N = P = 0
        if Q1:
            Q = parent1.genes["Q"]
        else:
            Q = parent2.genes["Q"]
        if D1:
            D = parent1.genes["D"]
        else:
            D = parent2.genes["D"]
        if N1:
            N = parent1.genes["N"]
        else:
            N = parent2.genes["N"]
        if P1:
            P = parent1.genes["P"]
        else:
            P = parent2.genes["P"]
        child = individual(Q, D, N, P)
        return child

    """

    """
    def mutate(self, individual):
        for gene in individual.genes:
            chance = random.random()
            if chance < 0.1:
                mutationChoice = random.randint(0, 6)
                if mutationChoice == 0:
                    self.positiveMutation1(individual)
                if mutationChoice == 1:
                    self.positiveMutation2(individual)
                if mutationChoice == 2:
                    self.positiveMutation3(individual)
                if mutationChoice == 3:
                    self.negativeMutation1(individual)
                if mutationChoice == 4:
                    self.negativeMutation2(individual)
                if mutationChoice == 5:
                    self.negativeMutation3(individual)
        return individual

        """
        Nathan mentioned positive and negative mutations and only doing
        mutations that would not be culled instantly. Before it just looped through
        the genes and potentially mutated to a random number.
        """
    def positiveMutation1(self, individual):
        if individual.genes["P"] >= 5:
            individual.genes["P"] -= 5
            individual.genes["N"] += 1

    def positiveMutation2(self, individual):
            if individual.genes["N"] >= 2:
                individual.genes["N"] -= 2
                individual.genes["D"] += 1

    def positiveMutation3(self, individual):
        if individual.genes["D"] >= 2 and individual.genes["N"] >= 1:
            individual.genes["D"] -= 2
            individual.genes["N"] -= 1
            individual.genes["Q"] += 1

    def negativeMutation1(self, individual):
        if individual.genes["Q"] >= 1:
            individual.genes["Q"] -= 1
            individual.genes["D"] += 2
            individual.genes["N"] += 1

    def negativeMutation2(self, individual):
        if individual.genes["D"] >= 1:
            individual.genes["D"] -= 1
            individual.genes["N"] += 2

    def negativeMutation3(self, individual):
        if individual.genes["N"] >= 1:
            individual.genes["N"] -= 1
            individual.genes["P"] += 5

    def breedGeneration(self):
        fitnessInfo = self.calculateFitness()
        parent1 = fitnessInfo[0]
        parent2 = fitnessInfo[1]
        del self.population[:]
        while len(self.population) < self.popSize:
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            if self.coinSum(child) == self.dollarAmount:
                self.population.append(child)





    def breedPerfection(self):
        while self.fitness != 0:
            self.generationNumber = self.generationNumber + 1
            self.breedGeneration()
            self.printGeneration()







if __name__ == "__main__":
    pop = evolution(sys.argv[1], sys.argv[2])
    #print(f'{int(sys.argv[1])}')
    #print(f'{float(sys.argv[2])}')
    #print(pop.getOptimalSolution())
    pop.generatePopulation()
    pop.printPopulation()
    print()
    pop.breedPerfection()
