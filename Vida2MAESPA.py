import sys
import csv
sys.path.append("Vida2MAESPA_Data")
import geometry_utils

#read in the template files
print "  Reading in confile template..."
theFile=open('Vida2MAESPA_Data/file_templates/confile_template.txt','r')
theConfileTemp=theFile.read()
theFile.close

print "  Reading in phy template..."
theFile=open('Vida2MAESPA_Data/file_templates/phy_template.txt', 'r')
thePhyTemp=theFile.read()
theFile.close

print "  Reading in str template..."
theFile=open('Vida2MAESPA_Data/file_templates/str_template.txt', 'r')
theStrTemp=theFile.read()
theFile.close

print "  Reading in trees template..."
theFile=open('Vida2MAESPA_Data/file_templates/trees_template.txt', 'r')
theTreesTemp=theFile.read()
theFile.close

#print theConfileTemp


with open('test-300.csv') as theCSVFile:
	print "  Reading in Vida simulation data..."
	theFileData=csv.DictReader(theCSVFile)
	#x max, min, y max, min of sample area
	xSampleMin=-200.0
	xSampleMax=200.0
	ySampleMin=-200.0
	ySampleMax=200.0
	#calculate the x min, max, y min, max
	theWorldSize=500.0
	theHalfSize=theWorldSize/2.0
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
	theSpeciesNameString=""
	thePhyFiles=""
	theStrFiles=""
	numbAllSpecies=0
	theITargets=""
	numbITargets=0
	theBoarderEdge=50
	print "Beginning data parsing (this might take some time)..."
	for row in theFileData:
		indivTrunkHeight=0
		indivCanopyArea=0

		#for trees.dat
		numbTrees=numbTrees+1
		theTreeX=float(row[' X Location'])
		theTreeY=float(row[' Y Location'])
		indivXY="%s %s\n" % (theTreeX, theTreeY)
		allXY=allXY+indivXY

		#for confile
		if (theTreeX<=xSampleMax and theTreeX>=xSampleMin):
			if (theTreeY<=ySampleMax and theTreeY>=ySampleMin):
				theITargets=theITargets+"'"+str(numbTrees)+"' "
				numbITargets=numbITargets+1

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

		#indivCanopyArea="%d\n" % (3.14*(float(row[' Radius Canopy'])**2.0))#this is just the projected area
		indivCanopyArea="%d\n" % (3.14*(float(row[' Radius Canopy'])**2.0)*2.0)#this should be the area of a hemisphere
		allCanopyArea=allCanopyArea+indivCanopyArea

		theSpeciesList.append(row[' Species'])
	#for row in theFileData:
	#	print(row['X Location'], row['Y Location'])
	#print allXY

	##make the list of species for use in confile.dat and trees.dat
	theSpeciesSet=set(theSpeciesList)
	numbAllSpecies=len(theSpeciesSet) #for confile
	numbSpecies=1
	theSpeciesDict={}
	for x in theSpeciesSet:
		theSpeciesNameString=theSpeciesNameString+"'"+x+"' " #for confile
		thePhyName=x+"_phy.dat"
		theStrName=x+"_str.dat"
		###needs to be expanded upon######
		print "  Writing "+thePhyName+"..."
		theWriteFile=open(thePhyName, 'w')
		theWriteFile.write(theStrTemp)
		theWriteFile.close()
		print "  Writing "+thePhyName+"..."
		theWriteFile=open(theStrName, 'w')
		theWriteFile.write(theStrTemp)
		theWriteFile.close()
		##################################
		thePhyFiles=thePhyFiles+"'"+thePhyName+"'' " #for confile
		theStrFiles=theStrFiles+"'"+theStrName+"' " #for confile
		theSpeciesDict[x] = numbSpecies
		numbSpecies=numbSpecies+1
	allSpecies=""
	for x in theSpeciesList:
		allSpecies=allSpecies+"%i\n" % (theSpeciesDict[x])
	#print allSpecies


print "  Writing trees.dat..."
theWriteFile=open('trees.dat', 'w')
theWriteFile.write(theTreesTemp % (xMin, yMin, xMax, yMax, numbTrees, allSpecies, allXY, allXRadius, allXRadius, allXRadius, allDBH, allBoleHeight, allCanopyArea))
theWriteFile.close()

print "  Writing confile.dat..."
theWriteFile=open('confile.dat', 'w')
theWriteFile.write( theConfileTemp % (numbAllSpecies, theSpeciesNameString, thePhyFiles, theStrFiles, numbITargets, theITargets, theBoarderEdge))
theWriteFile.close()

print "***File generation complete***"



