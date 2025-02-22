# Django Reddit

[![Django CI](https://github.com/madhvi-n/django-reddit/actions/workflows/django.yml/badge.svg)](https://github.com/madhvi-n/django-reddit/actions/workflows/django.yml)
[![CodeQL](https://github.com/madhvi-n/django-reddit/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/madhvi-n/django-reddit/actions/workflows/github-code-scanning/codeql)

A **feature-rich Reddit clone** built using **Django** for the backend and **Angular** for the frontend. This project allows users to create, interact, and engage in discussions within communities.

## 🚀 Features

- **User Authentication**: Sign up, log in, and manage accounts securely.
- **Create & Interact with Posts**: Standalone and group-based posts with threaded discussions.
- **Community Features**: Users can create and join groups (public, private, or restricted).
- **Engagement Mechanisms**: Upvote/downvote system for posts and comments.
- **Social Interaction**: Follow users and posts.
- **Content Moderation**: Report inappropriate content.
- **Bookmarks & Saves**: Users can save their favorite posts.
- **Invites & Membership Requests**: Manage group access through invites and requests.


## 📸 Screenshots

![Django Reddit Sign In Page](screenshots/image01.png?raw=true "Django Reddit Sign In")

![Django Reddit Feed](screenshots/image02.png?raw=true "Django Reddit Feed")

![Django Reddit Group](screenshots/image03.png?raw=true "Django Reddit Group")

![Django Reddit User Feed](screenshots/image04.png?raw=true "Django Reddit User Feed")

<br>

## 🔧 Requirements

### Backend
- Python 3.8+
- virtualenv
- WSL (Windows Subsystem for Linux)

### Frontend
- Angular 10.2.4 (or 10.2.5)
- Node 10.13.x+


## ⚙️ Installation

### Backend Setup
1. Clone the repository and navigate to the project directory:
    ```bash
    git clone https://github.com/madhvi-n/django-reddit.git
    cd django-reddit
    ```

2. Create and activate a virtual environment:
    ```bash
    virtualenv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate     # For Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set the **Django Secret Key**:
    - Edit `reddit_clone/settings.py` and manually set a secret key.
    - Or, export `SECRET_KEY` in your environment variables.

5. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

    Visit **`http://127.0.0.1:8000/`** to access the app.



### 🌐 Frontend Setup
1. Navigate to the frontend directory:
    ```bash
    cd static/frontend/reddit-app
    ```

2. Install Angular dependencies:
    ```bash
    npm install
    ```

3. Run the frontend development server:
    ```bash
    ng serve
    ```

    Visit **`http://127.0.0.1:4200/`** to access the frontend.


## 📈 Management Commands

### Generate Data in Django Shell
```python
from django.contrib.auth.models import User
from posts.models import Post
from groups.models import Group

user = User.objects.get(id=1)
post = Post.objects.create(title="Sample Post", content="Post content here", author=user)
group = Group.objects.create(name="Django", description="Official Django community on Django Reddit")
```

### Populate Dummy Data
```bash
python manage.py populate_users
python manage.py populate_posts
python manage.py populate_tags
python manage.py populate_groups
```


## 💡 Notes
- **Backend (Django) runs on WSL**
- **Frontend (Angular) runs directly on Windows**


## 📐 References
- [How to Install Python 3.8 on Ubuntu 18.04](https://linuxize.com/post/how-to-install-python-3-8-on-ubuntu-18-04/)
- [Installing Node.js on Windows](https://www.guru99.com/download-install-node-js.html)
- [Official Angular 10 Installation Guide](https://v10.angular.io/guide/setup-local)
- [Installing a Specific Version of Angular CLI](https://stackoverflow.com/questions/44759621/install-specific-version-of-ng-cli)
- [Angular, Angular CLI, and Node.js Compatibility](https://stackoverflow.com/questions/60248452/is-there-a-compatibility-list-for-angular-angular-cli-and-node-js)

### 🎉 **Happy Coding!** 🚀

