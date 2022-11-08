from dis import Instruction
from input import list_of_instructions


class Link:
    input = False
    output = False
    busy = False

class Router:
    head = ""
    f1 = ""
    f2 = ""
    f3 = ""
    tail = ""
    def __init__(self,x):
        self.x = x
    def get_head(self,head):
        self.head = head
    def get_f1(self,f1):
        self.f1 = f1
    def get_f2(self,f2):
        self.f2 = f2
    def get_f3(self,f3):
        self.f3 = f3
    def get_tail(self,tail):
        self.tail = tail



class Input:
    clock_cycle = 0
    head_sent = False
    source = ""
    destination = ""
    head = ""
    f1 = ""
    f2 = ""
    f3 = ""
    tail = ""
    sucess = False
    path =  []
    def __init__(self, instuction):
        self.clock_cycle = instuction[0]
        self.source = instuction[1]
        self.destination = instuction[2]
        self.head = "0000000000000000000000000000"+self.source+self.destination
        self.f1 = instuction[3][0:31]
        self.f2 = instuction[3][31:63]
        self.f3 = instuction[3][63:96]
        self.tail = "0000000000000000000000000000"
        self.path =  []
        self.get_path()
    
    def get_path(self):
        #path according to the routing algo: Midsem = XY
        if self.source==self.destination:
            return
        if self.source == "1":

            if self.destination == "2":
                self.path.append("1")
                self.path.append("2")

            if self.destination == "3":
                self.path.append("1")
                self.path.append("2")
                self.path.append("3")

            if self.destination == "4":
                self.path.append("1")
                self.path.append("4")


        if self.source == "2":

            if self.destination == "1":
                self.path.append("2")
                self.path.append("1")

            if self.destination == "3":
                self.path.append("2")
                self.path.append("3")

            if self.destination == "4":
                self.path.append("2")
                self.path.append("1")
                self.path.append("4")

        if self.source == "3":

            if self.destination == "1":
                self.path.append("3")
                self.path.append("4")
                self.path.append("1")

            if self.destination == "2":
                self.path.append("3")
                self.path.append("2")

            if self.destination == "4":
                self.path.append("3")
                self.path.append("4")

        if self.source == "4":

            if self.destination == "1":
                self.path.append("4")
                self.path.append("1")

            if self.destination == "2":
                self.path.append("4")
                self.path.append("3")
                self.path.append("2")

            if self.destination == "3":
                self.path.append("4")
                self.path.append("3")

        return

def print_list(list):
    for i in list:
        print("Source:",i.source,"Destination:",i.destination)

def Print(list):
    for i in list:
        # print(i)
        print(i)

class NoC:
    trafic1 = []
    trafic2 = []
    trafic3 = []
    trafic4 = []
    l1 = Link()
    l2 = Link()
    l3 = Link()
    l4 = Link()
    router = Router(1)
    def __init__(self, p):
        self.p = p
    def add_intruction(self, intructions):
        for x in intructions:
            x = list(map(str,x.split()))
            input = Input(x)

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
            
    def perform(self):
        
        return 
        
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
        p = 0
        c = 0
        for clock_cycle in range(total_tic):
            x = self.check(clock_cycle)
            if len(x) > 0:
                for i in x:
                    queue.append(i)

            print_list(queue)
            print("")
            for i in queue:
                if i.head_sent==False:
                    get_path = i.path
                    # count = 0
                    for path in get_path:
                        if(path=="1" and self.l1.busy==False):
                            self.l1.busy = True
                            

                        if(path=="2" and self.l2.busy==False):
                            self.l2.busy = True
                            

                        if(path=="3" and self.l3.busy==False):
                            self.l3.busy = True
                            

                        if(path=="4" and self.l4.busy==False):
                            self.l4.busy = True
                            

                    
                    print(i.source,i.destination)
                    self.router.get_head(i.head)
                    i.head_sent = True
                    break
                        

                else:
                    if(c==0):
                        self.router.get_f1(i.f1)
                        c += 1
                        break

                    if(c==1):
                        self.router.get_f2(i.f2)
                        c += 1
                        break

                    if(c==2):
                        self.router.get_f3(i.f3)
                        c += 1
                        break

                    if(c==3):
                        i.sucess = True
                        self.router.get_tail(i.tail)
                        print("GOT IT", i.source, i.destination)
                        self.l1.busy = False
                        self.l2.busy = False
                        self.l3.busy = False
                        self.l4.busy = False
                        c = 0
                        

        #             #check if the link is busy or free, if free, send the packet
                    
        #             # if tail is sent then i.sucess = True
                    
                if i.sucess:
                    queue.remove(i)

                
        
        # for i in queue:
        #     get_path = i.get_path()
        #     for path in get_path:
        #         pass
        #             #check if the link is busy or free, if free, send the packet
                    
        #     if i.success:
        #         queue.remove(i)
n = NoC(1)
n.add_intruction(list_of_instructions)
# Print(n.trafic1)
# print("")
# Print(n.trafic2)
# print("")
# Print(n.trafic3)
# print("")
# Print(n.trafic4)

n.play()
