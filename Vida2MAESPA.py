import csv

#read in the template files

theFile=open('file_templates/confile_template.txt','r')
theConfileTemp=theFile.read()
theFile.close

theFile=open('file_templates/phy_template.txt', 'r')
thePhyTemp=theFile.read()
theFile.close

theFile=open('file_templates/str_template.txt', 'r')
theStrTemp=theFile.read()
theFile.close

theFile=open('file_templates/trees_template.txt', 'r')
theTreesTemp=theFile.read()
theFile.close

print theTreesTemp


with open('smtest-500.csv') as theCSVFile:
	theFileData=csv.DictReader(theCSVFile)
	#calculate the x min, max, y min, max
	theWorldSize=500
	theHalfSize=theWorldSize/2
	xMin=-theHalfSize
	yMin=-theHalfSize
	xMax=theHalfSize
	yMax=theHalfSize
	numbTrees=0
	allXY=""
	allXRadius=""
	allYRadius=""
	allCanopyHeight=""
	allDBH=""
	allBoleHeight=""
	allCanopyArea=""
	theSpeciesList=[]
	for row in theFileData:
		indivTrunkHeight=0
		indivCanopyArea=0

		numbTrees=numbTrees+1
		indivXY="%s %s\n" % (row[' X Location'], row[' Y Location'])
		allXY=allXY+indivXY

		indivCanopyRadiusX="%s\n" % (row[' Radius Canopy'])
		allXRadius=allXRadius+indivCanopyRadiusX
		####right noe the following are the same as allXRadius
		#indivCanopyRadiusY="%s\n" % (row[' Radius Canopy'])
		#allYRadius=allYRadius+indivCanopyRadiusY
		#indivCanopyHeight="%s\n" % (row[' Radius Canopy'])
		#allCanopyHeight=allCanopyHeight+indivCanopyHeight

		indivDBH="%s\n" % (row[' Diameter Stem'])
		allDBH=allDBH+indivDBH

		indivBoleHeight="%d\n" % (float(row[' Height of Plant'])-float(row[' Radius Canopy']))
		allBoleHeight=allBoleHeight+indivBoleHeight

		indivCanopyArea="%d\n" % (3.14*(float(row[' Radius Canopy'])**2.0))
		allCanopyArea=allCanopyArea+indivCanopyArea

		theSpeciesList.append(row[' Species'])
	#for row in theFileData:
	#	print(row['X Location'], row['Y Location'])
	#print allXY

	##make the list of species for use in confile.dat and trees.dat
	theSpeciesSet=set(theSpeciesList)
	numbSpecies=1
	theSpeciesDict={}
	for x in theSpeciesSet:
		theSpeciesDict[x] = numbSpecies
		numbSpecies=numbSpecies+1
	allSpecies=""
	for x in theSpeciesList:
		allSpecies=allSpecies+"%i\n" % (theSpeciesDict[x])
	#print allSpecies




print theTreesTemp % (xMin, yMin, xMax, yMax, numbTrees, allSpecies, allXY, allXRadius, allXRadius, allXRadius, allDBH, allBoleHeight, allCanopyArea)