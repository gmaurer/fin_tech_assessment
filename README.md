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
