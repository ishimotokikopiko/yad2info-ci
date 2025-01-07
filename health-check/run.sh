#!/bin/bash

# Colors for output
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.11.0"
PORT=8080
HOST="0.0.0.0"

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
check_dependencies() {
    print_message "$CYAN" "Checking dependencies..."
    
    if ! command_exists pyenv; then
        print_message "$RED" "pyenv is not installed. Please install pyenv first."
        exit 1
    fi
    
    if ! command_exists poetry; then
        print_message "$RED" "poetry is not installed. Please install poetry first."
        exit 1
    fi
    
    print_message "$GREEN" "All dependencies are installed."
}

# Setup Python environment
setup_environment() {
    print_message "$CYAN" "Setting up Python environment..."
    
    # Set up pyenv
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    
    # Load bash configuration
    source ~/.bashrc
    
    # Set Python version
    pyenv local $PYTHON_VERSION
    
    print_message "$GREEN" "Python environment setup complete."
}

# Run the application
run_application() {
    print_message "$CYAN" "Starting application..."
    poetry install
    poetry run uvicorn main:app --host $HOST --port $PORT
}

# Main execution
main() {
    check_dependencies
    setup_environment
    run_application
}

# Execute main function
main