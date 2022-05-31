import numpy as np
def pointCompareY(set1, set2):
    x1 = set1[0]
    y1 = set1[1]
    x2 = set2[0]
    y2 = set2[1]
   

    
    if ( y1 > y2 and (y1 - y2)>100 )or ( y2 > y1) and (y2 - y1)>100:
        return True
    else:
        return False
    
def pointCompareX(set1, set2):
    x1 = set1[0]
    y1 = set1[1]
    x2 = set2[0]
    y2 = set2[1]
   

    
    if ( x1 > x2 and (x1 - x2)>100 )or ( x2 > x1) and (x2 - x1)>100:
        return True
    else:
        return False

                        # TL BL BR TR
def translationParameterGenerator(p1,p2,p3,p4):
    
    x1 = p1[0]
    y1 = p1[1]
    
    x2 = p2[0]
    y2 = p2[1]
    
    x3 = p3[0]
    y3 = p3[1]
    
    x4 = p4[0]
    y4 = p4[1]
    
    #Edge co-ordinates respective to the Projector(Constant)
    projectorCooridinates = np.array([[0, 0], [1000, 0],[1000,1000],[0,1000]])

    X1 = projectorCooridinates[0,0]
    Y1 = projectorCooridinates[0,1]

    X2 = projectorCooridinates[1,0]
    Y2 = projectorCooridinates[1,1]

    X3 = projectorCooridinates[2,0]
    Y3 = projectorCooridinates[2,1]

    X4 = projectorCooridinates[3,0]
    Y4 = projectorCooridinates[3,1]
    
    matrix1 = np.array([[x1, y1, 1, 0,  0,  0, - x1 * X1, - y1 * X1],
                    [x2, y2, 1, 0,  0,  0, - x2 * X2, - y2 * X2],
                    [x3, y3, 1, 0,  0,  0, - x3 * X3, - y3 * X3],
                    [x4, y4, 1, 0,  0,  0, - x4 * X4, - y4 * X4],
                    [0,  0,  0, x1, y1, 1, - x1 * Y1, - y1 * Y1],
                    [0,  0,  0, x2, y2, 1, - x2 * Y2, - y2 * Y2],
                    [0,  0,  0, x3, y3, 1, - x3 * Y3, - y3 * Y3],
                    [0,  0,  0, x4, y4, 1, - x4 * Y4, - y4 * Y4],
                    ])

    matrix2 = np.array([[X1],
                        [X2],
                        [X3],
                        [X4],
                        [Y1],
                        [Y2],
                        [Y3],
                        [Y4]])
    
    
    matrix1inverse = np.linalg.inv(matrix1) 
    translationParameters = np.matmul(matrix1inverse, matrix2)
    return translationParameters

def coordinateConverter(coord,translationParameters):
    print("------")
    print(coord)
    
    a = translationParameters[0,0]
    b = translationParameters[1,0]
    c = translationParameters[2,0]
    d = translationParameters[3,0]
    e = translationParameters[4,0]
    f = translationParameters[5,0]
    g = translationParameters[6,0]
    h = translationParameters[7,0]
    
    x = coord[0]
    y = coord[1]
    
    X = ((a * x) + (b * y) + c )/((g * x) + (h * y) + 1)
    Y = ((d * x) + (e * y) + f )/((g * x) + (h * y) + 1)
    
    X = int(X)
    Y = int(Y)

    outputCoordinate = np.array([Y,X])

    return list(outputCoordinate)
    