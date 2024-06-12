#!/bin/bash
#python3 /project/pipeline.py

#!/bin/bash
python -m pip install --upgrade pip
pip install -r ./requirements.txt

# Define the base directory paths
BASE_DIR=$(dirname $(realpath $0))  # This should point to the project directory
PROJECT_DIR="$BASE_DIR"
TEST_DIR="$PROJECT_DIR"  

# Ensure the output directory exists
OUTPUT_DIR="$TEST_DIR/output"
mkdir -p $OUTPUT_DIR

# Print a message indicating the start of the test setup
echo "Setting up test environment..."

# Ensure any old SQLite databases are removed before tests
rm -f "$BASE_DIR/data/emission_data.sqlite"
rm -f "$BASE_DIR/data/temperature_data.sqlite"

# Run the unit tests
echo "Running unit tests..."
python -m unittest discover -s "$TEST_DIR" -p "test_pipeline_loader.py"

# Capture the result of the tests
RESULT=$?

# Clean up test environment
echo "Cleaning up test environment..."
rm -rf $OUTPUT_DIR

# Print the result of the tests
if [ $RESULT -eq 0 ]; then
    echo "All tests passed successfully!"
else
    echo "Some tests failed. Please check the output above."
fi

# Exit with the result code
exit $RESULT
