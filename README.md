# KNJIGAKLOPE
## Developed a fully functional recipe website using the Flask framework, which allows users to discover various recipes or create and store their own recipes. The website utilizes the power of Python and its libraries to deliver dynamic and responsive content to the users, while also providing seamless navigation and user-friendly interfaces. The project involved implementing various features such as recipe creation, user authentication, and other.
## How To Use App
### To use this code, you also need to have the following installed on your machine:

1. Python
2. Flask
3. sqlite3.db
## Technical Specifications
The primary objective of this website was to create a user-friendly page that can serve as an everyday helper. The UI was designed to be modern, while the functionality was optimized for maximum ease-of-use, which was the primary focus of the project.

#### Description:
THIS IS KNJIGAKLOPE
I had an idea to create a webpage for recipes because I spent a lot of time contemplating what to eat and whether or not it's healthy, as well as searching for a place to store my recipes. As a result, I created an "index.html" file, which serves as the landing page and provides an overview of what the page offers, as well as options to register or log in for registered users.

Upon logging in, users are directed to their own dashboard, where the page offers a selection of recipes (which can be updated with new recipes weekly), with filters for breakfast, lunch, and dinner. If a user wishes to learn more about a specific recipe, they can click on a button to be directed to the "blog.html" page, which provides detailed information and a picture about that recipe.

I also created a "my-recipes.html" page that lists all of the user-submitted recipes with a "read more" option, and a "submit.html" option, where users can submit their recipes and have them stored in one place. All pages and fields are connected and all data comes from the "recipe.db", so when new recipes are inserted, they are automatically added to the "recipe.db".

Creating a webpage with a modern design was a one-off to priorities for me. I knew that in order to attract a lot of users and make the page enjoyable to use, it had to look appealing and professional. I spent a considerable amount of time researching the latest web design trends and techniques, as well as user experience principles, in order to create a design that is both visually appealing and user-friendly.

The "401. html" and "404.html" - This pages serves as a friendly and informative message to users who have encountered a broken link or an unavailable page, letting them know that the page they were looking for cannot be found. With a well-designed 404 page, you can help to improve user experience and reduce frustration by offering alternative paths for users to follow or suggestions for resolving the issue. A clear and concise message, coupled with easy-to-use navigation options, can make all the difference in keeping users engaged and satisfied with your website.

The "bfast.html", "din.html", and "laun.html" are used as a filters on the /mydash page.

app.py:
The homepage() function defines the behavior of the homepage. It simply renders an HTML template called index.html.

The login() function defines the behavior of the login page. If the request method is POST, it first checks if the user has entered their email and password. If not, it displays an error message. If the email and password are entered, it checks if the email exists in the SQLite database and if the password matches the hashed password stored in the database. If everything is valid, it adds the user's ID to the Flask session and redirects to the 'mydash' function.

The register() function defines the behavior of the registration page. If the request method is POST, it first checks if the user has entered their first name, email, password, and confirmation password. If not, it displays an error message. If all the fields are entered, it checks if the first name contains only letters, the email is valid, and the password and confirmation password match. If any of these conditions fail, it displays an error message. If everything is valid, it checks if the email is already in the SQLite database. If not, it generates a hashed password and inserts the new user into the database. Finally, it adds the user's ID to the Flask session and redirects to the 'mydash' function.

The route, /mydash, displays the user's dashboard page. This page shows the user's weekly recipes list, which is a list of recipes they plan to make in the current week. The user's name is displayed on this page as well. If the user submits a POST request to this route, the mydashboard.html page is displayed.

The route, /favorites, displays the user's favorites page. This page shows the user's favorite recipes, which are stored in the database. The user's name is displayed on this page as well. To access this page, the user must be logged in.

The route, /submit, displays the submit recipe page. This page allows the user to submit a new recipe to the database. The user's name is displayed on this page as well. If the user submits a POST request to this route, the form data is added to the database, and the extend-dash.html page is displayed with the details of the new recipe that was just added.

The  "/breakfast" route is which when accessed, renders a template that displays a list of recipes filtered by the type of "Breakfast". The list is obtained by iterating through a pre-defined list called "list_of_rec" and selecting only those recipes with the "Breakfast" type.

The "/launch" route is which displays recipes filtered by "Launch" type in a similar manner as the "/breakfast" route.

The "/dinner" route is which displays recipes filtered by "Dinner" type in a similar manner as the "/breakfast" and "/launch" routes.

 @app.route("/blog/<>"), is decorated with @login_required which means that the user needs to be authenticated to access the content of the page. The route takes an integer parameter num which is used to query a database table named blog. The query fetches a single row from the blog table where the id field matches the input id+1 value. The fetched row's name, image, description, ingridients, and type fields are stored in separate variables to be passed to the render_template function, which is responsible for rendering an HTML template named blog.html with these variables as arguments. Finally, the user's firstname value is fetched from the users table and also passed as an argument to the render_template function.

 @app.route("/myrecipes"), is also decorated with @login_required which means that the user needs to be authenticated to access the content of the page. This route fetches the user's firstname value from the users table and all rows from the recipes table where the user_id matches the user's id value. These values are then passed to the render_template function along with the my-recipes.html HTML template as arguments.

@app.route("/myrec/"), is also decorated with @login_required which means that the user needs to be authenticated to access the content of the page. This route takes an integer parameter num which is used to query a database table named recipes. The query fetches a single row from the recipes table where the id and user_id fields match the input id+1 and the user's id value, respectively. The fetched row's name, image, description, ingridients, and instructions fields are stored in separate variables to be passed to the render_template function, which is responsible for rendering an HTML template named myrec.html with these variables as arguments. Finally, the user's firstname value is fetched from the users table and also passed as an argument to the render_template function.

All these routes have the "@app.route" decorator, which maps the URL to the function that should handle the request. They also have the "@login_required" decorator, which ensures that only authenticated users can access the routes. Finally, these routes extract the user's first name from the database and pass it to the template, along with the list of filtered recipes and other relevant variables.

recipe.db:

The users table has four columns: id, firstname, email, and hash. The id column is an integer type and is defined as the primary key with the AUTOINCREMENT keyword, which means that its value will be automatically incremented for each new record inserted into the table. The firstname and email columns are of the TEXT data type and are defined as NOT NULL, which means that these columns cannot be left empty. The hash column is also of the TEXT data type and is defined as NOT NULL, which means that this column cannot be left empty either. The users table is most likely used to store user information such as name, email, and password hashes for authentication purposes.

The blog table has six columns: id, name, type, image, description, and ingridients. The id column is an integer type and is defined as the primary key with the AUTOINCREMENT keyword. The name, type, image, description, and ingridients columns are all of the TEXT data type and are defined as NOT NULL, which means that these columns cannot be left empty. The blog table is most likely used to store blog posts where each row represents a single blog post.

The recipes table has seven columns: id, name, image, description, ingridients, instructions, and user_id. The id column is an integer type and is defined as the primary key with the AUTOINCREMENT keyword. The name, image, description, ingridients, and instructions columns are all of the TEXT data type and can be left empty. The user_id column is also an integer type and is used to store the id of the user who created the recipe. The recipes table is most likely used to store user-created recipes where each row represents a single recipe.

## Contact
Any information, bugs or questions can be sent on the e-mail adress: adzamija@icloud.com


