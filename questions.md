## Answer Sheet: Lab09

**Question 1:** What is the purpose of the `@app.route('/health')` decorator in the code?

**Answer:**

The purpose is to allow the user to run a health_check() function and return the response when they visit the /health URL. It lets external systems verify that the app is responsive and running correctly.

----------------
**Question 2:** In Jinja2, what is the difference between `{{ my_variable }}` and `{% for item in my_list %}`?

**Answer:**

`{{ my_variable }}` - Prints the value of a variable passed from Python to the template.

`{% for item in my_list %}` - Runs loop logic, repeating content for each item in a list.

----------------
**Question 3:** In `app.py`, why is it important to use `(?, ?)` and pass the variables as a tuple in the `conn.execute()` command instead of using f-strings to put the variables directly into the SQL string? What is this technique called?

**Answer:**

We avoid f-strings to prevent SQL injection attacks, and use (?,?) and tuples instead to keep the SQL and data seperate, which is much safer. 
The technique is called Paramterized Queries

----------------
**Question 4:** What is the purpose of `event.preventDefault()` in the JavaScript code? What would happen if you removed that line?

**Answer:**

With `event.preventDefault()`, the pages doesnt reload, and can use AJAX/API calls, with smoother UX. 
If you removed the line, the full pagr would reload and forms submits the old way with unconventional refreshing. 


----------------
**Question 5:** In the `Dockerfile`, why is the `CMD` `["flask", "run", "--host=0.0.0.0"]` necessary? Why wouldn't the default `flask run` (which uses host 127.0.0.1) work?

**Answer:**




----------------
**Question 6:** In the `docker-compose.yml` setup, Nginx is configured to `proxy_pass http://flask-app:5000`. How does the Nginx container know the IP address of the `flask-app` container?

**Answer:**



