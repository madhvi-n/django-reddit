# Django Reddit
A Reddit clone using Django and Angular

### Features

- User authentication.
- User can create stand alone posts and group posts.
- User can follow people, posts.
- Thread discussions on posts
- Upvote and downvotes on posts and comments
- Report posts
- Bookmark posts
- User can join groups, create groups which can be private, restricted or public.
- Invites and member joining requests for groups


![Django Reddit Sign In Page](screenshots/image01.png?raw=true "Django Reddit Sign In")

![Django Reddit Feed](screenshots/image02.png?raw=true "Django Reddit Feed")

# Requirements
- Backend
    - Python 3.8+
    - virtualenv
    - WSL


- Frontend
    - Angular 10.2.4 (or 10.2.5)
    - Node 10.13.x +



# Installation

Clone the repository and enter the root directory
```
git clone https://github.com/madhvi-n/django-reddit.git
cd django-reddit
```


Create a virtual environment and activate it
```
virtualenv venv
source venv/bin/activate
```

Making sure your virtual environment is activated, install the dependencies using `pip`
```
pip install -r requirements.txt
```

You can set the secret key for django project in 2 ways
- Edit the `reddit_clone/settings.py` file and add a key manually, some random string.
- Edit the venv file to export `SECRET_KEY`


After installing dependencies, migrate Django apps.(You will find the list of apps when you run the command `python manage.py runserver`)
```
python manage.py migrate
```

Finally start your Django server
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` or `localhost:8000` for running web server
Alternatively you can access the admin interface on `http://127.0.0.1:8000/admin/` or `localhost:8000/admin`

Access python shell
```
python manage.py shell
```


### Generating data using shell
```
from django.contrib.auth.models import User
from posts.models import Post
from groups.models import Group

user = User.objects.get(id=1)
post = Post.objects.create(title="Something here", content="A very long text as the content here", author=user)

group = Group.objects.create(name="Django", description="Official Django community on Django Reddit")

```

### Generating dummy data using management commands

```
python manage.py populate_users
python manage.py populate_posts
python.manage.py populate_tags
python.manage.py populate_groups
```


### Frontend

Start another shell tab and access the root of frontend directory `reddit-app` (without bash or activated virtual environment). <br>
Install the angular dependencies
```
npm install
```

<br>

Visit `http://127.0.0.1:4200` or `localhost:4200` to access frontend.


#### Note: Django/Backend runs on WSL and Angular/Frontend runs directly on Windows


## References

- [How to install Python3.8 on Ubuntu 18.04](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
- [Installing NodeJs on Windows](https://www.guru99.com/download-install-node-js.html)
- [Official Angular 10 installation guide](https://v10.angular.io/guide/setup-local)
- [Installing a specific version of ng cli or packages](https://stackoverflow.com/questions/44759621/install-specific-version-of-ng-cli)
- [Compatibility list for Angular, Angular Cli and Node Js](https://stackoverflow.com/questions/60248452/is-there-a-compatibility-list-for-angular-angular-cli-and-node-js)
