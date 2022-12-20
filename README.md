# CA-Project Cycle Accurate Simulator for an NoC Router and Mesh

Group number 6  
Rahul Sehgal | 2020248  
Sahas Marwah | 2020237  
Sparsh Mehrotra | 2020232  
Yash Thakran | 2020269


## Structure of the Simulator

We have made a simple NOC router and followed a 2x2 mesh architecture.   
The mesh has 4 blocks named A, B, C and D.  For our implementation, we have made connections like:  
A -- B  
| &nbsp; &nbsp; &nbsp; |  
D -- C 

We have provided 2 types of ```Routing Algorithms```  
1. XY Routing prioritizes horizontal movement over vertical movement.
2. YX Routing prioritizes horizontal movement over vertical movement.

```Packet``` is the basic unit of transfer in NOC which is broken down into 5 parts:
1. Head Flit: contains the control information, the source and the destination.
2. Data Flit 1
3. Data Flit 2
4. Data Flit 3
5. Tail Flit: indicates the end of the packet.

The ```Crossbar``` and the ```Switch Allocator``` is made using python code and integrated into the mesh.


## Working of the Simulator

Our simulator takes an ```input traffic file``` which describes which packets are inserted in the NOC at various clock cycles. The structure of the input file is:
1. Cycle Number (1 bit)
2. Source Processor (1 bit)
3. Destination Processor (1 bit)
4. Payload: Data flit 1 + flit 2 + flit 3 (96 bits)

The ```Data Flits``` payload is a binary input of length 96.
Each data flit contains data of 32 bits. 

With this input file, we also take the user input to choose the type of routing algorithm XY or YX.

The simulator outputs a ```log file``` which indicates:
1. The Cycle Number
2. Type of Flit
3. Source of the Flit
4. Destination of the Flit


## The Usage of your Graph Plotter
Through the log file we plot two graphs.
1. A bar graph which plots the number of flits sent over a connection. 
2. A bar graph showing the packet transfer latency for each packet.

The first graph keeps a check of the numberof flits that pass through a given connection and plots them.

The second graph depicts the number of clock cycles a given flit takes to go from the source to destination.

## The Building and Usage Instructions
We run the file by the following command in terminal:

    python <insert name of main file>.py

After this it would take input from the ```input.txt``` file that we had provided and two user inputs:

    How many clock cycles do you want to simulate?

and

    What routing algo to implement? Type 1 for XY and 2 for YX "

After taking the inputs, the file runs and generates the log file. 
Through the log file, we make the two graphs.
