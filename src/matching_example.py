men_preferences = {
    'a': ['e', 'f', 'g', 'h'],
    'b': ['f', 'e', 'h', 'g'],
    'c': ['e', 'h', 'g', 'f'],
    'd': ['h', 'g', 'f', 'e'],
}

women_preferences = {
    'e': ['b', 'a', 'd', 'c'],
    'f': ['d', 'c', 'b', 'a'],
    'g': ['b', 'c', 'a', 'd'],
    'h': ['a', 'b', 'c', 'd'],
}

engagements = []

free_men = []

def init_free_man():
    for man in men_preferences.keys():
        free_men.append(man)

def begin_matching(man):
    for woman in men_preferences[man]:

        taken_match = [couple for couple in engagements if woman in couple]

        if len(taken_match) == 0: #woman is single
            engagements.append([man, woman])
            free_men.remove(man)

            break
        else:

            current_man = women_preferences[woman].index(taken_match[0][0])
            potential_man = women_preferences[woman].index(man)

            if current_man > potential_man:
                free_men.append(taken_match[0][0])

                free_men.remove(man)

                taken_match[0][0] = man #pass by reference


def stable_matching():
    while(len(free_men) > 0):
        for man in free_men:
            begin_matching(man)

def main():
    init_free_man()
    stable_matching()

    print(engagements)

main()