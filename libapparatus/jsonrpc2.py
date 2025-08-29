import json


class JSONRPC2:
    """
    A class to handle JSON-RPC 2.0 messages.
    Provides methods to create requests, responses, and error messages,
    as well as parsing incoming messages.
    """
    # JSON-RPC protocol version used in all messages
    JSONRPC_VERSION = "2.0"
    # General methods for registration and status
    REGISTER = 1
    UNREGISTER = 2
    PING = 3
    GET_STATUS = 5
    GET_NODE_STATUS = 6
    GET_USER_STATUS = 7
    # Configuration methods
    GET_CONFIG = 10
    SET_CONFIG = 11
    # Methods for camera control
    INIT_CAMERA = 20
    GET_CAMERA_STATUS = 21
    GET_CAMERA_CONFIG = 22
    SET_CAMERA_CONFIG = 23
    GET_CAMERA_FRAME = 24
    START_CAMERA_STREAM = 25
    STOP_CAMERA_STREAM = 26
    # Methods for motor control
    INIT_MOTOR = 30
    GET_MOTOR_STATUS = 31
    GET_MOTOR_CONFIG = 32
    SET_MOTOR_CONFIG = 33
    START_MOTOR = 34
    STOP_MOTOR = 35

    TYPE_REQUEST = "REQUEST"
    TYPE_RESPONSE = "RESPONSE"
    TYPE_NOTIFICATION = "NOTIFICATION"

    @staticmethod
    def check_message(message):
        """
        Validates a JSON-RPC message.
        :param message: The JSON-RPC message to validate.
        :return: True if valid, False otherwise.
        """
        if not isinstance(message, dict):
            return False
        if "jsonrpc" not in message or message["jsonrpc"] != JSONRPC2.JSONRPC_VERSION:
            return False
        return True

    @staticmethod
    def check_request(message):
        """
        Validates a JSON-RPC request message.
        Requests have the following fields:
         - jsonrpc: Must be set to "2.0".
         - method:  Must be a string representing the method to invoke.
         - id:      Must be a unique identifier (int or str) for the request.
         - params:  Optional, this can be a dictionary or a list.
        :param message: The JSON-RPC message to validate.
        :return: True if valid, False otherwise.
        """
        if not isinstance(message, dict):
            return False
        if message.get("jsonrpc") != JSONRPC2.JSONRPC_VERSION:
            return False
        if "method" not in message or not isinstance(message["method"], str):
            return False
        if "id" not in message or not isinstance(message["id"], (int, str)):
            return False
        return True

    @staticmethod
    def check_response(message):
        """
        Validates a JSON-RPC response message.
        Responses have the following fields:
            - jsonrpc: Must be set to "2.0".
            - result:  Must be present if the request was successful.
            - error:   Must be present if the request failed.
            - id:      Must be a unique identifier (int or str) matching the request.
        :param message: The JSON-RPC message to validate.
        :return: True if valid, False otherwise.
        """
        if not isinstance(message, dict):
            return False
        if message.get("jsonrpc") != JSONRPC2.JSONRPC_VERSION:
            return False
        if "result" not in message and "error" not in message:
            return False
        if "id" not in message or not isinstance(message["id"], (int, str)):
            return False
        return True

    @staticmethod
    def check_notification(message):
        """
        Validates a JSON-RPC notification message.
        Notifications have the following fields:
            - jsonrpc: Must be set to "2.0".
            - method:  Must be a string representing the method to invoke.
        They do not have id or params fields.
        :param message: The JSON-RPC message to validate.
        :return: True if valid, False otherwise.
        """
        if not isinstance(message, dict):
            return False
        if message.get("jsonrpc") != JSONRPC2.JSONRPC_VERSION:
            return False
        if "method" not in message or not isinstance(message["method"], str):
            return False
        if "id" in message:
            return False
        if "params" in message and not isinstance(message["params"], (dict, list)):
            return False
        return True

    @staticmethod
    def get_message_type(message):
        """
        Checks the message type of  a JSON-RPC message, which can be a request, response, or notification.
        :param message: The JSON-RPC message to validate.
        :return: True if valid, False otherwise.
        """
        if not isinstance(message, dict):
            return False
        if "jsonrpc" not in message or message["jsonrpc"] != JSONRPC2.JSONRPC_VERSION:
            return False
        if JSONRPC2.check_request(message):
            return JSONRPC2.TYPE_REQUEST
        elif JSONRPC2.check_response(message):
            return JSONRPC2.TYPE_RESPONSE
        elif JSONRPC2.check_notification(message):
            return JSONRPC2.TYPE_NOTIFICATION

    @staticmethod
    def make_request(method, id=None, params=None):
        """
        Constructs a JSON-RPC request object.
        :param method: The method name to invoke.
        :param params: Optional parameters for the method.
        :return: Dictionary representing the JSON-RPC request.
        """
        req = {
            "jsonrpc": JSONRPC2.JSONRPC_VERSION,
            "method": method,
            "id": id if id is not None else getattr(JSONRPC2, method),
            "params": params if params is not None else {}
        }
        return req

    @staticmethod
    def make_notification(method, params=None):
        """
        Constructs a JSON-RPC request object.
        :param method: The method name to invoke.
        :param params: Optional parameters for the method.
        :return: Dictionary representing the JSON-RPC request.
        """
        req = {
            "jsonrpc": JSONRPC2.JSONRPC_VERSION,
            "method": method
        }
        if params is not None:
            req["params"] = params
        return req

    @staticmethod
    def make_response(id, result=None):
        """
        Constructs a JSON-RPC response object.
        :param id: The identifier of the request being responded to.
        :param result: The result of the method invocation.
        :return: Dictionary representing the JSON-RPC response.
        """
        return {
            "jsonrpc": JSONRPC2.JSONRPC_VERSION,
            "id": id,
            "result": result,
        }

    @staticmethod
    def make_error(code, message, id=None, data=None):
        """
        Constructs a JSON-RPC error response object.
        :param code: Error code.
        :param message: Error message.
        :param id: Optional identifier of the request.
        :param data: Optional additional error data.
        :return: Dictionary representing the JSON-RPC error response.
        """
        err = {
            "jsonrpc": JSONRPC2.JSONRPC_VERSION,
            "error": {
                "code": code,
                "message": message
            },
            "id": id
        }
        if data is not None:
            err["error"]["data"] = data
        return err

    @staticmethod
    def parse_message(msg):
        """
        Parses a JSON-RPC message from a string or JSON dict.
        :param msg: JSON string or dict representing the message.
        :return: Parsed dictionary, or None if parsing fails.
        """
        try:
            if isinstance(msg, str):
                message = json.loads(msg.strip())
            elif isinstance(msg, dict):
                message = msg
        except Exception as ex:
            print(f"Error parsing JSON-RPC message: {ex}")
            return None
        assert "jsonrpc" in message, f"Invalid JSON-RPC message: {message}, missing 'jsonrpc' field"
        return message