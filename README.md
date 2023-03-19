# channels_app
A private research firm is conducting test on different animal species. 
The researchers send secured data to the server in order to do some ML task on them. 
The communication between the researcher and the server is end-to-end encrypted. 
The firm wants to build a secure system which will let the researcher communicate with the server in the most secure way using sockets. 

 

### Task 

Task is to build a duplex system using WebSocket where backend is written in Django and Channels. 
Please write the client-side code in plain python. 

The client will send an encrypted array of numbers to the server. 

The server will decrypt the array, rearrange it such that every second element becomes greater than its right and left elements. 
Assume that no duplicate elements are present in the array. The server will then send back the updated array to the client. 

The client will decrypt the received array and print it to the terminal. 
