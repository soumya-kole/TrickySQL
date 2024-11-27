import subprocess
import time
import logging
import pytest
import os

# Setup logging
logging.basicConfig(
    filename="docker_compose_test.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def docker_compose():
    """
    Pytest fixture to set up and tear down Docker Compose services for MSSQL.
    """
    # Path to the provided docker-compose.yml
    docker_compose_file = "./docker-compose.yml"

    try:
        # Start Docker Compose services
        logger.info("Starting Docker Compose services...")
        subprocess.run(["docker-compose", "-f", docker_compose_file, "up", "-d"], check=True)

        # Wait for the MSSQL service to be ready
        logger.info("Waiting for MSSQL service to be ready...")
        wait_for_mssql_service(timeout=60)
        logger.info("MSSQL service is ready.")

        yield  # This is where the tests will execute

    finally:
        # Tear down Docker Compose services
        logger.info("Stopping Docker Compose services...")
        subprocess.run(["docker-compose", "-f", docker_compose_file, "down"], check=True)
        logger.info("Docker Compose services stopped.")

def wait_for_mssql_service(timeout=60):
    """
    Wait until the MSSQL service is available.
    """
    import pymssql

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Connect to MSSQL service
            connection = pymssql.connect(
                server="localhost",
                user="sa",
                password="YourStrong!Password",
                database="master",
                port=1433,
            )
            connection.close()
            return True
        except pymssql.OperationalError as e:
            logger.warning(f"MSSQL service not ready: {e}")
            time.sleep(5)
    raise TimeoutError("MSSQL service did not become ready within the timeout period.")

def test_example(docker_compose):
    """
    Example test that depends on Docker Compose being up.
    """
    logger.info("Running test with Docker Compose services...")
    assert True  # Replace with actual assertions
