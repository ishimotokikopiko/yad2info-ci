#!/usr/bin/bash
set -e
set x

# Download the latest runner package
curl -o actions-runner-linux-x64-2.322.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-x64-2.322.0.tar.gz
# Optional: Validate the hash
echo "b13b784808359f31bc79b08a191f5f83757852957dd8fe3dbfcc38202ccf5768  actions-runner-linux-x64-2.322.0.tar.gz" | shasum -a 256 -c
# Extract the installer
tar xzf ./actions-runner-linux-x64-2.322.0.tar.gz


# Create the runner and start the configuration experience
./config.sh --url https://github.com/ishimotokikopiko/yad2info-ci --token AQ5WZIUKBF7SL4TGM5FYHHTHYGTO2
# Last step, run it!
./run.sh