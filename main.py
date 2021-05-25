from level import Level
from hashlib import sha1
import tkinter as tk
import random
import matplotlib.pyplot as plt
import statistics


def hashbits(string, bits):
	digest = int.from_bytes(sha1(bytes(string, 'ascii')).digest(), 'little')
	return (digest >> 160-bits)
	
def hashhex(string):
	return str(hex(hash8bit(string)))[2:]
	
def numbertocolour(n):
	n = min(max(0, n), 255)
	h = str(hex(n))[2:]
	s = h.zfill(2)
	return f'#{s*3}'

def generate_grid(size):
	grid = [[(x+y*size) for x in range(size)] for y in range(size)]
	groups = { (x+y*size):[[x, y]] for x in range(size) for y in range(size)}
	for y in range(size):
		for x in range(size):
			# get direction to link to
			direction = [
				(0, 1),
				(1, 0),
				(0, -1),
				(-1, 0),
			][hashbits(f'{x},{y}', 2)]
			nx = x + direction[0]
			ny = y + direction[1]
			
			
			# if new cell in grid, and is in different group to current cell
			if nx in range(size) and ny in range(size):
				current_cell_group = grid[y][x]
				new_cell_group = grid[ny][nx]
				
				if current_cell_group != new_cell_group:
					
					# move all cells in current group to new group
					
					current_group_cells = groups[current_cell_group]
					for [cx, cy] in current_group_cells:
						grid[cy][cx] = new_cell_group
						
					groups[new_cell_group].extend(current_group_cells)
					del groups[current_cell_group]
				
	convert_group = { current_group:i for i, current_group in enumerate(groups)}
	groups = {convert_group[group]: groups[group] for group in groups}
	grid = [[convert_group[grid[y][x]] for x in range(size)] for y in range(size)]
	
	
	group_to_colour = { group: ("#%03x" % random.randint(0, 0xFFF) if len(groups[group]) > 12 else '#000000') for group in groups}
	# group_to_colour = { group: numbertocolour(len(groups[group])*4) for group in groups}
	
	group_sizes = [len(groups[group]) for group in groups]
	
	print('mean:', statistics.mean(group_sizes))
	print('median:', statistics.median(group_sizes))
	print('mode:', statistics.mode(group_sizes))
			
	return grid, group_to_colour, groups




if __name__ == '__main__':
	
	s = 5
	r = 200
	grid, group_to_colour, groups = generate_grid(r)
	
	def interactive_highlight():
		root = tk.Tk()
		label = tk.Label(root, text='...')
		label.pack()
		canvas = tk.Canvas(root, width=r*s, height=r*s)
		global prev_group
		prev_group = 0
		rect_grid = []
		
		def motion(e):
			global prev_group
			x, y = e.x, e.y
			group = grid[y//s][x//s]
			text = f'group: {group}, size: {len(groups[group])}'
			label.config(text=text)
			if group != prev_group:
				highlight_group(prev_group, highlight=False)
				highlight_group(group, highlight=True)
			
		def highlight_group(group, highlight=False):
			global prev_group
			outline = 'white' if highlight else group_to_colour[group]
			for [x, y] in groups[group]:
				canvas.itemconfig(rect_grid[y][x], outline=outline)
			prev_group = group
			
		canvas.bind('<Motion>', motion)
		canvas.pack()
		
		for y in range(r):
			rect_grid.append([])
			for x in range(r):
				col = group_to_colour[grid[y][x]]
				rect = canvas.create_rectangle(x*s, y*s, (x+1)*s-1, (y+1)*s-1, fill=col, outline=col, width=1)
				rect_grid[-1].append(rect)
			
		
		root.mainloop()
	
	interactive_highlight()

	def bar_graph():
		D = {}
		for group in groups:
			length = len(groups[group])
			if length in D:
				D[length] += length
			else:
				D[length] = length
				

		plt.bar(list(D.keys()), D.values(), color='g')

		plt.show()
	
	# bar_graph()
	
	# level = Level(100)
	
	