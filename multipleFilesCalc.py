import csv

#file_name = 'TESTING_SURVEY'
file_type = '.csv'

teams = 6

file_names = ['E4_S17_MDP_Section_3_Team_1',
              'E4_S17_MDP_Section_3_Team_2',
              'E4_S17_MDP_Section_3_Team_3',
              'E4_S17_MDP_Section_3_Team_4',
              'E4_S17_MDP_Section_3_Team_5',
              'E4_S17_MDP_Section_3_Team_6']


id_row = 3

# each id corresponds to a comment
# we need to average the scores of each comment
# then find all comments of same id and average the average scores

#num_ratings = 1 #number of ratings per comment
num_ratingsList = [2, 2, 4, 4, 4, 4]
               # [num per comment from team 1
               # num per comment from team 2
               # num per comment from team 3
               # num per comment from team 4
               # num per comment from team 5
               # num per comment from team 6]
total_comments = [78, 70, 62, 59, 60, 76] #number of comments made for this team

# format as {'student ID': 'cumulative score for tone, etc.'}
totalEaseOfUse = {}
totalTone = {}
totalOriginality = {}
totalImportance = {}
totalComments = {}
totalRatings = {}


# format as {'student ID': ['average ease of use', 'average tone', 'average originality', 'average importance']}
id_scores = {}

survey_sections = {'ids':'ID1', # first ID
		   'comments':'QID3_1'} # modify this depending on the row name of the first comment


def main():
    
    for i in range(len(file_names)):
        with open(file_names[i] + file_type, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            reader.next()

            #comment number i corresponds with IDi
            rowCounter = 0;
            score = range(num_ratingsList[i])
            for row in reader:
            	#score[0] stores the row of comments and ID colunm names
            	#the rest store student ids and comment scores
            	#scores: ease of use, tone, originality, importance
            	score[rowCounter] = row #score row 1
            	#print score[rowCounter]
            	rowCounter += 1
        for j in range(total_comments[i]):
            #keeps track of columns for new comments (QIDcol_n) where n is 1-4 for scores
            col = 2 + 2*(j+1) # for odd col
            print col
            ID = score[0]['ID' + str(j+1)]
            #print ID

            for r in range(rowCounter):
                if (score[r]['QID' + str(col) + '_1'] == ''): #checks if entry is blank
                    ease = 3.0
                else:
                    ease = float(score[r]['QID' + str(col) + '_1'])
                
                if (score[r]['QID' + str(col) + '_2'] == ''): #checks if entry is blank
                    tone = 3.0
                else:
                    tone = float(score[r]['QID' + str(col) + '_2'])
                
                if (score[r]['QID' + str(col) + '_3'] == ''): #checks if entry is blank
                    orig = 3.0
                else:
                    orig = float(score[r]['QID' + str(col) + '_3'])
                
                if (score[r]['QID' + str(col) + '_4'] == ''): #checks if entry is blank
                    impo = 3.0
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
                    totalComments[ID] = [0,0,0,0,0,0]
                    totalRatings[ID] = [0,0,0,0,0,0]
            totalRatings[ID][i] = num_ratingsList[i]
            totalComments[ID][i] += 1.0

    
        #this will calculate average scores across all teams in a section
        #we'll need the average for each team, then average those over total teams in section
    for key in totalEaseOfUse.keys(): #when importing multiple files, take out of file_names loop
        print totalRatings[key]
        print totalEaseOfUse[key]
        print totalComments[key]
        c = [x*y for x,y in zip(totalRatings[key], totalComments[key])]
        print c
        avgEase = totalEaseOfUse[key]/sum(c) #change to num_ratings[num]
        avgTone = totalTone[key]/sum(c)
        avgOrig = totalOriginality[key]/sum(c)
        avgImpo = totalImportance[key]/sum(c)
        avgScores = [avgEase, avgTone, avgOrig, avgImpo, sum(totalComments[key])]
        id_scores[key] = avgScores
    write_scores()

def write_scores():
    f = open('student_scoresMultiS3.csv', 'w+')
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

