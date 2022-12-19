from input import list_of_instructions
import matplotlib.pyplot as plt
outfile = open('log.txt', 'w')

class Link:
    input = False
    output = False
    busy = False
    flits_transferred = 0

class Router:
    counter = 0 
    source = ""
    destination = ""
    
    def add_source(self, source):
        self.source = source
        self.counter += 1
    def add_destination(self, destination):
        self.destination = destination 
        self.counter += 1
    def add_flit(self):
        self.counter += 1
    def add_tail(self):
        self.counter = 0

    def update(self,instruction, clock_cyle, statement):
        if len(instruction.path) == 1:
            L = ["Clock cycle: ", str(clock_cyle) + " ", "Flit: ", str(statement) + " ", "Source: ", instruction.source + " ", "Destination: ", instruction.destination, "\n"]
        else:
            if instruction.counter%2== 0 or instruction.head_sent == 0 or instruction.tail_next == 0:
                L = ["Clock cycle: ", str(clock_cyle) + " ", "Flit: ", str(statement) + " ", "Source: ", instruction.source + " ", "Destination: ", str(instruction.path[0]), "\n"]
            else:
                L = ["Clock cycle: ", str(clock_cyle) + " ", "Flit: ", str(statement) + " ", "Source: ", str(instruction.path[0]) + " ", "Destination: ", instruction.destination, "\n"]
        outfile.writelines(L)
        # print("Clock cycle:", clock_cyle, "Flit:", statement, "Source:", instruction.source, "Destination:", instruction.destination)
        return 


class Instruction:
    clock_cycle = 0
    head_sent = 0
    source = ""
    destination = ""
    head = ""
    f1 = ""
    f2 = ""
    f3 = ""
    tail = ""
    counter = -1
    tail_next = -1
    path =  []
    latency = 0
    start_time = -1
    def __init__(self, instuction):
        self.clock_cycle = int(instuction[0])
        self.source = instuction[1]
        self.destination = instuction[2]
        self.head = "0000000000000000000000000000"+self.source+self.destination
        self.f1 = instuction[3][0:31]
        self.f2 = instuction[3][31:63]
        self.f3 = instuction[3][63:96]
        self.tail = "0000000000000000000000000000"
        self.path =  []
    
    def get_path_XY(self):
        #path according to the routing algo: Midsem = XY
        self.path = []
        if self.source==self.destination:
            return
        if self.source == "1":

            if self.destination == "2":
                self.path.append("2")

            if self.destination == "3":
                self.path.append("2")
                self.path.append("3")

            if self.destination == "4":
                self.path.append("4")


        if self.source == "2":

            if self.destination == "1":
                self.path.append("1")

            if self.destination == "3":
                self.path.append("3")

            if self.destination == "4":
                self.path.append("1")
                self.path.append("4")

        if self.source == "3":

            if self.destination == "1":
                self.path.append("4")
                self.path.append("1")

            if self.destination == "2":
                self.path.append("2")

            if self.destination == "4":
                self.path.append("4")

        if self.source == "4":

            if self.destination == "1":
                self.path.append("1")

            if self.destination == "2":
                self.path.append("3")
                self.path.append("2")

            if self.destination == "3":
                self.path.append("3")

        return self.path
    
    def get_path_YX(self):
        #path according to the routing algo: YX
        self.path = []
        if self.source==self.destination:
            return
        if self.source == "1":

            if self.destination == "2":
                self.path.append("2")

            if self.destination == "3":
                self.path.append("4")
                self.path.append("3")

            if self.destination == "4":
                self.path.append("4")


        if self.source == "2":

            if self.destination == "1":
                self.path.append("1")

            if self.destination == "3":
                self.path.append("3")

            if self.destination == "4":
                self.path.append("3")
                self.path.append("4")

        if self.source == "3":

            if self.destination == "1":
                self.path.append("2")
                self.path.append("1")

            if self.destination == "2":
                self.path.append("2")

            if self.destination == "4":
                self.path.append("4")

        if self.source == "4":

            if self.destination == "1":
                self.path.append("1")

            if self.destination == "2":
                self.path.append("1")
                self.path.append("2")

            if self.destination == "3":
                self.path.append("3")

        return self.path

# def print_list(list):
#     for i in list:
#         print("Source:",i.source,"Destination:",i.destination)

# def Print(list):
#     for i in list:
#         # print(i)
#         print(i)

class NoC:
    trafic1 = []
    trafic2 = []
    trafic3 = []
    trafic4 = []
    l1 = Link()
    l2 = Link()
    l3 = Link()
    l4 = Link()
    list1 = [0,0,0,0]
    
    r1 = Router()
    r2 = Router()
    r3 = Router()
    r4 = Router()
    list1 = []
    
    def add_intruction(self, intructions):
        for x in intructions:
            x = list(map(str,x.split()))
            input = Instruction(x)

            if input.source == "1":
                self.trafic1.append(input)
                self.trafic1.sort(key=lambda x: x.clock_cycle)
            elif input.source == "2":
                self.trafic2.append(input)  
                self.trafic2.sort(key=lambda x: x.clock_cycle)
            elif input.source == "3":
                self.trafic3.append(input)
                self.trafic3.sort(key=lambda x: x.clock_cycle)
            elif input.source == "4":
                self.trafic4.append(input)
                self.trafic4.sort(key=lambda x: x.clock_cycle)
            
        
    def check(self, clock_cycle):
        list = []
        if len(self.trafic1)>0 and int(self.trafic1[0].clock_cycle) == clock_cycle:
            list.append(self.trafic1[0])
            self.trafic1.pop(0)
        if len(self.trafic2)>0 and int(self.trafic2[0].clock_cycle)  == clock_cycle:
            list.append(self.trafic2[0])
            self.trafic2.pop(0)
        if len(self.trafic3)>0 and int(self.trafic3[0].clock_cycle)  == clock_cycle:
            list.append(self.trafic3[0])
            self.trafic3.pop(0)
        if len(self.trafic4)>0 and int(self.trafic4[0].clock_cycle)  == clock_cycle:
            list.append(self.trafic4[0])
            self.trafic4.pop(0)
        return list

    def func1(self,instruction):
        if len(instruction.path) == 1:
            s = instruction.source
            d = instruction.destination
            if(s=="2" and d=="1"):
                self.l1.input = s
                self.l1.output = d
                self.l1.flits_transferred+=1
            elif(s=="4" and d=="1"):
                self.l4.input = s
                self.l4.output = d
                self.l4.flits_transferred+=1
        
        else:
            if instruction.counter%2== 0 or instruction.head_sent == 0 or instruction.tail_next == 0:
                s = instruction.source
                d = str(instruction.path[0])
                if(s=="2" and d=="1"):
                    self.l1.input = s
                    self.l1.output = d
                    self.l1.flits_transferred+=1
                elif(s=="4" and d=="1"):
                    self.l4.input = s
                    self.l4.output = d
                    self.l4.flits_transferred+=1
                    
            else:
                s = str(instruction.path[0])
                d = instruction.destination
                if(s=="2" and d=="1"):
                    self.l1.input = s
                    self.l1.output = d
                    self.l1.flits_transferred+=1
                elif(s=="4" and d=="1"):
                    self.l4.input = s
                    self.l4.output = d
                    self.l4.flits_transferred+=1
        return

    def func2(self,instruction):

        if len(instruction.path) == 1:
            s = instruction.source
            d = instruction.destination
            if(s=="1" and d=="2"):
                self.l1.input = s
                self.l1.output = d
                self.l1.flits_transferred+=1
            elif(s=="3" and d=="2"):
                self.l2.input = s
                self.l2.output = d
                self.l2.flits_transferred+=1
            
        else:
            if instruction.counter%2== 0 or instruction.head_sent == 0 or instruction.tail_next == 0:
                s = instruction.source
                d = str(instruction.path[0])
                if(s=="1" and d=="2"):
                    self.l1.input = s
                    self.l1.output = d
                    self.l1.flits_transferred+=1
                elif(s=="3" and d=="2"):
                    self.l2.input = s
                    self.l2.output = d
                    self.l2.flits_transferred+=1
                    
            else:
                s = str(instruction.path[0])
                d = instruction.destination
                if(s=="1" and d=="2"):
                    self.l1.input = s
                    self.l1.output = d
                    self.l1.flits_transferred+=1
                elif(s=="3" and d=="2"):
                    self.l2.input = s
                    self.l2.output = d
                    self.l2.flits_transferred+=1
        return
                        
    def func3(self,instruction):
        if len(instruction.path) == 1:
            s = instruction.source
            d = instruction.destination
            if(s=="2" and d=="3"):
                self.l2.input = s
                self.l2.output = d
                self.l2.flits_transferred+=1
            elif(s=="4" and d=="3"):
                self.l3.input = s
                self.l3.output = d
                self.l3.flits_transferred+=1
            
        else:
            if instruction.counter%2== 0 or instruction.head_sent == 0 or instruction.tail_next == 0:
                s = instruction.source
                d = str(instruction.path[0])
                if(s=="2" and d=="3"):
                    self.l2.input = s
                    self.l2.output = d
                    self.l2.flits_transferred+=1
                elif(s=="4" and d=="3"):
                    self.l3.input = s
                    self.l3.output = d
                    self.l3.flits_transferred+=1
                    
            else:
                s = str(instruction.path[0])
                d = instruction.destination
                if(s=="2" and d=="3"):
                    self.l2.input = s
                    self.l2.output = d
                    self.l2.flits_transferred+=1
                elif(s=="4" and d=="3"):
                    self.l3.input = s
                    self.l3.output = d
                    self.l3.flits_transferred+=1
        return 

    def func4(self,instruction):
        if len(instruction.path) == 1:
            s = instruction.source
            d = instruction.destination
            if(s=="1" and d=="4"):
                self.l4.input = s
                self.l4.output = d
                self.l4.flits_transferred+=1
            elif(s=="3" and d=="4"):
                self.l3.input = s
                self.l3.output = d
                self.l3.flits_transferred+=1
            
        else:
            if instruction.counter%2== 0 or instruction.head_sent == 0 or instruction.tail_next == 0:
                s = instruction.source
                d = str(instruction.path[0])
                if(s=="1" and d=="4"):
                    self.l4.input = s
                    self.l4.output = d
                    self.l4.flits_transferred+=1
                elif(s=="3" and d=="4"):
                    self.l3.input = s
                    self.l3.output = d
                    self.l3.flits_transferred+=1
                    
            else:
                s = str(instruction.path[0])
                d = instruction.destination
                if(s=="1" and d=="4"):
                    self.l4.input = s
                    self.l4.output = d
                    self.l4.flits_transferred+=1
                elif(s=="3" and d=="4"):
                    self.l3.input = s
                    self.l3.output = d
                    self.l3.flits_transferred+=1
        return
                               
    
    
    def play(self):
        total_tic = int(input("How many clock cycles do you want to simulate? "))
        routing = int(input("What routing algo to implement ?. Type 1 for XY and 2 for YX  "))
        queue = [] #add input objects to this queue
        queue_temp = []
        for clock_cycle in range(total_tic):
            queue = queue_temp.copy()
            x = self.check(clock_cycle)
            if len(x) > 0:
                for i in x:
                    queue.append(i)
            
            for instruction in queue:
                queue_temp = queue.copy()
                if routing == 1:get_path = instruction.get_path_XY()
                else: get_path = instruction.get_path_YX()
                if instruction.head_sent < len(get_path):  
                    if get_path[instruction.head_sent] == "1":
                        self.func1(instruction)
                        if(instruction.start_time == -1):
                            instruction.start_time = clock_cycle 
                        self.r1.update(instruction,clock_cycle,  "Head")
                    elif get_path[instruction.head_sent] == "2":

                        self.func2(instruction)
                        if(instruction.start_time == -1):
                            instruction.start_time = clock_cycle
                        self.r2.update(instruction, clock_cycle,  "Head")
                    elif get_path[instruction.head_sent] == "3":

                        self.func3(instruction)
                        if(instruction.start_time == -1):
                            instruction.start_time = clock_cycle
                        self.r3.update(instruction, clock_cycle, "Head")
                    elif get_path[instruction.head_sent] == "4":
                        
                        self.func4(instruction)
                        if(instruction.start_time == -1):
                            instruction.start_time = clock_cycle
                        self.r4.update(instruction, clock_cycle, "Head")
                    
                    instruction.head_sent += 1
                    
                    if instruction.head_sent == len(get_path):
                        # instruction.start_time = clock_cycle
                        instruction.head_sent = 3
                        instruction.counter = 0


                elif instruction.head_sent == 3 and instruction.tail_next == -1:
                    if instruction.counter // len(get_path) == 0:
                            if(get_path[instruction.counter % len(get_path)] == "1"):
                               
                                self.func1(instruction)
                                self.r1.update(instruction, clock_cycle, "flit 1")
                            if(get_path[instruction.counter % len(get_path)] == "2"):

                                self.func2(instruction)
                                self.r2.update(instruction, clock_cycle, "flit 1")
                            if(get_path[instruction.counter % len(get_path)] == "3"):
                                self.func3(instruction)
                                self.r3.update(instruction, clock_cycle, "flit 1")
                            if(get_path[instruction.counter % len(get_path)] == "4"):
                                self.func4(instruction) 
                                self.r4.update(instruction, clock_cycle, "flit 1")
                    if instruction.counter // len(get_path) == 1:
                            if(get_path[instruction.counter % len(get_path)] == "1"):
                    
                                self.func1(instruction)
                                self.r1.update(instruction, clock_cycle, "flit 2")
                            
                            if(get_path[instruction.counter % len(get_path)] == "2"):

                                self.func2(instruction)
                               
                                self.r2.update(instruction, clock_cycle, "flit 2")
                            
                            if(get_path[instruction.counter % len(get_path)] == "3"):
                            
                                self.func3(instruction)
                      
                                self.r3.update(instruction, clock_cycle, "flit 2")
                            
                            if(get_path[instruction.counter % len(get_path)] == "4"):
                                
                                self.func4(instruction)
                                self.r4.update(instruction, clock_cycle, "flit 2")
                    
                    if instruction.counter // len(get_path) == 2:
                            if(get_path[instruction.counter % len(get_path)] == "1"):
                               self.func1(instruction)
                               self.r1.update(instruction, clock_cycle, "flit 3")
                            
                            if(get_path[instruction.counter % len(get_path)] == "2"):

                                self.func2(instruction)
                                self.r2.update(instruction, clock_cycle, "flit 3")
                            
                            if(get_path[instruction.counter % len(get_path)] == "3"):
                                self.func3(instruction)
                                self.r3.update(instruction, clock_cycle, "flit 3")
                            
                            if(get_path[instruction.counter % len(get_path)] == "4"):
                                self.func4(instruction)
                                self.r4.update(instruction, clock_cycle, "flit 3")
                    
                    instruction.counter += 1
                    
                    if instruction.counter == 3*(len(get_path)):
                        instruction.tail_next = 0
                        instruction.counter = 7
                
                elif instruction.tail_next >=0 and instruction.tail_next < len(get_path):
                    if get_path[instruction.tail_next] == "1":

                        self.func1(instruction)
                        self.r1.update(instruction,clock_cycle,  "Tail")
                    
                    elif(get_path[instruction.tail_next] == "2"):

                        self.func2(instruction)
                        self.r2.update(instruction, clock_cycle, "Tail")
                            
                    elif(get_path[instruction.tail_next] == "3"):

                        self.func3(instruction)
                        self.r3.update(instruction, clock_cycle, "Tail")
                    
                    elif(get_path[instruction.tail_next] == "4"):
                        
                        self.func4(instruction)
                        self.r4.update(instruction, clock_cycle, "Tail")
                    
                    
                    instruction.tail_next += 1
                    
                    if instruction.tail_next == len(get_path):
                        instruction.latency = clock_cycle - instruction.start_time
                        self.list1.append(instruction)
                        queue_temp.remove(instruction)
                
                           
n = NoC()
n.add_intruction(list_of_instructions)

n.play()
X = ["L1","L2","L3","L4"]
Y = [n.l1.flits_transferred,n.l2.flits_transferred,n.l3.flits_transferred,n.l4.flits_transferred]
fig = plt.figure(figsize = (10, 5))
X1 = []
list1 = n.list1

list1 = sorted(list1, key=lambda x: x.start_time) 

for i in range(len(list1)):
    X1.append("P"+str(i+1))
Y1 = []
for i in range(len(list1)):
    Y1.append(list1[i].latency)

plt.subplot(1, 2, 1)
plt.bar(X, Y, color ='maroon', width = 0.4)
plt.xlabel("Links")
plt.ylabel("No. of flits transferred")
plt.title("No. of flits transferred as a function of conections")
plt.subplot(1, 2, 2)
plt.plot(X1, Y1, color ='maroon', marker = 'o')
plt.ylabel('Latency of Packets')
plt.xlabel('Packets sent')
plt.title("Latency as a function of packets sent")
plt.show()

