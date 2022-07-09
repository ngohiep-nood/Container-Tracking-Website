template = {
    # "swagger": "2.0",
    "info": {
        "title": "Container Tracking API",
        "description": "API for container tracking",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "hoanghiephai@gmail.com",
            "url": "www.twitter.com/deve",
        },
        "termsOfService": "www.twitter.com/deve",
        "version": "1.0.0"
    },
    "schemes": ['http', 'https'],
    "basePath": "/",  # base bash for blueprint registration
    "securityDefinitions": {
        "bearerAuth": {
            "name": "Authorization",
            "in": "header",
            "type": "apiKey",
            "description": "JWT Authorization header"
        }
    },
    "security": [{"bearerAuth": []}],
    "consumes": [
        "multipart/form-data",
        "application/x-www-form-urlencoded",
        "application/json"
    ]
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
