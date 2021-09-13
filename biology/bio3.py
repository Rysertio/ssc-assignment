#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import os
from time import sleep
import getch 

ATP_Values = [["NADH",3],
              ["FADH",2],
              ["Acytyl COA",12],
              ["Pyruvic Acid",30],
              ["Glucose",38],
              ["GTP",1]]

cards=[]

for i in range(15):
    if -1<=i<5:
        cards.append(ATP_Values[5])
    elif i==5:
        cards.append(ATP_Values[4])
    elif 5<i<8:
        cards.append(ATP_Values[3])
    elif 7<i<10:
        cards.append(ATP_Values[2])
    elif 9<i<13:
        cards.append(ATP_Values[1])
    elif 12<i<15:
        cards.append(ATP_Values[0])

print(cards)

a, b, c = 0,0,0

while (a==b or b==c or a==c):
    a = random.randint(0,14)
    b = random.randint(0,14)
    c = random.randint(0,14)


print("%d %d %d" % (a,b,c))

xyz_energy = [cards[a][1], cards[b][1], cards[c][1]]
xyz = [a,b,c]

energy1loc = min(xyz)
energy2loc = max(xyz)

energy2val = xyz_energy[1] + xyz_energy[2]

losingpos = sorted(xyz)[1]

starting_energy = sum(xyz_energy)
winning_energy = starting_energy + max(xyz_energy) 

movement_costa, food_costa = 0, 0

def get_costs():
    global movement_costa, food_costa, movement_cost, food_cost
    movement_costa = int(input("Which card would you pick as movement cost (Pick between 0..2):"))
    food_costa = int(input("Which card would you pick as food cost (Pick between 0..2 but not %d):" % movement_costa))
    if not (movement_costa==food_costa):
        try:
            movement_cost = xyz_energy[movement_costa]
            food_cost = xyz_energy[food_costa]
        except expression as identifier:
            print("PLease enter a valid value.")
            get_costs()
    else:
        print("Please choose different Food cost and Movement cost")
        get_costs()
    
movement_cost = 0
food_cost = 0

get_costs()

realstartingenergy = starting_energy

endcondition = False
logs = ["step | description of move | ATP gained | ATP used | nit ATP","0 | aomeba started at position 0 | %d | 0 | %d" % (starting_energy,starting_energy)]

def end(iswin):
    os.system("clear")

    global endcondition
    endcondition = True

    if iswin==0:
        print("You've Won. Aeomeba can now multiply")
    elif iswin==1:
        print("Aeomeba got into the last room. \n Game over")
    else:
        print("You've Lost. Aeomeba will now form a cist")

    print("a= %s \n b = %s \n c = %s" % (str(cards[a]),str(cards[b]),str(cards[c])))
    print("d=b+c=%d" % energy2val)
    print("e=a+b+c= %d"%realstartingenergy)
    print("f=e+%s=%d"%(indextostr(xyz_energy.index(max(xyz_energy))),winning_energy))
    print("movement_cost "+str(movement_cost))
    print("food_cost %d" % food_cost)
    print("position of x %d" % a)
    print("position of y %d" % b)
    print("position of z %d" % c)

    for i in logs:
        print(i)
    
def indextostr(indi):
    if indi==0:
        return 'a'
    if indi==1:
        return 'b'
    if indi==2:
        return 'c'

visited = []

currentpos = 0

bar = "-----------------"
text = "| %s | %s | %s | %s |"
step_counter = -1

def print_grid():
    global starting_energy 
    global step_counter
    os.system("clear")
    usable = []
    print("Use WASD to move")

    starting_energy = starting_energy - movement_cost 
    step_counter += 1
    if currentpos == energy1loc:
        starting_energy -= food_cost
        starting_energy += xyz_energy[0]
        logs.append("%d | aomeba moved to position %d and ate | %d | %d | %d" % (step_counter,currentpos, xyz_energy[0], movement_cost + food_cost, starting_energy))
    
    elif currentpos == energy2loc:
        starting_energy -= food_cost
        starting_energy += energy2val
        logs.append("%d | aomeba moved to position %d and ate | %d | %d | %d" % (step_counter,currentpos, energy2val, movement_cost + food_cost, starting_energy))
    
    else:
        logs.append("%d | aomeba moved to position %d | 0 | %d | %d" % (step_counter,currentpos, movement_cost, starting_energy))
    
    print(starting_energy)
    for i in range(16):
        if i==currentpos:
            usable.append('O')
        elif (i) not in visited:
            usable.append(str(i))
        else:
            usable.append('X')
    for i in range(4):
        print(bar)
        print(text % (usable[15-i*4-3],usable[15-i*4-2],usable[15-i*4-1],usable[15-i*4]))
    print(bar)
    
    if currentpos == losingpos:
        end(2)
    elif starting_energy==winning_energy:
        end(0)
    elif currentpos==15:
        end(1)

starting_energy += movement_cost 
print_grid()

while (not endcondition):
    try:
        op = getch.getch()
    except Exception as e:
        print(e)
    if starting_energy >= movement_cost:
        if op=='w' and 16>(currentpos +4) and (currentpos + 4) not in visited:
            visited.append(currentpos)
            currentpos +=4
            print_grid()
        elif op=='a' and -1<(currentpos - 1) and not currentpos%4==0 and (currentpos - 1) not in visited:
            visited.append(currentpos)
            currentpos-=1
            print_grid()
        elif op=='s' and 0<(currentpos - 4) and (currentpos - 4) not in visited:
            visited.append(currentpos)
            currentpos-=4
            print_grid()
        elif op=='d' and 16>(currentpos + 1) and not (currentpos%4)==3 and (currentpos + 1) not in visited:
            visited.append(currentpos)
            currentpos+=1
            print_grid()

