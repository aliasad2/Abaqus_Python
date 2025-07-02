from abaqus import *
from abaqusConstants import *

for i in range(1, 33):
    set_name = 'vertex_{}'.format(i)
    bc_name = 'Load_T_{}'.format(i)
    try:
        region = a.sets[set_name]
        model.DisplacementBC(
            name=bc_name,
            createStepName='Step-1',
            region=region,
            u1=UNSET, u2=UNSET, u3=-1e-6,
            ur1=UNSET, ur2=UNSET, ur3=UNSET,
            amplitude='Amp-3cy_200kHz_50sr',
            distributionType=UNIFORM,
            fieldName='',
            localCsys=None
        )
        print("Displacement BC applied to:", set_name)
    except:
        print("Failed to apply BC to:", set_name)

