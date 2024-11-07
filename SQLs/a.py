class Configuration:
    _instance = None  # Class variable to hold the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Use a guard variable to prevent reinitialization
        if not hasattr(self, "_initialized"):
            self._initialized = True  # Mark initialization
            self._last_value = None  # Initialize attribute to store the last value
            print("Configuration instance initialized")

    @classmethod
    def instance(cls):
        """Returns the singleton instance of Configuration."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # Method to set a value and return the previous one
    def set_and_get_previous(self, new_value):
        previous_value = self._last_value  # Store the previous value
        self._last_value = new_value  # Update with the new value
        return previous_value  # Return the previous value

# Testing the modified singleton class

# Access the singleton instance using the class method
config = Configuration.instance()

# First call: No previous value, so it should return None
result1 = config.set_and_get_previous("Value1")
print("Previous value (expected None):", result1)  # Output: None

# Second call: Returns "Value1" as the previous value
result2 = config.set_and_get_previous("Value2")
print("Previous value (expected 'Value1'):", result2)  # Output: Value1

# Third call: Returns "Value2" as the previous value
result3 = config.set_and_get_previous("Value3")
print("Previous value (expected 'Value2'):", result3)  # Output: Value2
