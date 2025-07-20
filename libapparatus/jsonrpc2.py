import json

# JSON-RPC protocol version used in all messages
JSONRPC_VERSION = "2.0"
IDS = {
    # General methods for registration and status
    "REGISTER": 1,
    "REGISTERED": 2,
    "UNREGISTER": 3,
    "PING": 4,
    "GET_STATUS": 6,

    # Configuration methods
    "GET_CONFIG": 10,
    "SET_CONFIG": 11,

    # Methods for camera control
    "INIT_CAMERA": 20,
    "GET_CAMERA_STATUS": 21,
    "GET_CAMERA_CONFIG": 22,
    "SET_CAMERA_CONFIG": 23,
    "GET_CAMERA_FRAME": 24,
    "START_CAMERA_STREAM": 25,
    "STOP_CAMERA_STREAM": 26,

    # Methods for motor control
    "INIT_MOTOR": 30,
    "GET_MOTOR_STATUS": 31,
    "GET_MOTOR_CONFIG": 32,
    "SET_MOTOR_CONFIG": 33,
    "GET_MOTOR_POSITION": 34,
    "SET_MOTOR_POSITION": 35,
}
METHODS = [k for k in IDS.keys()]


def make_request(method, params=None, id=None):
    """
    Constructs a JSON-RPC request object.
    :param method: The method name to invoke.
    :param params: Optional parameters for the method.
    :param id: Optional identifier for the request.
    :return: Dictionary representing the JSON-RPC request.
    """
    req = {
        "jsonrpc": JSONRPC_VERSION,
        "method": method,
    }
    if params is not None:
        req["params"] = params
    if id is not None:
        req["id"] = id
    return req

def make_response(result, id):
    """
    Constructs a JSON-RPC response object.
    :param result: The result of the method invocation.
    :param id: The identifier of the request being responded to.
    :return: Dictionary representing the JSON-RPC response.
    """
    return {
        "jsonrpc": JSONRPC_VERSION,
        "result": result,
        "id": id
    }

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
        "jsonrpc": JSONRPC_VERSION,
        "error": {
            "code": code,
            "message": message
        },
        "id": id
    }
    if data is not None:
        err["error"]["data"] = data
    return err

def parse_message(msg):
    """
    Parses a JSON-RPC message from a string or JSON dict.
    :param msg: JSON string representing the message.
    :return: Parsed dictionary, or None if parsing fails.
    """
    try:
        message = msg if isinstance(msg, dict) else json.loads(msg.strip())
        assert "jsonrpc" in message, f"Invalid JSON-RPC message: {message}, missing 'jsonrpc' field"
        assert "method" in message, f"Invalid JSON-RPC message: {message}, missing 'method' field"
        return message
    except Exception:
        return None