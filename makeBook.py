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

	bpy.ops.export_scene.fbx(filepath="./"+title+".fbx",use_selection=True)


f.close()
