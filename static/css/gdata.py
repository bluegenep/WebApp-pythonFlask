"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=5):
    np.random.seed(seed)
    #X = np.zeros((100,2))
    #Y = np.random.random(size = (100,))*200-100
    # Here's is an example of creating a Y from randomly generated
    # X with multiple columns
    # Y = X[:,0] + np.sin(X[:,1]) + X[:,2]**2 + X[:,3]**3


    #Each data set should include from 2 to 1000 columns in X, and one column in Y. The data should contain from 10 (minimum) to 1000 (maximum) rows.
    num_of_rows = np.random.randint(10, 1001)
    num_of_columns = np.random.randint(2,1001)
    print("NUMBER OF ROWS AND COLUMNS IN GEN DATA == " ,num_of_columns, num_of_rows)

    #get X
    X = np.random.normal(size=(num_of_rows, num_of_columns))
    print("X == ", X, X.ndim, X.shape )
    Y = np.array([1] * num_of_rows)
    for row in range(0,num_of_rows):
        temp_x = 0
        for col in range(0,num_of_columns):
            temp_x += X[row, col]
        Y[row] = np.array(temp_x + 5)
        print("Y[row] = [temp_x + 5]", temp_x ,"+ 5 ==", Y[row])
        #Y = Y + X[:, row] ** 2
    print("Y == ", Y, Y.ndim, Y.shape)
    return X, Y

def best4DT(seed=5):
    np.random.seed(seed)
    # X = np.zeros((100,2))
    # Y = np.random.random(size = (100,))*200-100
    num_of_rows = np.random.randint(10, 1001)
    num_of_columns = np.random.randint(2, 1001)
    print("NUMBER OF ROWS AND COLUMNS IN GEN DATA == " ,num_of_columns, num_of_rows)

    #get X
    X = np.random.standard_normal(size=(num_of_rows, num_of_columns))
    print("X == ", X, X.ndim, X.shape )
    Y = np.array([1] * num_of_rows)
    for col in range(0,num_of_columns):
        # temp_x = 0
        # for col in range(0,num_of_columns):
        #     print("COL == ", col)
        #     temp_x += ((X[row, col])* (-1)**col)
        # Y[row] = np.array(temp_x)
        # print("Y[row] = [temp_x + 5]", temp_x ,"+ 5 ==", Y[row])
        Y = Y + X[:, col] ** 5
    print("Y == ", Y, Y.ndim, Y.shape)
    return X, Y
    #return X, Y

def author():
    return 'pbhatta3' #Change this to your user ID

if __name__=="__main__":
    print ("they call me Tim.")
