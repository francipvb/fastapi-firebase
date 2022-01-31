# FastAPI Firebase integration

This package contains some utilities to work with firebase in a FastAPI project.

## Example usage

For example, if you want to send the firebase app name:

```python
from fastapi import FastAPI, Depends
from fastapi_firebase import setup_firebase, firebase_app
from firebase_admin.app import App

app=FastAPI()

setup_firebase(app)

@app.get("/appname")
def get_appname(fb_app: App = Depends(firebase_app)):
    return fb_app.name

```

See the `setup_firebase` documentation for how to initialize.
