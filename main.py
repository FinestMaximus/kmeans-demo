# -*- coding: utf-8 -*-

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        @author: LOUHAIDIA OUSSAMA
        @summary: TP k-means, advanced algorithms
        
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import inout
import os
import random

number_attributs = 0

'''''''''''''''''''''''''''''''''''''''''
    Netoyage du dossier runs afin d'y 
       mettre les nouveau mfiles
       
'''''''''''''''''''''''''''''''''''''''''

for root, dirs, files in os.walk('runs/' , topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

'''''''''''''''''''''''''''''''''''''''
   Generation des données de test
  par lecture d'un fichier externe 
    ou par générateur aléatoire

'''''''''''''''''''''''''''''''''''''''

generate_data_or_import_data = "s"

while ((generate_data_or_import_data != 'y') | (generate_data_or_import_data != 'n')):
    generate_data_or_import_data = raw_input("    -> Read data from an external file?? (y/n): ")
    if (generate_data_or_import_data == 'y'):
        
        #data reading
        pb = False
        while(pb == False):
            try:
                file_name = raw_input("    -> Enter the .cvs file name (without extension): ")
                observations = inout.read_data("data/{}.csv".format(file_name), True, False)
                # Si première collone contient le numéro de chaque ligne relir en l'ignorant
                if (observations[0][0] == '1'):
                    observations = inout.read_data("data/{}.csv".format(file_name), True, True)
                pb = True
            except IOError as e:
                print "    Not found! Try again!"
                
        number_attributs = len(observations[0])
        break

    elif (generate_data_or_import_data == 'n'):    
        # Variables reading
        number_attributs = int(raw_input("    -> Enter the number of attributes: "))
        number_observations = int(raw_input("    -> Enter the size of the DataSet: "))
    
        # Random Generation and stock of data
        observations = inout.generate_random_data(number_observations, number_attributs)
        inout.write_data(observations, "data/observations.csv")
        break
    
    else:
        print "    .... Please concentrate and put a correct character!"
        
'''''''''''''''''''''''''''''''''''''''
    Choosing distance criteria
    
'''''''''''''''''''''''''''''''''''''''

dist = 0

while ((dist != 1) | (dist != 2)):
    dist = int(raw_input("    -> Choose the distance for calculations (1 or 2)?????\n       (1-Euclidian distance.      2-Manhattan distance.)\n        -> "))
    if ((dist == 1) | (dist == 2)):
        break
    else:
        print "        Please concentrate and put a correct number!"

'''''''''''''''''''''''''''''''''''''''
    Choosing stop condition
    
'''''''''''''''''''''''''''''''''''''''

stop = 'a'

while ((stop != 'y') | (stop != 'n')):
    stop = raw_input("    -> Activate the automatic stop condition (y or n),\n       * else where a step by step execution is done: ")
    if ((stop == 'y') | (stop == 'n')):
        break
    else:
        print "    .... Please concentrate and put 'y' or 'n'!"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Generating random clusters by sampling observations
    
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

number_clusters = int(raw_input("    -> Enter -k- the number of clusters (min = 2): "))
print "            -------------------------------------------------------------------\n"
clusters = random.sample(observations, number_clusters)

'''''''''''''''''''''''''''''''''''''''''''''''
    1- The automated stop condition:
  continue if no clusters centers are moving
  
'''''''''''''''''''''''''''''''''''''''''''''''

stop_condition = "1"
if (stop == 'y'):
    number_iterations = 0
    updated_clusters = []
    a = True
    while a == True:
        number_iterations = number_iterations + 1
        L = [] # list containing all distances to all clusters
        for i in range(len(observations)):
            D = [] # list containing all distances for each observation
            for j in range(len(clusters)):
                if (dist == 1):
                    d = inout.calculate_euclidian_distance(observations[i], clusters[j])
                if (dist == 2):
                    d = inout.calculate_manhattan_distance(observations[i], clusters[j])
                D = D + [d]
            L = L + [D]

        G = []
        for i in range(len(observations)):
            G = G + [L[i].index(min(L[i]))] # Group of the element at the end of his distances list

        # T A list of lists that contains ordered in groups observations (a list of lists in a List!)
        T = []
        for j in range(len(clusters)):
            stack = []
            for i in range(len(observations)):
                if G[i] == j:
                    stack = stack + [observations[i]]
            T = T + [stack]

        updated_clusters = inout.points_center(T, clusters)
        
        if clusters == updated_clusters:
            break
        else:
            clusters = updated_clusters

        plot_colors = ['cs', 'r*', 'm.', 'k+', 'ro', 'm*', 'k.', 'b+', 'mo', 'k*', 'b.', 'r+', 'ko', 'b*', 'r.', 'k+']
        
        if (number_attributs == 2):
            inout.plot_matlab_2D(clusters, "runs/clusters.m", 'bo')
            for i in range(number_clusters):
                inout.plot_matlab_2D(T[i], "runs/group{}.m".format(i + 1), plot_colors[i % 15])
        if (number_attributs == 3):
            inout.plot_matlab_3D(clusters, "runs/clusters.m", 'bo')
            for i in range(number_clusters):
                inout.plot_matlab_3D(T[i], "runs/group{}.m".format(i + 1), plot_colors[i % 15])

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        Writing output file containing affectations to classes
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    inout.write_output(observations, G, "data/output.csv")
    
    '''''''''''''''''''''''''''''''''''''''''''''
        Python Console messages generation
        
    '''''''''''''''''''''''''''''''''''''''''''''
    
    print "The total number of iteration for this method is: ", number_iterations
    
    print "Results are: "
    
    print "--> List of Clusters: "
    for j in range(number_clusters):
        print "cluster %i:" % (j + 1) , T[j]
    
    print "--> List of Final centers: "
    for j in range(len(clusters)):
        print "center %i: " % (j + 1), clusters[j]

    '''''''''''''''''''''''''''''''''''''''
        2 - The main loop, continue if no 
                'exit' on the input
                
    '''''''''''''''''''''''''''''''''''''''

elif (stop == 'n'):
    while (stop_condition != "exit"):
        L = [] # list containing all distances to all clusters
        for observation in observations:
            D = [] # list containing all distances for each observation
            for center in clusters:
                d = inout.calculate_euclidian_distance(observation, center)
                D = D + [d]
            L = L + [D]
      
        G = [] # Clustring list
        for i in range(len(observations)):
            G = G + [L[i].index(min(L[i]))]
            # Group of the element at the end of his distances list
    
        T = []
        for j in range(len(clusters)):
            stack = []
            for i in range(len(observations)):
                if G[i] == j:
                    stack = stack + [observations[i]]
            T = T + [stack]
        
        clusters = inout.points_center(T, clusters)
        '''''''''''''''''''''''''''''''''''''''''
            Python Console messages generation
            
        '''''''''''''''''''''''''''''''''''''''''
    
        print "--> List of Groups: "
        for j in range(len(clusters)):
            print "group %i:" % (j + 1) , T[j]
        
        print "--> List of clusters at this point of the Algorithm: "
        for j in range(len(clusters)):
            print "center %i:" % (j + 1), clusters[j]
        
        plot_colors = ['r*', 'm.', 'k+', 'ro', 'm*', 'k.', 'b+', 'mo', 'k*', 'b.', 'r+', 'ko', 'b*', 'r.', 'k+']
        
        # Plotting if 2 or 3 - Dimentional, do nothing else where
        
        if (number_attributs == 2):
            inout.plot_matlab_2D(clusters, "runs/clusters.m", 'bo')
            for i in range(number_clusters):
                inout.plot_matlab_2D(T[i], "runs/group{}.m".format(i + 1), plot_colors[i % 15])
        if (number_attributs == 3):
            inout.plot_matlab_3D(clusters, "runs/clusters.m", 'bo')
            for i in range(number_clusters):
                inout.plot_matlab_3D(T[i], "runs/group{}.m".format(i + 1), plot_colors[i % 15])
        
        stop_condition = raw_input("tape 'exit' to stop, or enter to continue: ")
    
    inout.write_output(observations, G, "data/output.csv")

print "\n-> The dunn index for this issue is: ", inout.dunn_index(T, dist)
print "-> The DB index for this issue is: ", inout.DB_index(dist, clusters, L, G)
print "-> The RSQ index is: ", inout.inter_cluster_distance(clusters, observations, dist)/(inout.inter_cluster_distance(clusters, observations, dist)+inout.intra_cluster_distance(T, clusters, dist))
print "\n"
print "    * M-files have been created in the /runs folder. \n"
print "      * Refresh the folder if you can't see them. \n"
print "      Execute them on matlab to view 2D or 3D results\n"
print "    * Resulting data have been saved to 'output.csv' (assigned data)\n             & 'clusters.csv' (resulting centers)\n"
print "         ***** END, execute again to make other tests *****!"
