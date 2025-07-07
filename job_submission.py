from abaqus import *
from abaqusConstants import *
import job

# Use one model for all jobs
model_name = 'Model-1'
model = mdb.models[model_name]

# List of job numbers you want to create and submit
#job_indices = [1, 17]  # Customize as needed
job_indices = range (1,33)

for i in job_indices:
    job_name = 'Defected_Job_{}'.format(i)
    active_bc = 'Disp_T_{}'.format(i)

    # Suppress all BCs first
    for j in range(1, 33):
        bc_name = 'Disp_T_{}'.format(j)
        if bc_name in model.boundaryConditions:
            model.boundaryConditions[bc_name].suppress()

    # Activate only the BC for this job
    if active_bc in model.boundaryConditions:
        model.boundaryConditions[active_bc].resume()  # use this
    else:
        print("Warning: BC not found -", active_bc)
        continue


    # Create the job
    mdb.Job(
        name=job_name,
        model=model_name,
        description='Job for BC {}'.format(active_bc),
        type=ANALYSIS,
        explicitPrecision=DOUBLE_PLUS_PACK,
        multiprocessingMode=DEFAULT,
        numCpus=7,
        numDomains=7,
        memory=90,
        memoryUnits=PERCENTAGE
    )
    print("Created job:", job_name)


    # Submit the job and wait
    #mdb.jobs[job_name].submit()
    #mdb.jobs[job_name].waitForCompletion()
    #print("Submitted and completed job:", job_name)