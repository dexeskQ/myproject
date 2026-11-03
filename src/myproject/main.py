import uvicorn
from myproject.setup import app

if __name__ == '__main__':
    uvicorn.run(app)

    