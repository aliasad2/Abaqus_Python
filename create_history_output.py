from abaqus import *
from abaqusConstants import *

# Access your model and assembly
model = mdb.models['Testing']
a = model.rootAssembly
step_name = 'Step-1'  # Replace with your actual step name if different

# Loop over all 32 vertex sets and create history output requests
for i in range(1, 33):
    set_name = 'vertex_{}'.format(i)
    output_name = 'output_{}'.format(set_name)

    try:
        region = a.sets[set_name]

        model.HistoryOutputRequest(
            name=output_name,
            createStepName=step_name,
            variables=('U', 'UR'),     # Displacements + Rotations
            region=region,
            frequency=1,               # Every time increment
            sectionPoints=DEFAULT,
            rebar=EXCLUDE
        )
        print("✅ History output created for:", set_name)

    except KeyError:
        print("❌ Set not found in assembly:", set_name)
