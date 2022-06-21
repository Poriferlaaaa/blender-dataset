import bpy
import numpy as np
import cv2
import glob
import random

imgfolderPath = "/home/fiborobotlab/18-06-2022FootballF/imageFBF/*.png"
greenfolderPath = "/home/fiborobotlab/18-06-2022FootballF/greenFBF/*.png"
objfolderPath = "/home/fiborobotlab/18-06-2022FootballF/objFBF/"
ptcname = "ptcHair"
num = 0
x_pix2m = 0.005
y_pix2m = 0.005


def genplan(mylocation, myname):
    bpy.ops.mesh.primitive_plane_add(
        size=1,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=mylocation,
        rotation=(0, 0, 0))
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname
    return 0

def newMaterial(id):
    mat = bpy.data.materials.get(id)
    if mat is None:
        mat = bpy.data.materials.new(name=id)
    mat.use_nodes = True
    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()
    return mat

def getimagPath(path):
    #call image from folder
    imgname = path.replace("/","//")    
    #convert string to crrect format for cv2.imread & path for shader plane
    return cv2.imread(imgname)

imglist = glob.glob(imgfolderPath)
greenpath = glob.glob(greenfolderPath)

for path in range(len(imglist)):
    img = getimagPath(imglist[path])
#    img = cv2.imread("//home//fiborobotlab//15-06-2022FootballF//footballF.png")
#    path ="/home/fiborobotlab/15-06-2022FootballF/footballF.png"
    imgShape = img.shape
    genplan((0,0,0),"Plane")
    
    
    #------------------------------------------------------------------------
#    verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(0,5,5),(5,5,5),(5,0,5)]
#    faces = [(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
#    
#    mymesh = bpy.data.meshes.new("Cube")
#    myobject = bpy.data.object.link(myobject)
#    
#    mymesh.from_pydata(verts,[],faces)
#    mymesh.update(calc_edges=True)
    
    #-------------------------------------------------------------------------
       
    plane = bpy.data.objects['Plane']
    plane.scale[0] = imgShape[1]*x_pix2m 
    plane.scale[1] = imgShape[0]*x_pix2m 
    
#    bpy.context.object.scale[0] = 11

#   plane.scale = np.array([imgShape[1]*x_pix2m,imgShape[0]*y_pix2m,0.0])
    
#    obj = bpy.context.active_object
    
    ptc = bpy.ops.object.particle_system_add()
    bpy.data.particles["ParticleSettings"].type = "HAIR" 
    
    
    
    bpy.context.object.particle_systems["ParticleSystem"].seed = random.randint(1,100)
    bpy.data.particles["ParticleSettings"].count = 7000
    bpy.data.particles["ParticleSettings"].hair_length = random.uniform(0.05,0.1)
    bpy.data.particles["ParticleSettings"].child_type = 'SIMPLE'
    bpy.context.object.particle_systems["ParticleSystem"].child_seed = random.randint(1,100)
    bpy.data.particles["ParticleSettings"].roughness_2 = random.uniform(0.01,0.025)
#    bpy.data.collections['My Collection'].hide_viewport = True
    bpy.data.particles["ParticleSettings"].name = ptcname+str(num)
    
#    plane.hide_viewport = True
    
#    plane.scenes["Scene"].(null) = True








#    bpy.data.particles["ParticleSettings"].hair_length = random.uniform(0.100,0.5)
#    bpy.data.particles["ParticleSettings"].roughness_2 = random.uniform(0.100,0.200)
#    bpy.data.particles["ParticleSettings"].name = ptcname+str(num)
    





#    if len(obj.particle_systems) == 0:
#        obj.modifiers.new("part", type='PARTICLE_SYSTEM')
#        part = obj.particle_systems[0]

#        settings = part.settings
#        settings.emit_from = 'VERT'
#        settings.physics_type = 'NO'
#        settings.particle_size = 0.1
#        settings.render_type = 'OBJECT'
##        settings.duplicate_particle_system  = bpy.data.objects['footballfield']
#        settings.show_unborn = True
#        settings.use_dead = True

#        bpy.ops.object.duplicates_make_real()
##        
# 
#=========================================================       
    ob = bpy.context.view_layer.objects.active
    
    

    mat = bpy.data.materials.new(name="FootBall_F")
    mat.use_nodes = True
#    bsdf = mat.node_tree.nodes["Principled BSDF"]
    matOut = mat.node_tree.nodes.get('Material Output')
#    matOut = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(imglist[path])
    greenImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    greenImage.image = bpy.data.images.load(greenpath[path])
    mixShader = mat.node_tree.nodes.new('ShaderNodeMixShader')
    
    
#    mat.node_tree.links.new(bsdf.inputs['Base Color'], greenImage.outputs['Color'])
    
    mat.node_tree.links.new(mixShader.inputs[1],greenImage.outputs['Color'])
    mat.node_tree.links.new(mixShader.inputs[2],texImage.outputs['Color'])
    mat.node_tree.links.new(matOut.inputs['Surface'],mixShader.outputs['Shader'])
    


    # Assign it to object
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
    break
#=========================================================
    
    