![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)


<p align="center">
  <img alt="logo" src="https://user-images.githubusercontent.com/63566699/129224789-6198792d-3f76-4582-b09a-9cfab37732b1.png">
</p>



# Covid19Monitoring

This is a small Python project for Covid19 monitoring. I used Python with Flask, MySql and Plotly library for graphs.

The data used are those present at the following link: https://documenter.getpostman.com/view/10808728/SzS8rjbc

**_The whole project (including DB) is hosted on PythonAnyWhere at the following link:_ http://alby98.pythonanywhere.com/**

Plotly documentation: https://plotly.com/python/

The project consists of a database that contains the data to be displayed, a single web page and python that takes care of retrieving the data from the API, inserting them into the database and displaying them in the graphs through the Plotly library.


# Code
https://github.com/albino98/Covid19Monitoring/tree/main/covid19Monitoring

Note that there is no python virtual env folder in the code repository, so you will need to create one. I used python 3.6.2. (https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#env-requirements)

For the database create a new database named covid19 and import the file covid19.sql in the code folder. The database already contains some data.

:warning: **Attention**: the data is not official so it may not always be correct / updated with great precision.


![immagine](https://user-images.githubusercontent.com/63566699/170736279-0cb7ff87-0f5f-45bf-a2c3-96c7a922219d.png)

![immagine](https://user-images.githubusercontent.com/63566699/170736505-7a831402-fd79-455d-8410-531cf98ed397.png)

![immagine](https://user-images.githubusercontent.com/63566699/170736580-6542986a-d40f-4652-bc88-e786e9d04012.png)




# License


License: [APACHE 2.0](https://github.com/albino98/Covid19Monitoring/blob/769b9cff4c4f8d0114e73bbbd9a253069326bf6b/LICENSE)


