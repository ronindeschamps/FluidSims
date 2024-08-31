import matplotlib.pyplot as plt
import numpy as np
import time
import math

def main():
    
    def get_frac(num):
        decimal_part = math.modf(num)[0]
        if decimal_part > 0:
            return int(str(decimal_part)[2])
        else: 
            return 0
        
    #graph creation -----------------
    
    nx, ny = 300, 100
    fig, axs = plt.subplots(figsize=(12, 4))

    plt.ion() 
    plt.show() 
    
    changet = (0.1) 
       
    #fluid varible creation -----------------
    
    grid = np.zeros((nx, ny))
    
    vxarray = [[0.0 for _ in range(102)] for _ in range(302)]
    vyarray = [[0.0 for _ in range(102)] for _ in range(302)]
    
    #divergence(d)
    darray = [[0.0 for _ in range(101)] for _ in range(301)]
    
    #stick(s)
    sarray = [[1.0 for _ in range(102)] for _ in range(302)]
    
    for j in range(102):
        sarray[0][j] = 0.0
        sarray[301][j] = 0.0
        
    for i in range(302):
        sarray[i][0] = 0.0
        sarray[i][101] = 0.0
        
    s_totalarray = [[0.0 for _ in range(102)] for _ in range(302)]

        
    vyavgs = [[0.0 for _ in range(101)] for _ in range(301)]
    new_vy = [[0.0 for _ in range(102)] for _ in range(302)]
    new_vx = [[0.0 for _ in range(102)] for _ in range(302)]
    vvectors = [[(0.0, 0.0) for _ in range(101)] for _ in range(301)]
    prelocations = [[(0.0, 0.0) for _ in range(101)] for _ in range(301)]
    
    vf = -9.8 #flow velocity
        
    while True:

        for i in range(1, 301):
            for j in range(1, 101):
                vyarray[i][j] += changet * vf
                    
        #divergence = d = vx(i+1,j)-vx(i,j)+vy(i,j+1)-vy(i,j)
        
        for i in range(1, 301):
            for j in range(1, 101):
                
                s_totalarray[i][j] = sarray[i+1][j] + sarray[i-1][j] + sarray[i][j+1] + sarray[i][j-1]

                darray[i][j] = 1.9*(vxarray[i+1][j] - vxarray[i][j] + vyarray[i][j+1] - vyarray[i][j])
  
                vxarray[i][j] += darray[i][j] * (sarray[i-1][j] / s_totalarray[i][j])
                vxarray[i+1][j] -= darray[i][j] * (sarray[i+1][j] / s_totalarray[i][j])
                vyarray[i][j] += darray[i][j] * (sarray[i][j-1] / s_totalarray[i][j])
                vyarray[i][j+1] -= darray[i][j] * (sarray[i][j+1] / s_totalarray[i][j])
                
            #advection
        for i in range(1, 301):
            for j in range(1, 101):
                vyavgs[i][j] = (vyarray[i][j] + vyarray[i][j+1] + vyarray[i-1][j] + vyarray[i-1][j+1])/4
                #compute vvectors[i][j]
                vvectors[i][j] = (vxarray[i][j], vyavgs[i][j])
                #compute previous locaton
                prelocations[i][j] = (i - (changet * vvectors[i][j][0]), j - (changet * vvectors[i][j][1]))
                

                #-----------------------------------------------------------------------------------------------------
                
        for i in range(1, 301):
            for j in range(1, 101):
                
                (pri, prj) = (int(prelocations[i][j][0]), int(prelocations[i][j][1]))
                x = get_frac(prelocations[i][j][0])
                y = get_frac(prelocations[i][j][1])

                w1 = 1-x
                w2 = x
                w3 = 1-y
                w4 = y 
                
                if not (pri > 300 or prj > 100 or pri < 0 or prj < 0): 
                    
                    new_vy[i][j] = w1*w3*vyarray[pri][prj] + w2*w3*vyarray[pri+1][prj] + w2*w4*vyarray[pri][prj+1] + w1*w4*vyarray[pri+1][prj+1]
                    new_vx[i][j] = w1*w3*vxarray[pri][prj] + w2*w3*vxarray[pri+1][prj] + w2*w4*vxarray[pri][prj+1] + w1*w4*vxarray[pri+1][prj+1]
                 
                    '''if pri == 299:
                        new_vy[i][j] = w1*w3*vyarray[pri][prj] + 0 + w2*w4*vyarray[pri][prj+1] + 0
                    else:
                        new_vy[i][j] = w1*w3*vyarray[pri][prj] + w2*w3*vyarray[pri+1][prj] + w2*w4*vyarray[pri][prj+1] + w1*w4*vyarray[pri+1][prj+1]
                    if pri == 300:
                        new_vx[i][j] = w1*w3*vxarray[pri][prj] + 0 + w2*w4*vxarray[pri][prj+1] + 0
                    else:
                        new_vx[i][j] = w1*w3*vxarray[pri][prj] + w2*w3*vxarray[pri+1][prj] + w2*w4*vxarray[pri][prj+1] + w1*w4*vxarray[pri+1][prj+1]
                    '''
                
        vyarray = new_vy
        vxarray = new_vx


        #update color values
        
        for i in range(1, 301):
            for j in range(1, 101):
                try:
                    magnitude = np.sqrt(vyarray[i][j]**2 + vxarray[i][j]**2)
                    grid[i-1][j-1] = magnitude / 2
                except OverflowError as e:
                    print(f"OverflowError at index ({i}, {j}): vyarray[i][j]={vyarray[i][j]}, vxarray[i][j]={vxarray[i][j]}")
                    raise e
        
        #-------------------------------
        axs.clear()
        
        velocity_magnitudes = grid

        # Normalize the magnitudes to range [0, 1] for colormap
        norm_velocity = (velocity_magnitudes - np.min(velocity_magnitudes)) / (np.max(velocity_magnitudes) - np.min(velocity_magnitudes))

        rotated_velocity = np.rot90(norm_velocity)
        # Display the grid with colors based on velocity
        axs.imshow(rotated_velocity, cmap='rainbow')
        
        
        plt.pause(changet)
        
        plt.show()
    
        if not plt.get_fignums(): 
            break 

    plt.ioff()

main()