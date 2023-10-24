# FOODCRITIC
#### Video Demo: https://youtu.be/r_ThIDmzJlM
#### Description:
Hi! My name is Thejus and i am from Singapore. I have created a simple webapp called FOODCRITIC that users can use to
keep track of the restaurants they have visited before.

When i run the flask program it goes to the "/" route that rediredts to "/login" route as login is required and thus opens the login page. This page is from the login.html file that i created that has all the specific to the 
form that i created to login. Both username and password have been made required fields. When you click enter i use python to check if the username and password
tallies with the table called users that i created in the SQL database file called uniplanner.db. Once verified, it redirects to the "/" route which is the home.

Inside the homepage, there are several buttons on top respectively the "Home", "Ask", "Search" and "Log Off" button that using GET method to route to
"/", "/ask", "search" and "/logoff" respectively. In the homepage there is also a "ADD RESTAURANT" button that routes to "/add" via GET. This opens
add.html file that shows a form where user can review the restaurant. It has a few fields but the decription field is purposely left optional user may not 
neccessarily have an explicit opinion about the restaurant. Once you click enter the information is passed back to "/add" via POST which inserts the info
into another table i created called restaurants in uniplanner.db. 

The "Ask" button, when clicked, routes to "/ask" via the GET route that opens up the ask.html file. I imported openai and generated a free api key(limited use)
to create a python function called gpt_ask(question) in helpers.py. Using this i took the users input and sent it as a question to the function. It returned
a list that i sent back to ask.html and used iteration via for loop to print the info.

The "Search" button when clicked, routes to "/search" via the GET route that opens up the search.html file. User can input the name or cusine of the restaurant which is send back
to "/search" route via POST. I use this information and use it in SQL to check if the name or cusines outputs anything. If yes then it is sent back to that search.html file

