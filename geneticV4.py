"""
Author: Travis Stop
Class: Artificial Intelligence (CSC 3250)
Professor: Dr. Jason Pittman

Description: given a population size and a dollar amount
at the command line, this program will first generate a population composed of
individuals made up of Quarters, Dimes, Nickels and Pennies that add up to the
specified dollar amount. Then the program will "breed" using the fittest individuals
until there is a generation that has an individual with the least amount
of coins possible that still adds up to the dollar amount.

To run: py geneticV4.py [population size (integer)] [dollar amount (float)]
"""
import random
from random import randrange
import sys

"""
keeps track of information about an individual in a population
"""
class individual:
    def __init__(self, Q, D, N, P):
        self.genes = {"Q": Q, "D": D, "N": N, "P": P}

"""
the meat and potatoes. Keeps track of and implements all functionality
in order to generate a population and breed it over multiple generations towards
the goal of having an optimal amount of coins
"""
class evolution:
    """
    takes an integer popSize and a float dollarAmount and assigns them to member
    variables.
    """
    def __init__(self, popSize, dollarAmount):
        self.population = []
        self.popSize = int(popSize)
        self.dollarAmount = float(dollarAmount)
        self.generationNumber = 1
        self.fitness = -1
        self.secondFitness = -1
        self.optimalCoinCount = self.getOptimalSolution()
        self.bestIndividual = None
        self.secondBestIndividual = None

    """
    generates a population of a specified size and whose individuals all add
    up to the specified dollar amount
    """
    def generatePopulation(self):
        for i in range(self.popSize):
            popMember = self.generateIndividual()
            while self.coinSum(popMember) != self.dollarAmount:
                popMember = self.generateIndividual()
            self.population.append(popMember)
        self.calculateFitness()

    """
    generates and returns an individual with a random number of quarters, dimes,
    nickels, and pennies and
    """
    def generateIndividual(self):
        Q = randrange(0, self.dollarAmount*100//25+1)
        D = randrange(0, self.dollarAmount*100//10+1)
        N = randrange(0, self.dollarAmount*100//5+1)
        P = randrange(0, self.dollarAmount*100//1+1)
        return individual(Q, D, N, P)

    """
    takes an individual and returns the value that the coins add up to
    """
    def coinSum(self, individual):
        return round(0.25*individual.genes["Q"] + 0.1*individual.genes["D"] + 0.05*individual.genes["N"] + 0.01*individual.genes["P"], 2)

    """
    gets the optimal number of coins for a specified dollar amount. Useful for
    fitness.
    """
    def getOptimalSolution(self):
        Q = round(self.dollarAmount*100, 0)//25
        D = round(self.dollarAmount*100, 0)%25//10
        N = round(self.dollarAmount*100, 0)%25%10//5
        P = round(self.dollarAmount*100, 0)%25%10%5
        #print(f'Q: {Q}, D: {D}, N: {N}, P: {P}')
        return int(Q + D + N + P)

    """
    used for printing the initial population and its fitness.
    """
    def printPopulation(self):
        for individual in self.population:
            print(f'S:{individual.genes}')
        print(f'Fitness: {self.fitness}')

    """
    used for printing generations after the initial population.
    """
    def printGeneration(self):
        for i in range(len(self.population)):
            print(f'{i+1}: {self.population[i].genes}')
        print(f'Generation number: {self.generationNumber}')
        print(f'Fitness: {self.fitness}')

    """
    Calculates the fitness of the current generation (fitness of best individual)
    and adjusts the self.fitness member variable accordingly. Also returns the
    first and second best individuals.
    """
    def calculateFitness(self):
        self.fitness = self.secondFitness = sys.maxsize
        firstBest = secondBest = self.population[0]
        for individual in self.population:
            currentFitness = self.individualFitness(individual)
            if currentFitness < self.fitness:
                self.fitness = currentFitness
                firstBest = individual
            elif currentFitness < self.secondFitness:
                self.secondFitness = currentFitness
                secondBest = individual
        self.bestIndividual = firstBest
        self.secondBestIndividual = secondBest
        return (firstBest, secondBest)

    """
    returns the fitness of an individual. (the less coins the lower the fitness
    the better)
    """
    def individualFitness(self, individual):
        return self.countCoins(individual) - self.optimalCoinCount

    """
    takes an individual and returns the total number of coins.
    """
    def countCoins(self, individual):
        count = 0
        for coin in individual.genes:
            count += individual.genes[coin]
        return count

    """
    takes two individuals as parameters and returns an individual that has a
    combination of the two parents "genes"
    """
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
    takes an individual and potentially returns a mutated individual.
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
        #print(f'RETURNED INDIVIDUAL: {individual.genes}')
        return individual

    """
    Nathan mentioned positive and negative mutations and only doing
    mutations that would not be culled instantly. Before it just looped through
    the genes and potentially mutated to a random number. all of these positive
    and negative mutation functions are used in the mutate function.

    takes 5 pennies from an individual and turns them into a nickel.
    """
    def positiveMutation1(self, individual):
        if individual.genes["P"] >= 5:
            individual.genes["P"] -= 5
            individual.genes["N"] += 1

    """
    takes 2 nickels from an individual and turns them into a dime.
    """
    def positiveMutation2(self, individual):
            if individual.genes["N"] >= 2:
                individual.genes["N"] -= 2
                individual.genes["D"] += 1

    """
    takes 2 dimes and a nickel -> quarter
    """
    def positiveMutation3(self, individual):
        if individual.genes["D"] >= 2 and individual.genes["N"] >= 1:
            individual.genes["D"] -= 2
            individual.genes["N"] -= 1
            individual.genes["Q"] += 1

        #print(f'FUCK: {individual.genes}')

    """
    1 quarter -> 2 dimes and a nickel
    """
    def negativeMutation1(self, individual):
        if individual.genes["Q"] >= 1:
            individual.genes["Q"] -= 1
            individual.genes["D"] += 2
            individual.genes["N"] += 1
    """
    1 dime -> 2 nickels
    """
    def negativeMutation2(self, individual):
        if individual.genes["D"] >= 1:
            individual.genes["D"] -= 1
            individual.genes["N"] += 2

    """
    1 nickel -> 5 pennies
    """
    def negativeMutation3(self, individual):
        if individual.genes["N"] >= 1:
            individual.genes["N"] -= 1
            individual.genes["P"] += 5

    """
    takes the top 2 individuals and breeds the next generation from them.
    Each generation is the same size as the initial population.
    """
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
        self.calculateFitness()

    """
    runs breedGeneration until there is at least one completely fit individual
    in a generation.
    """
    def breedPerfection(self):
        while self.fitness != 0:
            self.generationNumber = self.generationNumber + 1
            self.breedGeneration()
            self.printGeneration()
        print(f'Finished! Optimal: {self.bestIndividual.genes}')
        print(f'Optimal coin count: {self.countCoins(self.bestIndividual)}')


"""
\"Driver\"
"""
if __name__ == "__main__":
    pop = evolution(sys.argv[1], sys.argv[2])
    pop.generatePopulation()
    pop.printPopulation()
    print()
    pop.breedPerfection()
