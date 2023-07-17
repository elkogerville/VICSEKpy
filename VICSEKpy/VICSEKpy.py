def d3_vicsek(N, v0, box_lim, timesteps, dt, **kwargs):
    """
    this function calculates the x,y,z, positions and velocities of active matter based on the vicsek model
    -------------------------------------------------------------------------------------------------------
    N [integer]: number of particles in simulation
    v0 [float]: magnitude of initial velocity
    box_lim [integer]: boundary conditions of simulation
    timesteps [integer]: number of timesteps in simulation
    dt [float]: time interval of simulation
    --------
    **kwargs:
    eta [float]: default = 0.5; scale factor of random noise added to particle angles
    dampening [float]: default = 0.5; dampens random noise added to particle angles
    --------------------------------------------------------------------------------
    OUTPUT [numpy array]: returns x, y, z positions and velocities for all timesteps
    """
    import numpy as np
    
    ####################
    # initial conditions
    ####################
    
    # sphere of influence
    R = 1
    # ensure quantities are integers
    timesteps = int(timesteps)
    box_lim = int(box_lim)
    # noise parameter
    eta = 0.5
    if ('eta') in kwargs:
        eta = kwargs['eta']
    # dampening parameter
    dampening = 0.5
    if ('dampening') in kwargs:
        dampening = kwargs['dampening']
    
    # initialize Nx1 x, y, z, positions within box limits
    xpos = np.random.rand(N, 1)*box_lim
    ypos = np.random.rand(N, 1)*box_lim
    zpos = np.random.rand(N, 1)*box_lim
    
    # initialize theta and phi angles for spherical coordinates
    theta =  np.pi*np.random.rand(N,1) # randomized array of zenithal angles between 0 and pi
    phi = 2*np.pi*np.random.rand(N,1) # randomized array of azimuthal angles between 0 ans 2pi
    
    # x, y, z, velocities in spherical coordinates
    xvel = v0 * np.sin(theta) * np.cos(phi)
    yvel = v0 * np.sin(theta) * np.sin(phi)
    zvel = -v0 * np.cos(theta)
    
    # arrays for plotting
    xarr, vx = xpos, xvel
    yarr, vy = ypos, yvel
    zarr, vz = zpos, zvel
    
    #################
    # simulation loop
    #################
    
    print('\nsimulation running....  /ᐠ –ꞈ –ᐟ\<[pls be patient]')
    
    for i in range(timesteps):
        
        # advance particles using velocity
        xpos += xvel * dt
        ypos += yvel * dt 
        zpos += zvel * dt
        
        # apply boundary conditions using modulo operator
        xpos = xpos % box_lim
        ypos = ypos % box_lim
        zpos = zpos % box_lim 
        
        # append positions to array
        xarr = np.append(xarr, xpos, 0)
        yarr = np.append(yarr, ypos, 0)
        zarr = np.append(zarr, zpos, 0)
        
        # initiate average angles 
        avg_theta = theta
        avg_phi = phi

        for boid in range(N): # loop through every boid
            
            # calculate number of particles inside sphere of influence
            neighbors = ((xpos-xpos[boid])**2 + (ypos-ypos[boid])**2 + (zpos-zpos[boid])**2) < R**2
            
            # sum cos/sin of angles of boids inside sphere
            thetax = np.sum(np.cos(theta[neighbors]))
            thetay = np.sum(np.sin(theta[neighbors]))
            phix = np.sum(np.cos(phi[neighbors]))
            phiy = np.sum(np.sin(phi[neighbors]))
            
            # find the arctan of sums
            avg_theta[boid] = np.arctan2(thetay, thetax)
            avg_phi[boid] = np.arctan2(phiy, phix)
        
        # compute next angle using average angle and added noise
        theta = avg_theta + eta*(np.random.rand(N,1) - dampening)
        phi = avg_phi + eta*(np.random.rand(N,1) - dampening)
        
        # update velocities using new angles
        xvel = v0 * np.sin(theta) * np.cos(phi)
        yvel = v0 * np.sin(theta) * np.sin(phi)
        zvel = v0 * np.cos(theta)
        
        # append velocities to array
        vx = np.append(vx, xvel, 0)
        vy = np.append(vy, yvel, 0)
        vz = np.append(vz, zvel, 0)
        
        # print progress steps
        if i == timesteps/4:
            print('25% [...]')
            
        if i == timesteps/2:
            print('50% [...]')
            
        if i == timesteps*(3/4):
            print('75% [...]')
    
    print('simulation complete [yay!!! (ﾐΦ ﻌ Φﾐ)✿ *ᵖᵘʳʳ*]')
    
    return xarr, yarr, zarr, vx, vy, vz
