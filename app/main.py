from fastapi import FastAPI
from fastapi.middleware import cors


def get_app():
    from app.router import router
    from fastapi_firebase import setup_firebase

    app = FastAPI(
        title="FastAPI firebase test app",
        description="Just a test app to check the firebase integration works.",
    )
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        expose_headers=["*"],
    )
    setup_firebase(app, "./.vscode/firebase.json")

    app.include_router(router, prefix="/firebase")

    return app


app = get_app()

if __name__ == "__main__":
    import uvicorn

    from app.settings import settings

    uvicorn.run(
        app,
        host=str(settings.HOST),
        port=settings.PORT,
    )
