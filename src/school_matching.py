import sys
import pprint

professor_preferences_entry = {}

professor_preferences = {}

professor_abilities = {}

abilities_professor = {}

school_positions = {}

school_preferences = {}

matches = []

free_professors = []

free_schools = []

free_positions = []

def read_file(filename):
    with open(filename, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            if line[0] == '(':
                member, *preferences = line.replace('(', '').replace(')', '').replace('\n', '').split(':')

                if member[0] == 'P':
                    #deal with professors
                    professor = member.strip().split(',')
                    
                    #add relation in professor_abilities set
                    professor_abilities[professor[0]] = professor[1].strip()

                    if professor[1].strip() not in abilities_professor.keys():
                        abilities_professor[professor[1].strip()] = []
                    
                    abilities_professor[professor[1].strip()].append(professor[0].strip())

                    preferenceList = [preference.strip() for preference in preferences[0].split(',')]

                    for preference in preferenceList:
                        if professor[0] not in professor_preferences_entry.keys():
                            professor_preferences_entry[professor[0]] = [preference]
                        
                        else:
                            professor_preferences_entry[professor[0]].append(preference)


                elif member[0] == 'E':
                    #deal with schools
                    for preference in preferences:

                        if member.strip() not in school_positions.keys():
                            school_positions[member.strip()] = [preference.strip()]
                        else:
                            school_positions[member.strip()].append(preference.strip())
                #else do nothing

def init_free_schools():
    for school, position_list in school_positions.items():
        free_schools.append(school)
        for position in position_list:
            free_positions.append((school, position))

def clear_preference_list():
    for professor in professor_preferences_entry.keys():
        professor_preferences[professor] = []

    for professor in professor_preferences.keys():

        for school in professor_preferences_entry[professor]:
            positions = [position for position in school_positions[school] if position <= professor_abilities[professor]]
            
            if len(positions) > 0:
                professor_preferences[professor].append(school)

    for school in school_positions.keys():
        school_preferences[school] = {}
        for position in school_positions[school]:
            school_preferences[school][position] = []
    
    for school, position_list in school_positions.items():

        for position in position_list:

            for qualification in abilities_professor.keys():
                if position <= qualification:
                    school_preferences[school][position] += abilities_professor[qualification]

    pprint.pprint(school_preferences)

def is_matched(school):
    taken = [couple for couple in matches if school in couple]

    return len(taken) > 0

def assign(school, professor, position):

    matches.append((professor, school, position))

    if school in free_schools:
        free_schools.remove(school)

    print("Matched {} with {} at position {}".format(professor, school, position))

def unassign(pair):
    matches.remove(pair)

    professor, school, position = pair

    if not is_matched(school):
        free_schools.append(school)

    free_positions.append((school, position))

    print("Unmatched {} with {} at position {}".format(professor, school, position))

def try_match(school, professor, position):
    print("Trying to match {} with {} at position {}".format(school, professor, position))
    taken_match = [couple for couple in matches if professor in couple]

    if len(taken_match) == 0:
        assign(school, professor, position)
    
    else:
        try:
            current_school = professor_preferences[professor].index(taken_match[0][1])
        except:
            current_school = 100

        try:
            potential_school = professor_preferences[professor].index(school)
        except:
            potential_school = 101
        
        if potential_school < current_school or taken_match[0][2] > position:
            unassign(taken_match[0])
            assign(school, professor, position)

        else:
            free_positions.append((school, position))

def try_match_free(school, professor, position):
    print("Trying to match {} with {} at position {}".format(school, professor, position))
    taken_match = [couple for couple in matches if professor in couple]

    if len(taken_match) == 0:
        assign(school, professor, position)
    
    else:
        try:
            current_school = professor_preferences[professor].index(taken_match[0][1])
        except:
            current_school = 100

        try:
            potential_school = professor_preferences[professor].index(school)
        except:
            potential_school = 101

        taken_school = [couple for couple in matches if taken_match[0][1] in couple]
        if potential_school < current_school or taken_match[0][2] > position and len(taken_school) > 1:
            unassign(taken_match[0])
            assign(school, professor, position)

        else:
            free_positions.append((school, position))

def school_optimal():
    clear_preference_list()
    init_free_schools()
    pprint.pprint([free_schools, free_positions])

    # this will break for now but the logic is here
    while len(free_schools) > 0:

        school = free_schools.pop()

        position = [x[1] for x in free_positions if x[0] == school][0]

        free_positions.remove((school, position))

        professor = school_preferences[school][position].pop()

        try_match(school, professor, position)

    #     pprint.pprint(free_schools)
    #     pprint.pprint(len(matches))
    

    school, position = free_positions.pop()

    while len(free_positions) > 0:  
        if len(school_preferences[school][position]) > 0:

            professor = school_preferences[school][position].pop()

            try_match_free(school, professor, position)

        school, position = free_positions.pop()



        



if __name__ == "__main__":
    fname  = sys.argv[1]
    read_file(fname)

    school_optimal()

    pprint.pprint(sorted(matches, key= lambda x: int(x[1][1:])))
    pprint.pprint(len(matches))