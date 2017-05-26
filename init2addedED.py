import csv

##########
# Instruction: Go to Data&Analysis > Export&Import > Export Data > Export Data with Legacy Format
# Download the csv file in the same directory as this python script
# Open terminal, type: "python init.py" and return
# It will produce 6 (probably) files each named result(number).txt
# Create a survey by first copying a template (TODO: WHICH ONE) and import one of the result(number).txt file
##########

##########
# Setting some variables outside of main() so we can easily change them if necessary
# AND so that they are accessible by functions other than main() as well
##########

# Survey file name minus the team number
# & file type (if not .csv, the code needs to change..)
file_name = 'E4_S17_MDP_Design_Review_Section_3'
file_type = '.csv'

# Look at the csv file. How many rows do we not care about?
# (include the row with column names)
exclude_rows = 1

# Look at the file again. Are these column names correctly assigned?
# If not, change them
personal_info = {'last_name': 'Q5',
                 'first_name': 'Q6',
                 'student_id': 'Q7',
                 'gender': 'Q9',
                 'team': 'Q4'}

# column names for comments are irregular. Fill out the variables belows accordingly
# col_name_rules = { nth comment group : {'has_decimal': true if in the format of 'Q3.1' / false if in the format of 'Q499',
#                                           'starting_number': 3 or 499 or whatever}
col_name_rules = {'1' : {'has_decimal' : 'false', 'starting_number' : 14},
                  '2' : {'has_decimal' : 'false', 'starting_number' : 45},
                  '3' : {'has_decimal' : 'false', 'starting_number' : 76},
                  '4' : {'has_decimal' : 'false', 'starting_number' : 107},
                  '5' : {'has_decimal' : 'false', 'starting_number' : 138}}

# Up to how many comments are we allowing the students to provide?
max_comments = 9

# How many subquestions asked per comment, not including the comment?
sub_qs = 2

# number of teams in this section
teams = 6

# Obviously each team will evaluate (teams - 1) presentations..
# Created a variable so that it's super obvious where it's used
# But it's only used once so honestly it shouldn't exist
num_presentations = teams - 1


# Set for student name and hash (id)
# Each item in the set looks like this: ('lastName,firstName', 'hash', 'gender', 'team')
# consult this doc for accessing and setting values in a python set:
# https://docs.python.org/2/library/sets.html#module-sets
student_hash = set()

# List of comments for each group
# Each comment looks like this: ('commenter hash', 'commenter team', comment')
comment_lists = list()
for team in range(teams + 1): # 0 ~ 6 while first row is empty
    comment_lists.append(list())



# method for creating a "secret id" (called hash) for a student. hash is a built-in function fyi
def hash_student(last_name, first_name, student_id):
    return hash((last_name, first_name, student_id))

def main():
    with open(file_name + file_type, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # This line is causing problems!
        for skip_row in range(exclude_rows):
            reader.next()

        # Iterating over all the rows in a file. Each row = commenter
        for row in reader:
            # create a hash id per student and add to the set
            last_name = row[personal_info['last_name']]
            first_name = row[personal_info['first_name']]
            student_id = row[personal_info['student_id']]
            gender = row[personal_info['gender']]
            commenting_team = row[personal_info['team']]

            hash_id = hash_student(last_name, first_name, student_id)
            
            student_hash.add((last_name + ',' + first_name, hash_id, gender, team))

            # check the rest of the columns for comments
            for comment_group_number in range(1, num_presentations + 1): 

                starting_number = col_name_rules[str(comment_group_number)]['starting_number']
                if col_name_rules[str(comment_group_number)]['has_decimal'] == 'true':
                    presenting_team = row['Q' + str(starting_number) + '.1'] # "Q3.1"

                    col_decimal = 3 # skip to 3, where comments start

                    for comment_num in range(max_comments):
                        if comment_num == 5:
                            col_decimal += 1

                        comment = row['Q' + str(starting_number) + '.' + str(col_decimal)]

                        if comment: # Checking if the comment exists
                            (comment_lists[int(presenting_team)]).append((student_id, commenting_team, comment)) # Breaks because trying to convert a string into integer

                        col_decimal += 1

                        for sub_q in range(sub_qs):
                            # May use later to collect self topic and importance stuff
                            col_decimal += 1
                else:
                    presenting_team = row['Q' + str(starting_number)] # "Q499"
                    starting_number += 2 # skip to where comments start

                    for comment_num in range(max_comments):
                        if comment_num == 5:
                            starting_number += 1

                        comment = row['Q' + str(starting_number)]

                        if comment:
                            (comment_lists[int(presenting_team)]).append((student_id, commenting_team, comment)) # Breaks because trying to convert a string into integer

                        starting_number += 1

                        for sub_q in range(sub_qs):
                            starting_number += 1



    # -- testing --
    # print_comment_list(comment_lists)
    # print_student_list(student_hash)
    # -- survey of survey --
    write_survey_file()
    # -- making some files that helps check that response.py worked--
    write_comment_list(comment_lists)
    count_comments(comment_lists)
    write_student_set(student_hash)



def write_comment_list(this_list):
    ind = 0
    for row in this_list:
        if ind != 0:
            f = open('comments_for_team'+str(ind)+'.csv', 'w+')
            f.write('student_id,team,comment\n')
            for col in row:
                f.write(str(col[0]))
                f.write(',')
                f.write(str(col[1]))
                f.write(',')
                f.write(col[2])
                f.write('\n')
            f.close
        ind += 1

def count_comments(this_list):
    count_map = {} # 'hash': [t1Comment, t2Comment, etc.]
    ind = 0
    for row in this_list:
        if ind != 0:
            for col in row:
                s_hash = str(col[0])
                team = col[1]
                if s_hash not in count_map:
                    count_map[s_hash] = [team,0,0,0,0,0,0]
                
                count_map[s_hash][ind] += 1
        ind += 1

    f = open('comment_counts.csv', 'w+')
    f.write('student_id,team,')
    for i in range(teams):
        f.write(str(i+1))
        f.write(',')
    f.write('\n')

    for sHash, array in count_map.iteritems(): 
        f.write(sHash+',')
        for j in range(len(array)):
            f.write(str(array[j]))
            f.write(',')
        f.write('\n')
    f.close

def write_student_set(this_set): # testing that comments are gathered correctly
    f = open('section_student_hash.csv', 'w+')
    f.write("hash,lastname,firstname,gender\n")
    for row in this_set:
        f.write(str(row[1])) # hash first
        f.write(',')
        f.write(row[0]) # name second
        f.write(',')
        f.write(row[2]) # gender third
        f.write('\n')
    f.close

def write_survey_file():
    for x in range(teams): # teams is one longer than the number of teams
        team_number = x + 1
        f = open('MDPSection3Team'+str(team_number)+'.txt', 'w+')
        group_comments = comment_lists[team_number]
        f.write('[[AdvancedFormat]]\n\n')

        f.write('[[Question:Text]]\n\n')
        f.write('\n\n')

        for i in range(len(group_comments)):
            f.write('[[ED:ID' + str(i+1) + ':' + str(group_comments[i][0]) +']]\n')
            f.write('[[Question:Matrix]]\n')
            f.write(str(i+1) + '. ' + group_comments[i][2] + '\n\n')
            f.write('[[AdvancedChoices]]\n[[Choice]]\nEase of use\n[[Choice]]\nTone\n[[Choice]]\nOriginality\n[[Choice]]\nImportance\n\n')
            f.write('[[AdvancedAnswers]]\n[[Answer:1]]\n1\n[[Answer:2]]\n2\n[[Answer:3]]\n3\n[[Answer:4]]\n4\n[[Answer:5]]\n5\n\n')

            f.write('[[Question:MC:SingleAnswer:Horizontal]]\n')
            f.write('Please indicate the primary topic of comment ' + str(i+1) + '.\n\n')
            f.write('[[Choices]]\nPresentation\nDesign artifact\nDesign process\nOther\n\n')

        f.write('[[Question:TextEntry:SingleLine]]\n')
        f.write('Please identify three best comments (i.e. 1,2,3).\n\n')

        f.write('[[Question:TextEntry:SingleLine]]\n')
        f.write('Please identify three worst comments (i.e. 1,2,3).\n\n')

        f.close

def print_comment_list(this_list):
    # The first row of this list is going to be empty.
    ind = 0

    for row in this_list:
        if ind != 0:
            print ("Comments for team " , str(ind))
        for col in row:
                print (col)

        ind += 1
        print

def print_student_list(this_list): # testing that comments are gathered correctly
    for row in this_list:
        print (row)


if __name__ == "__main__":
    main()