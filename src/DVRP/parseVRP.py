from math import *

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
	
    def Distance(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        return sqrt(dx*dx + dy*dy)

    def __str__(self):
        return "("+ str(self.x) + ", " + str(self.y)+")"
    

class VRP:
    def __init__(self, filename = None):
        self.name = "problem1"
        self.num_depots = 1
        self.num_caps = 1
        self.num_visits = 1
        self.num_locations = 1
        self.num_vehicles = 1
        self.caps = 100
        self.demands = []
        self.location_coords = []
        self.locations = []
        self.durations = []
        self.times = []
        if(filename != None):
            text = open(filename).read()
            text = text.split('\n')
            section = 0 #1 - depots, 2 - demands, 3 - location coord, ...
            data_section = False
            for i in range(len(text)):
                line = text[i].split()
                a = line[0]
                if(a == "COMMENT:" or a == "VRPTEST"):
                    continue
                if(data_section == False):
                    if(a == "NAME:"):
                        self.name = line[1]
                    elif(a == "NUM_DEPOTS:"):
                        self.num_depots = int(line[1])
                    elif(a == "NUM_CAPACITIES:"):
                        self.num_caps = int(line[1])
                    elif(a == "NUM_VISITS:"):
                        self.num_visits = int(line[1])
                    elif(a =="NUM_LOCATIONS:"):
                        self.num_locations = int(line[1])
                    elif(a == "NUM_VEHICLES:"):
                        self.num_vehicles = int(line[1])
                    elif(a == "CAPACITIES:"):
                        self.caps = int(line[1])
                    elif(a == "DATA_SECTION"):
                        data_section = True
                else:
                    if(a == "DEPOTS"):
                        section = 1
                    elif(a == "DEMAND_SECTION"):
                        section = 2
                    elif(a == "LOCATION_COORD_SECTION"):
                        section = 3
                    elif(a == "DEPOT_LOCATION_SECTION"):
                        section = 4
                    elif(a == "VISIT_LOCATION_SECTION"):
                        section = 5
                    elif(a == "DURATION_SECTION"):
                        section = 6
                    elif(a == "DEPOT_TIME_WINDOW_SECTION"):
                        section = 7
                    elif(a == "TIME_AVAIL_SECTION"):
                        section = 8
                    elif(a == "EOF"):
                        section = 0
                    elif(section == 1):
                        self.demands.insert(int(a), 0)
                    elif(section == 2):
                        self.demands.insert(int(a), int(line[1]))
                    elif(section == 3):
                        x = int(line[1])
                        y = int(line[2])
                        self.location_coords.insert(int(a), Point(x,y))
                    elif(section == 4 or section == 5):
                        i = int(a)
                        x = int(line[1])
                        self.locations.insert(i, x)
                    elif(section == 6):
                        i = int(a)
                        t = int(line[1])
                        self.durations.insert(i,t)
                    elif(section == 7):
                        i = int(a)
                        t1 = int(line[1])
                        t2 = int(line[2])
                        self.times.insert(i, {"start" : t1, "end" : t2})
                    elif(section == 8):
                        i = int(a)
                        T = int(line[1])
                        self.times.insert(i, T)
                    
                    
                        
                    
