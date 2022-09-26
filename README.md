# Association-Rule-Mining

a. Teammates:
Paras Tehria - pt2557
Sakshi Arora - sa3871


b. Files Submitted :
project3.py readme.txt example-run.txt Integrated_Dataset.csv


c. Commands for running :
python3 project3.py Integrate_Dataset.csv <min_support> <min_confidence>


We used min_support of 0.1 and confidence of 0.5 for testing purposes

We used the Civilian Complaint Review Board (CCRB) - Allegations Closed dataset.
From this dataset, we used the Allegation FADO Type, Allegation, Complaint Outcome Path, Complaint Disposition, Borough Of Incident and Patrol
Borough Of Incident columns and removed the remaining columns like run date, allegation id, unique random complaint id ets to get meaningful association rules.
We also cropped the dataset to include 1500 rows from the dataset and removed the column names.


We used min_support of 0.1 and confidence of 0.5 for testing purposes. The association rules generated are of the kind : gun pointed implies full investigation which are interesting
as they tell us about what kind of crimes have warranted full investigations and which have been truncated. We chose this dataset to get some insights and
the relationships between types of crimes and boroughs and other similar associations.


Internal Structure of the project:-
We have used apriori algorithm for this task. We first generate all possible itemset with support greater than the
threshold(0.1 in our case). Itemset generation step includes combining and pruning itemset from the previous iteration.
Once we have the itemset we find associations with confidence value greater than the threshold(0.5 in our case)
