from abaqus import *
from abaqusConstants import *

model = mdb.models['Model-1']
part = model.parts['Part-1']

num_damping = 75
alpha_base = 3e6  # Adjust this if needed

for i in range(1, num_damping + 1):
    material_name = 'damping_{}'.format(i)
    section_name = 'Section_{}'.format(i)
    set_name = 'absorbing layer_{}'.format(i)

    # Redefine the material
    material = model.Material(name=material_name)
    material.Density(table=((2.7E-09,),))
    material.Elastic(table=((71500.0, 0.33),))

    alpha_value = alpha_base * ((i / float(num_damping)) ** 3)
    material.Damping(alpha=alpha_value, beta=0.0)

    # Redefine the section with the new material
    model.HomogeneousSolidSection(name=section_name, material=material_name)

    # Safely reassign the section to the existing set
    try:
        region = part.sets[set_name]
        part.SectionAssignment(region=region, sectionName=section_name)
        print(" Updated values for:", set_name)
    except:
        print(" Could not update:", set_name)
