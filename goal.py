import bpy
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader
import random


xfield=4.5
radius = random.uniform(0.08, 0.12)
btwpost=2.6+(2*radius)
crossbarheight=1.2+radius

color = (random.uniform(0.75,0.99),random.uniform(0.75,0.99) ,random.uniform(0.75,0.99), 1)

def draw():
    #material = bpy.data.materials.get("Material")
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=False, align='WORLD', location=(xfield, btwpost/2, crossbarheight/2), scale=(1, 1,crossbarheight/2 ))
    obj = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=False, align='WORLD', location=(xfield, -btwpost/2, crossbarheight/2), scale=(1, 1,crossbarheight/2 ))
    obj2 = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=False, align='WORLD', location=(xfield, 0, crossbarheight), scale=(1, 1,crossbarheight+2*radius))
    bpy.context.object.rotation_euler[0] = 1.5708
    obj3 = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=False, align='WORLD', location=(-xfield, btwpost/2, crossbarheight/2), scale=(1, 1,crossbarheight/2 ))
    obj4 = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=False, align='WORLD', location=(-xfield, -btwpost/2, crossbarheight/2), scale=(1, 1,crossbarheight/2 ))
    obj5 = bpy.context.active_object
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=False, align='WORLD', location=(-xfield, 0, crossbarheight), scale=(1, 1,crossbarheight+2*radius))
    bpy.context.object.rotation_euler[0] = 1.5708
    obj6 = bpy.context.active_object
    
    
    mat = bpy.data.materials.new(name='NewMat')
    mat.use_nodes = True
    mat_nodes = mat.node_tree.nodes
    mat_links = mat.node_tree.links
    
    obj.data.materials.append(mat)
    obj2.data.materials.append(mat)
    obj3.data.materials.append(mat)
    
    obj4.data.materials.append(mat)
    obj5.data.materials.append(mat)
    obj6.data.materials.append(mat)
    
    mat_nodes["Principled BSDF"].inputs["Metallic"].default_value=1.0
    mat_nodes["Principled BSDF"].inputs[0].default_value = color

if __name__ == "__main__":
    draw()