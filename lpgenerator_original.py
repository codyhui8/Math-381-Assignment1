fileName = 'nutrition_data.csv'

def readCSV(fileName):
    lines = []
    with open(fileName, 'rb') as f:
        for line in f.readlines():
            line = line.upper().decode("utf-8")
            # print("Line :" + line)
            name = line.strip().split(',')
            lines.append(name)
    return lines

fileNameUpperLower = 'upperLower.csv'

def readCSVUpperLower(fileName):
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

# restaurants = [dubStreet, fireCracker]

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

# nutrition = [price, calories, totalFat, saturatedFat, cholesterol, sodium, carbohydrate, fiber, sugar,
#             protein, calcium, vitaminC]

nutrition = [price, calories, totalFat, saturatedFat, cholesterol, sodium, carbohydrate, fiber, sugar,
             protein, calcium, vitaminC]

nutritionRange = range(1, len(nutrition))

def generateUpperLower(upperLower):
    for values in range(0,len(nutrition) - 1):
        nutrition[values + 1][1] = upperLower[0][values]
        nutrition[values + 1][2] = upperLower[1][values]
        print(nutrition[values + 1])

def generateObjective(lines):
    objectiveValues = "/* Objective function */ \n" \
                      "min: "
    for places in restaurants:
        # print("Restaurant")
        for foods in places:
            for times in range(0,3):
                # print("Item: " + str(lines[items]))
                # objectiveValues += "+p_" + str(foods) + " " + "y_" + str(times) + "_" + str(foods) + " "
                objectiveValues += "+" + str(lines[foods][nutrition.index(price)]) + " y_" + str(times) + "_" + str(foods) + " "
    objectiveValues  = objectiveValues + "; \n"
    return objectiveValues

def generateConstraints(lines):
    constraintValues = "/* Constraints */ \n"

    # Constraint: Time + Location + Eat or Not
    for places in restaurants:
        for foods in places:
            for times in range(0,3):
                constraintValues = constraintValues + "+y_" + str(times) + "_" + str(foods) + " "
        constraintValues += "<= 2; \n"

    # Constraint: Can only get each type of food once a day
    for places in restaurants:
        for foods in places:
            for times in range(0,3):
                constraintValues += "+y_" + str(times) + "_"  + str(foods) + " "
            constraintValues += "<= 1; \n"

    # # Constraint: Price
    # for places in restaurants:
    #     for foods in places:
    #         constraintValues += "p_" + str(foods) + " = " + str(lines[foods][nutrition.index(price)]) + "; \n"

    # # Constraint: Nutritional Value for Each Item
    # for nut in nutritionRange:
    #     for places in restaurants:
    #         for foods in places:
    #             constraintValues += nutrition[nut][0] + "_" + str(foods) + \
    #                                 " = " + str(lines[foods][nutrition.index(nutrition[nut])]) + "; \n"

    #Constraint: Min and Max for each Nutritional Value
    for nut in nutritionRange:
        # for places in restaurants:
        #     for foods in places:
        #         for times in range(0,3):
        #             constraintValues += "+" + nutrition[nut][0] + "_" + str(foods) + \
        #                                 " y_" + str(times) + "_"  + str(foods) + " "
        # constraintValues += " >= " + str(nutrition[nut][1]) + "; \n"

        for places in restaurants:
            for foods in places:
                for times in range(0, 3):
                    constraintValues += "+" + str(lines[foods][nutrition.index(nutrition[nut])]) + \
                                        " y_" + str(times) + "_" + str(foods) + " "
        constraintValues += " >= " + str(nutrition[nut][1]) + "; \n"

        # for places in restaurants:
        #     for foods in places:
        #         for times in range(0, 3):
        #             constraintValues += "+" + nutrition[nut][0] + "_" + str(foods) + \
        #                                 " y_" + str(times) + "_" + str(foods) + " "
        # constraintValues += " <= " + str(nutrition[nut][2]) + "; \n"

        for places in restaurants:
            for foods in places:
                for times in range(0, 3):
                    constraintValues += "+" + str(lines[foods][nutrition.index(nutrition[nut])]) + \
                                        " y_" + str(times) + "_" + str(foods) + " "
        constraintValues += " <= " + str(nutrition[nut][2]) + "; \n"

    # Constraint: Need at least 3 meals
    for times in range(0, 3):
        for places in restaurants:
            for food in places:
                constraintValues += "+y_" + str(times) + "_" + str(food) + " "
        constraintValues += " >= 1; \n"

    # Constraint: Binary values
    constraintValues = constraintValues + "bin "
    for values in range(0, 23):
        for times in range(0,3):
            constraintValues = constraintValues + "y_" + str(times) + "_" + str(values) + ", "

    constraintValues = constraintValues[:-2] + ";"
    return constraintValues

lines = readCSV(fileName)
upperLower = readCSVUpperLower(fileNameUpperLower)
generateUpperLower(upperLower)
print(generateObjective(lines))
print(generateConstraints(lines))

f1 = open('./lpproblem.lp', 'w+')
f1.write(generateObjective(lines))
f1.write(generateConstraints(lines))

f2 = open('./lpproblem.txt', 'w+')
f2.write(generateObjective(lines))
f2.write(generateConstraints(lines))