'''
Created on Oct 7, 2022

@author: lisias
'''

import PlanetNomads.SaveDirectory as PNS

def main():
	directory = PNS.Directory()
	for d in sorted(directory, key=lambda k:k.modified_at, reverse=True):
		print(d)

if __name__ == '__main__':
	exit(main())
