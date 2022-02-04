from pathlib import Path

from fastapi import FastAPI, status
from fastapi.middleware import cors
from fastapi.staticfiles import StaticFiles


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)

        if response.status_code == status.HTTP_404_NOT_FOUND:
            response = await super().get_response(".", scope)

        return response


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
    setup_firebase(app)

    app.include_router(router, prefix="/firebase")
    app.mount(
        "/",
        SPAStaticFiles(
            directory=Path(__file__).parent.resolve() / "fbtoken-util" / "dist",
            html=True,
            check_dir=True,
        ),
    )

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
