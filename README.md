I read the original data file line by line.
 If it is the first line, I get the index for each 
 column in the header. If it is not the first line, 
 I process line to get the relevant string, 
 and then divide it into three separate strings, 
 drug name, patient and cost. Then, I use a dictionary
 to save these information by drug name. Then, 
 I transform the dictionary to list to do the sorting. 
 After the sorting, I save the results into the output file. 