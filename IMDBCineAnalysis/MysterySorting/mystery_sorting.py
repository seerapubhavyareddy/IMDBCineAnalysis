import pandas as pd
import heapq as hp
import os
import csv
import sys
sys.path.append("../Sorting_Algorithms")
from sorting_algos import merge_sort


column_names= ['tconst', 'primaryTitle', 'originalTitle', 'startYear',
               'runtimeMinutes', 'genres', 'averageRating', 'numVotes', 'ordering',
               'category', 'job', 'seasonNumber', 'episodeNumber', 'primaryName', 'birthYear',
               'deathYear', 'primaryProfession']

####################################################################################
# Donot Modify this Code
####################################################################################
class FixedSizeList(list):
    def __init__(self, size):
        self.max_size = size

    def append(self, item):
        if len(self) >= self.max_size:
            raise Exception("Cannot add item. List is full.")
        else:
            super().append(item)
            
            
####################################################################################
# Cleaning Folder
####################################################################################
def clear_folder(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))

    
####################################################################################
# Mystery_Function
####################################################################################
def Mystery_Function(file_path, memory_limitation, columns):
    
    #First we need to clean the folder before starting the sorting
    clear_folder("Final")
    
    #file_List contains the names of all the individual files
    #files contains all the file pointers pointing to files first position
    file_list, files = [], []
    
    #no_of_files denotes the number of files present in individual folder
    no_of_files = len([entry for entry in os.listdir(file_path) 
                       if os.path.isfile(os.path.join(file_path, entry))])
    
    
    for i in range(no_of_files):
        file_list.append(file_path + "/Sorted_{}.csv".format(i+1))
    

    for file_name in file_list:
        files.append(open(file_name, "r", encoding='utf-8'))
    
    #chunks_2000 always make sure given memeory_limitation is never exceeded
    chunks_2000 = FixedSizeList(memory_limitation)
    chunks_2000 = [csv.reader(f) for f in files]
    
    #we will collect all the headers of all files into a list
    column_headers = [next(chunk) for chunk in chunks_2000]
    
    #we will collect all the first row elements of the files into a list
    current_chunk = [next(chunk) for chunk in chunks_2000]
    
    #We will maintain a list of boolean values to check if our code reached the end or not
    reached_end = [False] * len(file_list)
    
    os.makedirs("Final", exist_ok=True)
    row_counter = 0
    file_number = 1
    
    #First we will build a min-heap with current_chunk which contains the current_chunk 
    #values and this steps guarantees that we will get the min_ element of the whole data
    #And then we will simply remove this root element with next element 
    
    #This next element is selected from the file from which the mininmum element is obtained
    #And again we repeat the above process of heapifying until the heap is empty
    csv_file_name = "Final/Sorted_" + str(file_number) + ".csv"
    output_file = open(csv_file_name, "w", encoding='utf-8', newline="")
    writer = csv.writer(output_file)
    writer.writerow(column_headers[0])  # Write the headers only once
    
    min_heap = [(row[1:], i) for i, row in enumerate(current_chunk) if row is not None]
    hp.heapify(min_heap)
    
    #Till the heap is empty repeat the above mentioned process again
    while min_heap:
        row, file_index = hp.heappop(min_heap)
        writer.writerow(current_chunk[file_index])
    
        row_counter += 1
        if row_counter == memory_limitation:
            
            row_counter = 0
            file_number += 1
            csv_file_name = "Final/Sorted_" + str(file_number) + ".csv"
            output_file.close()
            
            output_file = open(csv_file_name, "w", encoding='utf-8', newline="")
            writer = csv.writer(output_file)
            writer.writerow(column_headers[0])  # Write the headers only once
            
          
        current_chunk[file_index] = next(chunks_2000[file_index], None)

        # If the chunk is not empty, add its first row to the heap
        if current_chunk[file_index] is not None:
            hp.heappush(min_heap, (current_chunk[file_index][1:], file_index))
        else:
            # If the file has reached its end, mark it as such
            current_chunk[file_index] = None
            reached_end[file_index] = True
        
    
        if all(reached_end):
            #After all files are read we will close all the files
            output_file.close()
            break
   
    


####################################################################################
# Data Chuncks
####################################################################################
def data_chuncks(file_path, columns, memory_limitation):
        """
        # file_path : dataset file_path for imdb_dataset.csv (datatype : String)
        # columns : the columns on which dataset needs to be sorted (datatype : list of strings)
        # memory_limitation : At each time how many records from the dataframe can be loaded (datatype : integer)
        # Load the 2000 chunck of data every time into Data Structure called List of Sublists which is named as "chuncks_2000"
        # NOTE : This data_chuncks function uses the records from imdb_dataset. Only 2000 records needs to be loaded at a
                # Time in order to process for sorting using merge sort algorithm. After sorting 2000 records immediately
                # Store those 2000 sorted records into Floder named Individual by following Naming pattern given below.
        #Store all the output files in Folder named "Individual".
        #Output csv files must be named in the format Sorted_1, Sorted_2,...., Sorted_93
        #The below Syntax will help you to store the sorted files :
                    # name_of_csv = "Individual/Sorted_" + str(i + 1)
                    # sorted_df.reset_index(drop=True).to_csv(name_of_csv, index=False)

        # ***NOTE : Every output csv file must have 2000 sorted records except for the last ouput csv file which
                    might have less than 2000 records.

        Description:
        This code reads a CSV file, separates the data into chunks of data defined by the memory_limitation parameter,
        sorts each chunk of data by the specified columns using the merge_sort algorithm, and saves each sorted chunk
        as a separate CSV file. The chunk sets are determined by the number of rows in the file divided by the
        memory_limitation. The names of the sorted files are stored as "Individual/Sorted_" followed by a number
        starting from 1.
        """
        
        clear_folder("Individual")
            
        #Load the 2000 chunck of data every time into Data Structure called List of Sublists which is named as "chuncks_2000"
        chuncks_2000 = FixedSizeList(memory_limitation)

        #Write code for Extracting only 2000 records at a time from imdb_dataset.csv
        df = pd.read_csv(file_path)
        chuncks_2000 = [df.loc[start : start+memory_limitation-1] for start in range(0, df.shape[0], memory_limitation)]
        num_chunks = df.shape[0]//memory_limitation
        column_indxes = [0]
        for column in columns:
            column_indxes.append(column_names.index(column))
        for i in range(num_chunks+1):
            data = chuncks_2000[i].iloc[:, column_indxes].values.tolist()
            chuncks_2000[i] = pd.DataFrame(merge_sort(data, column_indxes), columns = ['tconst'] + columns)
            name_of_csv = "Individual/Sorted_" + str(i + 1)+".csv"
            chuncks_2000[i].reset_index(drop=True).to_csv(name_of_csv, index=False) 

        #Passing the 2000 Extracted Records and Columns indices for sorting the data
        #column_indxes are Extracted from the imdb_dataset indices by mapping the columns need to sort on which are
        #passed from the testcases.


#Enable only one Function each from data_chuncks and Mystery_Function at a time

#Test Case 13
#C:/Users/seera/OneDrive/Desktop/algorithms_project1_package/Mystery_Sorting/
data_chuncks('imdb_dataset.csv', ['startYear'], 2000)

#Test Case 14
#data_chuncks('imdb_dataset.csv', ['primaryTitle'], 2000)

#Test Case 15
#data_chuncks('imdb_dataset.csv', ['startYear','runtimeMinutes' ,'primaryTitle'], 2000)



#Test Case 13
Mystery_Function("Individual", 2000, ['startYear'])

#Test Case 14
#Mystery_Function("Individual", 2000, ['primaryTitle'])

#Test Case 15
#Mystery_Function("Individual", 2000, ['startYear','runtimeMinutes' ,'primaryTitle'])
