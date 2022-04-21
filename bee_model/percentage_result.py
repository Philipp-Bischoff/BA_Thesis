#This file is used to calculate the results for the parameter settings
#And calculate how many of the repitions resulted in what site being chosen



def get_percentage(simulation_Dict):
    #Replication : {Succes, Site}, {Sucess, Site} }

    high_site_strong = 0
    medium_site_strong = 0
    low_site_strong = 0
    failure_strong = 0

    high_site_weak = 0
    medium_site_weak = 0
    low_site_weak = 0
    failure_weak = 0

    for replication_Number in simulation_Dict:

        simulation_Result = simulation_Dict[replication_Number]
        result_weak = simulation_Result[0][0]
        result_strong = simulation_Result[1][0]

        if(result_weak == 'Success'):
            if(simulation_Result[0][1] == 5):
                high_site_weak += 1
            if(simulation_Result[0][1] == 4):
                medium_site_weak += 1
            if(simulation_Result[0][1] == 3):
                low_site_weak += 1
        elif (simulation_Result[0][1]<= 2) or (simulation_Result[0][1] == 0 and simulation_Result[0][0] == "Failure"):
                failure_weak += 1  
 
        if(result_strong == 'Success'):
            if(simulation_Result[1][1] == 5):
                high_site_strong += 1
            if(simulation_Result[1][1] == 4):
                medium_site_strong += 1
            if(simulation_Result[1][1] == 3):
                low_site_strong += 1
        elif(simulation_Result[0][1]<= 2) or (simulation_Result[1][1] == 0 and simulation_Result[1][0] == "Failure"):
            failure_strong += 1

    print("best site weak:", high_site_weak)
    print("2nd best site weak:", medium_site_weak)
    print("3rd best site weak:", low_site_weak)
    print("no site", failure_weak)

    print("best site strong:", high_site_strong)
    print("2nd best site strong:", medium_site_strong)
    print("3rd best site strong:", low_site_strong)
    print("no site", failure_strong)

            

