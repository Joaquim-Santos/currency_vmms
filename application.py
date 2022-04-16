import os
from currency_vmms_api import application

if __name__ == "__main__":
    debug = application.config.get('DEBUG')
    host = os.getenv("HOST", 'localhost')
    port = os.getenv("PORT", 5000)

    application.run(host=host, port=port, debug=debug)
