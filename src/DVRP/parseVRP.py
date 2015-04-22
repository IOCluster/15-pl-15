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
        return str(self.x) + " " + str(self.y)+" "
    

class VRP:
    def __init__(self, text = None):
        self.name = "problem1"
        self.num_depots = 1
        self.num_caps = 1
        self.num_visits = 1
        self.num_locations = 1
        self.num_vehicles = 1
        self.caps = 100
        self.depots = []
        self.demands = []
        self.location_coords = []
        self.locations = []
        self.durations = []
        self.times = []
        self.start = 0
        self.end = 0
        self.cutoff = 0.5
        if(text != None):
            #print(text)
            text = text.split('\n')
            section = 0 #1 - depots, 2 - demands, 3 - location coord, ...
            data_section = False
            for i in range(len(text)):
                line = text[i].split()
                #print(line)
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
                        break
                    elif(section == 1):
                        self.depots.insert(int(a), 0)
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
                        if self.start > t1:
                            self.start = t1
                        if self.end < t2:
                            self.end = t2
                    elif(section == 8):
                        i = int(a)
                        T = int(line[1])
                        self.times.insert(i, T)
                        
    def CreateFromFile(filename):
        text = open(filename).read()
        return VRP(text)
        
    
    def __str__(self):
        s = "VRPTEST "+self.name+"\n"
        s += "NAME: "+self.name+"\n"
        s += "NUM_DEPOTS: "+str(self.num_depots)+"\n"
        s +="NUM_CAPACITIES: "+str(self.num_caps)+"\n"
        s +="NUM_VISITS: "+str(self.num_visits)+"\n"
        s +="NUM_LOCATIONS: "+str(self.num_locations)+"\n"
        s +="NUM_VEHICLES: "+str(self.num_vehicles)+"\n"
        s +="CAPACIETIES: "+str(self.caps)+"\n"
        s +="DATA_SECTION\n"
        s +="DEPOTS\n"
        for i in range(self.num_depots):
            s +=str(i)+"\n"
        s +="DEMAND_SECTION\n"
        for i in range(self.num_visits):
            s += str(i + self.num_depots) + " " + str(self.demands[i])+"\n"
        s +="LOCATION_COORD_SECTION\n"
        for ind in self.locations:
            s += str(ind) + " " + str(self.location_coords[ind])+"\n"
        s +="DEPOT_LOCATION_SECTION\n"
        for i in range(self.num_depots):
            s += str(i)+" " +str(self.locations[i])+"\n"
        s +="VISIT_LOCATION_SECTION\n"
        for i in range(self.num_visits):
            s += str(i + self.num_depots)+" " +str(self.locations[i+self.num_depots])+"\n"
        s +="DURATION_SECTION\n"
        for i in range(self.num_visits):
            s += str(i + self.num_depots)+" " +str(self.durations[i])+"\n"
        s +="DEPOT_TIME_WINDOW_SECTION\n"
        for i in range(self.num_depots):
            s += str(i)+" " +str(self.times[i]["start"])+" " +str(self.times[i]["end"])+"\n"
        s +="TIME_AVAIL_SECTION\n"
        for i in range(self.num_visits):
            s += str(i + self.num_depots)+" " +str(self.times[i+self.num_depots])+"\n"
        s +="EOF"
        return(s)
                        
                    
