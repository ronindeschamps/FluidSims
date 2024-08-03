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
    
    changet = (0.03)
    t = 0  
    
    #fluid varible creation -----------------
    
    numcells = 100 * 300
    
    grid = np.zeros((nx, ny))
    
    vxarray = [[0.0 for _ in range(101)] for _ in range(301)]
    vyarray = [[0.0 for _ in range(101)] for _ in range(300)]
    
    #divergence(d)
    dxarray = [[0.0 for _ in range(100)] for _ in range(301)]
    dyarray = [[0.0 for _ in range(101)] for _ in range(300)]
    
    #stick(s)
    sxarray = [[1.0 for _ in range(100)] for _ in range(301)]
    syarray = [[1.0 for _ in range(101)] for _ in range(300)]
    
    sxarray[0] = [0.0 for _ in range(100)]
    sxarray[300] = [0.0 for _ in range(100)]
    for i in range(300):
        syarray[i][0] = 0
        syarray[i][100] = 0

    s_totalarray = [[0.0 for _ in range(100)] for _ in range(300)]
    
    for i in range(300):
        for j in range(100):
                s_totalarray[i][j] = sxarray[i][j] + sxarray[i+1][j] + syarray[i][j] + syarray[i][j+1]
        
    vyavgs = [[0.0 for _ in range(100)] for _ in range(300)]
    new_vy = [[0.0 for _ in range(101)] for _ in range(300)]
    new_vx = [[0.0 for _ in range(101)] for _ in range(301)]
    vvectors = [[(0.0, 0.0) for _ in range(100)] for _ in range(300)]
    prelocations = [[(0.0, 0.0) for _ in range(100)] for _ in range(300)]
    
    vf = -9.8 #flow velocity
        
    while True:


        #update fluid logic ------------
        for x in range(25, 76):
            vyarray[x][70] = 10

        
        for i in range(300):
            for j in range(101):
                if j == 0 or j == 100:
                    pass
                else:
                    vyarray[i][j] += changet * vf
                    
            #divergence = d = vx(i+1,j)-vx(i,j)+vy(i,j+1)-vy(i,j)
        
        for i in range(301):
            for j in range(100):
                if i == 0 or i == 300:
                    dxarray[i][j] = 0
                else:
                    dxarray[i][j] = vxarray[i+1][j]-vxarray[i][j]
                    
        for i in range(300):
            for j in range(101):
                if j == 0 or j == 100:
                    dyarray[i][j] = 0
                else:
                    dyarray[i][j] = vyarray[i][j+1]-vyarray[i][j]
                    
        darray = dyarray + dxarray
        darray = [[element * 1 for element in row] for row in darray]
        
            #correct for divergence
            
        for i in range(300):
            for j in range(100):
                vxarray[i][j] += darray[i][j] * (sxarray[i][j] / s_totalarray[i][j])
                vxarray[i+1][j] += darray[i][j] * (sxarray[i+1][j] / s_totalarray[i][j])
                vyarray[i][j] += darray[i][j] * (syarray[i][j] / s_totalarray[i][j])
                vyarray[i][j+1] += darray[i][j] * (syarray[i][j+1] / s_totalarray[i][j])
                
            #advection
        for i in range(300):
            for j in range(100):
                vyavgs[i][j] = (vyarray[i][j] + vyarray[i][j+1] + vyarray[i-1][j] + vyarray[i-1][j+1])/4
                #compute vvectors[i][j]
                vvectors[i][j] = (vxarray[i][j], vyavgs[i][j])
                #compute previous locaton
                prelocations[i][j] = (i - changet * vvectors[i][j][0], j - changet * vvectors[i][j][1])
                
        for i in range(300):
            for j in range(100):
                (pri, prj) = (int(prelocations[i][j][0]), int(prelocations[i][j][1]))
                x = get_frac(prelocations[i][j][0])
                y = get_frac(prelocations[i][j][1])
                #print(prelocations[i][j][0], prelocations[i][j][1])
                #print(pri, prj)
                #print(x, y)

                w1 = 1-x
                w2 = x
                w3 = 1-y
                w4 = y 
                
                if not (pri > 299 or prj > 99 or pri < 0 or prj < 0): 
                 
                    if pri == 299:
                        new_vy[i][j] = w1*w3*vyarray[pri][prj] + 0 + w2*w4*vyarray[pri][prj+1] + 0
                    else:
                        new_vy[i][j] = w1*w3*vyarray[pri][prj] + w2*w3*vyarray[pri+1][prj] + w2*w4*vyarray[pri][prj+1] + w1*w4*vyarray[pri+1][prj+1]
                    if pri == 299:
                        new_vx[i][j] = w1*w3*vxarray[pri][prj] + 0 + w2*w4*vxarray[pri][prj+1] + 0
                    else:
                        new_vx[i][j] = w1*w3*vxarray[pri][prj] + w2*w3*vxarray[pri+1][prj] + w2*w4*vxarray[pri][prj+1] + w1*w4*vxarray[pri+1][prj+1]
                
        vyarray == new_vy
        vxarray == new_vx


        #update color values
        
        for i in range(300):
            for j in range(100):
                pass
                grid[i][j] = np.sqrt(vyarray[i][j]**2 + vxarray[i][j]**2)/2
        
        #-------------------------------
        axs.clear()
        
        velocity_magnitudes = grid

        # Normalize the magnitudes to range [0, 1] for colormap
        norm_velocity = (velocity_magnitudes - np.min(velocity_magnitudes)) / (np.max(velocity_magnitudes) - np.min(velocity_magnitudes))

        # Display the grid with colors based on velocity
        axs.imshow(norm_velocity, cmap='viridis')
        
        
        plt.pause(changet)
        
        plt.show()
    
        if not plt.get_fignums(): 
            break 

    plt.ioff()

main()