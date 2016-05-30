import bpy
import os
from itertools import count



def createBook(binding,dims):

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
	sc = 0.00015

	l = lwh[0] * sc
	w = lwh[1] * sc
	h = lwh[2] * sc

	#overwrite any zero dimensions; use binding info 
	if "Paperback" in binding:
		if l == 0:
			l = .015
		if w == 0:
			w = .05
		if h == 0:
			h = .09
	else: #set to average hardcover dims
		if l == 0:
			l = .020
		if w == 0:
			w = .1
		if h == 0:
			h = .15

	#set dimensions of book cube
	bpy.ops.transform.resize(value=(l, w, h))

	#smooth
	bpy.ops.object.shade_smooth()

	return book

def createMaterials(book,isbn):
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

def exportFbx(book,isbn,title):
	titleStart = title[:8].replace(" ","").replace(":","") #truncated and trimmed version
	filename = isbn+"_"+titleStart+".fbx"
	book.select
	bpy.ops.export_scene.fbx(filepath="./fbx/"+filename,use_selection=True,global_scale=1.0, axis_forward='-Z', axis_up='Y', object_types={'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='FACE', use_mesh_edges=False, use_anim=True, use_anim_action_all=True, use_default_take=True, use_anim_optimize=True, anim_optimize_precision=6.0, path_mode='AUTO', batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)

	return


## Main

bookList = open('sample-book-list.txt','r')
while True:
	isbn = bookList.readline().rstrip('\n')
	title = bookList.readline().rstrip('\n')
	binding = bookList.readline().rstrip('\n')
	dims = bookList.readline().rstrip('\n')
	if not dims: break

	book = createBook(binding,dims)
	createMaterials(book,isbn)
	exportFbx(book,isbn,title)

bookList.close()
