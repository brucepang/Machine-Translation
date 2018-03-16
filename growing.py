from collections import defaultdict
import sys
import time
import pickle

class GrowingAlign(object):
	"""docstring for GrowingAlign"""
	def __init__(self, f2e, e2f):
		self.f2e = f2e
		self.e2f = e2f
		self.f2e_align = dict()
		self.e2f_align = dict()
		self.intersection = dict()
		self.union = dict()
		self.grow = dict()

	def initialize_align(self,dev_en,dev_es):
		eng_l  = dev_en.readline()
		for_l = dev_es.readline()

		count = 1
		while eng_l and for_l:
		    eline = eng_l.strip()
		    fline = for_l.strip()
		    if eline and fline: # both nonempty lines
		    	self.f2e_align[count] = [[0 for i in \
		    		range(len(fline.split())+1)] for j in range(len(eline.split())+1)]
		    	self.e2f_align[count] = [[0 for i in \
		    		range(len(fline.split())+1)] for j in range(len(eline.split())+1)]
		        count+=1
		    eng_l = dev_en.readline()
		    for_l = dev_es.readline()


	def parse_align(self):
		f2e_l = self.f2e.readline()
		while f2e_l:
			fields      = f2e_l.split()
			line_number = int(fields[0])
			f_index     = int(fields[1])
			e_index     = int(fields[2])

			self.f2e_align[line_number][e_index][f_index] = 1
			f2e_l = self.f2e.readline()

		e2f_l = self.e2f.readline()
		while e2f_l:
			fields      = e2f_l.split()
			line_number = int(fields[0])
			e_index     = int(fields[1])
			f_index     = int(fields[2])

			self.e2f_align[line_number][e_index][f_index] = 1
			e2f_l = self.e2f.readline()		


	def find_intersection(self):
		for line_number in range(1,len(self.e2f_align)+1):
			intersection = [[0 for i in \
		    		range(len(self.f2e_align[line_number][0]))] \
		    		for j in range(len(self.f2e_align[line_number]))]
			for i in range(len(self.f2e_align[line_number])):
				for j in range(len(self.f2e_align[line_number][0])):
					intersection[i][j] = self.f2e_align[line_number][i][j]*\
										 self.e2f_align[line_number][i][j]
			self.intersection[line_number] = intersection

	def find_union(self):
		for line_number in range(1,len(self.e2f_align)+1):
			union = [[0 for i in \
		    		range(len(self.f2e_align[line_number][0]))] \
		    		for j in range(len(self.f2e_align[line_number]))]
			for i in range(len(self.f2e_align[line_number])):
				for j in range(len(self.f2e_align[line_number][0])):
					union[i][j] = self.f2e_align[line_number][i][j]|\
										 self.e2f_align[line_number][i][j]
			self.union[line_number] = union

	def growing_addFromIntersection(self):
		# start from intersection
		self.grow = dict(self.intersection)
		for line_number in range(1,len(self.grow)+1):
			matrix = self.grow[line_number]
			union_matrix = self.union[line_number]
			findNeighbor = False
			# if line_number == 33:
			# 	self.print_as_matrix(33)
			for i in range(1,len(matrix)):
				# if findNeighbor: break
				for j in range(1,len(matrix[0])):
					if matrix[i][j] == 0 and union_matrix[i][j] == 1 and self.hasNeighbor(matrix,i,j):
						# print "found "+str(line_number)
						# print (i,j)
						matrix[i][j] = 1
						# findNeighbor = True
						# break


	def growing_removeFromUnion(self):
		# start from union
		self.grow = dict(self.union)
		for line_number in range(1,len(self.grow)+1):
			matrix = self.grow[line_number]
			findNeighbor = False
			for i in range(1,len(matrix)):
				if findNeighbor: break
				for j in range(1,len(matrix[0])):
					if not self.hasNeighbor(matrix,i,j):
						matrix[i][j] = 0
						findNeighbor = True
						break

	def neighbors(self, a, row, column):
		# print (row,column)
		return [a[j][i] if j >= 0 and j < len(a) and i >= 0 and i < len(a[0]) and (j,i)!=(row,column) else 0\
			for j in range(column-1, column+2) \
				for i in range(row-1, row+2)]

	def hasNeighbor(self,matrix,row,column):
		neighbors = self.neighbors(matrix,row,column)
		result = 0
		for neighbor in neighbors:
			result = result | neighbor
		if result == 0:
			return False
		else:
			return True

	def write_alignment(self):
		output = file("dev_grow.out","w")
		for line_number in range(1,len(self.grow)+1):
			matrix = self.grow[line_number]
			# if matrix != self.intersection[line_number]:
			# 	print "not same"
			# 	self.print_as_matrix(line_number)
			for i in range(1,len(matrix)):
				for j in range(1,len(matrix[0])):
					if matrix[i][j] == 1:
						result = "{} {} {}\n".format(line_number,i,j)
						output.write(result)
		output.close()


	def print_as_matrix(self,line_number):
		f2e_matrix   = self.f2e_align[line_number]
		e2f_matrix   = self.e2f_align[line_number]
		inter_matrix = self.intersection[line_number]
		union_matrix = self.union[line_number]
		grow_matrix  = self.grow[line_number]
		print "f2e align"
		for arr in f2e_matrix:
			print arr
		print "e2f align"
		for arr in e2f_matrix:
			print arr
		print "intersection"
		for arr in inter_matrix:
			print arr
		print "union"
		for arr in union_matrix:
			print arr
		print "grow"
		for arr in grow_matrix:
			print arr

if __name__ == '__main__':
	f2e    = file("f2e.out","r")
	e2f    = file("e2f.out","r")
	dev_en = file("dev.en","r")
	dev_es = file("dev.es","r")

	grow = GrowingAlign(f2e,e2f)
	# test = [[0,0,0],[0,1,0],[0,0,0]]
	# print test
	# print grow.hasNeighbor(test,1,1)
	grow.initialize_align(dev_en,dev_es)
	grow.parse_align()
	grow.find_intersection()
	grow.find_union()
	# grow.growing_removeFromUnion()
	grow.growing_addFromIntersection()
	grow.print_as_matrix(33)
	grow.write_alignment()

	
		