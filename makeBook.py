import bpy

f = open('sample-book-list.txt','r')
while True:
	title = f.readline().rstrip('\n')
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

	#check variable blender commands
#	print "bpy.ops.transform.resize(value=(%s,%s,%s))" %(d,w,h)
	

	bpy.ops.mesh.primitive_cube_add()
	bpy.ops.transform.resize(value=(d,w,h))
	bpy.ops.object.shade_smooth()


	bpy.ops.export_scene.fbx(filepath="./"+title+".fbx",use_selection=True,global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='FACE', use_mesh_edges=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)


f.close()
