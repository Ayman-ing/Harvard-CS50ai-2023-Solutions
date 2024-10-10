started by a just two layers , input layer 
and ouptut layer , by learning 32 filters 
using a 3*3 kernel , a max-pooling of size(2,2)
i got an accuracy of 0.9298 and a loss of 0.6252

then I added a hidden layer of 128 without 
dropout Igot accuracy 0.8885 and loss 0.7725 ,
so it was worse , that's why  I thought about 
adding a dropout of 0.5 to prevent overfitting ,
but it didn't go as I expected , accuracy was
0.0562 and loss 3.5041
I tried adding hidden layers with dropout but 
it was always a bad accuracy , so i eliminated 
the dropout 

i played around with number of hidden layers 
and number of units in each but it wasn't there 
a great improvement compared to the additional
time of execution added. so i removed all the 
hidden layers as they were not helping 

doubling the filters from 32 to 64, changing
the kernel dimensions and different pool size 
weren't helpful also 


adding convulation layers and pooling layers has
speeded up the process but the accuracy was down

deleting the pooling layer has made the time of execution 
higher without additional accuracy compared to 
the first test ,so i restored it and even with 
a size of (4,4)

the best experience was with a hidden layer of 
480 units and a dropout of 1/3 , but it takes 
14s for each epoch 
i kept it like that 