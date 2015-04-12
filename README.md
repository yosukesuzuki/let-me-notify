[![Circle CI](https://circleci.com/gh/yosukesuzuki/let-me-notify.svg?style=svg)](https://circleci.com/gh/yosukesuzuki/let-me-notify)

# What's this?
This is notification tools for infra developers.

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

## run tests with tox
```
$ tox
```

# add application folder
```
$ cd project
$ python manage.py startapp appname
```

