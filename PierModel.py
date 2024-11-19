def units():
    global kN, T, Kg, m, cm, mm, N, sec, Pa, MPa, GPa
    kN = 1
    T = kN/9.81
    Kg = T / 1000
    m = 1
    cm = m / 100
    mm = m / 1000
    N = kN / 1000
    sec = 1
    Pa = N / m**2
    MPa = Pa * 1000000
    GPa = MPa * 1000

# Call the function to initialize the variables
units()

# List all variables to be exported
__all__ = ['kN', 'T', 'Kg', 'm', 'cm', 'mm', 'N', 'sec', 'Pa', 'MPa', 'GPa']


def materialProperties():
    global fpc1, fpcu1, epsc01, epsU1, lam1, ft1, Ets1, Fy, E0, b, R0, cR1, cR2,fpc2, fpcu2, epsc02, epsU2, lam2, ft2, Ets2
    # Confined concrete (set k=1.3)
    fpc1 = -39.0 * MPa  # fpc = k*30 = 1.3*30 = 39
    fpcu1 = -7.8 * MPa 
    epsc01 = -0.00285
    epsU1 = -0.01424
    lam1 = 0.1
    ft1 =  4.2 * MPa
    Ets1 = 2100 * MPa

    # Reinforcing steel
    Fy = 500.0* MPa  # referenced to steel 02 paper
    E0 = 20.0 * GPa
    b =  0.01
    R0 = 18 
    cR1 =  0.925
    cR2 = 0.15

    # Unconfined concrete
    fpc2 = -30.0* MPa  # fpc = k*30 = 1.3*30 = 39
    fpcu2 = -6.0 * MPa 
    epsc02 = -0.003
    epsU2= -0.01
    lam2 = 0.1
    ft2 =  4.2 * MPa
    Ets2 = 2100 * MPa

materialProperties()

__all__ += ['fpc1', 'fpcu1', 'epsc01', 'epsU1', 'lam1', 'ft1', 'Ets1', 'Fy', 'E0', 'b', 'R0', 'cR1', 'cR2','fpc2', 'fpcu2', 'epsc02', 'epsU2', 'lam2', 'ft2', 'Ets2']

def ModelPier():
    import openseespy.opensees as op
    import opsvis as opsv
    import vfo.vfo as vfo
    import matplotlib.pyplot as plt
    
    op.wipe()
    # Create ModelBuilder (with two-dimensions and 3 DOF/node)
    op.model('basic', '-ndm', 3, '-ndf', 6)

    op.node(102, 26.475, 0, -3.415)
    op.node(103, 26.475, 0, -8.995)

    #middle point
    # op.node(104,26.475,0,-6.205)

    op.mass(102,42.46,42.46, 42.46, 0, 0, 0)
    # op.mass(104,253*T, 253*T, 253*T, 0, 0, 0)
    # op.mass(103,100*T, 100*T, 100*T, 0, 0, 0)
    
    
    
    #fiber section
    op.uniaxialMaterial('Concrete02', 1, fpc1, epsc01, fpcu1, epsU1, lam1, ft1, Ets1)
    op.uniaxialMaterial('Steel02', 2, Fy, E0, b, R0, cR1, cR2)
    op.uniaxialMaterial('Concrete02', 3, fpc2, epsc02, fpcu2, epsU2, lam2, ft2, Ets2)
# ####################
    op.section('Fiber', 1, '-GJ', 1e11)  # why is torsional stiffness 1.0e11
    op.patch('circ', 1, 38, 20, 0, 0, 0, 0.915, 0, 360)
    op.patch('circ', 3, 3, 20, 0, 0, 0.915, 0.975, 0, 360)
    op.layer('circ', 2, 38, 0.000804, 0, 0, 0.915)  # 32 mm dia
    # element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)

    # op.element("elasticBeamColumn", 103)
    
    
    # CONSTRAINTS
    op.fix(103, 1, 1, 1, 1, 1, 1)

    # INTEGRATION
    op.beamIntegration('Lobatto', 1, 1, 10)
    # TRANSFER TAG
    op.geomTransf("Linear", 1, 0, 1, 0)
    # ELEMENT
    op.element('dispBeamColumn', 103, 103, 102,1,1)

    # opsv.plot_model()
