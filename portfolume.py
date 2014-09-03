import datetime
import csv
import math
import svgwrite

startyear = 2007
endyear = 2014

ft_matrix = [[]]	#Full Time Work
pf_matrix = [[]]	#Personal and Freelance Work
all_matrix = [[]]	#All Work

#worktypes = [["GD",25,159,164],["WD",211,103,142],["UX",123,161,195],["DV",70,165,199],["PD",112,196,200],["MG",70,133,153]]
#worktypes = [["GD",90,124,149],["WD",211,103,142],["UX",123,161,195],["DV",70,165,199],["PD",112,196,200],["MG",149,188,139]]
worktypes = [["GD",25,159,164],["WD",211,103,142],["UX",123,161,195],["DV",70,165,199],["PD",112,196,200],["MG",149,188,139]]
shape_size = 4

def worktype(wt):
	if wt=="GD":
		return 0
	elif wt=="WD":
		return 1
	elif wt=="UX":
		return 2
	elif wt=="DV":
		return 3
	elif wt=="PD":
		return 4
	elif wt=="MG":
		return 5
	else:
		return 6

def isfulltime(workkind):
	if workkind.startswith("Full Time Work"):
		return True
	else:
		return False

def iso_year_start(iso_year):
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta 

def isnewmonth(iso_year,iso_week,curmo):
	year_start = iso_year_start(iso_year)
	gregorian_date = year_start + datetime.timedelta(days=3, weeks=iso_week-1)
	if gregorian_date.month == curmo:
		return False
	else:
		return True

def rangetolist(x):
	result = []
	for part in x.split(','):
		if '-' in part:
			a, b = part.split('-')
			a, b = int(a), int(b)
			result.extend(range(a, b + 1))
		else:
			a = int(part)
			result.append(a)
	return result		

def countweeks(year):
	return int(datetime.date(year, 12, 31).strftime("%W"))

def buildmatrix(m):		
	for i in range (startyear,endyear+1):		
		j = 0
		isowc = countweeks(i) #counts weeks per year
		m.append([])
		for j in range (0,isowc):
			curyear = i - startyear #the index starts with 0 = startyear, 1 = startyear+1...
			m[curyear].append([0,0,0,0,0,0]) #work type counts per week

def printmatrix(m,d):
	x_pos = 0
	y_pos = 0
	yearnum = 0		
	for y in m: #for every year in the matrix		
		curmo = 1
		weeknum = 0
		for w in y: #for every week in the year
			x_pos = 0
			if(isnewmonth(yearnum+startyear,weeknum+1,curmo)):
				curmo += 1
				y_pos += shape_size + 2 #new month
			else:
				y_pos += shape_size + 1 #new week
			typecount = 0	
			for t in w: #for every square count in the week
				n = 0 #count number of squares				
				while n < t:
					#d.add(d.rect((x_pos, y_pos), (shape_size, shape_size), fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print square
					d.add(d.circle((x_pos, y_pos), shape_size/2, fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print circle
					x_pos += shape_size + 1
					n += 1
				typecount += 1	
			weeknum += 1
		y_pos += 6 #new year
		yearnum += 1
	d.save()

def printmatrixbiweekly(m,d,h): #matrix, drawing, hours per shape
	x_pos = 0
	y_pos = 0
	yearnum = 0		
	for y in m: #for every year in the matrix		
		curmo = 1
		weeknum = 0

		while (weeknum < len(y)): #for every week in the year
			x_pos = 0
			if(isnewmonth(yearnum+startyear,weeknum+1,curmo)):
				curmo += 1
				y_pos += shape_size + 2 #new month
			elif(isnewmonth(yearnum+startyear,weeknum+2,curmo)):
				curmo += 1
				y_pos += shape_size + 2 #new month
				
			else:
				y_pos += shape_size + 1 #new week
			typecount = 0	
			for t in y[weeknum]: #for every square count in the week
				squarecounter = t
				if(weeknum+1<len(m[yearnum])):
					squarecounter += m[yearnum][weeknum+1][typecount]
					#print(squarecounter)
				n = 0 #count number of squares	
				squarecounter = math.ceil(squarecounter/h) #1 circle = h hours							
				while n < squarecounter:
					#d.add(d.rect((x_pos, y_pos), (shape_size, shape_size), fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print square
					d.add(d.circle((x_pos, y_pos), shape_size/2, fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print circle
					x_pos += shape_size + 1
					n += 1
				typecount += 1	
			weeknum += 2
		y_pos += 6 #new year
		yearnum += 1
	d.save()	

def printmatrixmonthly(m,d): #matrix, drawing
	x_pos = 0
	y_pos = 0
	yearnum = 0		
	for y in m: #for every year in the matrix		
		curmo = 1
		weeknum = 0
		x_pos = 0
		#print(yearnum+startyear)
		for w in y: #for every week in the year
			#print(weeknum)			
			if(isnewmonth(yearnum+startyear,weeknum+1,curmo)):
				x_pos = 0				
				curmo += 1
				y_pos += shape_size + 2 #new month			
				#d.add(d.text(curmo, insert=(x_pos, y_pos), fill='red'))
				#x_pos += 5
			typecount = 0	
			for t in w: #for every square count in the week
				n = 0 #count number of squares				
				while n < t:
					#d.add(d.rect((x_pos, y_pos), (shape_size, shape_size), fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print square
					d.add(d.circle((x_pos, y_pos), shape_size/2, fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print circle
					x_pos += shape_size + 1
					n += 1
				typecount += 1	
			weeknum += 1
		d.add(d.rect((0, y_pos+1), (6, 4), fill=svgwrite.rgb(0,0,0))) #new year marker
		y_pos += 6 #new year
		yearnum += 1
	d.save()	

def printmatrixmonthly2(m,d): #matrix, drawing
	x_pos = 0
	y_pos = 0
	yearnum = 0		
	dotcounter = 0
	for y in m: #for every year in the matrix		
		curmo = 1
		weeknum = 0
		#print(yearnum+startyear)
		if(len(y)>0):
			while (weeknum < 50): #for every month in the year
				#my_date = datetime.datetime.strptime(str(curmo), "%m")
				#print(my_date.strftime("%b"))
				x_pos = 0
				#d.add(d.text(curmo, insert=(x_pos, y_pos), fill='red'))
				x_pos += 5
				new_wn = weeknum+3
				getnewmonth = True
				counter = 1
				if(weeknum >= 48):
					new_wn = countweeks(yearnum+startyear)
				else:
					while getnewmonth:
						if(isnewmonth(yearnum+startyear,weeknum+counter+1,curmo)):						
							new_wn = weeknum+counter
							getnewmonth = False
						else:
							pass
						counter += 1					
				typecount = 0
				for t in y[weeknum]: #for every square count in the week					
					squarecounter = t
					wc = weeknum + 1
					while wc < new_wn:
						squarecounter += m[yearnum][wc][typecount]
						wc += 1
					n = 0 #count number of squares
					squarecounter = math.ceil(squarecounter/2) #1 circle = 2 hours				
					while n < squarecounter:
						#d.add(d.rect((x_pos, y_pos), (shape_size, shape_size), fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print square
						d.add(d.circle((x_pos, y_pos), shape_size/2, fill=svgwrite.rgb(worktypes[typecount][1], worktypes[typecount][2], worktypes[typecount][3]))) #print circle
						dotcounter += 1
						x_pos += shape_size + 1
						n += 1
					#print(worktypes[typecount][0]+": "+str(squarecounter))
					typecount += 1	
				weeknum = new_wn
				curmo += 1
				y_pos += shape_size + 2 #new month
		#d.add(d.rect((0, y_pos+1), (6, 4), fill=svgwrite.rgb(0,0,0))) #new year marker
		y_pos += 6 #new year
		yearnum += 1
	d.save()
	#print(dotcounter)	

buildmatrix(ft_matrix)
buildmatrix(pf_matrix)
buildmatrix(all_matrix)


ifile  = open('mika_work.csv', "rt", encoding="utf-8")
read = csv.reader(ifile)
firstline = True
totalhours = 0
for row in read:
	if firstline:
		firstline = False
		continue
	year = int(row[0]) - startyear
	wt = worktype(row[4])
	hours = row[12]
	kind = row[6]
	weeks = rangetolist(row[2])
	totalhours += int(hours)
	new_hours = math.ceil(int(hours)/len(weeks))
	
	if isfulltime(kind):
		for i in weeks:
			ft_matrix[year][i-1][wt] += new_hours
			all_matrix[year][i-1][wt] += new_hours
	else:
		for i in weeks:
			#print (str(year)+" "+str(i)+" "+str(wt))
			pf_matrix[year][i-1][wt] += new_hours
			all_matrix[year][i-1][wt] += new_hours	


ft_dwg = svgwrite.Drawing('ft_circles_biweekly.svg', profile='tiny')
pf_dwg = svgwrite.Drawing('pf_circles_biweekly.svg', profile='tiny')
all_dwg = svgwrite.Drawing('all_circles_monthly.svg', profile='tiny')
all_dwg2 = svgwrite.Drawing('all_circles_monthly2.svg', profile='tiny')

all_dwg_biweekly = svgwrite.Drawing('all_circles_biweekly2.svg', profile='tiny')

printmatrixbiweekly(all_matrix, all_dwg_biweekly, 2)
#printmatrixmonthly(all_matrix, all_dwg)
#printmatrixmonthly2(all_matrix, all_dwg2)
