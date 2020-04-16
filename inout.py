import math
import random
#import gmpy # combinatory analysis 

def read_data(filename, skip_first_line=False, ignore_first_column=False):
    '''
    Loads data from a csv file and returns the corresponding list.
    All data are expected to be floats, except in the first column.
    @param filename: csv file name.
    @param skip_first_line: if True, the first line is not read.
    Default value: False.
    @param ignore_first_column: if True, the first column is ignored.
    Default value: False.
    @return: a list of lists, each list being a row in the data file.
    Rows are returned in the same order as in the file.
    They contains floats, except for the 1st element which is a string
    when the first column is not ignored.
    '''
    f = open(filename, 'r')
    if skip_first_line:
        f.readline()
    
    data = []
    for line in f:
        line = line.split(",")
        line[1:] = [ float(x) for x in line[1:] ]
        if ignore_first_column:
            line = line[1:]
        data.append(line)
    f.close()
    return data

def write_data(data, filename, indexation=0):
    '''
    Writes data in a csv file.
    @param data: a list of lists
    @param filename: the path of the file in which data is written.
    The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    f.write("numero, attribut 1, attribut 2,... attribut n\n")
    for item in data:
        i = data.index(item) + 1
        f.write("%i" % i)
        f.write(",")
        f.write(','.join([repr(x) for x in item]))
        f.write('\n')
    f.close()

def write_output(data, groups, filename):
    '''
    Writes output in a csv file.
    @param data: a list of lists
    @param filename: the path of the file in which data is written.
    The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    f.write("numero, attribut 1, attribut 2,... attribut n, cluster number\n")
    for item in data:
        i = data.index(item) + 1
        f.write("%i" % i)
        f.write(",")
        f.write(','.join([repr(x) for x in item]))
        f.write(",")
        f.write("%i" % (groups[data.index(item)] + 1))
        f.write('\n')
    f.close()


def plot_matlab_2D(data, filename, group):
    '''
    Writes data in a .mat file.
    @param data: a list of lists
    @param filename: the path of the file in which data is written.
    The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    for item in data:
        #item = item[0:2] ---> Activate to plot the sepales caracteristics for the IRIS data  
        #item = item[2:4] ---> Activate to plot the petales caracteristics for the IRIS data
        f.write('plot(')
        f.write(','.join([repr(x) for x in item]))
        f.write(",'{}')".format(group))
        f.write(';')
        f.write('hold on')
        f.write('\n')
    f.close()

def plot_matlab_3D(data, x, y, z, filename, group):
    '''
    Writes data in a .mat file.
    @param data: a list of lists
    @param filename: the path of the file in which data is written.
    The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    for item in data:
        f.write('plot3(')
        f.write(','.join([repr(x) for x in item]))
        f.write(",'{}')".format(group))
        f.write(';')
        f.write('hold on')
        f.write('\n')
    f.close()

def generate_random_data(nb_objs, nb_attrs, frand=random.random):
    '''
    Generates a matrix of random data.
    @param frand: the fonction used to generate random values.
        It defaults to random.random.
        Example::
            import random
            generate_random_data(5, 6, lambda: random.gauss(0, 1))
    @return: a matrix with nb_objs rows and nb_attrs+1 columns. The 1st
        column is filled with line numbers (integers, from 1 to nb_objs).
    '''
    data = []
    for i in range(nb_objs):
        #line = [i+1]
        #for j in range(numAtt):
        #line.append(frand())
        i = i + 1
        line = map(lambda x: frand(), range(nb_attrs))
        data.append(line)
    return(data)

def calculate_euclidian_distance(vector_1, vector_2):
    '''
    Generate the Euclidian distance between two vectors
    @param param: the two vectors
    @return: the distance between the two input vectors
    '''
    if len(vector_1) == len(vector_2):
        s = 0
        for i in range(len(vector_1)):
            s = s + math.pow(float(vector_1[i]) - float(vector_2[i]), 2)
        return float(math.sqrt(s))

def calculate_manhattan_distance(vector_1, vector_2):
    '''
    Generate the distance of Manhattan between two vectors
    @param param: the two vectors
    @return: the distance between the two input vectors
    '''
    if len(vector_1) == len(vector_2):
        s = 0
        for i in range(len(vector_1)):
            s = s + math.fabs(float(vector_1[i]) - float(vector_2[i]))
        return float(s)

def points_center(L, ancient_centers):
    '''
    @return: The new center of the group L
    @param L: A list of vectors
    @param ancient_centers: the list of centers during the precedent iteration
    '''
    C = [] #empty group problem 
    for x in range(len(L)):
        c = []
        for y in range(len(ancient_centers[0])):
            s = 0.0000
            t = 0
            for z in range(len(L[x])):
                s = s + float(L[x][z][y])
                t = t + 1
            if len(L[x]) != 0:
                c = c + [s / len(L[x])]
            else:
                c = ancient_centers[x] #same center, doesn't change
        C = C + [c]
    return C

def dunn_index(U, dist):
    '''
    @return: Dunn index of quality
    @param U: a list of lists (containing observations ordered in clusters)
    @param dist: the distance methode
    '''
    D = []
    K = []
    for i in range(len(U) - 1):#compare elements one time
        for j in range(i + 1, len(U)):# //
            for k in range(len(U[i])):#calculate distance 
                for l in range(len(U[j])):
                    if dist == 1:
                        d = calculate_euclidian_distance(U[i][k], U[j][l])
                    if dist == 2:
                        d = calculate_manhattan_distance(U[i][k], U[j][l])
                    D = D + [d]
            K = K + [min(D)]
 
    #Same thing here
    DD = []
    KK = []
    for i in range(len(U)):
        for j in range(len(U[i])):
            for k in range(len(U[i])):
                if dist == 1:
                    d = calculate_euclidian_distance(U[i][j], U[i][k])
                if dist == 2:
                    d = calculate_manhattan_distance(U[i][j], U[i][k])
                DD = DD + [d]

        m = max(DD)
        if m :
            KK = KK + [m]
            return float(min(K) / max(KK))
        else : 
            return 0

def DB_index(dist, centers, U, G):
    '''
    @return: DB index of quality
    @param U: a list of lists (containing distances of all elements to all centers at the end of the algorithm)
    @param dist: the distance methode
    @param G: listing groups of the i_th element of the observations list
    @param centers: list of centers of clusters at the end of the algorithm 
    '''
    K = []
    for i in range(len(U[0])):
        K = K + [0.0] # Creating a list of length(u(i)) float elements
    for i in range(len(U)):
        k = G[i] - 1 # to get the index
        K[k] = K[k] + U[i][k]
    K = [t / len(centers) for t in K]
    #Sum of all distances of intra cluster elements to the center i
    s = 0
    S = []
    for i in range(len(centers)):
        for j in range(len(centers)):
            if i == j:
                continue
            if calculate_euclidian_distance(centers[i], centers[j]) == 0.:
                continue
            if calculate_manhattan_distance(centers[i], centers[j]) == 0. :
                continue
            if dist == 1 :
                d = (K[i] + K[j]) / calculate_euclidian_distance(centers[i], centers[j])
            if dist == 2:
                d = (K[i] + K[j]) / calculate_manhattan_distance(centers[i], centers[j])
            S = S + [d]
        m = max (S)
        s = s + m
        S = []
    return s / len(centers)

def intra_cluster_distance(T, centers, dist):
    '''
        @return: Calcule la somme de toutes les distances intra-clusters
        @param T: vecteur de list de veteur des elements classer
        @param centers: list des vecteurs centres
        @param dist: distance calculation methode 
    '''
    s = 0.
    for t in T:
        for element in t:
            if dist == 1:
                d = calculate_euclidian_distance(element, centers[T.index(t)])
            if dist == 2:
                d = calculate_manhattan_distance(element, centers[T.index(t)])
            s = s + d
    return s

def inter_cluster_distance(centers,observations, dist):
    '''
    @return: Calcule la somme de toutes les distances inter-clusters
    @param observations: vecteur de list de veteur des elements a classer
    @param centers: list des vecteurs centres
    @param dist: distance calculation methode 
    '''
    s=0.
    g = []
    # Calcule du centre de gravite
    for i in range(len(observations[0])):
        for observation in observations:
            s = s + observation[i]
        g = g + [s/len(observations[0])]

    for center in centers:
        if dist==1:
            d=calculate_euclidian_distance(center, g)
        if dist==2:
            d=calculate_manhattan_distance(center, g)
        s =s+d
    return s
