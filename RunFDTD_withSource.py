import os
from subprocess import call

#define some convenience variables and functions
run = True
needsRef = True   #False only if you have the signal time data for these parameters

x = '1 0 0'
y = '0 1 0'
z = '0 0 1'

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
gridSize = [0.01, 0.01, 0.01]

#total size of simulation domain
totalSize = [3, 3, 2]

#total time (scaled)
totalTime = 200

#duration of source (in scaled time)
sourceDuration = 200

#position of source (point source) (x,y,z)
sourcePos = [0.3,0,0]

#amplitude of source (units?)
sourceAmplitude = 1

#source (polarization?) (x,y,z)
sourceDir = y

#time offset of source
sourceOffset = 8

#with of source pulse (scaled time)
sourceWidth = 2

#frequency of pulse modulation (scaled time)
sourceFreq = 0.8


ws = [.1]           #thickness of dielectrics
ts = [.1]           #thickness of metals
hs = [.1]           #width of rods
Ls = [.4]           #length of rods
ds = [0.1]            #center gap spacing
epsList = [1,3,2]     #dielectric constants (from top to bottom [source above])

metalType = 'gold'   #'PEC' or 'gold'

outputFields = 'ex ey hz'

measurePos = [0,0,0]  #
timeDataOutFile = 'signal5.dat'
timeStep = 0.002

fieldDataOutFile = 'fieldTime'
fieldStartTime = 60
fieldEndTime = 61
fieldTimeStep = 0.002

refOutput = 'signal_ref.dat'

os.chdir('/Users/twh/Documents/Fan/FDTD_PLUS/')

g = open('input_ref.txt', 'w')

sourceInputString = """
                   (Option CellParam      (CellType linear)
                                          (FieldType real)
                   )
                   (Option BoundaryParam  (Type pml pml pml) 
                                          (PmlParam (Type upml) (Size (X 0.5) (Y 0.5) (Z 0.5) )
                                          			(SigmaFactor (X 0.075) (Y 0.075) (Z 0.075) ) )
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
                                     (FileName """ + refOutput +  """)
                                     (OutputField """ + outputFields + """)
                   )
                    // Build a source.
                    (Object Point (SourceName Source1) (Center """ + list2Str(sourcePos) + """) 
                    )

                    """

g.write(sourceInputString)
g.close()

if (run) and (needsRef):
    os.chdir('/Users/twh/Documents/Fan/FDTD_PLUS/')
    os.system('/usr/local/bin/mpirun -n 2 /Users/twh/Documents/Fan/FDTD_PLUS/maxwell_bloch/fdtd_plus_mpi ./ input_ref.txt 2 1 1')

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
                    zCenter = 0
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
                    
                        
                    #open input file to write to
                    f = open('input.txt', 'w')


                  # TEST: 3D simulation of a linear antenna
                    inputString = """
                   (Option CellParam      (CellType linear)
                                          (FieldType real)
                   )
                   (Option BoundaryParam  (Type pml pml pml) 
                                          (PmlParam (Type upml) (Size (X 0.5) (Y 0.5) (Z 0.5) )
                                          			(SigmaFactor (X 0.075) (Y 0.075) (Z 0.075) ) )
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
                                      (StartTime """ + str(fieldEndTime) + """)
                                      (EndTime """ + str(fieldStartTime) + """)
                                      (TimeStep """ + str(fieldTimeStep) + """)
                                      (FileName """ + fieldDataOutFile + """)
                    )
                    // Build a source.
                    (Object Point (SourceName Source1) (Center """ + list2Str(sourcePos) + """) 
                    )

                    """ + blocks + """

                    """
    
                    f.write(inputString)
    
                    f.close()
                    #call(['ls ./'])

                    #call 'which mpirun' to get path to mpirun for all users
                    #also lets make path to FDTD_PLUS a global variable
                    #cruddy way to do this let's try subprocess.call() next time around
                    if (run):
                        #change directory to your FDTD Directory
                        os.chdir('/Users/twh/Documents/Fan/FDTD_PLUS/')
                        os.system('/usr/local/bin/mpirun -n 2 /Users/twh/Documents/Fan/FDTD_PLUS/maxwell_bloch/fdtd_plus_mpi ./ input.txt 2 1 1')
                        os.chdir('/Users/twh/Documents/Fan/PostProcessing')
       #                 os.system('/Applications/MATLAB_R2014a.app/bin/matlab -nodesktop -r "addpath(genpath("~/Documents/Fan/PostProcessing"));"')
      #                  os.system('/Applications/MATLAB_R2014a.app/bin/matlab -nodesktop -r "Transmission_Analysis"')
    
    
    
    
    
    
    
    
    
    