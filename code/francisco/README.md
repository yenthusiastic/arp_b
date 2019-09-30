*NodeJS Dummy Server*
-----------------------

The purpose of this server is for testing HTTP request from a NodeJS server hosted in the JupyterLab.

You can test the server locally or in your favorite cloud solution. Please, follow the next steps to run the test.

Install NodeJS on your local or remote equipment. In this case I used ubuntu 18.04, and installed through the terminal using the following command:


>$ sudo apt-get install nodejs

Once it is done, confirm that NodeJS is install by running the next command:

>$ node -v

The previous command should have output the version of NodeJs that you have installed. Then, run the following command to test the dummy server:

>$ node dummyserver.js

Now you should be able to see in the terminal "Listening port 5100". Go to your browser and insert the URL http://127.0.0.1:5100 and press enter. Now you should see the index.html page that is storage in this folder. If you are testing this from a remote server, please use the "server address" shown in the terminal.
