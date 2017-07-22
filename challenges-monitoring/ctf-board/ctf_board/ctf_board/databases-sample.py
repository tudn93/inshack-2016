def getDatabaseConfig(base_dir):
    import os
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(base_dir, 'db.sqlite3'),
        }
    }
    return DATABASES
