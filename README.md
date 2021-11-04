## Social Django REST API
An app mimicking a social media REST API with basic CRUD endpoints.
### Prerequisites
1. Python 3.8 +
2. Pip 20.5+
3. PostgresDB 9.6 +
4. API keys from Abstract API for the holiday and geolocation

### Getting started
1. Clone this repo
```bash
git clone <repo>
```

2. Check into the repo and install the requirements:

```bash
cd <repo> && python3 -m venv venv && pip install -r requirements.txt
```

3. Create a `.env` file at the root of the project directory using the `.env.sample` file at the root of the project directory and export it:

```bash
source .env && source venv/bin/activate
```
4. Run the tests:

```bash
python3 manage.py test
```
5. Run the migrations:
```bash
python manage.py makemigrations && python manage.py migrate
```
6. Run the app:
```bash
python manage.py runserver
```

### APIs used
1. Abstract Holiday API - For Holiday data enrichment
2. Abstract Geolocation API - For geolocation data enrichment

### Endpoints
1. POST `/auth/login` - the login endpoint
2. POST `/auth/signup` - the signup endpoint
3. POST `/auth/profile` - the profile endpoint for viewing present user profile
4. GET `/posts/list` - the list of all posts by users
5. GET `/posts/<str:post_id>` - to view a single post by id
6. PATCH `/posts/<str:post_id>` - update a post by id
7. DELETE `/posts/<str:post_id>` - Delete a post by id
8. POST `/post/<str:post_id>/like` - like a post
9. POST `/post/<str:post_id>/dislike` - dislike a post

Apart from the `/auth/signup` and `/auth/login` endpoints, all others are protected endpoints. This means you need a JWT token to access them.
You can get the token by logging into the app using the `/auth/login` endpoint. Pass the token under the authorization headers prefixed with the word: `Token` e.g `Token exjjbjbjsbdasdasdassdewfrfe`

### Pending requirements
1. Due to pressing time requirements, I could not set up the CI pipeline.

## Tech choices
1. Used Tenacity(https://tenacity.readthedocs.io/) for retries. Used it because of the simplicity of its API. 
2. Postgres - the most popular open-source SQL server. Chose this because it integrates pretty easily with Django and due to its present popularity. Lots of issues that arise in development have been met and solved too.
