A brief explaination of mystery sorting:-

#First we need to clean the folder before starting the sorting
#file_List contains the names of all the individual files
#files contains all the file pointers pointing to files first position
#no_of_files denotes the number of files present in individual folder
#current_chunk :- we will collect all the first row elements of the files into a list
#column_headers :- we will collect all the headers of all files into a list
	
    #First we will build a min-heap with current_chunk which contains the current_chunk 
    #values and this steps guarantees that we will get the min_ element of the whole data
    #And then we will simply remove this min value which is present at root loaction with next element 
    #This next element is selected from the file from which the mininmum element is obtained
    #And again we repeat the above process of heapifying until the heap is empty
#Till the heap is empty repeat the above mentioned process again