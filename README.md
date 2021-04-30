# Covid19Monitoring

This is a small Python project for Covid19 monitoring. I used Python with Flask, MySql and Plotly library for graphs.

The data used are those present at the following link: https://documenter.getpostman.com/view/10808728/SzS8rjbc

**_The whole project (including DB and tasks) is hosted on PythonAnyWhere at the following link:_ http://alby98.pythonanywhere.com/**

Plotly documentation: https://plotly.com/python/

The project consists of a task (executed once a day with the specific PythonAnyWhere functionality) which retrieves the data via api and inserts them into the database.

The website instead consists of a single web page that allows you to select the data to be displayed, then python retrieves the data present on the db and finally the Plotly library generates the graphs.

# Code
https://github.com/albino98/Covid19Monitoring/tree/main/covid19Monitoring

Note that there is no python virtual env folder in the code repository, so you will need to create one. I used python 3.6.2.

- For the database create a new database named covid19 and import the file covid19.sql in the code folder. The database already contains some data.
- When creating a task on PythonAnyWhere it may not work properly. To solve the problem it may be useful to specify in the command the version of python to use. Here is my task and the link to the documentation: https://help.pythonanywhere.com/pages/ScheduledTasks/
![Screenshot (9)_LI](https://user-images.githubusercontent.com/63566699/115157236-7abaf000-a088-11eb-9e38-890244444ee2.jpg)


# Donations

If you liked the project, offer me a coffee!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U84GRKK)


[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=3JUUFBA5MUU4Q)

![Screenshot (7)](https://user-images.githubusercontent.com/63566699/115144604-dd42ca80-a04d-11eb-9896-1bd9be36c0e1.png)


![Screenshot (5)](https://user-images.githubusercontent.com/63566699/115144610-e6339c00-a04d-11eb-9170-4f72f969ed53.png)


![Screenshot (6)](https://user-images.githubusercontent.com/63566699/115144618-ecc21380-a04d-11eb-9d44-48e73c621242.png)


![Screenshot (8)](https://user-images.githubusercontent.com/63566699/115144640-0e22ff80-a04e-11eb-9c9e-c826c3730110.png)

# License

https://github.com/albino98/Covid19Monitoring/blob/769b9cff4c4f8d0114e73bbbd9a253069326bf6b/LICENSE
