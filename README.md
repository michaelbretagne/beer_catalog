#Beer Catalog

This application was created as my submission for Project 5 of Udacity's Full Stack NanoDegree program.

##Project Description: 

In this project, I developed a web application that provides a list of beer within a variety of categories and integrates third party user registration and authentication. Authenticated users have the ability to post, edit, and delete their own items.

##Prerequisites:

**Git:** https://git-scm.com/downloads<br>
**Virtual Box:** https://www.virtualbox.org/wiki/Downloads<br>
**Vagrant:** https://www.vagrantup.com/downloads.html<br>

##Installation Steps:

1. Using Git, run: git clone **http://github.com/udacity/fullstack-nanodegree-vm**<br>
*This will create a new directory named fullstack*<br>
2. Move to the vagrant folder by entering: cd fullstack/vagrant/<br>
3. Clone the project: **https://github.com/michaelbretagne/beer_catalog.git**<br>
*This will create a directory inside the vagrant directory named tournament*<br>
4. Run Vagrant by entering: vagrant up<br>
5. Log into the Vagrant Machine by entering: vagrant ssh<br>
6. Move to the directory project folder by entering: cd /vagrant/beer_catalog<br>
7. Populate the application by entering: python brewery_populate.py
8. Run the application by entering: python application.py<br>
9. Insert your Client ID & Client Secret into **client_secrets.json** file<br>
  1. Create a new project on **https://console.developers.google.com**<br>
  2. Choose Credentials from the menu on the left<br>
  3. Create an OAuth Client ID<br>
  *You will then be able to get the client ID and client secret*<br>
10. Access and test your application locally by visiting **http://localhost:8000**<br>
11. Feel free to add your favorite beer into our database<br>

##Important:

This is not a commercial website. Some content has been quoted from **https://untappd.com/beer/top_rated**.<br>
I do not take credit for the content nor do I endorse or criticize any products listed. 
