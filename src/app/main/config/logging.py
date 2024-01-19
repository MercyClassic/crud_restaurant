def get_logging_dict(root_dir: str) -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'main_format': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'main': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 1_048_576,
                'backupCount': 50,
                'formatter': 'main_format',
                'filename': f'{root_dir}/logs/error.log',
            },
        },
        'loggers': {
            'app.main.exceptions.setup_exception_handlers': {
                'handlers': ['main'],
                'level': 'WARNING',
                'propagate': True,
            },
        },
    }
