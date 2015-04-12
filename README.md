[![Circle CI](https://circleci.com/gh/yosukesuzuki/kay-template.svg?style=svg)](https://circleci.com/gh/yosukesuzuki/kay-template)

# What's this?
This is the template for Kay-framework application.
Built-in tox

# Setup
## Setup Google Cloud SDK
install Google Cloud SDK


## make symlink 
```
sudo ln -s /some/whare/google_appengine /usr/local/google_appengine
```

## set environ variable for test

```
export AWS_ACCESS_KEY_ID=xxxxxxx
export AWS_SECRET_ACCESS_KEY=xxxxxxx
```

## run tox
```
$ tox
```

# add application folder
```
$ cd project
$ python manage.py startapp appname
```

