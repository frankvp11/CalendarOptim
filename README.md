
Currently Accomplished:
1) Logging users in and out
2) Adding a task to a user's schedule (with only themself). Also made it so that you can choose which tasks you want to see placed in your calendar as sort of a test, so that you know what tasks to add. Basically, select the tasks you want to see on your calendar, automatically selected as True.
3) Made it so that tasks could be shared amongst users. You can have multiple users sharing a single task, which is also optimized with the determineBestTime function that I created. 
4) I created the backend which determines the best time to create a task
5) The backend consists of multiple databases, which control the user's notifications, events, and stats (wip). I also have a database which controls the shared tasks - aka TaskStatus's. 
6) I created multiple pages / UI's that can be used to see your calendar. There is one main page for viewing your calendar. There is one that can be access when you want to see how your* task looks when you add it, and there is one in the notification page when you want to see what an invitation would look like in your calendar. 


To Do:
1) Make the UI prettier (all pages). 
2) Fix the button clicking for Logout and notification - should be like the sidebar
3) Clear junk from the database (possibly just delete all them re-build it)
4) Refactor the code - both front and backend
5) Add some safety catches - specifically for the Notifications database, as it appears when you delete it, all hell breaks loose
6) Make a video for this app so far
