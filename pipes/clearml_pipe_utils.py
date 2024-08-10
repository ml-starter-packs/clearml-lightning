import json
import logging

# Configure the root logger to a higher level
logging.basicConfig(level=logging.WARNING)

# Configure module's logger to DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def process_serialized_key(value):
    # Only attempt to deserialize strings
    if isinstance(value, str) and len(value) > 0:
        try:
            # Attempt to deserialize the string
            deserialized_value = json.loads(value)
            # If the deserialized value is not a string, update the dictionary
            if not isinstance(deserialized_value, str):
                logger.debug(f"Deserialized {value}")
                return deserialized_value
        except json.JSONDecodeError:
            # If deserialization fails, just move on
            logger.info(f"Deserialization failed on {value}")
            # at this point we are being returned a string. If "True" or "False" were passed,
            # json loads will fail and we will return the original string. Handle this here:
            if value == "True":
                logger.info(f"Determined {value} to be boolean: True")
                return True
            elif value == "False":
                logger.info(f"Determined {value} to be boolean: False")
                return False
    # Otherwise, return original value unmodified
    return value


def deserialize_dict(d):
    """Processes a dictionary, attempting to deserialize any string values that
    represent serialized lists or dictionaries.

    Args:
    - d (dict): The dictionary to process.

    Returns:
    - dict: The dictionary with serialized string values deserialized.
    """
    for key, value in d.items():
        logger.debug(f"Deserializing {key}...")
        d[key] = process_serialized_key(value)
    return d
