# Flask API For Container Tracking



## Dependencies

- [flask](https://palletsprojects.com/p/flask/): Python server of choise
- [flasgger](https://github.com/flasgger/flasgger): Used to generate the swagger documentation
- [flask-marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/): My favourite serializer
- [apispec](https://apispec.readthedocs.io/en/latest/): Required for the integration between marshmallow and flasgger

## Set Up

1. Check out the code
2. Install requirements
    ```
    pipenv install
    ```
3. Build database:
    ```
    python run build_db.py
    ```
4. Start the server with:
    ```
   pipenv run python -m flask run
    ```
   
5. Visit http://localhost/ for the home api

6. Visit http://localhost/upload for the admin upload page
   
