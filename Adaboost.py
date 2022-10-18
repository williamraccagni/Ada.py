import sys
import csv
from copy import deepcopy
import math

#----Funzioni----

#Funzioni di composizione

def transform_func_to_mp (func):
    return lambda x : 1 if func(x)==True else -1

def weighted_func (weight, func):
    return lambda x : weight * func(x)

def merge_func (func1, func2):
    return lambda x : func1(x) + func2(x)

def func_tobool (func):
    return lambda x : True if func(x)>=0 else False

#----

def bc_fun(i,t):
    return lambda x: x[i] >= t

def bc_fun_inverted(i,t):
    return lambda x: x[i] < t

#----

def bool_to_oneminusone(bool_value):
    if bool_value==True:
        return 1
    else:
        return -1

def indicator_function(bool_value):
    if bool_value==True:
        return 1
    else:
        return 0

#----

def bc_family_generator(dataset):

    family = []

    for feature_index in range(10):
        for sample_index in range(0,len(dataset),int(len(dataset)/100)):
            family.append(bc_fun(feature_index, dataset[sample_index][feature_index]))
            family.append(bc_fun_inverted(feature_index, dataset[sample_index][feature_index]))

    for feature_index in range(10,54):
        family.append(bc_fun(feature_index, 0.5))
        family.append(bc_fun_inverted(feature_index, 0.5))

    return family

def function_error(function, dataset):

    error = 0

    for d_index in range(len(dataset)):

        #zero-one loss function
        error += indicator_function(function(dataset[d_index]) != dataset[d_index][-1])

        #if( function(dataset[d_index]) != dataset[d_index][-1] ):
        #    error = error + 1

    error = error/len(dataset)

    return error

def best_h_algorithm(dataset, P, H_family):

    f_weights = []

    for H_index in range(len(H_family)):
        e = 0
        for sample_index in range(len(dataset)):
            e += indicator_function(H_family[H_index](dataset[sample_index]) != dataset[sample_index][-1]) * P[sample_index]
        f_weights.append([H_index, e])

    f_weights.sort(key=lambda x: x[1])

    return H_family[f_weights[0][0]]

#----AdaBoost

def adaboost(trainingset, H_family, algorithm_A, T_parameter):

    m = len(trainingset)
    P = [ (1/m) for x in range(m)]

    for i in range(T_parameter):

        #Trovo hi
        hi = algorithm_A(trainingset, P, H_family)

        #Calcolo ei
        ei = 0
        for training_index in range(len(trainingset)):
            ei += indicator_function(hi(trainingset[training_index]) != trainingset[training_index][-1]) * P[training_index]

        #BREAK
        if ( ei==0 or ei==0.5 or ei==1):
            break

        #Calcolo wi
        wi = 0.5 * math.log((1-ei)/ei)

        #Aggiorno la funzione
        if(i==0):
            function = weighted_func(wi, transform_func_to_mp(hi))
        else:
            function = merge_func(function, weighted_func(wi, transform_func_to_mp(hi)))

        #Ricalcolo P
        Ei = 0
        for training_index in range(len(trainingset)):
            Ei += math.exp( -1 * wi * bool_to_oneminusone(hi(trainingset[training_index]) == trainingset[training_index][-1]) ) * P[training_index]

        for training_index in range(len(trainingset)):
            P[training_index] = (P[training_index] * math.exp( -1 * wi * bool_to_oneminusone(hi(trainingset[training_index]) == trainingset[training_index][-1]) )) / Ei



    function = func_tobool(function)
    return function

#----Main----

if __name__ == "__main__":

    #----Variabili----
    dataset = []
    percentage_trainingset = 0.75
    N_for_validation = 10
    T_parameter = int(sys.argv[1])

    #----Disclaimer----
    print("Parametro T inserito: " + str(T_parameter))

    #----Lettura Dataset da file csv----
    with open('forest-cover-type.csv') as file_csv:
        csv_reader = csv.reader(file_csv, delimiter=',')
        skip = 0
        for row in csv_reader:
            if skip == 0:
                skip += 1
            else:
                dataset.append(row[1:])

    #----Conversione valori dataset----
    for x in range(len(dataset)):
        for y in range(len(dataset[0])):
            dataset[x][y]=int(dataset[x][y])

    #----Definizione training set e test set----
    #Training set
    trainingset = deepcopy(dataset)
    del trainingset[int(percentage_trainingset * len(dataset)):]
    #Test set
    testset = deepcopy(dataset)
    del testset[:int(percentage_trainingset * len(dataset))]



    #----Generazione dei 7 classificatori AdaBoost e trainingerror testerror per ogni classe----

    for class_index in range(1,8):

        #Adattamento trainingset per l'i-esima classe
        class_trainingset = deepcopy(trainingset)
        for i in range(len(class_trainingset)):
            if class_trainingset[i][-1]==class_index:
                class_trainingset[i][-1]=True
            else:
                class_trainingset[i][-1]=False

        #Adattamento testset per l'i-esima classe
        class_testset = deepcopy(testset)
        for i in range(len(class_testset)):
            if class_testset[i][-1]==class_index:
                class_testset[i][-1]=True
            else:
                class_testset[i][-1]=False

        #----Variazioni del validationset----

        N_functions = []
        Nf_weights = []
        for N_index in range(1, (N_for_validation+1)):

            #Creazione validationset e rispettivo class_trainingset all'i-sima iteriazione
            validationset = deepcopy(class_trainingset)
            if N_index < N_for_validation:
                validationset = validationset[((N_index-1) * int(len(class_trainingset)/N_for_validation)):(N_index * int(len(class_trainingset)/N_for_validation))]
            else:
                validationset = validationset[((N_index-1) * int(len(class_trainingset)/N_for_validation)):]

            new_class_trainingset = deepcopy(class_trainingset)
            if N_index < N_for_validation:
                del new_class_trainingset[((N_index-1) * int(len(class_trainingset)/N_for_validation)):(N_index * int(len(class_trainingset)/N_for_validation))]
            else:
                del new_class_trainingset[((N_index-1) * int(len(class_trainingset)/N_for_validation)):]

            #Genero la famiglia H
            H_family = bc_family_generator(new_class_trainingset)

            #Eseguo l'algoritmo AdaBoost
            func = adaboost(new_class_trainingset, H_family, best_h_algorithm, T_parameter)

            N_functions.append(func)

            Nf_weights.append([(N_index-1), function_error(N_functions[(N_index-1)], validationset)])

        #Ritorno la funzione migliore per la classe
        #-Riordino in base all'errore
        Nf_weights.sort(key=lambda x: x[1])

        #Ottengo il migliore
        class_function = N_functions[Nf_weights[0][0]]

        #Training error
        class_training_error = function_error(class_function, class_trainingset)

        #Test error
        class_test_error = function_error(class_function, class_testset)

        print("Il training error per la classe " + str(class_index) + " è: " + str(class_training_error))

        print("Il test error per la classe " + str(class_index) + " è: " + str(class_test_error))
