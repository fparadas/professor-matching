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
    # we start every school and position to be free
    for school, position_list in school_positions.items():
        free_schools.append(school)
        for position in position_list:
            free_positions.append((school, position))

def clear_preference_list():
    # starting professor preference list
    for professor in professor_preferences_entry.keys():
        professor_preferences[professor] = []

    # the professor list will only allow schools who would accept him, so we remove the other from there
    # the order in this list is very important
    for professor in professor_preferences.keys():

        for school in professor_preferences_entry[professor]:
            positions = [position for position in school_positions[school] if position <= professor_abilities[professor]]
            
            if len(positions) > 0:
                professor_preferences[professor].append(school)

    # starting the schools preference list
    for school in school_positions.keys():
        school_preferences[school] = {}
        for position in school_positions[school]:
            school_preferences[school][position] = []
    
    # the school preference list will be every professor that has at leat the qualification needed for the position
    # the order in this list is not important
    for school, position_list in school_positions.items():

        for position in position_list:

            for qualification in abilities_professor.keys():
                if position <= qualification:
                    school_preferences[school][position] += abilities_professor[qualification]

def is_matched(school):
    taken = [couple for couple in matches if school in couple]

    return len(taken) > 0

def assign(school, professor, position):

    # append the new match to the match list
    matches.append((professor, school, position))

    # if the assigned school is in the free_schools list, we remove it
    if school in free_schools:
        free_schools.remove(school)

    print("Matched {} with {} at position {}".format(professor, school, position))

def unassign(pair):
    # remove the match from the matches list
    matches.remove(pair)

    professor, school, position = pair

    # if the school is not on another match, we append it back to free_schools list
    if not is_matched(school):
        free_schools.append(school)

    # we append the position back to the free positions list
    free_positions.append((school, position))

    print("Unmatched {} with {} at position {}".format(professor, school, position))

def try_match(school, professor, position, free=False):
    print("Trying to match {} with {} at position {}".format(school, professor, position))
    school_has_other_match = True
    taken_match = [couple for couple in matches if professor in couple]

    # if current professor is not already allocated, match it with the school
    if len(taken_match) == 0:
        assign(school, professor, position)
    
    else:
        try:
            # current school index in the professor preference list, signifing the professor preference for it
            current_school = professor_preferences[professor].index(taken_match[0][1])
        except:
            # if current school not in professor preference list, we give a number bigger then the lenght of it
            current_school = 100

        try:
            # potential school index in the professor preference list
            potential_school = professor_preferences[professor].index(school)
        except:

            # if potential school not in the list, we give it a number bigger then the lenght of it
            # and bigger then the current_school max index possible
            potential_school = 101

        #if we want to unmatch school only if it is on another match
        if free:
            school_has_other_match = len([couple for couple in matches if taken_match[0][1] in couple]) > 1

        # if the potential school preference is bigger then the current and, optionally, the current is already on another match
        if potential_school < current_school or taken_match[0][2] > position and school_has_other_match:

            # we unassign the old match
            unassign(taken_match[0])

            # we assign the new match
            assign(school, professor, position)

        else:
            # else, we put the position back to the possible positions list
            free_positions.append((school, position))

def school_optimal():
    clear_preference_list()
    init_free_schools()

    # first loop to allocate at least one professor for each school
    while len(free_schools) > 0:

        school = free_schools.pop()

        position = [x[1] for x in free_positions if x[0] == school][0]

        free_positions.remove((school, position))

        professor = school_preferences[school][position].pop()

        try_match(school, professor, position)

    #     pprint.pprint(free_schools)
    #     pprint.pprint(len(matches))
    

    # second loop to finish the matching keeping the condition from the first loop true
    school, position = free_positions.pop()

    while len(free_positions) > 0:  
        if len(school_preferences[school][position]) > 0:

            professor = school_preferences[school][position].pop()

            try_match(school, professor, position, free= True)

        school, position = free_positions.pop()



        



if __name__ == "__main__":
    fname  = sys.argv[1]
    read_file(fname)

    school_optimal()

    print("Emparelhamentos realizados ordenados por escolas:")
    pprint.pprint(sorted(matches, key= lambda x: int(x[1][1:])))
    pprint.pprint("Professores alocados estavelmente: {}".format(len(matches)))