import random
from sites import Site
from bees import Bee
import numpy as np
import math
import plotly.graph_objects as go
import graphing
import percentage_result


#Bees are in one of these two states
bee_state_0 = 'NO DANCE'
bee_state_1 = 'DANCE'

#Measure of independent the bees are where 0 = Full Independence, and 1 = only other Bees
interdependance_weight = 0.8
mean = 0
reliability_sigma = 0.2

#Probability that the duration at t+1 is unrelated to the quality of the site
#capturing the possibility that the bees dance is prompted by mimicking other bees
#rather than by the inspection of a site
independence_mu = 0

#Quality independent constant factor (highest quality of site)
K = 10
#Duration of Simulation
T = 300
#Amount of Bees
N = 200

#Creating the Sites
Site_0_Bees = []
Site_1_Bees = []
Site_2_Bees = []
Site_3_Bees = []
Site_4_Bees = []
Site_5_Bees = []

#This serves as the 'home base'
Site_0 = Site(0, 0 ,0.75, Site_0_Bees)

#These are potential new sites
Site_1 = Site(1, 3, 0.05, Site_1_Bees)
Site_2 = Site(2, 5, 0.05, Site_2_Bees)
Site_3 = Site(3, 7, 0.05, Site_3_Bees)
Site_4 = Site(4, 9, 0.05, Site_4_Bees)
Site_5 = Site(5, 10, 0.05,Site_5_Bees)

#3.5, 4, 4.5, 5, 5.5

#List of all Sites
Sites = [Site_0, Site_1, Site_2, Site_3, Site_4, Site_5]

#List of all bees
Bees = []

#Auxillary Functinons

def current_situation(Sites):
    for site in Sites:
        print("There are ", site.count_bees_at_site(), "Bees at Site" , site.get_site_id())

def bees_engaged(bees):
    amount_dancing = 0
    for bee in bees:
        if (bee.get_state() == 'DANCE'):
            amount_dancing += 1
    return amount_dancing

def match_site_id(site_id, Sites):
    for site in Sites:
        if (site.get_site_id()==site_id):
            return site

def update_site_probabilities(Site, updated_sites):
    for site in Site:
        updated_sites[site.get_side_id()] = site.get_site_probability()      
    return updated_sites        

def match_site_id(site_id, Sites):
    for site in Sites:
        if (site.get_site_id()==site_id):
            return site    

#initialize the model by assuming there is no
#dancing activity at time 0
def initialize_model(N):
    for b in range(N):
        new_Bee = Bee(b, 0, bee_state_0, 0, 0)
        Site_0.add_bee_to_site(b)
        Bees.append(new_Bee)

def set_bees_to_home(Bees):
    for b in Bees:
        b.set_site(0)

def consensus_test_less_demanding(Sites):
    #Dictionary to store the sites and their proportion
    site_proportions = {}

    #This tests if the first and the second list have been compared yet
    comparison = False

    #Calculating the different Site proportions
    for site in Sites:
        site_id = site.get_site_id()
        proportion = (site.count_bees_at_site()/N)
        site_proportions[site_id]=proportion
        
    #Sorting the sites in descending order by proportion of bees dancing for them
    sorted_prop = dict(sorted(site_proportions.items(), key=lambda item: item[1], reverse=True))

    #The idea here being that if I order the list from highest to lowest
    #and the highest is higher than the 2nd highest, it's the highest overall.
    for index_1 in sorted_prop:
        for index_2 in sorted_prop:
            #We want to compare the first with the second highest site. However we need to
            #exclude the possibility that the highest site is the base site (!=0).
            if ( (index_1 != index_2) and (index_1 != 0) and (comparison == False )and (sorted_prop[index_1]>sorted_prop[index_2])):
                #The condition above will be true iff the first and second site are compared for the first time and the
                #simple majority consensus have been achieved.
                print("Consensus has been reached according to weak criterion")
                comparison = True
                return ["Success", index_1]
            if(comparison):
                #This means the first and second highest have been compared but 
                #no consensus has been achieved.
                print("No Consensus reached")
                return ["Failure", 0]
        print("No Consensus reached")
        return ["Failure", 0]
        
def consensus_test_more_demanding(Sites, Bees):
    
    #Dictionary to store the sites and their proportion
    site_proportions = {}

    #Calculating the different Site proportions but exclude base site
    for site in Sites:
        if(site.get_site_id() != 0):
            amount_bees = site.count_bees_at_site()
            site_proportions[site]=amount_bees

    sorted_proportion = dict(sorted(site_proportions.items(), key=lambda item: item[1], reverse=True))

    #print("Consensus Hierarchy")

    for site in sorted_proportion:
        print("Site:", site.get_site_id())
        print("Bees:", sorted_proportion[site])

    for site_1 in sorted_proportion:
        for site_2 in sorted_proportion:
            if sorted_proportion[site_1]>sorted_proportion[site_2] and (site_1.get_site_id() != site_2.get_site_id()):
                if site_1.count_bees_at_site() > 2*site_2.count_bees_at_site():
                    if bees_engaged(Bees) > 0.2*N:
                        print("Consensus reached according to strong criterion")
                        return ["Success", site_1.get_site_id()]
                else:
                    print("No Consensus achieved according to strong criteria")
                    print("FIRST FAILURE")
                    return ["Failure", 0]

    
def finding_new_site(Sites, Bee):

    updated_site_probabilites = {}

    for site in Sites:
        #Get a sites a priori probability (π_j)
        site_probability = site.get_site_probability()
        #Get sites proportion of bees dancing for it(f_j,t)
        site_proportion = site.count_bees_at_site()/N
        #Get entire probability of site
        new_probability = ( (1-interdependance_weight)*site_probability) + (interdependance_weight*site_proportion)
        #Storing them in a dictionary
        updated_site_probabilites[site.get_site_id()] = new_probability


    #The key:value pair in the dictionary is the site's ID and the site's probability
    #I therefore randomly chose one of the key's with it's corresponding probability
    site_Choice = random.choices(list(updated_site_probabilites.keys()), weights=list(updated_site_probabilites.values()), k=1)

    #Getting the previous site as an object
    original_Site = match_site_id(Bee.get_site(), Sites)

    #Get the current site as an object
    Site = match_site_id(site_Choice[0], Sites)

    #The bee has not found a new Site and went back to home site
    if(site_Choice[0] == 0):
        pass
        #print("The bee has not found a site")

    Bee.set_site(site_Choice[0])
    original_Site.remove_bee_from_site()
    Site.add_bee_to_site(Bee)

def calculate_dance_duration(Sites, Bee):

    #Getting Site ID
    IDx = Bee.get_site()

    #Getting actual site object
    Site = match_site_id(IDx, Sites)

    if (Site.get_site_id() == 0):
        return 0
    else:
        #Calculate the dance duration for the site it has found

        #quality of site times exp*
        fluctation = np.random.normal(0,reliability_sigma)

        choices = [Site.get_quality()*(math.exp(fluctation)), K*(math.exp(fluctation))]
        choice = np.random.choice(choices, p = [1-independence_mu, independence_mu])
        b.set_state(bee_state_1)
        return choice


csv_dict = {}
progress_dict = {}
iteration = 0
replication = {}

if __name__ == "__main__":
    
    #We should have N Bees at Site 0
    initialize_model(N)
    print("Initializing New Model")

    #Repitions of the simulation
    for i in range(250):

        print("(", i, "/250)")  

        #Simulation 
        for t in range(T):

            progress_dict.clear()

            for b in Bees:

                #Storing each bee and it's current site for graphing
                progress_dict[b.get_id()] = (match_site_id(b.get_site(), Sites)).get_site_id() 

                if(b.state == 'NO DANCE'):
                    #Looking for a new Site & setting bees to 'DANCE'
                    finding_new_site(Sites, b)
                    #Seeing if site was found and update dance duration accordingly
                    b.set_dance_duration(calculate_dance_duration(Sites, b))
                    continue

                if(b.state == 'DANCE'):
                    #If the bee is dancing reduce dance time by 1
                    if(b.get_dance_duration()>0):
                        b.reduce_dance_duration()
                    elif(b.get_dance_duration() == 0):
                        b.set_state(bee_state_0)
                    else:
                        #A dance duration can go slightly below 0, because
                        #they're continues values. 
                        b.set_dance_duration(0)
                        b.set_state(bee_state_0)

            #csv_dict[iteration] = progress_dict.copy()
            #iteration += 1

        #current_situation(Sites)

        #Storing the Results for Analysis for each repition
        result_weak = consensus_test_less_demanding(Sites)
        result_strong = consensus_test_more_demanding(Sites, Bees)

        #List for summary of repitions
        replication[i] = [result_weak, result_strong]

        #This was used for creating the sankey diagram
        #I restructured the code to only run 1 repition when I investigated
        #it with the diagram
        csv_dict[iteration] = progress_dict.copy()
        iteration += 1
        
        #graphing.sankey_diagram(csv_dict, Sites)

        #Returning the simulation to
        #starting condition
        set_bees_to_home(Bees)
        for site in Sites:
            site.empty_site()
        

    #Getting the final results
    percentage_result.get_percentage(replication)

