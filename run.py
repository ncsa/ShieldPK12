from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from app import app

subdirectory_app = DispatcherMiddleware(
    None, {
        '/shieldpk12': app
    }
)

if __name__ == '__main__':
    run_simple('localhost', 5000, subdirectory_app, use_reloader=True)