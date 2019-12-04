import sys
import numpy as np
import json
import re
import csv
from pyspark import SparkContext

# change get_semantic_type function to add more semantic types
<<<<<<< HEAD
school_level = ['k-2', 'elementary', 'elementary school', 'middle']
borough = ['brooklyn', 'manhattan', 'bronx', 'staten island', 'queens']

=======
school_level = ['elementary', 'high school', 'high school transfer', 'k-2',
                'k-3', 'k-8', 'middle', 'yabc', 'elementary school', 'k-8 school',
                'middle school', 'transfer school', 'transfer high school', 'd75']
neighborhood_name = ['arrochar-shore acres', 'dongan hills', 'grant city', 'grymes hill',
          'new springville', 'rosebank', 'silver lake', 'sunnyside', 'tompkinsville',
          'bedford park/norwood', 'belmont', 'bronxdale', 'city island', 'east tremont',
          'highbridge/morris heights', 'kingsbridge/jerome park', 'morris park/van nest',
          'morrisania/longwood', 'mott haven/port morris', 'parkchester',
          'pelham parkway south', 'riverdale', 'schuylerville/pelham bay', 'soundview',
          'throgs neck', 'williamsbridge', 'airport la guardia', 'astoria', 'bayside',
          'briarwood', 'college point', 'corona', 'elmhurst', 'far rockaway',
          'flushing meadow park', 'flushing-north', 'flushing-south', 'forest hills',
          'glendale', 'hammels', 'howard beach', 'jackson heights', 'jamaica estates',
          'kew gardens', 'little neck', 'long island city', 'maspeth', 'middle village',
          'oakland gardens', 'ozone park', 'rego park', 'ridgewood', 'rockaway park',
          'south ozone park', 'whitestone', 'woodhaven', 'woodside', 'bath beach',
          'bay ridge', 'bedford stuyvesant', 'bensonhurst', 'boerum hill', 'borough park',
          'brighton beach', 'brooklyn heights', 'bushwick', 'canarsie', 'carroll gardens',
          'clinton hill', 'cobble hill', 'cobble hill-west', 'crown heights',
          'downtown-fulton ferry', 'downtown-fulton mall', 'downtown-metrotech',
          'dyker heights', 'east new york', 'flatbush-central', 'flatbush-east',
          'flatbush-lefferts garden', 'flatbush-north', 'fort greene', 'gowanus',
          'gravesend', 'greenpoint', 'kensington', 'madison', 'midwood', 'mill basin',
          'ocean hill', 'ocean parkway-north', 'park slope', 'park slope south',
          'prospect heights', 'sheepshead bay', 'sunset park', 'williamsburg-central',
          'williamsburg-east', 'williamsburg-north', 'williamsburg-south',
          'windsor terrace', 'wyckoff heights', 'hillcrest', 'jamaica']

interest = ['animal science', 'architecture', 'business', 'communications',
            'computer science & technology', 'cosmetology', 'culinary arts',
            'engineering', 'environmental science', 'film/video', 'health professions',
            'hospitality, travel and tourism', 'humanities & interdisciplinary',
            'jrotc', 'law & government', 'performing arts',
            'performing arts/visual art & design', 'science & math', 'teaching',
            'visual art & design', 'zoned']

borough = ['brooklyn', 'manhattan', 'bronx', 'staten island', 'queens', 'k', 'r', 'm', 'x', 'q']
agency = ['311', 'acs', 'bic', 'boe', 'bpl', 'cchr', 'ccrb', 'cuny', 'dca',
          'dcas', 'dcla', 'dcp', 'ddc', 'dep', 'dfta', 'dhs', 'dob', 'doc',
          'doe', 'dof', 'dohmh', 'doi', 'doitt', 'dop', 'doris', 'dot', 'dpr',
          'dsny', 'dvs', 'dycd', 'fdny', 'hpd', 'hra', 'law', 'lpc', 'nycem',
          'nycha', 'nychh', 'nypd', 'nypl', 'oath', 'qpl', 'sbs', 'sca', 'tlc',
          'edc', 'nypl-research', 'ocme']
agency_name = ['admin. for children services', 'board of correction', 'board of elections',
               'brooklyn public library', 'business integrity commission', 'campaign finance board',
               'city clerk', 'city council', 'city university', 'citywide pension contributions',
               'citywide savings initiatives', 'civil service commission', 'civilian complaint review bd.',
               'commission on human rights', 'community boards (all)', 'conflicts of interest board', 'd.o.i.t.t.',
               'debt service', 'department for the aging', 'department of buildings', 'department of city planning',
               'department of consumer affairs', 'department of correction', 'department of cultural affairs',
               'department of education', 'department of finance', 'department of investigation',
               'department of probation', 'department of sanitation', 'department of social services',
               'department of transportation', 'dept health & mental hygiene', 'dept of citywide admin srvces',
               'dept of environmental prot.', 'dept of parks and recreation', 'dept of records & info serv.',
               'dept. of design & construction', 'dept. of emergency management', 'dept. of homeless services',
               "dept. of veterans' services", 'dept. small business services', 'district attorney - bronx',
               'district attorney - kings', 'district attorney - n.y.', 'district attorney - queens',
               'district attorney - richmond', 'energy adjustment', 'equal employment practices com',
               'financial info. serv. agency', 'fire department', 'general reserve', 'health and hospitals corp.',
               'housing preservation & dev.', 'independent budget office', 'landmarks preservation comm.',
               'law department', 'lease adjustment', 'mayoralty', 'miscellaneous', 'new york public library',
               'ny public library - research', 'off. of prosec. & spec. narc.', 'office admin trials & hearings',
               'office of admin. tax appeals', 'office of collective barg.', 'office of payroll admin.',
               'office of the actuary', 'office of the comptroller', 'otps inflation adjustment', 'police department',
               'president,borough of brooklyn', 'president,borough of manhattan', 'president,borough of queens',
               'president,borough of s.i.', 'president,borough of the bronx', 'public administrator - bronx',
               'public administrator - n.y.', 'public administrator - queens', 'public administrator -richmond',
               'public administrator- brooklyn', 'public advocate', 'queens borough public library',
               'taxi & limousine commission', 'youth & community development']
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 1, size_y - 1])
>>>>>>> UPDATE: part two, type with list

def get_semantic_type(line):
    if re.match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", line) is not None:
        return "WebSites"
    elif line in school_level:
        return "School Level"
    elif line in borough:
        return "Borough"
    elif line in neighborhood_name:
        return "Neighborhood"
    elif line in interest:
        return "Area Of Study"
    elif line in agency:
        return "Agency"
    elif line in agency_name:
        return "Agency Name"
    elif re.match("(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", line) is not None:
        return "Phone Number"
    elif re.match("\(\d+, \d+\)", line) is not None:
        return "LAT/LON coordinates"
    elif re.match("r\d[-(0-9a-z)]+", line) is not None:
        return "Building Classification"
    return "Others"


def semanticCheck(sc, file_name):
    file_name = file_name.strip()[1:-1]
    file_path = "/user/hm74/NYCColumns/" + str(file_name)
    data = sc.textFile(file_path, 1).mapPartitions(
        lambda x: csv.reader(x, delimiter='\t', quotechar='"'))
    # key is semantic type, value is count
    semantic_information = {}
    semantic_type = data.map(lambda x: (get_semantic_type(
        x[0].lower()), int(x[1]))).reduceByKey(lambda x, y: x+y).collect()
    for row in semantic_type:
        semantic_information["semantic_type"] = row[0]
        semantic_information["count"] = row[1]
    with open(file_name+'_semantic_result.json', 'w') as fp:
        json.dump({"semantic_types": semantic_information}, fp)


sc = SparkContext()

file_list = open('cluster3.txt').readline().strip().replace(' ', '').split(",")

for item in file_list[1:10]:
    semanticCheck(sc, item)
#for i in range(5):
#    semanticCheck(sc, file_list[i])
