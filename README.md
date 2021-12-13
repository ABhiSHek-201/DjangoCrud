# DjangoCrud

### This is Discourse web application where can join and publish his advertisements. This repository consists of only the backend part of the applicaton. It is made using Django web framework and it performs all the CRUD operations over the user and adveritisements data. Following are the APIs that this application offers:


Request|APIs|function
-------|----|----------
GET| /api/all_user | It will return all the users registered on the application.
POST| /api/register |It will add the user on this application.
POST| /api/login |It can be used for user login into this application with the help of JWT (Json Web Token) Authentication. 
PUT| /api/edit |It can be used to edit user details into this application for the logged in user.
DELETE| /api/delete |It can be used to delete logged in user from this application.
GET| /api/user |It can be used to fetch details of the logged user.
GET| /api/logout |It can be used to logout user from this application.
GET| /advertisements/ | It will return all the published advertisments.
GET| /advertisements/all | It will return all the advertisments that are created by the logged in user (both published and un-published ads).
POST| /advertisements/create | It can be used to create an advertisement by a logged in user. (initially ads are un-published)
GET| /advertisements/view/<int:adv_id> | It will return all the details of an advertisments whose 'id' is mentioned in the url.
PUT| /advertisements/edit/<int:adv_id> | It is used to edit the mentioned advertisement's details. (only the author of the advertisements can edit the advertisement.)
DELETE| /advertisements/delete/<int:adv_id> | It is used to delete the mentioned advertisement's details. (only the author of the advertisements can delete the advertisement.).
PUT| /advertisements/publish/<int:adv_id> | It is used to edit the mentioned advertisement. (only the author of the advertisements can publish the advertisement.).


## Deployed over Heroku. 
#### Check the below link:
https://backend-fsd.herokuapp.com/
