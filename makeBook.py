import bpy
import os

f = open('sample-book-list.txt','r')
while True:
	isbn = f.readline().rstrip('\n')
	title = f.readline().rstrip('\n')
	binding = f.readline().rstrip('\n')
	dim = f.readline().rstrip('\n')
	if not dim: break

	#just checking...
#	print "title: %s, dim: %s" %(title, dim)
	
	#parse dimensions into d<w<h (assumed proportions for most books)
	dims = dim.split('x')
	dwh = []
	for n in dims:
		dwh.append(float(n))
	dwh.sort()

	#extract and apply scaling factor
	sc = 0.00015

	d = dwh[0] * sc
	w = dwh[1] * sc
	h = dwh[2] * sc

	#overwrite any zero dimensions; use binding info
	if binding == "Paperback":
		if d == 0:
			d = .015
		if w == 0:
			w = .05
		if h == 0:
			h = .09
	else:
		if d == 0:
			d = .020
		if w == 0:
			w = .1
		if h == 0:
			h = .15

	#check variable blender commands
#	print "bpy.ops.transform.resize(value=(%s,%s,%s))" %(d,w,h)
	

	#clear anything from before
	#bpy.ops.object.mode_set(mode='OBJECT')
	#bpy.ops.object.select_by_type(type='MESH')
	#bpy.ops.object.delete(use_global=False)

	#for item in bpy.data.meshes:
	#    bpy.data.meshes.remove(item)

	#build mesh
	bpy.ops.mesh.primitive_cube_add()
	bpy.ops.transform.resize(value=(d,w,h))
	bpy.ops.object.shade_smooth()
	
	#apply texture
	#bpy.ops.object.editmode_toggle()
	#bpy.ops.uv.cube_project()
	#m1 = bpy.data.materials.new("cover")
	#m1.texture_slots.add()
	#t1 = bpy.data.textures.new("texture1",'IMAGE')
	#imagefile = isbn+".jpg"
	#imagedir = os.getcwd()+"/img/"
	#bpy.ops.image.open(filepath=imagefile, directory=imagedir, files=[{"name":imagefile}], relative_path=True, show_multiview=False)
	#m1.texture_slots[0].texture = t1
	#m1.texture_slots[0].texture_coords = 'OBJECT'
	#m1.texture_slots[0].object = bpy.data.objects["Cube.001"]
	#bpy.context.scene.render.resolution_percentage = 100


	#construct filename and export
	titleStart = title[:8].replace(" ","").replace(":","") #truncated and trimmed version
	filename = isbn+"_"+titleStart+".fbx" 
	bpy.ops.export_scene.fbx(filepath="./fbx/"+filename,use_selection=True,global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='FACE', use_mesh_edges=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)


f.close()
