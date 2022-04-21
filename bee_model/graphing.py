import plotly.graph_objects as go

#This file creates a sankey diagram depicting the movement
#of bees across the simulation

def sankey_diagram(Dict, Sites):
    #Label needs to bee all Sites for all iterations 
    label = []
    #How many bees migrate 
    value_list = []
    #Bees at site s for t-1
    source = []
    #Bees at site s for t
    target = []

    #For visualisation reasons we're only depicting
    #every 30th Iteration
    nth = 30

    #Dict is the dict that contains the states for the iterations
    #Index is the Iteration Index
    for index, value in enumerate(Dict):
        #Looping through all states
        for id in range(len(Sites)):
            #Creating the States + Adding identifier S0,S1, S2, S3, S4 or S5
            label.append("S" + str(id)) 
        #No we go through alle lists of agent:state pairs
        if(index==0):
            #First Iteration
            past_dict = Dict[index]
            continue
        else:
            if(index%nth == 0):
                present_dict = Dict[index]
                for key, v in enumerate(present_dict):
                    #comparing the states at t and t-1
                        target_index = (index*len(Sites))+present_dict[key]
                        source_index = ( (index-nth) *len(Sites))+past_dict[key]
                        value_int = 1
                        source.append(source_index)
                        target.append(target_index)
                        value_list.append(value_int)
                past_dict = present_dict
            if(index == 299):
                #Last iteration needed a seperate condition
                present_dict = Dict[index]
                for key, v in enumerate(present_dict):
                    target_index = (index*len(Sites))+present_dict[key]
                    source_index = ( (index-29) *len(Sites))+past_dict[key]
                    value_int = 1
                    source.append(source_index)
                    target.append(target_index)
                    value_list.append(value_int)


    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            color = "black",
            label = label,
        ),
        link = dict(
            source = source, # indices correspond to labels, eg A1, A2, A1, B1, ...
            target = target,
            value = value_list
    ))])

    fig.update_layout(title_text="Site activity throughout simulation - 150 Bees - Normal Site Quality", font_size=10)
    fig.show()