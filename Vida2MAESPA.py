import sys
import os
import csv
import argparse
import ConfigParser
sys.path.append("Vida2MAESPA_Data")
import geometry_utils


##########################################
#Import the options#
try:
    theConfig=ConfigParser.RawConfigParser()
    theConfig.optionxform = str 
    theConfig.read('Vida2Maespa.ini')
    theConfigSection='Vida2Maespa Options'
except ConfigParser.MissingSectionHeaderError:
    print("Warning: Invalid config file, no [%s] section.") % (theConfigSection)
    raise

theDefaults={}
for i in theConfig.items(theConfigSection):
    theItem=i[0]
    try:
        theValue=theConfig.getint(theConfigSection, theItem)
    except:
        try:
            theValue=theConfig.getboolean(theConfigSection, theItem)
        except:
            try:
                theValue=theConfig.getfloat(theConfigSection, theItem)
            except:
                try:
                    theValue=theConfig.get(theConfigSection, theItem)
                    if theValue=="None": theValue=None
                except:
                    print "what the...?"
    theDefaults[theItem]=theValue
#print theDefaults 

def main():
	#read in the template files
	print "  Reading in confile template..."
	theFile=open('Vida2MAESPA_Data/file_templates/confile_template.txt','rb')
	theConfileTemp=theFile.read()
	theFile.close

	print "  Reading in points template..."
	theFile=open('Vida2MAESPA_Data/file_templates/points_template.txt','rb')
	thePointsTemp=theFile.read()
	theFile.close

	print "  Reading in phy template..."
	theFile=open('Vida2MAESPA_Data/file_templates/phy_template.txt', 'rb')
	thePhyTemp=theFile.read()
	theFile.close

	print "  Reading in str template..."
	theFile=open('Vida2MAESPA_Data/file_templates/str_template.txt', 'rb')
	theStrTemp=theFile.read()
	theFile.close

	print "  Reading in trees template..."
	theFile=open('Vida2MAESPA_Data/file_templates/trees_template.txt', 'rb')
	theTreesTemp=theFile.read()
	theFile.close

	#print theConfileTemp

	#print filePath
	#with open('test_files/test-500.csv') as theCSVFile:
	with filePath as theCSVFile:
		print "  Reading in Vida simulation data..."
		theFileData=csv.DictReader(theCSVFile)
		#x max, min, y max, min of sample area
		xSampleMin = -(theAreaSize/2)
		xSampleMax =  (theAreaSize/2)
		ySampleMin = -(theAreaSize/2)
		ySampleMax =  (theAreaSize/2)
		#calculate the x min, max, y min, max
		# theWorldSize=500.0
		theHalfSize=theWorldSize/2.0
		xMin=-theHalfSize
		yMin=-theHalfSize
		xMax=theHalfSize
		yMax=theHalfSize
		####
		numbTrees=0
		allXY=""
		allXRadius=""
		allYRadius=""
		allCanopyHeight=""
		allDBH=""
		allBoleHeight=""
		allCanopyArea=""
		allVidaUID=["Vida UID, Maespa Tree Index"]
		theSpeciesList=[]
		theSpeciesNameString=""
		thePhyFiles=""
		theStrFiles=""
		numbAllSpecies=0
		theITargets=""
		numbITargets=0
		#this is used in confile.dat if area sample is not listed
		theBoarderEdge=50
		theTallestTree=0.0

		print "Marking target directories..."
		#this could be smarter and get the values from a run argument
		theOutputDir='Maespa-'+simulationName+'/input_files/'
		theOutputDir1='Maespa-'+simulationName+'/'
		if not os.path.exists(theOutputDir): os.makedirs(theOutputDir)
		if not os.path.exists('Maespa-'+simulationName+'/output_files'): os.makedirs('Maespa-'+simulationName+'/output_files')

		print "Beginning data parsing (this might take some time)...\n"
		#i = 1
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
			theTreeX
			if (theTreeX<=xSampleMax and theTreeX>=xSampleMin):
				if (theTreeY<=ySampleMax and theTreeY>=ySampleMin):
					theITargets=theITargets+str(numbTrees)+" "
					print numbTrees
					numbITargets=numbITargets+1
					#for the MAESPA <-->Vida tree id key file
					theUIDandIndex = "%s, %i" % (row[' Plant Name'], numbTrees) 
					allVidaUID.append(theUIDandIndex)
					#i=i+1

			indivCanopyRadiusX="%s\n" % (row[' Radius Canopy'])
			allXRadius=allXRadius+indivCanopyRadiusX
			####right noe the following are the same as allXRadius
			#indivCanopyRadiusY="%s\n" % (row[' Radius Canopy'])
			#allYRadius=allYRadius+indivCanopyRadiusY
			#indivCanopyHeight="%s\n" % (row[' Radius Canopy'])
			#allCanopyHeight=allCanopyHeight+indivCanopyHeight

			indivDBH="%s\n" % (row[' Diameter Stem'])
			allDBH=allDBH+indivDBH

			treeHeight=float(row[' Height of Plant'])
			if (theTallestTree<treeHeight):
				theTallestTree=round(treeHeight)
			indivBoleHeight="%f\n" % (treeHeight-float(row[' Radius Canopy']))
			indivBoleHeight=treeHeight-float(row[' Radius Canopy'])
			if indivBoleHeight<=0.0: 
				print "****WARNING: Bole height for tree %i was less than zero. Set to zero" % numbTrees
				indivBoleHeight = 0.0
			indivBoleHeight="%f\n" % indivBoleHeight

			allBoleHeight=allBoleHeight+indivBoleHeight

			#indivCanopyArea="%f\n" % (3.14*(float(row[' Radius Canopy'])**2.0))#this is just the projected area
			indivCanopyArea="%f\n" % (3.14*(float(row[' Radius Canopy'])**2.0)*2.0)#this should be the area of a hemisphere
			allCanopyArea=allCanopyArea+indivCanopyArea

			theSpeciesList.append(row[' Species'])
		if theITargets.strip()=="":
			print "****EXTREME WARNING: NO TARGET TREES FOUND. MAESPA WILL NOT WORK CORRECTLY****"

		#for row in theFileData:
		#	print(row['X Location'], row['Y Location'])
		#print allXY

		##make the list of species for use in confile.dat and trees.dat
		theSpeciesSet=set(theSpeciesList)
		numbAllSpecies=len(theSpeciesSet) #for confile
		numbSpecies=1
		theSpeciesDict={}
		for x in theSpeciesSet:
			theSpeciesNameString=theSpeciesNameString+" '"+x+"'"+" " #for confile
			thePhyName=x+"_phy.dat"
			thePhyName=thePhyName.replace(" ", "_")
			theStrName=x+"_str.dat"
			theStrName=theStrName.replace(" ", "_")
			###needs to be expanded upon######
			print "  Writing "+thePhyName+"..."
			theWriteFile=open(theOutputDir+thePhyName, 'wb')
			theWriteFile.write(thePhyTemp)
			theWriteFile.close()
			print "  Writing "+theStrName+"..."
			theWriteFile=open(theOutputDir+theStrName, 'wb')
			theWriteFile.write(theStrTemp)
			theWriteFile.close()
			##################################
			thePhyFiles=thePhyFiles+"'"+thePhyName+"' " #for confile
			theStrFiles=theStrFiles+"'"+theStrName+"' " #for confile
			theSpeciesDict[x] = numbSpecies
			numbSpecies=numbSpecies+1
		allSpecies=""
		for x in theSpeciesList:
			allSpecies=allSpecies+"%i\n" % (theSpeciesDict[x])
		#print allSpecies

	print "  Writing trees.dat..."
	theWriteFile=open(theOutputDir+'trees.dat', 'wb')
	theWriteFile.write(theTreesTemp % (xMin, yMin, xMax, yMax, numbTrees, allSpecies, allXY, allXRadius, allXRadius, allXRadius, allDBH, allBoleHeight, allCanopyArea))
	theWriteFile.close()

	print "  Writing confile.dat..."
	theWriteFile=open(theOutputDir1+'confile.dat', 'wb')
	theWriteFile.write( theConfileTemp % (simulationName, numbAllSpecies, theSpeciesNameString, thePhyFiles, theStrFiles, numbITargets, theITargets, theBoarderEdge))
	theWriteFile.close()

	print "  Writing key index file..."
	theWriteFile = open(theOutputDir+'UIDkey.csv', 'wb')
	for anItem in allVidaUID:
		theWriteFile.write("%s\n" % anItem)
		#print>>theWriteFile, anItem
	theWriteFile.close()

	###Make the sensor points
	#print numbPoints
	numbPoints=10
	pointDistance=geometry_utils.placePointsInGrid(numbPoints, theWorldSize)
	prevX=-theWorldSize/2.0
	prevY= theWorldSize/2.0
	prevZ= 0.0
	theXYPoints=[]
	theXYZPoints=[]
	for i in range(numbPoints):
		x=prevX+pointDistance
		y=prevY-pointDistance
		if x+pointDistance>=(theWorldSize/2.0):
			prevX=-theWorldSize/2.0
			prevY= prevY-pointDistance
		else:
			prevX=x
		theXYPoints.append ("%f %f" % (x, y))
	#z markers up a to the tallest tree height+1m, every 10 evenly spaced units
	theTallestTree=60 #this is just to keep the sensor grid consistant between multiple simulations
	theDistance=int(theTallestTree+1)/10
	#theDistance=int(10)/10
	for j in range(0, int(theTallestTree+theDistance), theDistance):
		for coords in theXYPoints:
			theXYZPoints.append(coords+" %f" % j)
			#print coords+" %f" % j
	numbPoints=len(theXYZPoints)
	print "  Writing points.dat..."
	theWriteFile=open(theOutputDir+'points.dat', 'wb')
	theWriteFile.write( thePointsTemp % (numbPoints, '\n'.join(theXYZPoints)))
	theWriteFile.close()

	print "***File generation complete***"
	print "***REMEMBER TO COPY MET AND WATPARS FILES INTO THE GENERATED INPUT DIRECTORY***"

if __name__ == '__main__':
	###Argument parsing
	parser = argparse.ArgumentParser(description='Arguments for Vida2Maespa')
	parser.add_argument('-n', type=str, metavar='string', dest='simulationName', required=False, help='Name of the simulation')
	parser.add_argument('-w', type=int, nargs='?', metavar='int', dest='theWorldSize', help='Size of the world')
	parser.add_argument('-a', type=int, nargs='?', metavar='int', dest='theAreaSize', help='Size of the sample area')
	parser.add_argument('-p', type=int, nargs='?', metavar='int', dest='numbPoints', help='Number of points in X & Y space')
	parser.add_argument('-d', dest='debug', action='store_true', required=False, help='Show debug messages')
	parser.add_argument('-b', dest='showProgressBar', action='store_true', required=False, help='Show progress bars')    
	parser.add_argument('-f', metavar='file', type=file, dest='filePath', required=False, help='Load a Vida csv file')   
	parser.add_argument('-ff', metavar='directory', dest='theDirectory', required=False, help='Directory Vida csv files are found. not working yet.') 

	##########    
	#parser.set_defaults(**theDefaults)
	parser.set_defaults(**theDefaults)
	#print vars(parser.parse_args())
	theOptsVals=vars(parser.parse_args())#have it presented as a dict
	theOpts=theOptsVals.keys()#this returns a list of the arguments entered
	globalVarsVals=globals()#dictionary of all local variables and their values

	for theVar in theOpts:
		globalVarsVals[theVar]=theOptsVals[theVar]

	print "     Simulation name: %s" % (simulationName)
	print "     World size (meters): %s" % (theWorldSize)
	print "     Sample size (meters): %s" % (theAreaSize)
	print "     File name: %s" % (filePath)
	print "     Number of sample points in X & Y: %s" % (numbPoints)
	print "################"
	#print debug
	#print showProgressBar
	#rint eventFile

	###parse seed placement options a bit more
	#if type(startPopulationSize)==list:
	#    seedPlacement=startPopulationSize[1]
	#    startPopulationSize=startPopulationSize[0]
	#if type(startPopulationSize)==file:
	#    sList=startPopulationSize.readlines()
	#    ##send the file off to make sure it's in the correct format
	#    sList=checkSeedPlacementList(sList)
	#    startPopulationSize=len(sList)



	    #for x in theOpts:
	#print "%s: \t%s   %s" % (x, theDefaults[x], globalVarsVals[x])

	theDefaults=None#just clear it to free up memory
	main()
else:
	print "here"
	main()


