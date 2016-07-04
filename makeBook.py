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

def getCyl(cylname):
	if bpy.data.objects.get(cylname) is None:
		bpy.ops.mesh.primitive_cylinder_add()
		cylobj = bpy.context.object
		cylobj.name = cylname
	else:
		cylobj = selectObjByName(cylname)
	return cylobj

def positionCutCube(ccname,l,w,h,x,y,z):
	ccobj = selectObjByName(ccname)
	bpy.ops.transform.resize(value=(l-2*x, w, h))
	ccobj.location[1] = y
	ccobj.location[2] = z
	return

def positionCyl(cylname,l,w,h,y):
	cylobj = selectObjByName(cylname)
	bpy.ops.transform.resize(value=(l,0.004,h)) #w = half of standard pb l
	cylobj.location[1] = y
	return

def cutWithCube(myObj,l,w,h,x,y,z):
	ccname = "Cutter"
	#create and position
	getCutCube(ccname)
	positionCutCube(ccname,l,w,h,x,y,z)
	#cut
	selectObj(myObj)
	bpy.ops.object.modifier_add(type='BOOLEAN')
	myObj.modifiers["Boolean"].operation = 'DIFFERENCE'
	myObj.modifiers["Boolean"].object = bpy.data.objects[ccname]
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Boolean")
	#delete
	selectObjByName(ccname)
	bpy.ops.object.delete()
	return

def addCyl(myObj,l,w,h,y):
	cylname = "Buldge"
	#create and position
	myCyl = getCyl(cylname)
	positionCyl(cylname,l,w,h,y)
	#add buldge
	selectObj(myObj)
	bpy.ops.object.modifier_add(type='BOOLEAN')
	myObj.modifiers["Boolean"].operation = 'UNION'
	myObj.modifiers["Boolean"].object = bpy.data.objects[cylname]
	bpy.ops.object.modifier_apply(apply_as='DATA',modifier="Boolean")
	#delete
	selectObjByName(cylname)
	bpy.ops.object.delete()
	return

def cutHardcover(l,w,h):
	#add spine buldge
	addCyl(book,l,w,h,-w)
	
	#introduce x,y,z factors to adjust cutting cubes relative to book l,w,h
	cutWithCube(book,l,w,h,0.001,0.003,2*h-0.002) #top
	cutWithCube(book,l,w,h,0.001,0.003,-2*h+0.002) #bottom
	cutWithCube(book,l,w,h,0.001,2*w-0.002,0) #side

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
			w = .052
		if h == 0:
			h = .084
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

def createPageMat():
        # Pages image texture
	pagPath = 'D:/vrbookdrop/img/pages.jpg'
	pag = bpy.data.images.load(pagPath)
	pagtex = bpy.data.textures.new('ImageTex','IMAGE')
	pagtex.image = pag
	pagtex.extension = 'EXTEND'
	pagtex.use_flip_axis = True

	mat3 = bpy.data.materials.new('PagMat')
	mat3.alpha = 0
	mat3.specular_intensity = 0
	pg_mtex = mat3.texture_slots.add()
	pg_mtex.texture = pagtex
	pg_mtex.texture_coords = 'UV'

	return mat3

def createHcvMat():
	mat4 = bpy.data.materials.new('HcvMat')
	mat4.alpha = 0
	mat4.specular_intensity = 0
	mat4.diffuse_color = (0.8,0.8,0.8)
	
	return mat4

def createMaterials(isbn,titleStart,mat3,mat4):
	global book

	suffix = isbn+titleStart

	# make faces
	bpy.ops.mesh.uv_texture_add()
	bpy.ops.object.editmode_toggle()
	bpy.ops.uv.cube_project()
	bpy.ops.object.editmode_toggle()

	# Cover image texture
	imgPath = 'D:/vrbookdrop/img/'+isbn+'.jpg'
	if os.path.isfile(imgPath):
		img = bpy.data.images.load(imgPath)
	else:
		img = bpy.data.images.load('D:/vrbookdrop/img/noimage.png')
	imtex = bpy.data.textures.new('ImageTex','IMAGE')
	imtex.image = img
	imtex.extension = 'CLIP'
	
	# Marble texture
	#mbtex = bpy.data.textures.new('MarbleTex','MARBLE')
	#mbtex.noise_depth = 1
	#mbtex.noise_scale = 1.6
	#mbtex.noise_basis = 'BLENDER_ORIGINAL'
	#mbtex.turbulence = 5
	
	# Cloud texture
	#cltex = bpy.data.textures.new('CloudsTex','CLOUDS')
	#cltex.noise_basis = 'BLENDER_ORIGINAL'
	#cltex.noise_scale = 1.05
	#cltex.noise_type = 'SOFT_NOISE'
	
	# Create materials
	mat0 = bpy.data.materials.new('FrCovMat'+suffix)
	mat0.alpha = 0
	mat0.specular_intensity = 0.25
	im_mtex0 = mat0.texture_slots.add()
	im_mtex0.texture = imtex
	im_mtex0.texture_coords = 'UV'

	mat1 = bpy.data.materials.new('SpCovMat'+suffix)
	mat1.alpha = 0
	mat1.specular_intensity = 0.25
	im_mtex1 = mat1.texture_slots.add()
	im_mtex1.texture = imtex
	im_mtex1.texture_coords = 'UV'
	
	mat2 = bpy.data.materials.new('BkCovMat'+suffix)
	mat2.alpha = 0
	mat2.specular_intensity = 0.25
	im_mtex2 = mat2.texture_slots.add()
	im_mtex2.texture = imtex
	im_mtex2.texture_coords = 'UV'

	# Map cloud to alpha, reflection and normal, but not diffuse
	#cl_mtex = mat2.texture_slots.add()
	#cl_mtex.texture = cltex
	#cl_mtex.texture_coords = 'UV'
	#cl_mtex.use_map_alpha = True
	#cl_mtex.use_map_reflect = True
	#cl_mtex.use_map_normal = True
	
	# Add the two materials to mesh
	me = book.data
	me.materials.append(mat0)
	me.materials.append(mat1)
	me.materials.append(mat2)
	me.materials.append(mat3)
	me.materials.append(mat4)
	
	
	# Assign mats to faces
	for f in me.polygons:
		vsumx = 0
		vsumy = 0
		vsumz = 0
		for v in f.vertices:
			vert = me.vertices[v]
			vsumx += vert.co.x
			vsumy += vert.co.y
			vsumz += vert.co.z
		if vsumx == 4: #front
			f.material_index = 0
		elif vsumy == -4: #spine
			f.material_index = 1
		elif vsumx == -4: #back
			f.material_index = 2
		elif vsumz/4 == vert.co.z: #pages, top and bottom
			f.material_index = 3
		elif vsumy/4 == vert.co.y and vsumy > 0: #pages, side
			f.material_index = 3
		elif vsumz > 4 or vsumz < -4: #hard cover edge, top and bottom
			f.material_index = 4
		elif vsumy/4 == vert.co.y and vsumy < 0: #hard cover edge, inside spine
			f.material_index = 4
		else: #inner faces of hardcover, e.g., dust jacket flaps
			f.material_index = 0 

	return

def exportFbx(isbn,titleStart):
	global book

	filename = isbn+"_"+titleStart+".fbx"
	book.select
	bpy.ops.export_scene.fbx(filepath="./fbx/"+filename,use_selection=True,global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='FACE', use_mesh_edges=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)

	return



##DEBUG: Interactive Mode
#bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(0.5, -0.5, -0.5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
#bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0.00192985, -0.00115219, 0.00415842), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

#bpy.ops.object.lamp_add(type='POINT', view_align=False, location=(-0.5, 0.5, 0.5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
#bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0.00192985, -0.00115219, 0.00415842), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

## MAIN
bookList = open('sample-book-list.txt','r')

mat3 = createPageMat()
mat4 = createHcvMat()

while True:
	isbn = bookList.readline().rstrip('\n')
	title = bookList.readline().rstrip('\n')
	binding = bookList.readline().rstrip('\n')
	dims = bookList.readline().rstrip('\n')
	if not dims: break

	#truncated and clean version of human readable title
	titleStart = title[:8].replace(" ","").replace(":","").replace("'","").replace("(","") 
	#call functions
	createBook(binding,dims)
	createMaterials(isbn,titleStart,mat3,mat4)
	exportFbx(isbn,titleStart)

bookList.close()
