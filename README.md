<h1>The shopping assistant-project</h1>
<p>The shopping-assistant project involves developing a robot to help people manage their personal shopping list. Communication was done through voice conversation with the user. For this purpose, the robot used a microphone. </p>
<p>The robot is able to manage a different list for each person it talks to:
	<ul>
		<li>If a new person is met, the robot asks for his or her name and creates a new shopping list</li>
		<li>If it is not a new user, the robot should recognize the user based on the face or voice</li>
		</ul></p>
<p>After recognizing the user's identity, the robot allows the user to:
	<ul>
		<li>Add a new item to the shopping list</li>
		<li>Remove an item from the shopping list</li>
		<li>Show the shopping list</li>
		<li>Empty the shopping list</li>
		</ul></p>
<p>The shopping list is filled with items that are identified by name and quantity. </p>
<p>There are also some environmental restrictions, such as the distance between the user and the robot (should be less than 2 meters), no ambient sounds during the conversation, and only 1 user can talk to the robot at a time.</p>
<p>Python language is used to code this project, with the ROS package. The robot on which the software was tested is the Pepper robot.</p>
  
<img src='https://user-images.githubusercontent.com/87570436/200055730-faa3e9a3-f3b4-405b-94bf-cde6bc59c054.png'/>
<p>Picture: Architecture of the code</p>

<p>For this project ROS (Robot Operating System) was used. It is a set of software libraries and tools that helps build robot applications. </p>

<p>The applications are designed as unit known as Nodes. In a robot system, sensors, motion controllers or algorithms components can be nodes. Nodes communicate with each other via Topic, Service Invocation or Actions. This communication has publish/subscribe architecture where data produced and published by a node is subscribed by another. The data types used in topic communication are called message.</p>
<p>The ROS Master provides naming and registration services to the rest of the nodes in the system. His role is to enable individual nodes to locate one another. Once they have located each other, they can communicate.</p>

<p>For this project, it was decided to use RASA. It is an open-source AI for buildings conversational chatbots. It is used to automate the text and voice-based assistants.</p>
<p>RASA has advantages such as:
<ul>
	<li>Being open-source</li>
	<li>Being flexible: you can add/remove what you want so it fits better to your project</li>
	<li>Learning on its own</li>
</ul></p>
<p>RASA works on 3 main elements that are Natural Language Understanding (NLU), Natural Language Generation (NLG) and Dialogue Management. NLU converts text into vectors to identify the intention of the sentence. It is tagging each work with a part of speech (noun, verb, ect) and then regroup them into groups. It first finds the request in the sentence and then extract the entity.
NLG is taking inputs of non-linguistic format and converts it into a human-understandable form.
The Dialogue Management is – as its name suggest – managing the dialogue with the user.</p>

<p>To implement RASA, you need the command “rasa init”; it creates all the files that a RASA project needs. There is the list of the files:
	<ul>
		<li>__init__.py -> empty file that helps python find your actions</li>
<li>actions.py -> code for the custom actions</li>
<li>config.yml -> configuration of the NLU and Core models</li>
<li>credentials.yml -> details for connecting to other devices</li>
<li>data/nlu.md -> the NLU training data</li>
<li>data/stories.md -> stories</li>
<li>domain.yml -> assistant’s domain</li>
<li>endpoints.yml -> details for connecting to channel</li>
<li>models/<timestamp>.tar.gz -> initial model</li>
		</ul>
	</p>
<p>You can define your model configuration by using a pipeline. You can now teach how to respond to your messages (dialogue management) and this part is handled by the Core model. The domain defines the universe where we will be (what input it should expect, actions, how to respond, …). You have 3 things; Intents (things you expect the user to say), Actions (Things the algorithm can do and say) and Responses (response strings for the things the algorithm can say). It’s the Core’s job to choose the right action to execute at each step of the conversation.  Every time you update the domain or the configuration, you must re-train your model.</p>

<h2>Chatbot</h2>
<p>In this case the following intents were created:
	<ul>
		<li>Greet 
  <li>Goodbye</li>
  <li>Introduction</li>
  <li>Insert</li>
  <li>Remove</li>
  <li>Show</li>
		</ul>
</p>
<p>Every intents except goodbye could detect 2 kinds of entities: username and product. Entities were saved as slots automatically. 
To manage a conversation with a user, rules had to be written on which the chatbot learned. Rules were used to describe these rules. Below are examples of some of them.</p>

<p>Once an intent is detected, each rule should proceed to perform the appropriate action. Actions used in the program:
	<ul>
<li>action_receive_product – custom action; add product to the list of active user</li>
<li>action_remove_product – custom action; remove product from the list of active user</li>
<li>action_show_basket – custom action; show active user’s basket</li>
<li>check_user_existance – custom action; check whether the user has been detected</li>
<li>update_user_database – custom action; update database by the username</li>
<li>utter_asistant – bot response; ask new user what he/she needs</li>
<li>utter_ask_name – bot response; ask user for name</li>
<li>utter_goodbye – bot response; say goodbye every time user says goodbye</li>
		<li>utter_hello – say hello every time user says hello</li>
		</ul>
</p>

<p>For each user new list was created. To manage multiple users and multiple lists I created nested dictionary in file dict.py. Nested dictionary has 3 methods: add, remove, show. Below example was presented. Each method has a key argument, which is the user, and a value, which specifies the product. Each product has a quantity. So this is how I create a dictionary within a dictionary. Each user is assigned a dictionary with products and their quantity.</p>

<h2>Voice identification</h2>
<p>So far, a chatbot project has been implemented, communicating with the user via keyboard and display. The second part of the project was to extend the project to communicate with the user by voice. The application should recognise not only the message but also the user.</p>
<p>The voice recognition is one of the important parts of this project. When the user is speaking with the robot, the robot should know if it is a new user or not. For this we are using a voice identification.</p>
<p>If the user is not in the data, the robot asks for his or her name and create a new shopping list for this user. But if the user already had a shopping list, then the robot skips this step.</p>
<p>For this, I implemented some classes: CheckUser & UpdateUserDataBase (in actions.py).</p>
p>For the voice recognition, I implemented an audio package (dialogue_interface.py & dialogue_server.py). Once the robot got the name of the user, it can work properly and do the actions he is told to do.</p>

<h2>Manage robot voice</h2>
<p>The basis for allowing the robot to speak is the NAOqi Audio API, which contains many functionalities, but I will focus on ALTextToSpeech module allows the robot to speak. It sends commands to a text-to-speech engine, and authorizes also voice customization. The result of the synthesis is sent to the robot’s loudspeakers.</p>
<p>I used the received work package "pepper_nodes", which contains some of the basic functions and configurations of the robot. The main parameter that had to be set was the IP address of the pepper.</p>
<p>Created a proxy on the text-to-speech module in dialog_interface file which include an chatbot text answer. Then applied, the function say takes as parameter “stringTosay”, that generate robot voice.</p>

<h2>Testing</h2>
<p>To conduct the tests, it is possible to used two terminals and command Line Interface delivered by rasa. The command line interface (CLI) gives you easy-to-remember commands for common tasks:  Functions describes below, explaining the behavior of the commands and the parameters you can pass to them.
	<ul>
		<li>Rasa run action - Starts an action server using the Rasa SDK,</li>
<li>Rasa shell - Loads your trained model and lets you talk to your assistant on the command line.</li>
		</ul>
</p>




