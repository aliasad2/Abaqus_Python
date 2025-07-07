from abaqus import *
from abaqusConstants import *

model = mdb.models['Model-1']
a = model.rootAssembly
instance_name = 'part-inst'  # <-- Update if your instance name is different

for i in range(1, 33):
    set_name = 'S{}'.format(i)
    bc_name = 'Disp_T_{}'.format(i)
    try:
        region = a.instances[instance_name].sets[set_name]
        model.DisplacementBC(
            name=bc_name,
            createStepName='Step-1',
            region=region,
            u1=UNSET, u2=UNSET, u3=-1e-6,  # Displacement in Z-direction
            ur1=UNSET, ur2=UNSET, ur3=UNSET,
            amplitude='Amp-200-3-1MHz',
            distributionType=UNIFORM,
            fieldName='',
            localCsys=None
        )
        print(" Displacement applied to:", set_name)
    except Exception as e:
        print(" Failed on {}: {}".format(set_name, e))
