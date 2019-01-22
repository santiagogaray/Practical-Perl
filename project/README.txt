
Contact Info

============

Name:					Santiago Garay

Email address:			SantiagoGaray@msn.com

Daytime phone number:	(978)443-5839



Physical Location of Running System

===================================

Real location of the *running* project's source code

~public_html/project



URL

===

~public_html/project/chat.htm



Overview

========
Chat: A basic chatting application.
When running the movie you are prompt to log-in or
create a new account (Im using the same 'accounts' table
used for hw5).
Once logged-in you are shown which members are logged by that
time including yourself (as a red point in the black bar).
Once you find other people logged, you can contact them by clicking
over the white point near them. If you are the person that
someone wants make contact to, the following is applicable two.
When someone makes contact, it would appear two windows in both 
members' movies:
The bigger one will show the text being sent by you and the text
received from the member you are connected to.
The smaller window is used to type the text to send. You can enter
as much text as you want and then press the 'Send' button. The person
you are connected to apears as a green point in the black bar.
At every moment you can close the session by clicking the
'Cancel' button.




File Listing

============

chat.cgi	
			Works like a basic server controlling the
			connected people in the chat room.
			Validates their accounts, connects to
			other people, sends messages, updates
			logged people.


chat_movie.dcr	
			The Shockwave movie. A chat interface.

chat.htm	
			the html page displaying the movie.


Also:
-----

chat.exe
			You'll also find a projector version of the movie,
			a stand alone app. that runs in a Windows sytem

chat_movie.dir
			The Director file of the movie where you can
			open and see all the Lingo stuff writen.

Temporary files
			Some temporary files are created in the
			~public_html/project/data subdirectory. 




Database Description

====================

I used the 'accounts' database used for hw5. Only
the Username, Password and id are used for log-in
and checking purposes.



Notes

======

This project lacks some security work and finish work. 
It's still quite slowly in the text sending and receiving process.
I did't want to speed up this process since I did't consider the
case where two users access, at the same time, the temporary 
files. 
Whould be good to offer other features such as chat session saving
and retrieving, multiuser sessions, etc.
Things to consider in the future.

