# fin_tech_assessment

## How to Run:
### Assumptions:
- python 3.8+ installed
- requirements.txt installed
- `cd` into base directory
- `python app/BookAnalyzer.py 200`
## Improvements with more time: 
- dockerize script to allow this to be set up on any environment since it would be self contained, this project was set up to facilitate a shift to containers
- strongly type function arguements better (pandas objects mainly)
- Improve how the dataframe is created and utilized

## Timing for different record counts in seconds:
### Format: "x records: time at target-size 1, time at target-size 200"
### A 4% performance gain was made by adjusting the input from an object to a dictionary, without outputting the list and just pure processing another 3% can be gained
- 100 records: 0.891, 0.873
- 1000 records: 1.747, 1.648
- 10,000 records: 11.225, 11.309
- 100,000 records: 131.562, 131.848


## Answers to Questions:
1. How did you choose your implementation language?
    * I chose Python because of the ease of getting working and my familiarity, if I had more experience with GoLang I would have gone with that as the performance would have been improved since GoLang is much faster than Python. 
2. How did you arrive at your final implementation? Were there other approaches that you considered or tried first?
    * I went thru several iterations of logic and how i would handle the data as that was the biggest hurdle, first was a layered dictionary, then creating an object, then I finally utilized Pandas dataframe objects which allowed better mutation, searching, and ordering compared to the first two thought processes.  Logic wise I had to revise the Reduce logic several times to catch all the edge cases that would come up.  This was a very fun puzzle to work though.  
3. How does your implementation scale with respect to the target size?
    * From the above timing target-size does not have a huge effect on the cost to run the program as it is a quick operation once the dataframe has been sorted.
4. How does your implementation scale with respect to the number of orders in the book?
    * I have included timing for differnt chunks of records.  As the size increases the execution slows (this is where GoLang would really showcase a better execution time). The potential improvements of a refactor to improve how Pandas dataframes were utilized could opitmize this as well. 
