import os

from wheretolive.webapp.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=os.environ.get("LOGLEVEL") == "DEBUG")
