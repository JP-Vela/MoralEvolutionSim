import random
import copy

init_pop_size = 100 #even split
global population
population = []
genes = ["E", "G"]
#genes = ["E", "G", "G"]

global donations
donations = 0


kill_rate = 0.0 #30% chance psychopath kills a member
steal_rate = 0.2 #30% chance egotistic steals from a member

def random_survival():
    return random.uniform(0.5,1.5)
    #return 1.0


#Morality Genes: Psychopathy, egotism, generosity, self-sacrifice

#Morality isn't utilitiarianism

#Psychopath: randomly kills someone in population
#Egotism: keeps surplus
#Generosity: gives surplus
#Self-sacrifice: generous but gives own life if no surplus (own kin)

#Reason excluded

#1 Gene at a time

#Initialize population
def Initialize_Populatiom():
    member = {}

    for i in range(init_pop_size):
        selected_gene = ""

        """if i < init_pop_size/4*1:
            selected_gene = genes[0]
        
        elif i < init_pop_size/4*2:
            selected_gene = genes[1]

        elif i < init_pop_size/4*3:
            selected_gene = genes[2]

        elif i < init_pop_size/4*5:
            selected_gene = genes[3]"""

        member["type"] = genes[random.randint(0,len(genes)-1)]
        member["chance"] = random_survival()#random.uniform(0.7,1.5)
        member["alive"] = True

        population.append(copy.deepcopy(member))


def Initialize_Populatiom_Generous():
    member = {}

    for i in range(init_pop_size):
        gene_selected = ""

        gene_selected = genes[2]

        member["type"] = gene_selected
        member["chance"] = random_survival()#random.uniform(0.7,1.5)
        member["alive"] = True

        population.append(copy.deepcopy(member))

def Initialize_Populatiom_Psychopath():
    member = {}

    for i in range(init_pop_size):
        gene_selected = ""

        gene_selected = genes[0]

        member["type"] = gene_selected
        member["chance"] = random.uniform(0.7,1.5)
        member["alive"] = True

        population.append(copy.deepcopy(member))


def Simulate():
    global population
    global donations
    #donations = 0


    for i in range(len(population)):
        member = population[i]

        #Actions, not determining survival

        if member["type"] == "P": #Psychopath (kill)
            if random.random() < kill_rate:
                target = random_exclude(0,len(population)-1,i)
                population[target]["alive"] = False #kill another member
                #population[i]["chance"] += population[target]["chance"]

        elif member["type"] == "E": #Egotistic (steal)
            if random.random() < steal_rate:
                target = random_exclude(0,len(population)-1,i)
                needed = 1-population[i]["chance"]
                stolen = min(population[target]["chance"], needed)
                population[i]["chance"]+=stolen #steal half of another member's chance to live
                population[target]["chance"] -= stolen

        elif member["type"] == "G": #Generous
            if member["chance"] > 1:
                #donations+=1

                surplus = member["chance"] - 1
                population[i]["chance"] -= surplus

                in_need = find_in_need_random(i)

                #Added green beard generosity
                if(in_need !=-1 and (population[in_need]["type"] == "G")):
                    population[in_need]["chance"] += surplus
                    #if(population[in_need]["chance"]>=1):
                    #donations+=1
                    #print("Donated to:" + str(population[in_need]["type"]))


        elif member["type"] == "S": #Self-Sacrifice
            in_danger = find_in_danger()

            needed = 1-population[in_danger]["chance"] #how much needed
            sacrifice = 0 #how much is being sacrificed

            if population[i]["chance"] >= needed:
                sacrifice = population[i]["chance"] - needed

            elif population[i]["chance"] < needed:
                sacrifice = population[i]["chance"]

            #Give chance to the one in danger of dying
            population[i]["chance"] -= sacrifice
            population[in_danger]["chance"] += sacrifice
        
    #print(f"DONATIONS: {donations}")


    #Determine survival and reproduction
    temp_pop = []
    death_toll = 0
    for i in range(len(population)):
        #print(population[i]["chance"])

        if(population[i]["chance"] < 1.0):
            population[i]["alive"] = False

        if population[i]["alive"]:
            population[i]["chance"] = random_survival()#random.uniform(0.7,1.5)
            
            #print(population[i]["chance"])
            
            temp_pop.append(copy.deepcopy(population[i]))
            temp_pop.append(copy.deepcopy(population[i]))
        else:
            death_toll+=1

    #print(f"DEATH TOLL: {death_toll}")
    population = copy.deepcopy(temp_pop)


def random_exclude(lower, upper, exclude):
    ret = random.randint(lower, upper)

    while(ret == exclude):
        ret = random.randint(lower, upper)

    return ret


def find_in_need():

    for i in range(len(population)):

        member = population[i]
        if(member["chance"] < 1): # and member["type"] == "G"):
            return i
        
    return - 1
        
def find_in_need_random(exclude):
    i = random.randint(0,len(population)-1)

    while i==exclude:
        i = random.randint(0,len(population)-1)
    
    member = population[i]
    if(member["chance"] < 1):
        return i
        
    return -1

def find_in_danger():
    most_need = 0

    for i in range(len(population)):

        member = population[i]

        if(member["chance"] < population[most_need]["chance"]):
            most_need = i

    return most_need



def generation_statistics():
    mw = 16 #message width

    num_P = 0
    num_E = 0
    num_G = 0
    num_S = 0
    size = len(population)
    if(size==0):
        return "Population died"

    for member in population:
        if member["type"] == "P":
            num_P += 1

        elif member["type"] == "E":
            num_E += 1

        elif member["type"] == "G":
            num_G += 1

        elif member["type"] == "S":
            num_S += 1

    percent_P = round(num_P/size*100)
    percent_E = round(num_E/size*100)
    percent_G = round(num_G/size*100)
    percent_S = round(num_S/size*100)

    global donations
    return f"Psychopaths: {percent_P}% \nEgotistics: {percent_E}% \nGenerous: {percent_G}% \nSelf-Sacrificing: {percent_S}% \n\nPopulation Size: {size} \nDonations: {donations}"


def get_statistics():

    num_P = 0
    num_E = 0
    num_G = 0
    num_S = 0
    size = len(population)

    if(size==0):
        percent_P = 0
        percent_E = 0
        percent_G = 0
        percent_S = 0
        return {"P":percent_P, "E":percent_E, "G": percent_G, "S": percent_S, "size":size}
    
    for member in population:
        if member["type"] == "P":
            num_P += 1

        elif member["type"] == "E":
            num_E += 1

        elif member["type"] == "G":
            num_G += 1

        elif member["type"] == "S":
            num_S += 1

    percent_P = round(num_P/size*100)
    percent_E = round(num_E/size*100)
    percent_G = round(num_G/size*100)
    percent_S = round(num_S/size*100)

    #return {"P":percent_P, "E":percent_E, "G": percent_G, "S": percent_S, "size":size, "donations":donations}
    return {"P":num_P, "E":num_E, "G": num_G, "S": num_S, "size":size}