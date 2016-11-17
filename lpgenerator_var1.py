fileName = 'nutrition_data.csv'
fileNameUpperLower = 'upperLower.csv'
fileNameAvail = 'avail.csv'

def readCSV(fileName):
    lines = []
    with open(fileName, 'rb') as f:
        for line in f.readlines():
            line = line.upper().decode("utf-8")
            name = line.strip().split(',')
            lines.append(name)
    return lines

dubStreet = range(0,4)
fireCracker = range(4,8)
motosurf = range(8,11)
pagliacci = range(11,15)
redRadish = range(15,18)
subway = range(18,23)

restaurants = [dubStreet, fireCracker, motosurf, pagliacci, redRadish, subway]

price = "p"
calories = ["cal", 0, 100]
totalFat = ["tf", 0, 100]
saturatedFat = ["sf", 0, 100]
cholesterol = ["ch", 0, 100]
sodium = ["sd", 0, 100]
carbohydrate = ["carb", 0, 100]
fiber = ["f", 0, 100]
sugar = ["sug", 0, 100]
protein = ["pr", 0, 100]
calcium = ["calc", 0, 100]
vitaminC = ["vc", 0, 100]

nutrition = [price, calories, totalFat, saturatedFat, cholesterol, sodium,
             carbohydrate, fiber, sugar, protein, calcium, vitaminC]

nutritionRange = range(1, len(nutrition))

def generateUpperLower(upperLower):
    for values in range(0,len(nutrition) - 1):
        nutrition[values + 1][1] = upperLower[0][values]
        nutrition[values + 1][2] = upperLower[1][values]

# Generative the objective function
def generateObjective(lines):
    objectiveValues = "/* Objective function */ \n" \
                      "min: "
    for places in restaurants:
        for foods in places:
            for times in range(0,3):
                objectiveValues += "+" + str(lines[foods][nutrition.index(price)]) + \
                                   " y_" + str(times) + "_" + str(foods) + " "
    objectiveValues  = objectiveValues + "; \n"
    return objectiveValues

# Generate the constraints
def generateConstraints(lines, avail):
    constraintValues = "/* Constraints */ \n"

    # Constraint 1: Time + Location + Eat or Not
    for places in restaurants:
        for foods in places:
            for times in range(0,3):
                constraintValues += "+" + str(avail[times][foods]) + " y_" + str(times) + "_" \
                                   + str(foods) + " "
        constraintValues += "<= 2; \n"

    # Constraint 2: Can only get each type of food once a day
    for places in restaurants:
        for foods in places:
            for times in range(0,3):
                constraintValues += "+" + str(avail[times][foods]) + " y_" + str(times) + "_"  + str(foods) + " "
            constraintValues += "<= 1; \n"

    #Constraint 3: Min and Max for each Nutritional Value
    for nut in nutritionRange:
        for places in restaurants:
            for foods in places:
                for times in range(0, 3):
                    constraintValues += "+" + str(avail[times][foods]) + " " + str(lines[foods]
                                                  [nutrition.index(nutrition[nut])]) + \
                                        " y_" + str(times) + "_" + str(foods) + " "
        constraintValues += " >= " + str(nutrition[nut][1]) + "; \n"

        for places in restaurants:
            for foods in places:
                for times in range(0, 3):
                    constraintValues += "+" + str(avail[times][foods]) + " " + str(lines[foods]
                                                  [nutrition.index(nutrition[nut])]) + \
                                        " y_" + str(times) + "_" + str(foods) + " "
        constraintValues += " <= " + str(nutrition[nut][2]) + "; \n"

    # Constraint 4: Need at least 3 meals
    for times in range(0, 3):
        for places in restaurants:
            for food in places:
                constraintValues += "+" + str(avail[times][foods]) + " y_" + str(times) + "_" + str(food) + " "
        constraintValues += " >= 1; \n"
    print(constraintValues)

    # Constraint 5: Binary values
    constraintValues = constraintValues + "bin "
    for values in range(0, 23):
        for times in range(0,3):
            constraintValues = constraintValues + "y_" + str(times) + "_" + str(values) + ", "
    constraintValues = constraintValues[:-2] + ";"

    return constraintValues

lines = readCSV(fileName)
generateUpperLower(readCSV(fileNameUpperLower))
avail = readCSV(fileNameAvail)

objective = generateObjective(lines)
constraints = generateConstraints(lines, avail)

f1 = open('./lpproblem.lp', 'w+')
f1.write(objective)
f1.write(constraints)
print("File: lpproblem.lp has been generated.")

f2 = open('./lpproblem.txt', 'w+')
f2.write(objective)
f2.write(constraints)
print("File: lpproblem.txt has been generated.")