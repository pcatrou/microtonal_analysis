import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
def getDataFromFile (file):
    list = []
    with open('noteDeviations/'+ file +'.txt', 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            list.append(currentPlace)
    return list

halfToneNatural = [-1,0,2,4,5,7,None,None,None]
devNaturalScale = [-12,0,2,-14,-2,2,-16,-32,-12]

filesNames = []
filesNames.append("le-botchevrollier-melodie-gourin-2019")
filesNames.append("2018-fil-lorient-quillay-lothode-trophee-matilin-an-dall-12-aout")
filesNames.append("26 En Dro")
filesNames.append("27 Laridé")
filesNames.append("29 M'ami Mandal _ En Dro")
filesNames.append("30_Laride_Bal")
filesNames.append("28 Suite D'airs À Danser")

labels = [
    "Le bot/Chevrollier",
    "Lothodé/Quillay",
    "Magadur en dro",
    "Magadur Laridé", 
    "JM Tanguy En Dro",
    "Tanguy/Le Lain Laridé",
    "X. Burguin"]

markers =['k','g','go','gs','ro','rs','bo']

noteDeviations = []
noteHalfTones = []
halfTonesString = 'half-tones'
plt.plot(halfToneNatural,devNaturalScale,'b--', label ="échelle naturelle", linewidth=0.5)
i = 0
for file in filesNames:
    noteDeviations.append([float(item) for item in getDataFromFile(file)])
    noteHalfTones.append([int(item) if int(item) < 8 else None for item in getDataFromFile(file + halfTonesString)])
    plt.plot(noteHalfTones[i],noteDeviations[i],markers[i], label = labels[i])
    i += 1

plt.plot([4],[-84],'kX', label = "tierce mineure naturelle")
plt.axhline(0,color='gray') # x = 0
plt.axvline(0,color='gray') # y = 0
plt.grid(True)
#plt.plot(noteHalfTones[4],np.zeros(len(noteHalfTones[4])),'k')
plt.xlabel("demi-ton d'écart à la tonique")
plt.ylabel('déviation au tempérament égal (cents)')
plt.title('écart de hauteur des degrés par rapport au tempérament égal')
plt.legend()
plt.show()