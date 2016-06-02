import bpy
import os
from itertools import count

#global book
book = None

def selectObj(obj):
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.scene.objects.active = obj
	obj.select = True
	return

def selectObjByName(objName):
	obj = None
	for ob in bpy.context.scene.objects:
		if ob.type == 'MESH' and ob.name.startswith(objName):
			bpy.context.scene.objects.active = ob
			ob.select = True
			obj = ob
		else:
			ob.select = False
	return obj

def getCutCube(ccname):
	if bpy.data.objects.get(ccname) is None:
		bpy.ops.mesh.primitive_cube_add()
		ccobj = bpy.context.object
		ccobj.name = ccname
	else:
		ccobj = selectObjByName(ccname)

	return ccobj

def positionCutCube(ccname,l,w,h,x,y,z):
	ccobj = selectObjByName(ccname)
	bpy.ops.transform.resize(value=(l-2*x, w, h))
	ccobj.location[1] = y
	ccobj.location[2] = z
	return

def cutWithCube(l,w,h,x,y,z):
	ccname = "Cutter"
	#create and position
	getCutCube(ccname)
	positionCutCube(ccname,l,w,h,x,y,z)
	#cut
	selectObj(book)
	bpy.ops.object.modifier_add(type='BOOLEAN')
	book.modifiers["Boolean"].operation = 'DIFFERENCE'
	book.modifiers["Boolean"].object = bpy.data.objects[ccname]
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
	#delete
	selectObjByName(ccname)
	bpy.ops.object.delete()
	return

def cutHardcover(l,w,h):
	#introduce x,y,z factors to adjust cutting cubes relative to book l,w,h
	cutWithCube(l,w,h,0.001,0.003,2*h-0.002)
	cutWithCube(l,w,h,0.001,0.003,-2*h+0.002)
	cutWithCube(l,w,h,0.001,2*w-0.002,0)

	#reset active selection
	selectObj(book)	

	return

def createBook(binding,dims):
	global book

	#create book cube
	bpy.ops.mesh.primitive_cube_add()
	book = bpy.context.object

        #parse dimensions into l<w<h (assumed proportions for most books)
	eachdim = dims.split('x')
	lwh = []
	for n in eachdim:
		lwh.append(float(n))
	lwh.sort()

	#extract each dim and apply scaling factor
	sc = 0.000127 #primitive cube in hundreths of an inch = 2.54(cm/in)/100(cm/m)/100(hundreths in/in)/2(primitive cube in meters)

	l = lwh[0] * sc
	w = lwh[1] * sc
	h = lwh[2] * sc

	#overwrite any zero dimensions; use binding info 
	if "Paperback" in binding:
		if l == 0:
			l = .008
		if w == 0:
			w = .067
		if h == 0:
			h = .10
	else: #set to average hardcover dims
		if l == 0:
			l = .018
		if w == 0:
			w = .076
		if h == 0:
			h = .114

	#set dimensions of book cube
	bpy.ops.transform.resize(value=(l, w, h))

	#if not a paperback, then position and cut
	if "Paperback" not in binding:
		book.location[0] = 0
		book.location[1] = 0
		book.location[2] = 0
		cutHardcover(l,w,h)

	#smooth
	bpy.ops.object.shade_smooth()

	return 

def createMaterials(isbn):
	global book

	# make faces
	bpy.ops.mesh.uv_texture_add()
	bpy.ops.object.editmode_toggle()
	bpy.ops.uv.cube_project()
	bpy.ops.object.editmode_toggle()

	# Image texture
	imgPath = 'D:/vrbookdrop/img/'+isbn+'.jpg'
	img = bpy.data.images.load(imgPath)
	imtex = bpy.data.textures.new('ImageTex','IMAGE')
	imtex.image = img
	
	# Marble texture
	mbtex = bpy.data.textures.new('MarbleTex','MARBLE')
	mbtex.noise_depth = 1
	mbtex.noise_scale = 1.6
	mbtex.noise_basis = 'BLENDER_ORIGINAL'
	mbtex.turbulence = 5
	
	# Cloud texture
	cltex = bpy.data.textures.new('CloudsTex','CLOUDS')
	cltex.noise_basis = 'BLENDER_ORIGINAL'
	cltex.noise_scale = 1.05
	cltex.noise_type = 'SOFT_NOISE'
	
	# Create new material
	mat = bpy.data.materials.new('TexMat')
	mat.alpha = 0
		
	# Map image to color, this is the default
	im_mtex = mat.texture_slots.add()
	im_mtex.texture = imtex
	im_mtex.texture_coords = 'UV'
	
	# Create new material
	mat2 = bpy.data.materials.new('Blue')
	mat2.diffuse_color = (0.5, 0.5, 0.8)
	mat2.specular_color = (0.3, 0.3, 0.0)

	# Map marble to specularity
	mb_mtex = mat2.texture_slots.add()
	mb_mtex.texture = mbtex
	mb_mtex.texture_coords = 'UV'
	mb_mtex.use_map_specular = True
	
	# Map cloud to alpha, reflection and normal, but not diffuse
	#cl_mtex = mat2.texture_slots.add()
	#cl_mtex.texture = cltex
	#cl_mtex.texture_coords = 'UV'
	#cl_mtex.use_map_alpha = True
	#cl_mtex.use_map_reflect = True
	#cl_mtex.use_map_normal = True
	
	# Add the two materials to mesh
	me = book.data
	me.materials.append(mat)
	me.materials.append(mat2)
	
	# Assign mat2 to all faces to the left, with x coordinate > 0
	for f in me.polygons:
		left = True
		for v in f.vertices:
			vert = me.vertices[v]
			if vert.co.x < 0:
				left = False
				if left:
						f.material_index = 0
				else:
					f.material_index = 1
	return

def exportFbx(isbn,title):
	global book

	titleStart = title[:8].replace(" ","").replace(":","") #truncated and trimmed version
	filename = isbn+"_"+titleStart+".fbx"
	book.select
	bpy.ops.export_scene.fbx(filepath="./fbx/"+filename,use_selection=True,global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='FACE', use_mesh_edges=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)

	return



##DEBUG: Interactive Mode
bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(0.5, -0.5, -0.5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0.00192985, -0.00115219, 0.00415842), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(-0.5, 0.5, 0.5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0.00192985, -0.00115219, 0.00415842), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

## MAIN
bookList = open('sample-book-list.txt','r')
while True:
	isbn = bookList.readline().rstrip('\n')
	title = bookList.readline().rstrip('\n')
	binding = bookList.readline().rstrip('\n')
	dims = bookList.readline().rstrip('\n')
	if not dims: break

	createBook(binding,dims)
	createMaterials(isbn)
	exportFbx(isbn,title)

bookList.close()
