import logging
import logging.config
import time
import yaml

from watchdog.observers.polling import PollingObserver

from .celery import app
from .configuration import Configuration
from .handlers import SpecioEventHandler
from .tasks import pipeline


WATCH_MODE, WORKER_MODE, IDLE_MODE, PLAIN_MODE = (
  'watch',
  'worker',
  'idle',
  'plain'
)

logger = logging.getLogger(__name__)


def setup_logging(config):
    with open(config.logging_config) as f:
        logging_config = yaml.load(f)

    logging.config.dictConfig(logging_config)


def setup_celery(config):
    if not config.debug:
        # Do nothing.
        return

    logger.info('Starting Celery in debug mode. All tasks will execute locally.')
    app.conf.task_always_eager = True
    app.conf.task_eager_propagates = True


def get_event_handler(config):
    return SpecioEventHandler(
        config.as_dict(),
        patterns=config.patterns,
        ignore_patterns=config.ignore_patterns,
        ignore_directories=config.ignore_directories,
        case_sensitive=config.case_sensitive,
    )


def get_observer(config, handler):
    observer = PollingObserver()
    observer.schedule(
        handler,
        config.path,
        recursive=True
    )
    return observer


def main(mode=PLAIN_MODE, run_once=False):
    """ A method that watches files for changes and runs the full pipline. """
    config = Configuration()
    setup_logging(config)
    setup_celery(config)

    logger.info('Welcome to Specio!')

    # Start the app as a worker
    if mode == WORKER_MODE:
        app.worker_main()

    # Watch for file changes
    elif mode == WATCH_MODE:
        event_handler = get_event_handler(config)
        observer = get_observer(config, event_handler)

        logger.info(
            'In this mode, Specio will watch {config.path} for changes invoke the '
            'pipeline each time a ".yml" file changes.'
        )

        observer.start()

        logger.info('Entering runloop. Watching for changes...')

        try:
            while True: time.sleep(1)  # noqa
        except KeyboardInterrupt:
            logger.info('Runloop cancelled by user. Exiting.')
            observer.stop()

        observer.join()

    # Just sit and wait
    elif mode == IDLE_MODE:
        try:
            while True: time.sleep(1)  # noqa
        except KeyboardInterrupt:
            logger.info('Runloop cancelled by user. Exiting.')

    # Manual run once
    elif run_once:
        logger.info(
            'In this mode, Specio will not watch for file changes and must instead '
            'be invoked each time you want to re-run the pipline.'
        )
        configdict = config.as_dict()

        logger.info(f'Dispatching pipeline for {config.input}')
        result = pipeline(configdict, config.input)

        logger.debug(f'Waiting for pipeline to complete...')
        result.get()

        logger.info('Pipeline complete! Exiting.')

    # No valid run mode specified. Skipping.
    else:
        pass
