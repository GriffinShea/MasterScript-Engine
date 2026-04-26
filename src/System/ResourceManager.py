from config import *
from System.ShaderHelper import ShaderHelper

class ResourceManager:
	meshes = {}
	unloadedMeshes = set()
	shaders = {}
	unloadedShaders = set()
	textures = {}
	unloadedTextures = set()
	fonts = {}
	unloadedFonts = set()
	
	@classmethod
	def generateBasicMeshes(cls):
		
		print("Generating basic meshes...")
		
		#these meshes are all CCW wrapped and square like triangle meshes
		#i.e., the first vertex is the same on both triangles for each quad
		
		cls.meshes["frame"] = createFrame()
		cls.meshes["square"] = createSquare()
		cls.meshes["quadSquare"] = createQuadSquare()
		cls.meshes["plane"] = createPlane()				#a plane is a double sided square
		cls.meshes["sphere"] = createSphere(10, 10)
		cls.meshes["cylinder"] = createCylinder(20)
		cls.meshes["cube"] = createCube()
		cls.meshes["room"] = createRoom()				#room is a cube with inverted faces
		cls.meshes["dieCube"] = createDieCube()
		cls.meshes["nullElement"] = createNullElement()
		
		#===========================================================================================
		
		#(depreciated) debug shaders
		#depreciated method (use loadShader())
		#cls.shaders["colouredWireframe"] = ShaderHelper.loadShaderFromGLSLH("debug//colouredWireframe.glslh")
		#cls.shaders["normals"] = ShaderHelper.loadShaderFromGLSLH("debug//normals.glslh")
		#cls.shaders["orthographicDepthMap"] = ShaderHelper.loadShaderFromGLSLH("debug//orthographicDepthMap.glslh")
		#cls.shaders["perspectiveDepthMap"] = ShaderHelper.loadShaderFromGLSLH("debug//perspectiveDepthMap.glslh")
		#cls.shaders["gPos"] = ShaderHelper.loadShaderFromGLSLH("debug//gPos.glslh")
		#cls.shaders["gNorm"] = ShaderHelper.loadShaderFromGLSLH("debug//gNorm.glslh")
		#cls.shaders["gCol"] = ShaderHelper.loadShaderFromGLSLH("debug//gCol.glslh")
		#cls.shaders["frame"] = ShaderHelper.loadShaderFromGLSLH("debug//frame.glslh")
		
		#SHADER MASK REFERENCE:
		#	0 1 2 3 4
		#	  0 0   0
		#	B T L T I
		#	X Q   U
		#	      I
		#         S
		#
		#	0: (B)asic vertex calculation or ps(X)-like pixel jiggle effect
		#	1: (T)riangle or (Q)uad or no tesselation (0)
		#	2: apply (L)ighting or no lighting (0)
		#	3: (T)exture, (U)niform, (I)nterpolated, or (S)tatic colour
		#	4: enable (I)nvert colour or not (0)
		#
		
		#template shaders (these are also in sample.rsc)
		#cls.shaders["texture"] = ShaderHelper.createShaderFromMask("B0LT0")
		#cls.shaders["unLitTexture"] = ShaderHelper.createShaderFromMask("B00T0")
		#cls.shaders["invertedTexture"] = ShaderHelper.createShaderFromMask("B0LTI")
		#cls.shaders["solidUnlitColour"] = ShaderHelper.createShaderFromMask("B00U0")
		#cls.shaders["solidLitColour"] = ShaderHelper.createShaderFromMask("B0LU0")
		#cls.shaders["triTess"] = ShaderHelper.createShaderFromMask("BTLT0")
		#cls.shaders["quadTess"] = ShaderHelper.createShaderFromMask("BQLT0")
		
		return
	
	@classmethod
	def loadResources(cls, filename):
		print("Loading resources from " + filename + ".rsc...", sep="")
		with open("assets//resource_files//" + filename + ".rsc") as rscFile:
			resources = json.load(rscFile)
			
			print(".\tLoading textures...")
			for texName in resources["textures"]:
				cls.loadTexture(resources["textures"][texName], texName)
				
			print(".\tLoading meshes...")
			for meshName in resources["meshes"]:
				cls.loadMeshTris(resources["meshes"][meshName], meshName)
			
			print(".\tLoading shaders...")
			for shaderName in resources["shaders"]:
				cls.loadShader(resources["shaders"][shaderName], shaderName)
			
			print(".\tLoading fonts...")
			for fontName in resources["fonts"]:
				cls.loadFont(resources["fonts"][fontName], fontName)
			
		print("Done.\n")
		return
	
	@classmethod
	def unloadResources(cls, filename):
		#REVISIT: a problem - say there are two resource files and we run...
		#	Engine.loadResources("x")
		#	Engine.loadResources("y")
		#	Engine.unloadResources("x")
		#if an asset with the same name is in both x and y, it will be missing after x has unloaded
		print("Unloading resources from " + filename + ".rsc...", sep="")
		with open("assets//resource_files//" + filename + ".rsc") as rscFile:
			resources = json.load(rscFile)
			
			textureNames = [cls.textures[texName] for texName in resources["textures"]]
			n = len(textureNames)
			print(".\tUnloading", n, "textures...")
			gl.glDeleteTextures(n, glmh.makeArray(textureNames, ctypes.c_uint))
			for name in resources["textures"]:
				del cls.textures[name]
			
			meshes = [cls.meshes[meshName] for meshName in resources["meshes"]]
			print(".\tUnloading", len(meshes), "meshes...")
			vbos = [mesh[0] for mesh in meshes]
			gl.glDeleteVertexArrays(len(vbos), glmh.makeArray(vbos, ctypes.c_uint))
			ebos = [mesh[3] for mesh in meshes]
			gl.glDeleteBuffers(len(ebos), glmh.makeArray(ebos, ctypes.c_uint))
			for name in resources["meshes"]:
				del cls.meshes[name]
			
			shaders = [cls.shaders[shaderName][0] for shaderName in resources["shaders"]]
			print(".\tUnloading", len(shaders), "shaders...")
			for shader in shaders:
				gl.glDeleteProgram(shader)
			for name in resources["shaders"]:
				del cls.shaders[name]
			
			fontTextureNames = [cls.textures[fontName] for fontName in resources["fonts"]]
			n = len(fontTextureNames)
			print(".\tUnloading", n, "font textures...")
			gl.glDeleteTextures(n, glmh.makeArray(fontTextureNames, ctypes.c_uint))
			for name in resources["fonts"]:
				del cls.textures[name]
				del cls.fonts[name]
		
		print("Done.\n")
		return
	
	@classmethod
	def getFont(cls, name):
		if name in cls.fonts:
			return cls.fonts[name]
		if not name in cls.unloadedFonts:
			cls.unloadedFonts.add(name)
			print("WARNING: unloaded font:", name)
		return cls.fonts["basicFont"]
	
	@classmethod
	def getTexture(cls, name):
		if name in cls.textures:
			return cls.textures[name]
		if not name in cls.unloadedTextures:
			cls.unloadedTextures.add(name)
			print("WARNING: unloaded texture:", name)
		return cls.textures["die"]
	
	@classmethod
	def getMesh(cls, name):
		if name in cls.meshes:
			return cls.meshes[name]
		if not name in cls.unloadedMeshes:
			cls.unloadedMeshes.add(name)
			print("WARNING: unloaded mesh:", name)
		return cls.meshes["dolphin"]
	
	@classmethod
	def getShader(cls, name):
		if name in cls.shaders:
			return cls.shaders[name]
		if not name in cls.unloadedShaders:
			cls.unloadedShaders.add(name)
			print("WARNING: unloaded shader:", name)
		return cls.shaders["jelly"]
	
	@classmethod
	def loadTexture(cls, fileName, texName, transparentColour=None):
		print(".\t.\tLoading texture from file (" + fileName + ") as '" + texName + "'... ", end="")
		try:
			#load image as pygame surface
			surface = pygame.image.load("assets//textures//" + fileName).convert()
			surfaceString = pygame.image.tostring(surface, "RGBA", 1)
			
			#zero out alpha value of pixels with transparentColour
			if transparentColour:
				bytesList = []
				channelCounter = 0
				channelValues = [0, 0, 0, 0]
				for i in range(len(surfaceString)):
					if channelCounter == 3:
						if (
							channelValues[0] == transparentColour[0] and
							channelValues[1] == transparentColour[1] and
							channelValues[2] == transparentColour[2]
						):
							channelValues[channelCounter] = 0x00
						else:
							channelValues[channelCounter] = 0xff
						channelCounter = 0
						bytesList += channelValues
					else:
						channelValues[channelCounter] = surfaceString[i]
						channelCounter += 1
				surfaceString = bytes(bytesList)
			
			#get and bind a texture location
			location = gl.glGenTextures(1)
			gl.glBindTexture(gl.GL_TEXTURE_2D, location)
			
			#load surface data into texture
			gl.glTexImage2D(
				gl.GL_TEXTURE_2D,
				0,
				gl.GL_RGBA,
				surface.get_width(),
				surface.get_height(),
				0,
				gl.GL_RGBA,
				gl.GL_UNSIGNED_BYTE,
				surfaceString
			)
			
			#setup texture drawing rules and mipmap (if applicable)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
				
			filterLevel = [
				gl.GL_NEAREST_MIPMAP_NEAREST,
				gl.GL_LINEAR_MIPMAP_NEAREST,
				gl.GL_NEAREST_MIPMAP_LINEAR,
				gl.GL_LINEAR_MIPMAP_LINEAR
			][MIN_FILTER_LEVEL]
			gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, filterLevel)
			
			gl.glTexParameteri(
				gl.GL_TEXTURE_2D,
				gl.GL_TEXTURE_MAG_FILTER,
				gl.GL_LINEAR if MAG_FILER else gl.GL_NEAREST
			)
			
			gl.glGenerateTextureMipmap(location)
			cls.textures[texName] = location
			
		except pygame.error as message:
			print("Pygame error:", message)
			cls.textures[texName] = 2
		print("Done.")
		
		return
	
	@classmethod
	def loadMeshTris(cls, name, newName=None):
		newName = newName if newName else name[:-4]
		print(".\t.\tLoading mesh from file (" + name + ") as '" + newName + "'... ", end="")
		with open("assets//meshes//" + name) as file:
			positions = []
			texCoords = []
			normals = []
			
			verticiesDict = {}
			verticies = []
			triangles = []
			
			while True:
				line = file.readline().strip()
				if not line:
					break
				
				line = line.split(" ")
				if line[0] == "v":
					positions.append(glm.vec3(float(line[1]), float(line[2]), float(line[3])))
				elif line[0] == "vt":
					texCoords.append(glm.vec2(float(line[1]), float(line[2])))
				elif line[0] == "vn":
					normals.append(glm.vec3(float(line[1]), float(line[2]), float(line[3])))
				elif line[0] == "f":
					line[1:] = [line[3], line[2], line[1]]
					for vertexString in line[1:]:
						if not vertexString in verticiesDict:
							verticiesDict[vertexString] = len(verticies) / 8
							vertex = vertexString.split("/")
							verticies.append(positions[int(vertex[0])-1].x)
							verticies.append(positions[int(vertex[0])-1].y)
							verticies.append(positions[int(vertex[0])-1].z)
							verticies.append(normals[int(vertex[2])-1].x)
							verticies.append(normals[int(vertex[2])-1].y)
							verticies.append(normals[int(vertex[2])-1].z)
							if texCoords:
								verticies.append(texCoords[int(vertex[1])-1].x)
								verticies.append(texCoords[int(vertex[1])-1].y)
							else:
								verticies.append(0)
								verticies.append(0)
						triangles.append(int(verticiesDict[vertexString]))
			
			buffers = bindBuffers(verticies, triangles)
		
		cls.meshes[newName] = (
			buffers[0],
			8,
			((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)),
			buffers[1],
			len(triangles),
			3
		)
		
		print("Done.")
		return
	
	@classmethod
	def loadFont(cls, fontFileName, fontName):
		print(".\t.\tLoading font from file (" + fontFileName + ") as '" + fontName + "'... \n.\t", end="")
		with open("assets//fonts//" + fontFileName) as fontFile:
			font = json.load(fontFile)
			cls.loadTexture("bitmaps//" + font["bitmap"] + ".bmp", font["bitmap"])
			cls.fonts[fontName] = (font["bitmap"], glm.ivec2(font["bitmapDims"]), glm.ivec2(font["glyphDims"]))
		print(".\t.\tDone.")
		return
	
	@classmethod
	def loadShader(cls, filename, shaderName):
		print(".\t.\tLoading shader from file (" + filename + ") as '" + shaderName + "'... ", end="")
		if filename.find(".glslh") == -1:
			#filename is likely a mask and must be generated
			cls.shaders[shaderName] = ShaderHelper.createShaderFromMask(filename)
		else:
			#filename is a .glslh file
			cls.shaders[shaderName] = ShaderHelper.loadShaderFromGLSLH(filename)
		print("Done.")
		return

def bindBuffers(verticies, triangles):
	varray = glmh.makeArray(verticies, ctypes.c_float)
	tarray = glmh.makeArray(triangles, ctypes.c_uint)

	vbo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
	gl.glBufferData(gl.GL_ARRAY_BUFFER, varray, gl.GL_STATIC_DRAW)
	
	ebo = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
	gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, tarray, gl.GL_STATIC_DRAW)
	
	return (vbo, ebo)
	
def createNullElement():
	verticies = [0]
	triangles = [0, 0, 0]
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 1, [(1, gl.GL_FLOAT)], buffers[1], 1, 3)

def createFrame():
	verticies = (
		-1, -1, 0, 0,
		1, -1, 1, 0,
		-1, 1, 0, 1,
		1, 1, 1, 1
	)
	
	triangles = (
		1, 2, 0,
		1, 3, 2
	)
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 4, ((2, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 2, 3)

def createSquare():
	verticies = (
		-0.5, -0.5, 0, 0, 0, -1, 0, 0,
		0.5, -0.5, 0, 0, 0, -1, 1, 0,
		-0.5, 0.5, 0, 0, 0, -1, 0, 1,
		0.5, 0.5, 0, 0, 0, -1, 1, 1
	)
	
	triangles = (
		1, 2, 0,
		1, 3, 2
	)
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 2, 3)

def createQuadSquare():
	verticies = (
		-0.5, -0.5, 0, 0, 0, -1, 0, 0,
		0.5, -0.5, 0, 0, 0, -1, 1, 0,
		0.5, 0.5, 0, 0, 0, -1, 1, 1,
		-0.5, 0.5, 0, 0, 0, -1, 0, 1
	)
	
	quads = (
		0, 1, 2, 3
	)
	
	buffers = bindBuffers(verticies, quads)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 1, 4)

def createPlane():
	verticies = (
		-0.5, -0.5, 0, 0, 0, -1, 0, 0,
		0.5, -0.5, 0, 0, 0, -1, 1, 0,
		-0.5, 0.5, 0, 0, 0, -1, 0, 1,
		0.5, 0.5, 0, 0, 0, 1, 1, 1,
		-0.5, -0.5, 0, 0, 0, 1, 0, 0,
		0.5, -0.5, 0, 0, 0, 1, 1, 0,
		-0.5, 0.5, 0, 0, 0, 1, 0, 1,
		0.5, 0.5, 0, 0, 0, 1, 1, 1
	)
	
	triangles = (
		1, 2, 0,
		1, 3, 2,
		6, 5, 4,
		6, 7, 5
	)
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 4, 3)

def createSphere(h, v):	#h = horizontal slices, v = vertical slices
	verticies = []
	for i in range(v):
		verticies = verticies + [0, 0.5, 0, 0, 1, 0, i/v+1/(2*v), 1]
	for i in range(h):
		phi = (i+1)*glm.pi()/(h+1)
		sliceRadius = glm.sin(phi)/2
		sliceY = glm.cos(phi)/2
		for j in range(v+1):
			theta = j*glm.pi()/(v/2)
			position = (
				glm.angleAxis(glm.pi()/2, glmh.yUnit())
				* glm.vec3(sliceRadius*glm.cos(theta), sliceY, sliceRadius*glm.sin(theta))
			)
			normal = glm.normalize(position)
			verticies = verticies + [position.x, position.y, position.z]
			verticies = verticies + [normal.x, normal.y, normal.z]
			verticies = verticies + [abs(theta/(glm.pi()) - 1), sliceY+0.5]
	for i in range(v):
		verticies = verticies + [0, -0.5, 0, 0, -1, 0, i/v+1/(2*v), 0]
	
	triangles = []
	for i in range(v):
		triangles = triangles + [i, v+i, v+i+1]
	for i in range(h-1):
		for j in range(v):
			triangles = triangles + [(v+1)*i+j+v+1, (v+1)*i+j+v, (v+1)*(i+1)+j+v]
			triangles = triangles + [(v+1)*i+j+v+1, (v+1)*(i+1)+j+v, (v+1)*(i+1)+j+v+1]
	for i in range(v):
		triangles = triangles + [h*(v+1)+i, h*(v+1)+i-1, (h+1)*(v+1)+i-1]
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 2*h*v, 3)

def createCylinder(v):	#v = vertical slices
	verticies = []
	for i in range(v):
		verticies = verticies + [0, 0.5, 0, 0, 1, 0, i/v+1/(2*v), 1]
	for i in range(v+1):
		verticies = verticies + [glm.cos(i*glm.pi()/v*2)/2, 0.5, glm.sin(i*glm.pi()/v*2)/2, 0, 1, 0, i/v, 0]
	for i in range(v+1):
		position = glm.vec3(glm.cos(i*glm.pi()/v*2)/2, 0.5, glm.sin(i*glm.pi()/v*2)/2)
		normal = glm.normalize(glm.vec3(position.x, 0, position.z))
		verticies = verticies + [position.x, position.y, position.z, normal.x, normal.y, normal.z, i/v, 1]
	for i in range(v+1):
		position = glm.vec3(glm.cos(i*glm.pi()/v*2)/2, -0.5, glm.sin(i*glm.pi()/v*2)/2)
		normal = glm.normalize(glm.vec3(position.x, 0, position.z))
		verticies = verticies + [position.x, position.y, position.z, normal.x, normal.y, normal.z, i/v, 0]
	for i in range(v+1):
		verticies = verticies + [glm.cos(i*glm.pi()/v*2)/2, -0.5, glm.sin(i*glm.pi()/v*2)/2, 0, -1, 0, i/v, 0]
	for i in range(v):
		verticies = verticies + [0, -0.5, 0, 0, -1, 0, i/v+1/(2*v), 1]
	
	triangles = []
	for i in range(v):
		triangles = triangles + [i, v+i, v+i+1]
	for i in range(v):
		triangles = triangles + [3*(v+1)+i-1, 2*(v+1)+i, 2*(v+1)+i-1]
		triangles = triangles + [3*(v+1)+i-1, 3*(v+1)+i, 2*(v+1)+i]
	for i in range(v):
		triangles = triangles + [5*(v+1)+i-1, 4*(v+1)+i, 4*(v+1)+i-1]
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 4*v, 3)

def createCube():
	positions = (
		glm.vec3(-0.5, -0.5, -0.5),
		glm.vec3(-0.5, -0.5, 0.5),
		glm.vec3(-0.5, 0.5, -0.5),
		glm.vec3(-0.5, 0.5, 0.5),
		glm.vec3(0.5, -0.5, -0.5),
		glm.vec3(0.5, -0.5, 0.5),
		glm.vec3(0.5, 0.5, -0.5),
		glm.vec3(0.5, 0.5, 0.5)
	)
	
	normals = (
		glmh.yUnit(),
		glm.vec3(0, 0, -1),
		glmh.zUnit(),
		glmh.xUnit(),
		glm.vec3(-1, 0, 0),
		glm.vec3(0, -1, 0),
	)
	
	texCoords = (
		glm.vec2(0, 1),
		glm.vec2(0, 0),
		glm.vec2(1, 1),
		glm.vec2(1, 0)
	)
	
	faces = (
		2, 6, 3, 7,
		2, 0, 6, 4,
		7, 5, 3, 1,
		6, 4, 7, 5,
		3, 1, 2, 0,
		4, 0, 5, 1
	)
	
	verticies = []
	for i in range(len(faces)):
		verticies = verticies + [positions[faces[i]].x, positions[faces[i]].y, positions[faces[i]].z]
		verticies = verticies + [normals[int(i/4)].x, normals[int(i/4)].y, normals[int(i/4)].z]
		verticies = verticies + [texCoords[i%4].x, texCoords[i%4].y]
	
	triangles = []
	for i in range(6):
		triangles = triangles + [
			4*i+1, 4*i+2, 4*i,
			4*i+1, 4*i+3, 4*i+2
		]
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 12, 3)

def createRoom():
	positions = (
		glm.vec3(-0.5, -0.5, -0.5),
		glm.vec3(-0.5, -0.5, 0.5),
		glm.vec3(-0.5, 0.5, -0.5),
		glm.vec3(-0.5, 0.5, 0.5),
		glm.vec3(0.5, -0.5, -0.5),
		glm.vec3(0.5, -0.5, 0.5),
		glm.vec3(0.5, 0.5, -0.5),
		glm.vec3(0.5, 0.5, 0.5)
	)
	
	normals = (
		glmh.yUnit(),
		glm.vec3(0, 0, -1),
		glmh.zUnit(),
		glmh.xUnit(),
		glm.vec3(-1, 0, 0),
		glm.vec3(0, -1, 0),
	)
	
	texCoords = (
		glm.vec2(0, 1),
		glm.vec2(0, 0),
		glm.vec2(1, 1),
		glm.vec2(1, 0)
	)
	
	faces = (
		2, 6, 3, 7,
		2, 0, 6, 4,
		7, 5, 3, 1,
		6, 4, 7, 5,
		3, 1, 2, 0,
		4, 0, 5, 1
	)
	
	verticies = []
	for i in range(len(faces)):
		verticies = verticies + [positions[faces[i]].x, positions[faces[i]].y, positions[faces[i]].z]
		verticies = verticies + [normals[int(i/4)].x, normals[int(i/4)].y, normals[int(i/4)].z]
		verticies = verticies + [texCoords[i%4].x, texCoords[i%4].y]
	
	triangles = []
	for i in range(6):
		triangles = triangles + [
			4*i+2, 4*i+1, 4*i,
			4*i+2, 4*i+3, 4*i+1
		]
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 12, 3)

def createDieCube():
	positions = (
		glm.vec3(-0.5, -0.5, -0.5),
		glm.vec3(-0.5, -0.5, 0.5),
		glm.vec3(-0.5, 0.5, -0.5),
		glm.vec3(-0.5, 0.5, 0.5),
		glm.vec3(0.5, -0.5, -0.5),
		glm.vec3(0.5, -0.5, 0.5),
		glm.vec3(0.5, 0.5, -0.5),
		glm.vec3(0.5, 0.5, 0.5)
	)
	
	normals = (
		glmh.yUnit(),
		glm.vec3(0, 0, -1),
		glmh.zUnit(),
		glmh.xUnit(),
		glm.vec3(-1, 0, 0),
		glm.vec3(0, -1, 0),
	)
	
	texCoords = (
		glm.vec2(0, 0),
		glm.vec2(0, 1/2),
		glm.vec2(0, 1),
		glm.vec2(1/3, 0),
		glm.vec2(1/3, 1/2),
		glm.vec2(1/3, 1),
		glm.vec2(2/3, 0),
		glm.vec2(2/3, 1/2),
		glm.vec2(2/3, 1),
		glm.vec2(1, 0),
		glm.vec2(1, 1/2),
		glm.vec2(1, 1)
	)
	
	posCoordIndicies = (
		(2, 2), (6, 1), (3, 5), (7, 4),
		(2, 1), (0, 0), (6, 4), (4, 3),
		(7, 5), (5, 4), (3, 8), (1, 7),
		(6, 4), (4, 3), (7, 7), (5, 6),
		(3, 8), (1, 7), (2, 11), (0, 10),
		(4, 7), (0, 6), (5, 10), (1, 9)
	)
	
	verticies = []
	for i in range(len(posCoordIndicies)):
		verticies = verticies + [
			positions[posCoordIndicies[i][0]].x,
			positions[posCoordIndicies[i][0]].y,
			positions[posCoordIndicies[i][0]].z
		]
		verticies = verticies + [normals[int(i/4)].x, normals[int(i/4)].y, normals[int(i/4)].z]
		verticies = verticies + [texCoords[posCoordIndicies[i][1]].x, texCoords[posCoordIndicies[i][1]].y]
	
	triangles = []
	for i in range(6):
		triangles = triangles + [
			4*i+1, 4*i+2, 4*i,
			4*i+1, 4*i+3, 4*i+2
		]
	
	buffers = bindBuffers(verticies, triangles)
	
	return (buffers[0], 8, ((3, gl.GL_FLOAT), (3, gl.GL_FLOAT), (2, gl.GL_FLOAT)), buffers[1], 12, 3)
