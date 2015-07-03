import os

#define some convenience variables and functions

x = '( 1 0 0 )'
y = '( 0 1 0 )'
z = '( 0 0 1 )'

#puts something in this form [a,b,c] to this form '( a b c )' for slurm
def list2Str(list):
    string = ''
    for l in list:
        string += str(l)
        string += ' '
    return string

#creates a string for making a block (assuming cartesian axes)
def getBlock(material, center, size):
    block = '(Object  Block (MaterialName ' + material + ' )\
                   (Center ' + list2Str(center) + ')\
                   (Axis0  1 0 0)\
                   (Axis1  0 1 0)\
                   (Axis2  0 0 1)\
                   (Size ' + list2Str(size) + ')\
    )'
    return block


#units for all lengths (m) all lengths will be in these units
lengthScale = '0.000001'

#grid size [x,y,z] (in units above)
gridSize = [0.05, 0.05, 0.05]

#total size of simulation domain
totalSize = [2, 2, 2]

#total time (scaled)
totalTime = 200

#duration of source (in scaled time)
sourceDuration = 200

#position of source (point source) (x,y,z)
sourcePos = []

#amplitude of source (units?)
sourceAmplitude = 1

#source (polarization?) (x,y,z)
sourceDir = y

#time offset of source
sourceOffset = 8

#with of source pulse (scaled time)
sourceWidth = 1.0

#frequency of pulse modulation (scaled time)
sourceFreq = 2.0


ws = [1,2]        #thickness of dielectrics
ts = [1,2]        #thickness of metals
hs = [3,4]        #width of rods
Ls = [5]      #length of rods
d = [1,2]         #center gap spacing
eps = [2,3,4]     #dielectric constants (from top to bottom [source above])




#change directory to your FDTD Directory
os.chdir('/Users/twh/Documents/Fan/FDTD_PLUS/')


for L in Ls:
    
    
    #open input file to write to
    f = open('test.txt', 'w')

  # TEST: 3D simulation of a linear antenna
    inputString = """
   (Option CellParam      (CellType linear)
                          (FieldType real)
   )
   (Option BoundaryParam  (Type pml pml pml) 
                          (PmlParam (Type upml) (Size (X 0.5) (Y 0.5) (Z 0.5) )
                          			(SigmaFactor (X 0.375) (Y 0.375) (Z 0.375) ) )
   )
   (Option DimensionParam (LengthScale """ + str(lengthScale) + """)
                          (Center 0 0 0)
                          (Resolution  """ + list2Str(gridSize) + """)
                          (Size """ + list2Str(totalSize) + """)
                          (TimeParam (End """ + str(totalTime) + """) )
   )
   // To enable CheckInput, remove
   (\Option CheckInput)
   // File will be output to structure.h5 by default.
   (Option OutputStructure)
   // RelPermittivity here is from effective index of  Si.
   (Material Prp (MaterialName metal)   // MaterialName value is user defined.
                    (MaterialToken 8)   // MaterialToken value is user defined.
                    (EpsilonInfinity 1)
                    (RelPermeability 1)
                    (PoleResiduePair
                        (Pair1 (2.2217e16, -6.3742e18) (-1.4982e14, 3.0413e11) )
                        (Pair2 (-6.4292e15, 1.3091e18) (-2.8617e13, -3.4173e13) )
                        (Pair3 (2.1046e16, 1.4907e15)  (-3.2597e15, -4.3949e15) )
                        (Pair4 (1.0807e15, 5.889e14)   (-4.4078e14, -3.9961e15) )
                        (Pair5 (-7.173e15, 2.5124e18)  (-3.3045e12, -1.0357e13) )
                        (Pair6 (-5.3709e15, 2.517e15)  (-1.9179e15, 7.2146e15) )
                        (Pair7 (-7.8496e14, 3.3901e18) (2.39e13, -5.5125e12) )
                        (Pair8 (-7.1488e15, 5.1946e18) (4.5398e13, 1.2772e12) )
                    )
   )

   (Material Lossless (MaterialName metal2)
                      (MaterialToken 9)
                      (RelPermittivity 1e20)
                      (RelPermeability 1)
   
   )
   (Material Lossless (MaterialName diel3)
                      (MaterialToken 15)
                      (RelPermittivity 5)
                      (RelPermeability 1)
   )
   (Material Lossless (MaterialName diel4)
                      (MaterialToken 16)
                      (RelPermittivity 3)
                      (RelPermeability 1)
   )
   (Material Lossless (MaterialName diel5)
                      (MaterialToken 18)
                      (RelPermittivity 7)
                      (RelPermeability 1)
   )

   (Source GaussTime (SourceName Source1)
                     (Duration 200)
                     (Center 8)
                     (Width 1.0)
                     (Frequency 2.0) // centered at lambda = 1/Frequency
                     (Phase 0)
                     (Amplitude 1)
                     (Direction 0 1 0)
   )

   (Output FieldTime (Position 0 0 0)
                     (StartTime 0)
                     (EndTime 200)
                     (TimeStep  0.002)
                     (FileName signal.dat)
                     (OutputField ey ex hz)
   )

   (Output FieldSpace (OutputField ex ey hz)
                      (StartTime 60)
                      (EndTime 61)
                      (TimeStep .002)
                      (FileName field_space_wide3)
    )
    // Build a source.
    (Object Point (SourceName Source1) (Center 0.3 0 0) 
    )

    // Build one antenna.
    (Object  Block (MaterialName metal2)
                   (Center 0 0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )
    
    (Object  Block (MaterialName metal2)
                   (Center 0 -0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )
    (Object  Block (MaterialName diel4)
                   (Center 0.05 0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )

    (Object  Block (MaterialName diel4)
                   (Center 0.05 -0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )
    (Object  Block (MaterialName metal2)
                   (Center 0.1 0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )

    (Object  Block (MaterialName metal2)
                   (Center 0.1 -0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )

    (Object  Block (MaterialName metal2)
                   (Center 0.2 0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )

    (Object  Block (MaterialName metal2)
                   (Center 0.2 -0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )
    (Object  Block (MaterialName diel5)
                   (Center 0.25 0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )
    
    (Object  Block (MaterialName diel5)
                   (Center 0.25 -0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )
    (Object  Block (MaterialName metal2)
                   (Center 0.3 0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )

    (Object  Block (MaterialName metal2)
                   (Center 0.3 -0.15 0)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size 0.05 0.2 0.1)
    )

    """
    
    f.write(inputString)
    
    f.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    