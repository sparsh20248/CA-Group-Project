from input import list_of_instructions
import matplotlib.pyplot as plt 
outfile = open('log.txt', 'w')

class Link:
    input=  False
    output = False
    busy = False
    
class Router:
    name = ""
    counter = 0
    busy = False
    source = ""
    destination = ""
    def __init__(self, name):
        self.name = name
    def add_source(self, source):
        self.source = source
        self.counter += 1
    def add_destination(self, destination):
        self.destination = destination 
        self.counter += 1
    def add_header(self):
        self.counter += 1
    def add_flit(self):
        self.counter += 1
    def add_tail(self):
        self.counter = 0
    def update(self,instruction, clock_cyle, statement, source, destination):
        L = ["Clock cycle: ", str(clock_cyle) + " ", "Flit: ", str(statement) + " ", "Source: ", source.name + " ", "Destination: ", destination.name, "\n"]
        outfile.writelines(L)
        print("Clock cycle:", clock_cyle, "Flit:", statement, "Source:", instruction.source, "Destination:", instruction.destination)
        return 


class Instruction:
    head_path = []
    f1_path = []
    f2_path = []
    f3_path = []
    tail_path = []
    route = []
    head = ""
    f1 = ""
    f2 = ""
    f3 = ""
    tail = ""
    index = 0
    clock_cycle = 0
    end_time = 0
    start_time = -1
    source = ""
    destination = ""
    def __init__(self, instruction, routing, routing_list, index):
        self.index = index
        self.clock_cycle = int(instruction[0])
        self.source = instruction[1]
        self.destination = instruction[2]
        self.head = "0000000000000000000000000000"+self.source+self.destination
        self.f1 = instruction[3][0:31]
        self.f2 = instruction[3][31:63]
        self.f3 = instruction[3][63:96]
        self.tail = "0000000000000000000000000000"
        self.make_path(routing, routing_list)
    
    def make_path(self, direction, routing_list):
        if direction == 1:
            self.head_path = self.get_path_XY(routing_list)
            self.f1_path = self.get_path_XY( routing_list)
            self.f2_path = self.get_path_XY( routing_list)
            self.f3_path = self.get_path_XY( routing_list)
            self.tail_path = self.get_path_XY( routing_list)
            self.route = self.get_path_XY( routing_list)
        if direction == 2:
            self.head_path = self.get_path_YX( routing_list)
            self.f1_path = self.get_path_YX( routing_list)
            self.f2_path = self.get_path_YX( routing_list)
            self.f3_path = self.get_path_YX( routing_list)
            self.tail_path = self.get_path_YX( routing_list)
            self.route = self.get_path_YX( routing_list)
    
    def update_end(self, clock_cycle):
        self.end_time = clock_cycle
        
    
    def print_route(self):
        for i in self.route:
            print(i.name, end = " ")
        print()
        
    def get_path_XY(self, routing_list):
        #path according to the routing algo: Midsem = XY
        path = []
        if self.source==self.destination:
            return
        if self.source == "1":
            path.append(routing_list[0])
            if self.destination == "2":
                path.append(routing_list[1])

            if self.destination == "3":
                path.append(routing_list[1])
                path.append(routing_list[2])

            if self.destination == "4":
                path.append(routing_list[3])
                
        if self.source == "2":
            path.append(routing_list[1])
            if self.destination == "1":
                path.append(routing_list[0])

            if self.destination == "3":
                path.append(routing_list[2])

            if self.destination == "4":
                path.append(routing_list[0])
                path.append(routing_list[3])
                
        if self.source == "3":
            path.append(routing_list[2])
            if self.destination == "1":
                path.append(routing_list[3])
                path.append(routing_list[0])
            if self.destination == "2":
                path.append(routing_list[1])
            if self.destination == "4":
                path.append(routing_list[3])

        if self.source == "4":
            path.append(routing_list[3])
            if self.destination == "1":
                path.append(routing_list[0])
            if self.destination == "2":
                path.append(routing_list[2])
                path.append(routing_list[1])
            if self.destination == "3":
                path.append(routing_list[2])
        
        for i in path: print(i, end=" ")
        print()
        return path

    def get_path_YX(self,routing_list):
        #path according to the routing algo: YX
        path = []
        if self.source==self.destination:
            return
        if self.source == "1":
            path.append(routing_list[0])
            if self.destination == "2":
                path.append(routing_list[1])

            if self.destination == "3":
                path.append(routing_list[3])
                path.append(routing_list[2])

            if self.destination == "4":
                path.append(routing_list[3])


        if self.source == "2":
            path.append(routing_list[1])
            if self.destination == "1":
                path.append(routing_list[0])

            if self.destination == "3":
                path.append(routing_list[2])

            if self.destination == "4":
                path.append(routing_list[2])
                path.append(routing_list[3])

        if self.source == "3":
            path.append(routing_list[2])

            if self.destination == "1":
                path.append(routing_list[1])
                path.append(routing_list[0])

            if self.destination == "2":
                path.append(routing_list[1])

            if self.destination == "4":
                path.append(routing_list[3])

        if self.source == "4":
            path.append(routing_list[3])

            if self.destination == "1":
                path.append(routing_list[2])

            if self.destination == "2":
                path.append(routing_list[0])
                path.append(routing_list[1])

            if self.destination == "3":
                path.append(routing_list[2])
        for i in path: print(i.name, end=" ")
        print()
        return path
        
class NoC:
    traffic1 = []
    traffic2 = []
    traffic3 = []
    traffic4 = []
    all_intructions = []
    r1 = Router("Router 1")
    r2 = Router("Router 2")
    r3 = Router("Router 3")
    r4 = Router("Router 4")
    router_list = [r1, r2, r3, r4]
    def add_instruction(self, instructions, routing):
        index = 1
        for x in instructions:
            x = list(map(str,x.split()))    
            input = Instruction(x, routing, self.router_list, index)
            self.all_intructions.append(input)
            print(input.source)
            if(input.source == "1"):
                self.traffic1.append(input)
                self.traffic1.sort(key = lambda x: x.clock_cycle)
            if(input.source == "2"):
                self.traffic2.append(input)
                self.traffic2.sort(key = lambda x: x.clock_cycle)
            if(input.source == "3"):
                self.traffic3.append(input)
                self.traffic3.sort(key = lambda x: x.clock_cycle)
            if(input.source == "4"):
                self.traffic4.append(input)
                self.traffic4.sort(key = lambda x: x.clock_cycle)
            index+=1

    def check(self, clock_cycle):
        list = []
        if len(self.traffic1)>0 and int(self.traffic1[0].clock_cycle) == clock_cycle:
            list.append(self.traffic1[0])
            self.traffic1.pop(0)
        if len(self.traffic2)>0 and int(self.traffic2[0].clock_cycle)  == clock_cycle:
            list.append(self.traffic2[0])
            self.traffic2.pop(0)
        if len(self.traffic3)>0 and int(self.traffic3[0].clock_cycle)  == clock_cycle:
            list.append(self.traffic3[0])
            self.traffic3.pop(0)
        if len(self.traffic4)>0 and int(self.traffic4[0].clock_cycle)  == clock_cycle:
            list.append(self.traffic4[0])
            self.traffic4.pop(0)
        return list
    
    def play(self):
        everything = []
        total_tic = int(input("Enter the total number of clock cycles: "))
        queue = []
        queue_temp = []
        routing = int(input("Enter 1 for XY routing and 2 for YX routing: "))
        self.add_instruction(list_of_instructions, routing)

        for clock_cycle in range(total_tic):
            queue = queue_temp.copy()
            x = self.check(clock_cycle)
            if len(x) > 0:
                for i in x:
                    queue.append(i)
            print("clock cycle = ", clock_cycle, len(queue))
            
            for instruction in queue:
                queue_temp = queue.copy()
                if len(instruction.head_path) > 1 and instruction.head_path[1].busy == 0 and (instruction.head_path[0].busy == 0 or instruction.head_path[0].busy == instruction.index):
                    if instruction.start_time == -1: instruction.start_time = clock_cycle
                    instruction.head_path[1].busy = instruction.index
                    instruction.head_path[0].busy = instruction.index
                    everything.append([instruction.head_path[0],instruction.head_path[1]])
                    instruction.head_path[0].update(instruction, clock_cycle, "Head", instruction.head_path[0], instruction.head_path[1])
                    instruction.head_path.pop(0)
                    if len(instruction.route) == 2: continue
                    
                if len(instruction.head_path) - len(instruction.f1_path) == 2 or len(instruction.head_path) == 1:
                    check = False
                    if(len(instruction.f1_path) > 1) :
                        check = True
                        everything.append([instruction.f1_path[0],instruction.f1_path[1]])
                        instruction.f1_path[0].update(instruction, clock_cycle, "Flit 1", instruction.f1_path[0], instruction.f1_path[1])
                        instruction.f1_path.pop(0)
                    if check and len(instruction.route) == 2: continue
                    
                if len(instruction.f1_path) - len(instruction.f2_path) == 2 or len(instruction.f1_path) == 1:
                    check = False
                    if(len(instruction.f2_path) > 1) :
                        check = True
                        everything.append([instruction.f2_path[0],instruction.f2_path[1]])
                        instruction.f2_path[0].update(instruction, clock_cycle, "Flit 2", instruction.f2_path[0], instruction.f2_path[1])
                        instruction.f2_path.pop(0)
                    if check and len(instruction.route) == 2: continue
                
                if len(instruction.f2_path) - len(instruction.f3_path) == 2 or len(instruction.f2_path) == 1:
                    check = False
                    if(len(instruction.f3_path) > 1) :
                        check = True
                        everything.append([instruction.f3_path[0],instruction.f3_path[1]])
                        instruction.f3_path[0].update(instruction, clock_cycle, "Flit 3", instruction.f3_path[0], instruction.f3_path[1])
                        instruction.f3_path.pop(0)
                    if check and len(instruction.route) == 2: continue

                if len(instruction.f3_path) - len(instruction.tail) == 2 or len(instruction.f3_path) == 1:
                    check = False
                    if(len(instruction.tail_path) > 1) :
                        check = True
                        everything.append([instruction.tail_path[0],instruction.tail_path[1]])
                        instruction.tail_path[0].update(instruction, clock_cycle, "Tail", instruction.tail_path[0], instruction.tail_path[1])
                        instruction.tail_path[0].busy = False
                        instruction.tail_path.pop(0)
                    if len(instruction.tail_path) == 1 and instruction.end_time == 0: 
                        instruction.update_end(clock_cycle)
                        instruction.tail_path[0].busy = False
                        # queue.pop(0)
                        
        return everything
                        

        
n = NoC()

everything = n.play()

def plot_latency(n):
    list = []
    for i in n.all_intructions:
        print(i.start_time, i.end_time)
        list.append([i.start_time, i.end_time]) 
    list = sorted(list, key=lambda x: x[0]) 
    X1 = []
    for i in range(len(list)):
        X1.append("P"+str(i+1))
    Y1 = []
    for i in range(len(list)):
        Y1.append(list[i][1] - list[i][0])
    plt.bar(X1, Y1, color = 'blue', width = 0.4)
    plt.show()

def plot_links(everything):
    list = [0, 0, 0, 0, 0, 0, 0, 0]
    name = ["R1-R2", "R1-R4", "R2-R3", "R3-R4", "R1-PE1", "R2-PE2", "R3-PE3", "R4-PE4"]
    print(len(n.router_list))
    for j in everything:
        print(j[0].name, j[1].name)
        if j[0].name == "Router 1" and j[1].name == "Router 2":
            list[0]+=1
        if j[0].name == "Router 2" and j[1].name == "Router 1":
            list[0]+=1
        if j[0].name == "Router 1" and j[1].name == "Router 4":
            list[1]+=1
        if j[0].name == "Router 4" and j[1].name == "Router 1":
            list[1]+=1
        if j[0].name == "Router 3" and j[1].name == "Router 2":
            list[2]+=1
        if j[0].name == "Router 2" and j[1].name == "Router 3":
            list[2]+=1
        if j[0].name == "Router 4" and j[1].name == "Router 3":
            list[3]+=1
        if j[0].name == "Router 3" and j[1].name == "Router 4":
            list[3]+=1
        print(list)

    
    for i in n.all_intructions:
        if i.destination == "1":
            list[4]+=3
        if i.destination == "2":
            list[5]+=3
        if i.destination == "3":
            list[6]+=3
        if i.destination == "4":
            list[7]+=3
    
    plt.bar(name, list, color = 'blue', width = 0.4)
    plt.show()

plot_latency(n)
plot_links(everything)

