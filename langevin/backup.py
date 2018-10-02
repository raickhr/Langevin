# -*- coding: utf-8 -*-

"""Main module."""

import numpy as np
import argparse
import random
import matplotlib.pyplot as plt

#List of functions 
def calc__vis_force(velocity):
    #function to calculae the viscous force
    vis_force =  - gamma * velocity

    #returning the viscous force
    return vis_force

def calc_rand_force():
    #function to calculate the random force
    
    #first calculate the standard deviation. We already know that the mean is zero
    mean = 0.0
    variance = 2 * temperature * gamma * kB
    standard_deviation = np.sqrt(variance)

    # generate a random number with the calculated mean and standard deviation
    zeta = random.normalvariate(mean,standard_deviation)

    # returning the random force
    
    return zeta


def acc(velocity):
    #function to calculate acceleration from the 
    acc = calc__vis_force(velocity) + calc_rand_force()
    return acc 

def update_velocity(velocity):

    #calculate updated velocity from RK4 method
    k1 = dt * acc(velocity)
    k2 = dt * acc(velocity + k1/2)
    k3 = dt * acc(velocity * k2/2)
    k4 = dt * acc(velocity + k3)

    updated_velocity = velocity + 1/6 * k1 + 1/3 * k2  +1/3 * k3 + 1/6 * k4

    return updated_velocity

def update_pos(velocity,position):
     #calculate updated position from RK4 method

    k1 = dt * velocity
    k2 = dt * velocity
    k3 = dt * velocity
    k4 = dt * velocity

    updated_position = position + 1/6 * k1 + 1/3 * k2  +1/3 * k3 + 1/6 * k4

    return updated_position



# defining main function

def main():
    global initial_velocity, initial_position
    stop_time = [] # time the particle reaches to one of the walls

    ff =  open("../langevin/finalpositions.txt","w") #opening file to write index, stop time, position, velocity' at the time when the particle stops

    ff.write("index,\t stop time ,\t position ,\t velocity \n" ) # writing the headings in the first line

    fig = plt.figure() #figure for plotting the trajectories and histogram

    for runs in range(0,no_of_runs): # runs start here
    
        #for every run the following variables are to be initialized

        position = initial_position
        velocity = initial_velocity
        current_time = 0.0
        pos_array = [position]
        time_array = [current_time]

        #iterations start for every run
        for iterations in range(0,no_of_iterations):
        
            current_time += dt # update time
            velocity = update_velocity(velocity) # update velocity
            position = update_pos(velocity,position) # update position
            
            #condition for the particle to stop i.e. when the particle reaches wall
            if (position <= wall_pos1) or (position >= wall_pos2):
                stop_time.append(current_time)
                break   # stop iterations when the particle reaches the wall
    
            
            pos_array.append(position) # store position for every iteration to plot for the trajectory
            time_array.append(current_time) # store values for the time axis
        
            
        ff.write("%3d,\t% 5.4f,\t% 5.4f,\t% 5.4f \n" % (runs,current_time,position,velocity)) # write the time, final position, final_velocity, when the particle stops 
        plt.plot(time_array,pos_array) # plotting the trajectories

    #plt.show()
    fig.savefig('../langevin/trajectory.png') #saving figure as trajectory.png

    fig.clear() #clearing figure for writing histogram

    mybins = [0,2,4,6,8,10] # bins for the histogram
    plt.hist(stop_time, mybins, histtype= 'bar',rwidth = 0.8, range=(-1,11)) # plotting the histogram

    fig.savefig('../langevin/histogram.png') #saving the histogram

    #plt.show()
    ff.close() # closing the file

# Read the command line arguments if it is there else assing the default values 
parser = argparse.ArgumentParser()
parser.add_argument('--temperature', help="Temperature of the particle", type = float, default = 1)
parser.add_argument('--total_time', help="Total time of the simulation", type = float, default = 10)
parser.add_argument('--time_step', help="Timestep of the simulation", type = float, default = 1)
parser.add_argument('--initial_position', help="Initial position of the particle", type = float, default = 1)
parser.add_argument('--initial_velocity', help="Initial velocity of the particle", type = float, default = 1)
parser.add_argument('--damping_coefficient', help="Damping coefficient", type = float, default = 1)

args=parser.parse_args()

#Global variables
initial_position = args.initial_position
initial_velocity = args.initial_velocity
temperature = args.temperature
total_time = args.total_time
dt = args.time_step

gamma = args.damping_coefficient
kB = 1         #Boltzman constant

wall_pos1 = 0.0 # wall position 1
wall_pos2 = 5.0 # wall position 2

no_of_iterations = int(total_time//dt)  

no_of_runs = 100

if __name__ == '__main__':
    main()