from abaqus import *
from abaqusConstants import *

model = mdb.models['Model-1']
assembly = model.rootAssembly
instance = assembly.instances['part-inst']  # Update to your instance name

for i in range(1, 33):
    set_name = 'S{}'.format(i)
    region_name = set_name + '_Region'

    region = assembly.instances['part-inst'].sets[set_name]

    model.HistoryOutputRequest(
        name=region_name,
        createStepName='Step-1',
        variables=('U',),
        region=region,
        frequency=4, 
        sectionPoints=DEFAULT,
        rebar=EXCLUDE
    )
    print("History output created for:", set_name)