pip install -r requirements.txt

running API locally on your system after installing requirement.
py manage.py runserver

running on localhost:
    run url on postman: localhost/api or http://127.0.0.1:8000/api

running on live url:
    run url on Postman: https://djangcrud-5lks.onrender.com/api

I added some extra details to person with name
The details of the person are: name, first_name,last_name, username, email, date_of_birth, phone_number and address.
1.  Adding a new person: Bradt Elton (create)=> post https://djangcrud-5lks.onrender.com/api


    ![Alt text](image-17.png)


2.  To get all persons detail on DB(read)=> get https://djangcrud-5lks.onrender.com/api

   ![Alt text](image-16.png)
    



3.  To fetch details of a person(read)=> get https://djangcrud-5lks.onrender.com/api/10
    
    ![Alt text](image-18.png)

4.  Modifying details of an existing person(update)=> put https://djangcrud-5lks.onrender.com/api/10

    To change the new person: Bradt Elton to Bradt Johnson and also address to USA

    ![Alt text](image-19.png)


5.  Removing a person(delete) => delete https://djangcrud-5lks.onrender.com/api/7

    ![Alt text](image-6.png)

validation/error

first_name can not be digit, last_name can not be digit and username can be digit only string
   
    ![Alt text](image-7.png)
   
    ![Alt text](image-8.png)

    ![Alt text](image-9.png)

first_name can not be the same as last_name and also username can be the same as firstname or last_name

    ![Alt text](image-10.png)

    ![Alt text](image-11.png)

email validation error and date of birth validation error handling:

    ![Alt text](image-12.png)

    ![Alt text](image-13.png)



UML diagrams: https://drive.google.com/file/d/1Akm06_tHImRAENyEVZCZflzRL_8kUha7/view?usp=drive_link and https://drive.google.com/file/d/1u2_m5bwO49KjxM8LVVWiEwtXbkoJGxwN/view?usp=drive_link


To run test report:
command: python manage.py test



To display a summary of the code coverage, including which parts of your code were covered and which were not.
command: coverage run manage.py test
command: coverage report
