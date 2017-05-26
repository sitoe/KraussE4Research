import csv

file_name = 'E4_S17_MDP_Section_1_Team_4'
file_type = '.csv'

# file_names = [file for Section x Team 1
#               file for Section x Team 2
#               file for Section x Team 3
#               file for Section x Team 4
#               file for Section x Team 5
#               file for Section x Team 6]


id_row = 3

# each id corresponds to a comment
# we need to average the scores of each comment
# then find all comments of same id and average the average scores

num_ratings = 2 #number of ratings per comment
# num_ratings = [num per comment from team 1
#                num per comment from team 2
#                num per comment from team 3
#                num per comment from team 4
#                num per comment from team 5
#                num per comment from team 6]
total_comments = 54 #number of comments made for this team

# format as {'student ID': 'cumulative score for tone, etc.'}
totalEaseOfUse = {}
totalTone = {}
totalOriginality = {}
totalImportance = {}
totalComments = {}

# format as {'student ID': ['average ease of use', 'average tone', 'average originality', 'average importance']}
id_scores = {}

survey_sections = {'ids':'ID1', # first ID
		   'comments':'QID3_1'} # modify this depending on the row name of the first comment


def main():
    with open(file_name + file_type, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.next()

        #comment number i corresponds with IDi

        rowCounter = 0; 
        score = range(num_ratings)
        for row in reader:
        	#score[0] stores the row of comments and ID colunm names
        	#the rest store student ids and comment scores
        	#scores: ease of use, tone, originality, importance
        	score[rowCounter] = row #score row 1
        	#print score[rowCounter]
        	rowCounter += 1

    #print rowCounter
    for i in range(total_comments):
        col =  2*(i+1) #keeps track of columns for new comments (QIDcol_n) where n is 1-4 for scores
        #col =  1+ 2*(i+1) 
        ID = score[0]['ID' + str(i+1)]
        #print ID
        for r in range(rowCounter):
            ease = float(score[r]['QID' + str(col) + '_1'])
            tone = float(score[r]['QID' + str(col) + '_2'])
            orig = float(score[r]['QID' + str(col) + '_3'])
            if (col == 42):
                impo = 3
            else:
                impo = float(score[r]['QID' + str(col) + '_4'])
            if totalEaseOfUse.has_key(ID): #if one dictonary has the student's ID, they all should
                totalEaseOfUse[ID] = totalEaseOfUse[ID] + ease
                totalTone[ID] = totalTone[ID] + tone
                totalOriginality[ID] = totalOriginality[ID] + orig
                totalImportance[ID] = totalImportance[ID] + impo
            else:
                totalEaseOfUse[ID] = ease
                totalTone[ID] = tone
                totalOriginality[ID] = orig
                totalImportance[ID] = impo
                totalComments[ID] = 0.0
        totalComments[ID] += 1.0

    #this will calculate average scores across all teams in a section
    #we'll need the average for each team, then average those over total teams in section
    for key in totalEaseOfUse.keys(): #when importing multiple files, take out of file_names loop
        avgEase = totalEaseOfUse[key]/(totalComments[key]*num_ratings) #change to num_ratings[num]
        avgTone = totalTone[key]/(totalComments[key]*num_ratings)
        avgOrig = totalOriginality[key]/(totalComments[key]*num_ratings)
        avgImpo = totalImportance[key]/(totalComments[key]*num_ratings)
        avgScores = [avgEase, avgTone, avgOrig, avgImpo, totalComments[key]]
        id_scores[key] = avgScores
    write_scores()

def write_scores():
    f = open('student_scoresS1_T4.csv', 'w+')
    f.write('student_id, average_ease_of_use, average_tone, average_originality, average_importance, total_comments\n')
    for key in id_scores.keys():
        f.write(key)
        f.write(',')
        f.write(str(id_scores[key][0]))
        f.write(',')
        f.write(str(id_scores[key][1]))
        f.write(',')
        f.write(str(id_scores[key][2]))
        f.write(',')
        f.write(str(id_scores[key][3]))
        f.write(',')
        f.write(str(id_scores[key][4]))
        f.write('\n')
    f.close




if __name__ == "__main__":
    main()

