# Vida2Maespa
Tool for using Vida outputs to parameterize MAESPA

Vida2MAESPA is a tool for converting data from Vida simulations to parameterization for running MAESPA simulations.

	-n 		Output name	
	-w 		World size from Vida
	-a 		Area you want Maespa to simulate. V2M assumes centered at 0,0
	-p 		Number of points in X & Y space
	-d 		Show debuging text on the screen
	-b 		Show the progress bar
	-f 		File path to load a Vida csv file
	-ff 	Directory Vida csv files are found. not working yet.
Usage example:
	python Vida2Maespa.py -n myOutput -w 100 -a 30 -b -f <path to file>
	
Working:
     -Makes trees.dat and confile.dat based on Vida outputs

     -Makes phy and str files, but these are just copies of the templates

     -Output a points.dat file

     -Provides a key file for mapping MAESPA indexed output to VIDA tree UIDs

     -Argument parsing so you can easily define the file to process from the command line

To do:
     

     -Output a dxf based on the points.dat file
