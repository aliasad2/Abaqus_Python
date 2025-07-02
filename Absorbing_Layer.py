from abaqus import *
from abaqusConstants import *
import regionToolset
import part
import sketch
import material
import section
import assembly
import step
import job
import load
import mesh

model = mdb.Model(name='Testing')

sketch = model.ConstrainedSketch(name='Sketch', sheetSize=200.0)
sketch.rectangle(point1=(0.0, 0.0), point2=(400.0, 400.0))

part = model.Part(name='Plate', dimensionality=THREE_D, type=DEFORMABLE_BODY)
part.BaseSolidExtrude(sketch=sketch, depth=1.0)

# define absotbing layers parameters
num_damping = 10
total_thickness_alid = 20.0
model_x1=0.0
model_y1=0.0
model_z1=0.0
model_x2=400.0
model_y2=400.0
model_z2=1.0

for i in range(num_damping):
     # sketch
     sketchPlane = part.faces.findAt((model_x2/2, total_thickness_alid-(i*total_thickness_alid/num_damping),model_z2),)
     sketchUpEdge=part.edges.findAt((0, model_y2/2,model_z2),)
     transform = part.MakeSketchTransform(sketchPlane=sketchPlane, sketchUpEdge=sketchUpEdge, sketchPlaneSide=SIDE1, origin=(model_x2, model_y2, model_z2))
     partition_sketch=model.ConstrainedSketch(name='PartitionSketch_{}'.format(i), sheetSize=200.0, transform=transform)
     partition_sketch.setPrimaryObject(option=SUPERIMPOSE)
     part.projectReferencesOntoSketch(sketch=partition_sketch, filter=COPLANAR_EDGES)   
     x1 = max(model_x1 + 0.01, total_thickness_alid - ((total_thickness_alid / num_damping) * i))
     x2 = min(model_x2 - 0.01, (model_x2- total_thickness_alid) + ((total_thickness_alid / num_damping) * i))
     y1 = max(model_y1 + 0.01, total_thickness_alid - ((total_thickness_alid / num_damping) * i))
     y2 = min(model_y2 - 0.01, (model_y2- total_thickness_alid) + ((total_thickness_alid / num_damping) * i))
     partition_sketch.rectangle(point1=(x1, y1), point2=(x2, y2))
     part.PartitionFaceBySketch(sketchUpEdge=sketchUpEdge, faces=sketchPlane, sketch=partition_sketch)
     partition_sketch.unsetPrimaryObject()
     # partition
     #pickedCells = part.cells.findAt((model_x2/2, total_thickness_alid-(i*total_thickness_alid/num_damping), 1),)
     edge_1 = part.edges.findAt((total_thickness_alid-i*total_thickness_alid/num_damping,model_y2/2,model_z2),)
     edge_2 = part.edges.findAt(((model_x2-total_thickness_alid)+i*total_thickness_alid/num_damping,model_y2/2,model_z2),)
     edge_3 = part.edges.findAt((model_x2/2,(model_y2-total_thickness_alid)+i*total_thickness_alid/num_damping,model_z2),)
     edge_4 = part.edges.findAt((model_x2/2,total_thickness_alid-i*total_thickness_alid/num_damping,model_z2),)
     pickedEdges =(edge_1, edge_2 , edge_3 , edge_4)
     sweepedge = part.edges.findAt((0, 0, model_z2/2),)
     all_cells = part.cells[:] 
     part.PartitionCellBySweepEdge(sweepPath=sweepedge, cells=all_cells, edges=pickedEdges)

# Define AL material
material_name= 'AL'
material_AL = model.Material(name=material_name)
material_AL.Density(table=((2700e-12,),))
material_AL.Elastic(table=((70000.0, 0.33),))
section_name= 'AL'
model.HomogeneousSolidSection(name=section_name, material=material_name)
# creat a set for study area
cell = part.cells.findAt(((model_x2/2, model_y2/2,model_z2),))
set_name = 'study area'
part.Set(cells=cell, name=set_name)
# assign material for study area
region = part.sets[set_name]
part.SectionAssignment(region=region, sectionName=section_name)           

# Define damping materials
for i in range(1,num_damping+1):
      material_name = 'damping_{}'.format(i)
      material = model.Material(name=material_name)
      material.Density(table=((2700e-12,),))
      material.Elastic(table=((70000.0, 0.33),))
      alpha_damping = 3e6 * ((i / float(num_damping) )** 3)
      material.Damping(alpha=alpha_damping, beta=0.0, composite=0.0, structural=0.0)
      section_name = 'Section_{}'.format(i)
      model.HomogeneousSolidSection(name=section_name, material='damping_{}'.format(i))
      # creat sets for absorbing layers
      cell = part.cells.findAt(((total_thickness_alid-(i*(total_thickness_alid/num_damping))+0.1, model_y2/2, model_z2),))
      set_name = 'absorbing layer_{}'.format(i)
      part.Set(cells=(cell,), name=set_name)
      # assign material to absorbing layers
      region = part.sets[set_name]
      part.SectionAssignment(region=region, sectionName=section_name)







    
