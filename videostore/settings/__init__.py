from .development import Development
from .production import Production
from .test import Test

environments = {
    'test': Test,
    'development': Development,
    'production': Production,
}
