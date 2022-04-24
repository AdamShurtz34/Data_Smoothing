"""
Adam Shurtz
CS 1410
Project 6 - Data Visualization and Analysis
"""

import numpy as np
import glob
import matplotlib.pyplot as plt
import array



def analyze(fname):
    #create an array from data in file 'fname'
    a = np.loadtxt(fname)

    #create new 'smoothed' array of weighted averages from original array
    count = 3
    new_a_list = array.array('d',[a[0],a[1],a[2]])
    for i in range((len(a))-6):
        A = a[count-3]
        B = 2*a[count-2]
        C = 3*a[count-1]
        D = 3*a[count]
        E = 3*a[count+1]
        F = 2*a[count+2]
        G = a[count+3]
        newValue = (A+B+C+D+E+F+G)//15
        new_a_list.append(newValue)
        count += 1
    new_a_list.append(a[-3])
    new_a_list.append(a[-2])
    new_a_list.append(a[-1])

    #find pulses, adds the the start point of each pulse to an array
    countIndex = 0
    list_of_startPoints = array.array('i',[])
    for i in new_a_list:
        if countIndex == len(new_a_list)-2:
            break
        else:
            point1 = new_a_list[countIndex]
            point2 = new_a_list[countIndex+1]
            point3 = new_a_list[countIndex+2]
            rise = point3 - point1
            if rise >= 100:
                pulseStart = countIndex
                print(pulseStart)
                countIndex = countIndex + 2
                for i in new_a_list:
                    currentPoint = new_a_list[countIndex]
                    nextPoint = new_a_list[countIndex+1]
                    if nextPoint >= currentPoint:
                        countIndex += 1
                    else:
                        pulseStop = countIndex  #dont really need this variable
                        list_of_startPoints.append(pulseStart)
                        break    
            else:
                countIndex += 1
                
    #calculates the area of each pulse and adds it to an array
    areas_list = array.array('i',[])
    for i in range(len(list_of_startPoints)):
        if i == (len(list_of_startPoints)-1):
            point = list_of_startPoints[i]
            difference = (len(a)-1) - point
            if difference >= 50:
                total = 0
                for i in range(50):
                    total = total + a[point+i]
                areas_list.append(int(total))
            else:
                total = 0
                for i in range(difference):
                    total = total + a[point+i]
                areas_list.append(int(total))
                
        else:
            point = list_of_startPoints[i]
            nextPoint = list_of_startPoints[i+1]
            difference = nextPoint - point
        
            if difference > 50:
                total = 0
                for i in range(50):
                    total = total + a[point+i]
                areas_list.append(int(total))
            else:
                total = 0
                for i in range(difference):
                    total = total + a[point+i]
                areas_list.append(int(total))

    #writes pulse points and their areas to .out file
    filename = fname[:-4]+".out"
    file = open(filename,'w+')
    file.write(fname+':'+'\n')
    for i in range(len(list_of_startPoints)):
        startPoint = str((list_of_startPoints[i]) + 1)
        area = str(areas_list[i])
        file.write(startPoint + " " + "(" + area + ")" + "\n")
    file.close
      
    #create graphs for original and smooth arrays, save them to a pdf file
    fig,axes = plt.subplots(nrows=2)
    x = range(len(a))
    y = a
    axes[0].plot(x,y)
    axes[0].set(title=fname,ylabel='raw')
    x1 = range(len(new_a_list))
    y1 = new_a_list
    axes[1].plot(x1,y1)
    axes[1].set_ylabel("smooth")
    fig.savefig(fname[:-4]+".pdf")
    #plt.show()

    return("Analysis is complete: see output files")
    
    
def main():
    
    for fname in glob.glob('*.dat'):
        print(analyze(fname))
        
main()
