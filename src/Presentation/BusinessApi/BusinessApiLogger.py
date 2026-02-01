import logging

class BusinessApiLogger:
    @staticmethod
    def set_logger() -> logging.Logger:
        arify_consumer_logger = logging.getLogger('app')
        arify_consumer_logger.setLevel(logging.INFO)

        # Create console handler if it doesn't exist
        if not arify_consumer_logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(levelname)s:  %(asctime)s - %(name)s - %(message)s')
            console_handler.setFormatter(formatter)
            arify_consumer_logger.addHandler(console_handler)
        
        return arify_consumer_logger