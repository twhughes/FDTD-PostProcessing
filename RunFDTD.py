import os
from subprocess import call

#define some convenience variables and functions

x = '1 0 0'
y = '0 1 0'
z = '0 0 1'

reference = False

#puts something in this form [a,b,c] to this form '( a b c )' for slurm
def list2Str(list):
    string = ''
    for l in list:
        string += str(l)
        string += ' '
    return string

#creates a string for making a block (assuming cartesian axes)
def getBlock(material, center, size):
    block = """
    (Object  Block (MaterialName """ + material + """)
                   (Center """ + list2Str(center) + """)
                   (Axis0  1 0 0)
                   (Axis1  0 1 0)
                   (Axis2  0 0 1)
                   (Size """ + list2Str(size) + """)
    )
    """
    return block

#makes a new material (string)
def getMaterial(eps, index):
    mat = """
    (Material Lossless (MaterialName diel""" + str(index) + """)
            (MaterialToken """ + str(index) + """)
            (RelPermittivity """ + str(eps) + """)
            (RelPermeability 1)
    )
    """
    return mat
               
#units for all lengths (m) all lengths will be in these units
lengthScale = '0.000001'

#grid size [x,y,z] (in units above)
gridSize = [1.0, 1.0, 1.0]

pmlSize = [10.0,10.0,10.0]
#total size of simulation domain
totalSize = [100, 100, 50]

#total time (scaled)
totalTime = 5000

#duration of source (in scaled time)
sourceDuration = 2000

#position of source (point source) (x,y,z)
sourcePos = [-10.0,0,0]

#amplitude of source (units?)
sourceAmplitude = 1

#source (polarization?) (x,y,z)
sourceDir = y

#time offset of source
sourceOffset = 200

#with of source pulse (scaled time)
sourceWidth = 50

#frequency of pulse modulation (scaled time)
sourceFreq = 0.013

substrate = False

subType = 'gold'   #'PEC' 'gold' 'dielx' where 'x' is the diel constant

ws = [4.0]           #thickness of dielectrics
ts = [4.0]           #thickness of metals
hs = [4.0]           #width of rods
Ls = [10.0]           #length of rods
ds = [4.0]            #center gap spacing
epsList = [1,10,4]     #dielectric constants (from top to bottom [source above])

metalType = 'gold'   #'PEC' or 'gold'

outputFields = 'ex ey hz'

measurePos = [0,0,0]  #
timeDataOutFile = 'signal5.dat'
timeStep = 0.0002

fieldDataOutFile = 'fieldTime'
fieldStartTime = 60
fieldEndTime = 100
fieldTimeStep = 0.02

#change directory to your FDTD Directory
os.chdir('/Users/twh/Documents/Fan/FDTD_PLUS/')

if (reference):
    totalTime = sourceDuration
    
#loop through size parameters
for L in Ls:
    for t in ts:
        for w in ws:
            for h in hs:
                for d in ds:

                    materials = ''
                    blocks = ''
                
                    #offset index (material token) to make room for free space, PML, Au (4) and PEC (5)
                    index = 6
                
                    xCenter = 0
                    yCenter = d/2 + L/2
                    print d
                    print L
                    print yCenter
                    zCenter = 0
                    if (not reference):
                        for eps in epsList:
                            materials += getMaterial(eps, index)
                            matName = 'diel' + str(index)
                        
                            blocks += getBlock(metalType, [xCenter,  yCenter, zCenter], [t,L,h])
                            blocks += getBlock(metalType, [xCenter, -yCenter, zCenter], [t,L,h])
                        
                            xCenter += t/2 + w/2
                        
                            blocks += getBlock(matName, [xCenter,  yCenter, zCenter], [w,L,h])
                            blocks += getBlock(matName, [xCenter, -yCenter, zCenter], [w,L,h])
                        
                            xCenter += t/2 + w/2
                    
                            index += 1
                        blocks += getBlock(metalType, [xCenter,  yCenter, zCenter], [t,L,h])
                        blocks += getBlock(metalType, [xCenter, -yCenter, zCenter], [t,L,h])
                        
                        #substrate
                        if (substrate):
                            blocks += getBlock(subType, [1/4*totalSize[0]+t/4+xCenter/2,0,0], [totalSize[0]/2 - t/2 - xCenter,totalSize[1],totalSize[2]])
                    else:
                        timeDataOutFile = 'signal_ref.dat'
                        
                    #open input file to write to
                    f = open('input.txt', 'w')

                  # TEST: 3D simulation of a linear antenna
                    inputString = """
                   (Option CellParam      (CellType linear)
                                          (FieldType real)
                   )
                   (Option BoundaryParam  (Type pml pml pml) 
                                          (PmlParam (Type upml) (Size (X """ + str(pmlSize[0]) + """) (Y """ + str(pmlSize[1]) + """) (Z """ + str(pmlSize[2]) + """) )
                                          			(SigmaFactor (X """ + str(0.375*gridSize[0]*40/pmlSize[0]) + """) (Y """ + str(0.375*gridSize[1]*40/pmlSize[1]) + """) (Z """ + str(0.375*gridSize[2]*40/pmlSize[2]) + """) ) )
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
                   (Material Prp (MaterialName gold)   // MaterialName value is user defined.
                                    (MaterialToken 4)   // MaterialToken value is user defined.
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
                   (Material Lossless (MaterialName PEC)
                                      (MaterialToken 5)
                                      (RelPermittivity 1e20)
                                      (RelPermeability 1)
   
                   )

                   """ + materials + """

                   (Source GaussTime (SourceName Source1)
                                     (Duration """ + str(sourceDuration) + """)
                                     (Center """ + str(sourceOffset) + """)
                                     (Width """ + str(sourceWidth) + """)
                                     (Frequency """ + str(sourceFreq) + """) // centered at lambda = 1/Frequency
                                     (Phase 0)
                                     (Amplitude """ + str(sourceAmplitude) + """)
                                     (Direction """ + str(sourceDir) + """ )
                   )

                   (Output FieldTime (Position 0 0 0)
                                     (StartTime 0)
                                     (EndTime """ + str(totalTime) + """)
                                     (TimeStep  """ + str(timeStep) + """)
                                     (FileName """ + timeDataOutFile +  """)
                                     (OutputField """ + outputFields + """)
                   )

                   (Output FieldSpace (OutputField """ + outputFields + """)
                                      (StartTime """ + str(fieldStartTime) + """)
                                      (EndTime """ + str(fieldEndTime) + """)
                                      (TimeStep """ + str(fieldTimeStep) + """)
                                      (FileName """ + fieldDataOutFile + """)
                    )
                    // Build a source.
                    
                    (Object Plane (Center   """ + list2Str(sourcePos) + """)
                                  (SourceName Source1)
                                  (Axis0    0 1 0)
                                  (Axis1    0 0 1)
                                  (Size     """ + str(totalSize[1] - pmlSize[1]*2) + """ """ + str(totalSize[2] - pmlSize[2]*2) + """)
                    )

                    """ + blocks + """

                    """
    
                    f.write(inputString)
    
                    f.close()
                    #call(['ls ./'])

                    #call 'which mpirun' to get path to mpirun for all users
                    #also lets make path to FDTD_PLUS a global variable
                    #cruddy way to do this let's try subprocess.call() next time around
                    os.system('/usr/local/bin/mpirun -n 4 /Users/twh/Documents/Fan/FDTD_PLUS/maxwell_bloch/fdtd_plus_mpi ./ input.txt 2 2 1')
                    os.system('say "congradulations, Tyler.  your program has finished!"')
    
    
    #                    (Object Point (SourceName Source1) (Center """ + list2Str(sourcePos) + """) 
     #               )
    
    
    
    
    
    
    
    