from input import list_of_instructions
outfile = open('log.txt', 'w')

class Link:
    input = False
    output = False
    busy = False

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
    
    def get_path(self):
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
    
    r1 = Router()
    r2 = Router()
    r3 = Router()
    r4 = Router()
    
    
    def __init__(self, p):
        self.p = p
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


    
    def play(self):
        total_tic = int(input("How many clock cycles do you want to simulate? "))
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
                get_path = instruction.get_path()
                # print(get_path)
                #print("Clock Cycle: ",clock_cycle,"Source: ", instruction.source ,instruction.head_sent, instruction.tail_next)
                if instruction.head_sent < len(get_path):  
                    if get_path[instruction.head_sent] == "1":
                        self.r1.update(instruction,clock_cycle,  "Head")
                    elif get_path[instruction.head_sent] == "2":
                        self.r2.update(instruction, clock_cycle,  "Head")
                    elif get_path[instruction.head_sent] == "3":
                        self.r3.update(instruction, clock_cycle, "Head")
                    elif get_path[instruction.head_sent] == "4":
                        self.r4.update(instruction, clock_cycle, "Head")
                    
                    instruction.head_sent += 1
                    
                    if instruction.head_sent == len(get_path):
                        instruction.head_sent = 3
                        instruction.counter = 0


                elif instruction.head_sent == 3 and instruction.tail_next == -1:
                    if instruction.counter // len(get_path) == 0:
                            if(get_path[instruction.counter % len(get_path)] == "1"):
                                self.r1.update(instruction, clock_cycle, "flit 1")
                            if(get_path[instruction.counter % len(get_path)] == "2"):
                                self.r2.update(instruction, clock_cycle, "flit 1")
                            if(get_path[instruction.counter % len(get_path)] == "3"):
                                self.r3.update(instruction, clock_cycle, "flit 1")
                            if(get_path[instruction.counter % len(get_path)] == "4"):
                                self.r4.update(instruction, clock_cycle, "flit 1")
                    if instruction.counter // len(get_path) == 1:
                            if(get_path[instruction.counter % len(get_path)] == "1"):
                                self.r1.update(instruction, clock_cycle, "flit 2")
                            if(get_path[instruction.counter % len(get_path)] == "2"):
                                self.r2.update(instruction, clock_cycle, "flit 2")
                            if(get_path[instruction.counter % len(get_path)] == "3"):
                                self.r3.update(instruction, clock_cycle, "flit 2")
                            if(get_path[instruction.counter % len(get_path)] == "4"):
                                self.r4.update(instruction, clock_cycle, "flit 2")
                    if instruction.counter // len(get_path) == 2:
                            if(get_path[instruction.counter % len(get_path)] == "1"):
                                self.r1.update(instruction, clock_cycle, "flit 3")
                            if(get_path[instruction.counter % len(get_path)] == "2"):
                                self.r2.update(instruction, clock_cycle, "flit 3")
                            if(get_path[instruction.counter % len(get_path)] == "3"):
                                self.r3.update(instruction, clock_cycle, "flit 3")
                            if(get_path[instruction.counter % len(get_path)] == "4"):
                                self.r4.update(instruction, clock_cycle, "flit 3")
                    instruction.counter += 1
                    
                    if instruction.counter == 3*(len(get_path)):
                        instruction.tail_next = 0
                        instruction.counter = 7
                
                elif instruction.tail_next >=0 and instruction.tail_next < len(get_path):
                    if get_path[instruction.tail_next] == "1":
                        self.r1.update(instruction, clock_cycle, "Tail")
                    elif get_path[instruction.tail_next] == "2":
                        self.r2.update(instruction, clock_cycle, "Tail")
                    elif get_path[instruction.tail_next] == "3":
                        self.r3.update(instruction, clock_cycle, "Tail")
                    elif get_path[instruction.tail_next] == "4":
                        self.r4.update(instruction, clock_cycle, "Tail")
                    
                    instruction.tail_next += 1
                    
                    if instruction.tail_next == len(get_path):
                        queue_temp.remove(instruction)
                        
                
            
n = NoC(1)
n.add_intruction(list_of_instructions)

n.play()