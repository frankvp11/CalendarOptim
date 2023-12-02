
Currently Accomplished:
1) Logging users in and out
2) Adding a task to a user's schedule (with only themself). Also made it so that you can choose which tasks you want to see placed in your calendar as sort of a test, so that you know what tasks to add. Basically, select the tasks you want to see on your calendar, automatically selected as True.
3) Made it so that tasks could be shared amongst users. You can have multiple users sharing a single task, which is also optimized with the determineBestTime function that I created. 
4) I created the backend which determines the best time to create a task
5) The backend consists of multiple databases, which control the user's notifications, events, and stats (wip). I also have a database which controls the shared tasks - aka TaskStatus's. 
6) I created multiple pages / UI's that can be used to see your calendar. There is one main page for viewing your calendar. There is one that can be access when you want to see how your* task looks when you add it, and there is one in the notification page when you want to see what an invitation would look like in your calendar. 


To Do:
1) Make it show some graphs for the tasks completed - that could be quite interesting.
2) Make an agent - this should use the join link thing in the database and update the database. We should have 1 year worth of data -> 6 months previous and 6 months in advance
3) Make it so that the user can click on the events
4) Make a video for this app so far



To Do (specific):

1) Add Tasks
    1. Look into the time stuff and make sure it all adds up
    2. Look further into the algorithm - it should be +2 days (in the morning)

2) Stats
    1. Make a graph that can show you have many stats you've done every day (along with a database for this)
    2. Add a way to track them, and whatnot

3) Agent
    1. Make an agent in the backend that ensures every user always has a year of data, from their given database file
    2. Make an agent that can email a person about updates / notifications

4) Misc.
   1. Make it so that the user can delete from the calendar itself
   2. If the user deletes and there are people shared in that event, make it so that it notifies the other people























