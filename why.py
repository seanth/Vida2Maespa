import argparse

def main():
	print "yo"

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(description='Arguments for Vida2Maespa')
	parser.add_argument('-n', type=str, metavar='string', dest='simulationName', required=False, help='Name of the simulation')
	print parser.parse_args()