from input import list_of_instructions
    
class Link:
    input = False
    output = False
    busy = False
    
class Input:
    source = ""
    destination = ""
    head = ""
    f1 = ""
    f2 = ""
    f3 = ""
    tail = ""
    sucess = False
    path =  []
    def __init__(self, instuctions):
        self.source = instuctions[0][-2]
        self.destination = instuctions[0][-1]
        self.head = instuctions[0]
        self.f1 = instuctions[1]
        self.f2 = instuctions[2]
        self.f3 = instuctions[3]
        self.tail = instuctions[4]
        self.get_path()
    
    def get_path(self):
        #path according to the routing algo: Midsem = XY
        self.source == '1' and self.destination == '2'
        return
        
    
class NoC:
    trafic1 = []
    trafic2 = []
    trafic3 = []
    trafic4 = []
    l1 = Link()
    l2 = Link()
    l3 = Link()
    l4 = Link()
    def __init__(self, p):
        self.p = p
    def add_intruction(self, intructions):
        input = Input(intructions)
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
        if self.trafic1[0].clock_cycle == clock_cycle:
            list.append(self.trafic1[0])
            self.trafic1.pop(0)
        if self.trafic2[0].clock_cycle == clock_cycle:
            list.append(self.trafic2[0])
            self.trafic2.pop(0)
        if self.trafic3[0].clock_cycle == clock_cycle:
            list.append(self.trafic3[0])
            self.trafic3.pop(0)
        if self.trafic3[0].clock_cycle == clock_cycle:
            list.append(self.trafic4[0])
            self.trafic4.pop(0)
        return list


    
    def play(self):
        total_tic = int(input("How many clock cycles do you want to simulate? "))
        queue = [] #add input objects to this queue
        for clock_cycle in range(total_tic):
            if len(self.check(clock_cycle)) > 0:
                queue.append(i for i in self.check(clock_cycle))
            
            for i in queue:
                get_path = i.get_path()
                for path in get_path:
                    pass
                    #check if the link is busy or free, if free, send the packet
                    
                    # if tail is sent then i.sucess = True
                    
                if i.success:
                    queue.remove(i)
        
        for i in queue:
            get_path = i.get_path()
            for path in get_path:
                pass
                    #check if the link is busy or free, if free, send the packet
                    
            if i.success:
                queue.remove(i)
                
                
            


class Router:
    input = ""
    output = ""
    
    