The shopping-assistant project involves developing a robot to help people manage their personal shopping list. Communication was done through voice conversation with the user. For this purpose, the robot used a microphone. 
The robot is able to manage a different list for each person it talks to:
- If a new person is met, the robot asks for his or her name and creates a new shopping list
- If it is not a new user, the robot should recognize the user based on the face or voice
	After recognizing the user's identity, the robot allows the user to:
- Add a new item to the shopping list
- Remove an item from the shopping list
- Show the shopping list
- Empty the shopping list
The shopping list is filled with items that are identified by name and quantity. 
	There are also some environmental restrictions, such as the distance between the user and the robot (should be less than 2 meters), no ambient sounds during the conversation, and only 1 user can talk to the robot at a time.
	Python will be used to code this project, with the ROS package. The robot on which the software was tested is the Pepper robot.
  
  ![image](https://user-images.githubusercontent.com/87570436/200055730-faa3e9a3-f3b4-405b-94bf-cde6bc59c054.png)
Picture: Architecture of the code

For this project ROS (Robot Operating System) was used. It is a set of software libraries and tools that helps build robot applications. 

The applications are designed as unit known as Nodes. In a robot system, sensors, motion controllers or algorithms components can be nodes. Nodes communicate with each other via Topic, Service Invocation or Actions. This communication has publish/subscribe architecture where data produced and published by a node is subscribed by another. The data types used in topic communication are called message.
	The ROS Master provides naming and registration services to the rest of the nodes in the system. His role is to enable individual nodes to locate one another. Once they have located each other, they can communicate.

For this project, it was decided to use RASA. It is an open-source AI for buildings conversational chatbots. It is used to automate the text and voice-based assistants.
RASA has advantages such as:
- Being open-source
- Being flexible: you can add/remove what you want so it fits better to your project
- Learning on its own
RASA works on 3 main elements that are Natural Language Understanding (NLU), Natural Language Generation (NLG) and Dialogue Management. NLU converts text into vectors to identify the intention of the sentence. It is tagging each work with a part of speech (noun, verb, ect) and then regroup them into groups. It first finds the request in the sentence and then extract the entity.
NLG is taking inputs of non-linguistic format and converts it into a human-understandable form.
The Dialogue Management is – as its name suggest – managing the dialogue with the user.

To implement RASA, you need the command “rasa init”; it creates all the files that a RASA project needs. There is the list of the files:
- __init__.py -> empty file that helps python find your actions
- actions.py -> code for the custom actions
- config.yml -> configuration of the NLU and Core models
- credentials.yml -> details for connecting to other devices
- data/nlu.md -> the NLU training data
- data/stories.md -> stories
- domain.yml -> assistant’s domain
- endpoints.yml -> details for connecting to channel
- models/<timestamp>.tar.gz -> initial model

You can define your model configuration by using a pipeline. You can now teach how to respond to your messages (dialogue management) and this part is handled by the Core model. The domain defines the universe where we will be (what input it should expect, actions, how to respond, …). You have 3 things; Intents (things you expect the user to say), Actions (Things the algorithm can do and say) and Responses (response strings for the things the algorithm can say). It’s the Core’s job to choose the right action to execute at each step of the conversation.  Every time you update the domain or the configuration, you must re-train your model.

*******Chatbot*******
In this case the following intents were created:
  •	Greet 
  •	Goodbye 
  •	Introduction
  •	Insert
  •	Remove
  •	Show

Every intents except goodbye could detect 2 kinds of entities: username and product. Entities were saved as slots automatically. 
To manage a conversation with a user, rules had to be written on which the chatbot learned. Rules were used to describe these rules. Below are examples of some of them.

Once an intent is detected, each rule should proceed to perform the appropriate action. Actions used in the program:
•	action_receive_product – custom action; add product to the list of active user
•	action_remove_product – custom action; remove product from the list of active user
•	action_show_basket – custom action; show active user’s basket
•	check_user_existance – custom action; check whether the user has been detected
•	update_user_database – custom action; update database by the username
•	utter_asistant – bot response; ask new user what he/she needs
•	utter_ask_name – bot response; ask user for name
•	utter_goodbye – bot response; say goodbye every time user says goodbye
•	utter_hello – say hello every time user says hello


For each user new list was created. To manage multiple users and multiple lists I created nested dictionary in file dict.py. Nested dictionary has 3 methods: add, remove, show. Below example was presented. Each method has a key argument, which is the user, and a value, which specifies the product. Each product has a quantity. So this is how I create a dictionary within a dictionary. Each user is assigned a dictionary with products and their quantity.

******* Voice identification *******
So far, a chatbot project has been implemented, communicating with the user via keyboard and display. The second part of the project was to extend the project to communicate with the user by voice. The application should recognise not only the message but also the user.
The voice recognition is one of the important parts of this project. When the user is speaking with the robot, the robot should know if it is a new user or not. For this we are using a voice identification.
If the user is not in the data, the robot asks for his or her name and create a new shopping list for this user. But if the user already had a shopping list, then the robot skips this step.
For this, I implemented some classes: CheckUser & UpdateUserDataBase (in actions.py).
For the voice recognition, I implemented an audio package (dialogue_interface.py & dialogue_server.py). Once the robot got the name of the user, it can work properly and do the actions he is told to do.

******* Manage robot voice *******
The basis for allowing the robot to speak is the NAOqi Audio API, which contains many functionalities, but I will focus on ALTextToSpeech module allows the robot to speak. It sends commands to a text-to-speech engine, and authorizes also voice customization. The result of the synthesis is sent to the robot’s loudspeakers.
I used the received work package "pepper_nodes", which contains some of the basic functions and configurations of the robot. The main parameter that had to be set was the IP address of the pepper.
Created a proxy on the text-to-speech module in dialog_interface file which include an chatbot text answer. Then applied, the function say takes as parameter “stringTosay”, that generate robot voice.

******* Testing *******
To conduct the tests, it is possible to used two terminals and command Line Interface delivered by rasa. The command line interface (CLI) gives you easy-to-remember commands for common tasks:  Functions describes below, explaining the behavior of the commands and the parameters you can pass to them.
•	Rasa run action - Starts an action server using the Rasa SDK
•	Rasa shell - Loads your trained model and lets you talk to your assistant on the command line.





