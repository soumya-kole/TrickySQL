from abc import ABC, abstractmethod

class DataStore(ABC):
    """Abstract base class for different datastores."""

    _instances = {}  # Dictionary to store singleton instances

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance per unique set of parameters."""
        key = (cls, frozenset(kwargs.items()))
        if key not in cls._instances:
            instance = super().__new__(cls)
            instance._init_params(*args, **kwargs)  # Directly initialize
            cls._instances[key] = instance
        return cls._instances[key]

    @abstractmethod
    def _init_params(self, *args, **kwargs):
        """Initialize parameters but do NOT establish connection yet."""
        pass

    @abstractmethod
    def _connect(self):
        """Establish connection (lazy initialization)."""
        pass

    def get_datastore(self):
        """Return the datastore connection, establishing it if necessary."""
        if not hasattr(self, "connection") or self.connection is None:
            self.connection = self._connect()
        return self.connection

    @abstractmethod
    def execute_sql(self, query):
        """Execute SQL query."""
        pass

    @abstractmethod
    def close_connection(self):
        """Close the connection."""
        pass


# === Concrete Implementations ===

class BigQueryDataStore(DataStore):
    """BigQuery datastore implementation."""

    def _init_params(self, project_id, credentials):
        self.project_id = project_id
        self.credentials = credentials
        self.connection = None  # Connection not established yet

    def _connect(self):
        return f"BigQuery connection to project {self.project_id}"

    def execute_sql(self, query):
        conn = self.get_datastore()  # Ensures connection is established
        return f"Executing on {conn}: {query}"

    def close_connection(self):
        self.connection = None
        return "BigQuery connection closed"


class SnowflakeDataStore(DataStore):
    """Snowflake datastore implementation."""

    def _init_params(self, account, user, password):
        self.account = account
        self.user = user
        self.password = password
        self.connection = None  # Connection not established yet

    def _connect(self):
        return f"Snowflake connection to account {self.account}"

    def execute_sql(self, query):
        conn = self.get_datastore()
        return f"Executing on {conn}: {query}"

    def close_connection(self):
        self.connection = None
        return "Snowflake connection closed"


class MySQLDataStore(DataStore):
    """MySQL datastore implementation."""

    def _init_params(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None  # Connection not established yet

    def _connect(self):
        return f"MySQL connection to {self.database} at {self.host}"

    def execute_sql(self, query):
        conn = self.get_datastore()
        return f"Executing on {conn}: {query}"

    def close_connection(self):
        self.connection = None
        return "MySQL connection closed"


# === Usage Example ===
if __name__ == "__main__":
    # Ensure same parameters return the same object
    bq1 = BigQueryDataStore(project_id="project1", credentials="key1")
    bq2 = BigQueryDataStore(project_id="project1", credentials="key1")
    assert bq1 is bq2  # Same object

    # Different parameters should return a different object
    bq3 = BigQueryDataStore(project_id="project2", credentials="key2")
    assert bq1 is not bq3  # Different object

    # Test lazy connection setup
    print(bq1.execute_sql("SELECT * FROM dataset.table"))  # Establishes connection
    print(bq1.get_datastore())  # Now connection exists

    # Similar tests for Snowflake and MySQL
    sf1 = SnowflakeDataStore(account="acc1", user="user1", password="pass1")
    sf2 = SnowflakeDataStore(account="acc1", user="user1", password="pass1")
    assert sf1 is sf2  # Same object

    mysql1 = MySQLDataStore(host="localhost", user="root", password="123", database="db1")
    mysql2 = MySQLDataStore(host="localhost", user="root", password="123", database="db1")
    assert mysql1 is mysql2  # Same object

    print(sf1.execute_sql("SELECT * FROM warehouse.schema.table"))  # Establishes connection
    print(mysql1.execute_sql("SELECT * FROM users"))  # Establishes connection
