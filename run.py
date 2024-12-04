from flask import request
from app import create_app

app = create_app()

if __name__ == '__main__':
  app.run(debug=True)

# Stopped at page No: 97