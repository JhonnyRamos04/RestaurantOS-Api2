"""
Configuración de CORS para diferentes entornos
"""

def get_cors_config(env="development"):
    """
    Obtener configuración CORS según el entorno
    """
    if env == "production":
        return {
            r"/*": {
                "origins": [
                    "url"
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                "supports_credentials": True,
                "max_age": 3600  # Cache preflight por 1 hora
            }
        }
    elif env == "staging":
        return {
            r"/*": {
                "origins": [
                   "url"
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                "supports_credentials": True
            }
        }
    else:  # development
        return {
            r"/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                "supports_credentials": True
            }
        }
