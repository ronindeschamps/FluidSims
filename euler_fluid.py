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
        
    def samplefield(x, y, array, dx, dy):
        
        n = 302
        h1 = 1
        h2 = 0.5
        
        x0 = min(math.floor(x-dx), 300)
        tx = ((x-dx) - x0)
        x1 = min(x0 + 1, 300)
        y0 = min(math.floor(y-dy), 301)
        ty = (y-dy) - y0 
        y1 = min(y0 + 1, 101)
        
        sx = 1.0 - tx
        sy = 1.0 - ty
        
        val = sx*sy * array[x0][y0] + tx*sy * array[x1][y0] + tx*ty * array[x1][y1] + sx*ty * array[x0][y1]
        
        return val      
        
    #graph creation -----------------
    
    nx, ny = 300, 100
    fig, axs = plt.subplots(figsize=(12, 4))

    plt.ion() 
    plt.show() 
    
    changet = (0.003) 
       
    #fluid varible creation -----------------
    
    grid = np.zeros((nx, ny))
    
    vxarray = [[0.0 for _ in range(102)] for _ in range(302)]
    vyarray = [[0.0 for _ in range(102)] for _ in range(302)]
    
    marray = [[0.0 for _ in range(102)] for _ in range(302)]
    new_m = [[0.0 for _ in range(102)] for _ in range(302)]
    
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
        
    for j in range(40, 60):
        sarray[250][j] = 0.0

        
    vyavgs = [[0.0 for _ in range(101)] for _ in range(301)]
    new_vy = [[0.0 for _ in range(102)] for _ in range(302)]
    new_vx = [[0.0 for _ in range(102)] for _ in range(302)]
    vvectors = [[(0.0, 0.0) for _ in range(101)] for _ in range(301)]
    prelocations = [[(0.0, 0.0) for _ in range(101)] for _ in range(301)]
    
    g = 0.0
        
    while True:

        vxarray[299][45] = -300
        vxarray[299][46] = -300
        vxarray[299][47] = -300
        vxarray[299][48] = -300
        vxarray[299][49] = -300
        vxarray[299][50] = -300
        vxarray[299][51] = -300
        vxarray[299][52] = -300
        vxarray[299][53] = -300
        vxarray[299][54] = -300
       
        

        for i in range(1, 301):
            for j in range(1, 101):
               vyarray[i][j] += changet * g
                   
        #divergence = d = vx(i+1,j)-vx(i,j)+vy(i,j+1)-vy(i,j)
        #ajust velocities for incompressablity
        
        
        for i in range(1, 301):
            for j in range(1, 101):
                
                if sarray != 0:
                    d = 0.5*(vxarray[i+1][j] - vxarray[i][j] + vyarray[i][j+1] - vyarray[i][j])
                    
                    s = sarray[i+1][j] + sarray[i-1][j] + sarray[i][j+1] + sarray[i][j-1]

                    vxarray[i][j] += d* (sarray[i-1][j] / s)
                    vxarray[i+1][j] -= d* (sarray[i+1][j] / s)
                    vyarray[i][j] += d* (sarray[i][j-1] / s)
                    vyarray[i][j+1] -= d* (sarray[i][j+1] / s)
        
        #extrapolation
        
        for i in range(301):
            vxarray[i][0] = vxarray[i][1]
            vxarray[i][100] = vxarray[i][99]
        for j in range(101):
            vyarray[0][j] = vyarray[1][j]
            vyarray[300][j] = vyarray[299][j]
            
        #advection        
        
        for i in range(1, 301):
            for j in range(1, 101):
                
                if sarray[i][j] != 0 and sarray[i-1][j] != 0:
                    x = i 
                    y = j + 0.5
                    vx = vxarray[i][j]
                    vy = (vyarray[i][j] + vyarray[i][j+1] + vyarray[i-1][j] + vyarray[i-1][j+1])/4
                    x -= changet*vx
                    y -= changet*vy
                    vx = samplefield(x, y, vxarray, 0, 0.5)
                    new_vx[i][j] = vx
                    
                if sarray[i][j] != 0 and sarray[i][j-1] != 0:
                    x = i + 0.5
                    y = j
                    vx = (vxarray[i][j-1] + vxarray[i][j] + vxarray[i-1][j+1] + vxarray[i][j+1])/4
                    vy = vyarray[i][j]
                    vy = samplefield(x, y, vyarray, 0.5, 0)

        vyarray = new_vy
        vxarray = new_vx
        
        for i in range(1, 301):
            for j in range(1, 101):
                
                if sarray[i][j] != 0:
                    vx = (vxarray[i][j] + vxarray[i+1][j]) * 0.5
                    vy = (vyarray[i][j] + vyarray[i][j+1]) * 0.5
                    x = i + 0.5 - changet*vx
                    y = j + 0.5 - changet*vy
                    
                    new_m[i][j] = samplefield(x, y, marray, 0.5, 0.5) 
        marray = new_m

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