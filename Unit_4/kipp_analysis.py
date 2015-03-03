import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from os.path import expanduser

home = expanduser("~")

grade_path = home + "/Dropbox/Coding/python-data-science/Eiben_StoredGrades.csv"
regents_path = home + "/Dropbox/Coding/python-data-science/Eiben_RegentsScores.csv"

#load csv
gradeData = pd.read_csv(grade_path)
regentsData = pd.read_csv(regents_path)

#determine column titles
list(regentsData.columns.values)

#remove columns
gradeData = gradeData[["COURSE_NAME", "PERIOD", "STUDENT_NUMBER","STUDENT_GRADE_LEVEL_STORED", "COHORT", "IEP", "ETHNICITY", "GENDER", "MIDDLE_SCHOOL", "GRADE", "PERCENT", "STORECODE", "DEPARTMENT_COURSE"]]
regentsData = regentsData[["STUDENT_NUMBER", "ETHNICITY", "GENDER", "CURRENTGRADELEVEL", "COHORT", "IEP", "TESTGRADELEVEL", "EXAM", "SCORENAME", "TESTDATE", "TESTYEAR", "NUMSCORE"]]

#statistical summary
print regentsData.describe()