from NS1 import *
import matplotlib.pyplot as plt
import numpy as np

#plt.style.use('dark_background')
f = plt.figure()
f.set_figwidth(10)
f.set_figheight(6)


generations = 35

def main():
    print()

    Initialize_Populatiom()
    #Initialize_Populatiom_Generous()
    #Initialize_Populatiom_Psychopath()
    print(generation_statistics())

    print()

    generation = 0
    x = []
    P_Score = []
    E_Score = []
    G_Score = []
    S_Score = []

    for i in range(generations):
        print()
        Simulate()
        print(generation_statistics())
        print(f"Generation: {generation}")


        stats = get_statistics()
        #if(stats["size"]==0):
        #     break
        
        P_Score.append(stats["P"])
        E_Score.append(stats["E"])
        G_Score.append(stats["G"])
        S_Score.append(stats["S"])
        x.append(generation)
        generation+=1

        if(stats["size"]==0 or stats["size"]>5000):
            break
    #print(get_action_statistics())

    P_Score = np.array(P_Score)
    E_Score = np.array(E_Score)
    G_Score = np.array(G_Score)
    S_Score = np.array(S_Score)

    xpoints = np.array(x)

    plt.style.use('dark_background')

    plt.plot(xpoints, P_Score, label="Psychopath")
    plt.plot(xpoints, E_Score, label="Egotistic")
    plt.plot(xpoints, G_Score, label="Generous")
    plt.plot(xpoints, S_Score, label="Sacrifice")

    plt.legend()
    plt.show()

if __name__=="__main__":
        #for i in range(10):
        main()



"""
    So far it appears selfishness is evolutionarily more advantagous than generosity

    Running thoery:
        generosity is useful by the golden rule


    Self Sacrifice and Generosity are stable
    Generosity is Stable
    Self Sacrifice is not stable
    
    Introducing just a little egotism wins overall (gains benefit of generosity plus self interest)
    Even with green beard generosity egotism wins
"""