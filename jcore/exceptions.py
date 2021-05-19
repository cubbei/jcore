class JarvisException(Exception):
    """
    Base Exception Class for the project
    """
    pass


class SettingException(JarvisException):
    """
    Exception Handler for Settings Class
    """
    pass

class MissingSetting(SettingException):
    """
    Exception raised when Settings attempts to retrieve a setting that does not exist.
    """
    pass

class ConfigFileNotFound(SettingException):
    """
    Exception raised when the config file passed, nor the file backup locations cannot be found.
    """
    pass

class HTTPDriverException(JarvisException):
    """
    Exception raised in the HTTPClient.
    """
    pass

class HTTPDriverNotConfigured(HTTPDriverException):
    """
    Exception raised when the parameters passed to the HTTP Client are invalid.
    """
    
    
class MissingRequiredParameterException(JarvisException):
    """Exception thrown when a required parameter has not been provided."""
    pass

class TelemetryUnavailable(JarvisException):
    pass


class ExtensionAlreadyLoaded(JarvisException):
    pass

class ExtensionNotFound(JarvisException):
    pass

class ExtensionFailed(JarvisException):
    pass

class NoEntryPointError(JarvisException):
    pass

class NoTokenError(JarvisException):
    pass

class NoNickError(JarvisException):
    pass

class NoChannelsSet(JarvisException):
    pass

class DBConnectionUndefined(JarvisException):
    pass