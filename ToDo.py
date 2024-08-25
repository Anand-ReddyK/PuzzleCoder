"""
TODO: Create a Inttialize DB or Migrate Db file to create the necessary indexes
TODO: Create a form that takes the structure of the problem
//TODO: Add a difficulty field to the problems
TODO: Create a custom session expirey system to periodically remove the expired sessions
//TODO: Make the code editor window in problem_detail page to behave like a code editor.
//TODO: Disable the Run code and Submit code buttons in the frontend while request is processing

! Add collections:
    //TODO: User
    //TODO: User data(which store the code user submitted code and there problems statuses)
        * add a "submitted" field (if run code: submitted = false else if submit code: submitted = true)
        * the "status" field should be
            - 'null' if not attempted or opened the problem
            - 'In progress' if run code is pressed
            - 'Success' if all test cases passed
            - 'partial executed' if some test cases passed
            - 'failed' if no test cases passed
    //TODO: Sessions (To track users)
//TODO: Connect these above collections to get the user data

! Code Execution
//TODO: Save the code sent by the user in db under the user id and problem id in a user data collection 
//TODO: Send the code received from the frontend to redis queue
    * Run redis as a container and expose ports to access the redis queue and pub/sub
//TODO: Let the docker worker containers pick up these tasks
    ? How to let multiple containers interact with the queue
//TODO: Let the containers run the code with give language and test cases
used redis set and get method instead of pub/sub
//TODO: The container will post the results in a pub/sub system
//TODO: we will sub to the pub/sub with user id or name and send the results to the frountend.

! Efficiency
TODO: Insted of storing the whole code submitted by the use, we could implement what git when the content of a file is changed and only store that data
TODO: Keep a time limit for the code to be runned, this will also help in eliminating problems with infinite loops etc.
TODO: Store the problems page details int he client side cache so we don't have to request from the database every time
"""