# MY TO-DO
#### Video Demo:  https://youtu.be/pNbaI9bxdAA
#### Description:
## Introduction
This is a to-do list web application that is capable to register for a new account, login, logout, and add, view, check, edit and delete tasks.

## Register
The site provide to the user to securely sign up for a new account and use it to login.The register page can be reached trhough, clicking on register button in the navigation bar. The user asked to enter a username, password, and confirmation of this passwored. The site will check the data entry first. If the user does not enter valid data, if the input is blank, or if the username already exists, an error message will be shown to the user.

The register.html file contain a form uses `method="post"` to send the data from this form to a route called "/register" to handle the data from user's input and check for any errors. The route in the first will check for the input one by one and if any is missing it will send an error message to the user. After that if the user entered a username that is already taken it will tell the user about that. And if the user name the register will try to add the username and password to the database. If there was any SQL injections, an error message will be shown. The password will be hashed before it stored. After the user is assigned, he/she will be automaticly logined in and redirected to the index page.

## Login
The site provide to the user to securely login to his/her account. As previous in the register page the user will be asked to enter a username and password. If any left blank or the user entered invalid username, or passwored, an error message will be sent to the user.

The login.html file contain a form uses `method="post"` to  send the data from the form to a route called "/login" to handle the user's input and sign the user in. The route will check for the user's input if it is in the database or not, and if the hashed value of the password is the same as in the database or not. If any is not correct it will render error.html telling the user that the usernmae and/or password is incorrect.

## Log out
A route made to clear the session which will log the user out, and then redirect the user to the login page.

## Index
The index page shows the tasks and provide the abilty to check, edit, and delte them.

The index.html file has a list contains a `for` loop which add a `<li>` for each task the user has in the database. Also, each `<li>` contains 3 forms uses `"methos="post"` to allow the user to check, edit, and delete any task he/she wants to.

The checkbox is maid into a form to let it's value be stored so it can be kept as check even if the user refresh the page, or login later. This is done via a route called "/check_state" which suppor `"POST"` only! and this is to allow the data to be posted directly after the checkbox is clicked. It contains to A hidden button to know the task_id of the checkbox and to handle the fact that the page do not post the value of the non-checked checkboxes.

## Add Task
The add task page can be reached trhough, clicking on "ADD TASK" button in the navigation bar. The page contain a textarea to allow the user to enter the task he/she wants to add, and a button to allow the user to submit the task to the server.

The add.html file contains a form using the `method="post"` to send the data to the server. The `<textarea>` has been used to provide a wide space to let the user as the task freely. The route called "/addtask" handles the user's input and saves the task in a databes, and link it to the user's id and give it a task_id to distinguish each task.

## Edit Task
The edit task is a button redirects the user to a page to edit the task. This page has a textarea that contains the task and the curser is in the end of this text.

The edit.html has `<textarea>` contains the task and the curser is placed at the end of the text using the next javascript code
``` javascript
let input = document.getElementById("text");
        input.focus();
        input.setSelectionRange(input.value.length, input.value.length);
```
To make it possible to receive data via post and render template via get, i had to make a route that checks for the task's id and make sure that task is assigned to that user and save this data in query and send ir to another route that will show the edit page first and after submitting the form it will update the task  in the database then redirect the user to the index page.

## Delete Task
To allow the user to delete a task, a route made to get the task_id, make sure that task is assigned to this user, and the delete the task from the database.

## Databse
This site is connected to a database, that contains two tables. The first table, is made to store the user's username, the hashed password, and to distinguish every user by an id to be used in the data handling. The seconed table, is made to store the tasks, tasks' id , tasks' checked status, and to which user this task is assigned.

## Layout
An layout.html is made to have the repetetive work of html to be done in one file. Also, to follow the DRY principle.

### note:
There is a function called "login_required" is called in all pages and routes to make sure that the user is loged in.

It is called in "/", "/check_state", "/add_task", "/edit", "/edit_task", and "/delete" routes

#### THIS WAS CS50 MY TO-DO
##### made by: Sherif Gamal
