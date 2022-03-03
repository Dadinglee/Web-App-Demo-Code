## Explains how someone who clones the repository can set up and run your project locally (what to install, any extra files to add)
1. `pip3 install Flask python-dotenv requests`
2. Create a `.env` file in the top-level directory and enter the following as its contents: `API_KEY` (tmdb api key) and `DATABASE_URL_ALT` (postgres database url)
3. Run `python3 app.py`


## Detailed description of how implementing your project differed from your expectations during project planning.
1. Was expecting using less time on heroku deployment where the only thing needs to be changed is adding a database and change database url which turns out taking much longer then I expected.
2. Was planning to use the same html template for both Signup and Login page, but results in too much if/else blockes, which in the end I split it into two html templates

## Detailed description of 2+ technical issues and how you solved them 
1. Heroku does not allow me to chagne the DATABASE_URL config var, I tried to drop the database, detach or attach the database to my project. Finally I just setup another config var DATABASE_URL_ALT and changed in code to read through this config var.
2. spliting the file into modular fashion is tricky since circular dependency will be introduced. Both for SqlAlchemy models and flask-login callback overwrites, the solution is taking the idea from flask documentation where app_factory is introduced to hold the high-level instances, and let app.py and other modules to import from the factory.
3. Was having trouble hashing the password and compare the hashed result. I tried to use `bcrypt` lib, and take some ref code from stack overflow, but it always gives me `unicode object needs to be encoded before hash` error, where I did encoded it in code. Turns out I should `pip install py-bcrypt` instead of `pip install bcrypt`.

## Extra
I implemented authentication with password, and saving the password with hash.

