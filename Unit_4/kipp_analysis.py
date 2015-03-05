import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from os.path import expanduser

home = expanduser("~")

grade_path = home + "/Dropbox/Coding/python-data-science/Eiben_StoredGrades_WithSectionID.csv"
regents_path = home + "/Dropbox/Coding/python-data-science/Eiben_RegentsScores.csv"
#assignments_path = home + "/Dropbox/Coding/python-data-science/Assignments_All.csv"

#load csv
gradeData = pd.read_csv(grade_path)
regentsData = pd.read_csv(regents_path)
#assignmentsData = pd.read_csv(assignments_path)

#determine column titles
# print list(regentsData.columns.values

print gradeData['PERIOD'].unique()