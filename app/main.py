from fastapi import FastAPI
from api import user, curve_value, auth, permission
import uvicorn

app = FastAPI()

app.include_router(user.routes)
app.include_router(curve_value.routes)
app.include_router(auth.routes)
app.include_router(permission.routes)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
