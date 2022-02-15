"""A FastAPI integration for firebase.

This package contains tools to use firebase services within a FastAPI application.

The starting point is the app module because all other modules depend on it.
"""
from .app import firebase_app, setup_firebase

__version__ = "0.2.1"
