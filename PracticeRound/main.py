from itertools import combinations
import operator


class Pizza:
    def __init__(self, total_ingredients, ingredients, index):
        self.ingredients = ingredients
        self.index = index
        self.total_ingredients = total_ingredients

    def add_ingredients(self, ingredients):
        for ingredient in self.ingredients:
            if ingredient not in ingredients:
                ingredients.append(ingredient)
        return ingredients


class Order:
    def __init__(self, size_team, pizzas):
        self.size_team = size_team
        self.pizzas = pizzas
        self.score = 0

    def get_score(self):
        ingredients = []
        for pizza in self.pizzas:
            ingredients = pizza.add_ingredients(ingredients)
        return len(ingredients) ** 2


def get_pizza(pizzas, team_pizzas):
    # if (len(team_pizzas) == 0):
    #     return pizzas.pop(0)
    return pizzas.pop(0)

    # ingredients = []
    # for pizza in team_pizzas:
    #     ingredients = pizza.add_ingredients(ingredients)

    # filtered_pizzas = [pizza for pizza in pizzas if pizza.ingredients.some(item => !ingredients.includes(item))]


def get_result(teams, pizzas):
    result = {
        "number_teams": len(teams),
        "orders": [],
        "score": 0
    }

    # Reset list of pizzas for each teams combination
    mutable_pizzas = pizzas.copy()
    for size_team in teams:
        team_pizzas = []
        for i in range(size_team):
            # Select pizza to add to the team order
            team_pizzas.append(get_pizza(mutable_pizzas, team_pizzas))
        order = Order(size_team, team_pizzas)
        result["score"] += order.get_score()
        result["orders"].append(order)

    return result


# def get_combinations(total_pizzas, total_team_2, total_team_3, total_team_4):
#     # list of possible orders
#     teams = []
#     # all teams possibles (ex: [2, 3, 3, 4])
#     for x in range(int(total_team_2)):
#         teams.append(2)
#     for x in range(int(total_team_3)):
#         teams.append(3)
#     for x in range(int(total_team_4)):
#         teams.append(4)

#     results = []
#     for x in range(len(teams)):
#         combinaisons = list(combinations(teams, x))
#         if combinaisons != [()]:
#             # print(list(combinations(teams ,x)))
#             for combinaison in combinaisons:
#                 if sum(combinaison) <= int(total_pizzas) and combinaison not in results:
#                     results.append(combinaison)

    # results = unique combination per group (ex: [(2,), (3,), (4,), (2, 3)])
    # print(results)
    # return results


def get_combinations(total_pizzas, total_team_2, total_team_3, total_team_4):
    results = []
    total_pizzas = int(total_pizzas)
    for x in range(int(total_team_4)):
        if not total_pizzas < 4:
            total_pizzas -= 4
            #selected_4_person_team_num += 1
            results.append(4)

    for x in range(int(total_team_3)):
        if not total_pizzas < 3:
            total_pizzas -= 3
            #selected_3_person_team_num += 1
            results.append(3)

    for x in range(int(total_team_2)):
        if not total_pizzas < 2:
            total_pizzas -= 2
            #selected_2_person_team_num += 1
            results.append(2)

        #total_order = selected_2_person_team_num + selected_3_person_team_num + selected_4_person_team_num
    # print([results])
    return results


def print_result(combination):
    file = open("output6.txt", "w")
    print(combination["number_teams"])
    file.write(str(combination["number_teams"])+"\n")
    for order in combination["orders"]:
        result_team = str(order.size_team)
        for pizza in order.pizzas:
            result_team = result_team + " " + str(pizza.index)
        file.write(result_team+"\n")
        print(result_team)
    file.close()


def main():
    # parse inputs from text file
    f = open("e_many_teams.in", "r")
    input_data = f.read().splitlines()
    for i in range(len(input_data)):
        input_data[i] = input_data[i].strip().split(' ')

    # parse inputs from console
    # input_data = input().strip.split(' ')
    # for i in range(input_data[0]):
    #     input_data.append(input().split)

    # print(input_data)
    total_pizzas, total_team_2, total_team_3, total_team_4 = input_data[0]
    total_teams = int(total_team_2) + int(total_team_3) + int(total_team_4)

    pizzas = []
    input_pizzas = input_data[1:]
    for i in range(int(total_pizzas)):
        pizza = Pizza(int(input_pizzas[i][0]), input_pizzas[i][1:], i)
        pizzas.append(pizza)

    # pizzas = sorted(pizzas, key=operator.attrgetter('total_ingredients'), reverse=True)

    # nombre d'ingrédients
    # doublon de pizzas
    # occurences d'ingrédients
    combinaisons = get_combinations(total_pizzas, total_team_2, total_team_3, total_team_4)
    result = get_result(combinaisons, pizzas)
    print('score', result["score"])

    print_result(result)


if __name__ == '__main__':
    main()
