### THIS MODULE IS CREATED TO CHECK THE PERFORMANCE OF ELLIPTIC CURVE MULTIPLICATION WITH DIFFERENT SIZE OF PREPROCESSED BITS 

## How to run this?
* Download advanced_bitcoin_folder i.e.  .py file and .csv file. 
* Run the .py file

## For those who don't know how to run python file
 * Install python, if python is not already installed https://www.python.org/downloads/
 * Open command prompt/shell
 * nevigate to the directory where advance_bitcoin_finder.py file is located (make sure all.csv is in the same directory) 
 * type `python advance_bitcoin_finder.py` and press enter
 
## What do you expect from this program?
 Basically nothing.!!
 * __I or any of my code here not ensuring of getting any bitcoin.__ You might get iff you are Lucky.
 * __I or any of my code is not liable of any type of damage or loss__. You may run at your own risk. 
 
## How do I know I'm Lucky?
 If you are lucky you will get a STAR of DAVID as output or a non-empty found.btc file. (Without modifying the program obviously)
 
## What to do next if I get Star of David or a non-empty found.btc file?
 Simply email me: mukul0018@gmail.com
 

# Motivation
## How I actually minimizing the time complexity?
I'm minimizing time complexity by precalculating the results for certain no of bits. Let's understand how!
If we have to ECmultiply a 256 bit scaler number with generating point (can be multiplied with other valid points ofcourse), we eventually get the values of (2^i)*G for every setbit at i-th position in that 256 bit number and EC add them togather one after another to get (256 bit number)*G. Here, G is generating point of the curve, * is ECmultiplication  ans 2^i is 2 raise to i. (2^i)*G can be calculated by EC double, i.e. (2^(i+1))*G=ECdouble((2^i)*G)
This method will cost 256 ECdouble operation and no of ECadd will equal to no of set bit in the scaler number. Time Complexity O(no of bits in scaler * ECdouble + no of setbit * ECAdd),incase of 256 bit, time complexity be O(256*ECdouble+256*ECadd), if we preprocess ECdouble operation then time complexity be O(256*ECadd)

#### Optimization
if we preprocess 2 bits togather
 No of ECaddition required becomes 256/2=128 in worst case.
 No of preprocess data in every unit= 2^2=4 
     Therefore, total memory required= 256 bits * (4 *128) = 2^7*256bits=
     (updating soon)
