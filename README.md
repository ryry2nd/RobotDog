# RobotDog
its a robot and a dog
## Setup
Import requirements  
`pip install -r requirements.txt`  
  
Run these commands if on linux:  
```
sudo apt install espeak  
sudo apt install flac  
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```
If on windows just run this:  
`python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"`  
  
If you want to you can make a file called targetIp.txt to automatically type in the target ip address of the server.

### GPT4All instructions
For the robot to be able to think for itself you have to download a model from the GPT4All website  
The model I downloaded was `gpt4all-falcon-q4_0.gguf`  

To download a model go down to the Model Explorer section on the GPT4All website: https://gpt4all.io/index.html  
Any model should work but I haven't tested it.  

Be sure to put the file into this path: `Assets/aiModel`  
  
Don't forget to edit the .env file accordingly.
