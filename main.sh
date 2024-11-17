#!/bin/bash

echo "Welcome to the project automation scripts."
echo "Please select an option to proceed:"
echo "1. Build the project"
echo "2. Deploy the project"
echo "3. Test the project"
echo "4. Exit"

read -p "Enter your choice [1-4]: " choice

case $choice in
  1)
    ./build.sh
    ;;
  2)
    ./deploy.sh
    ;;
  3)
    ./test.sh
    ;;
  4)
    echo "Exiting. Goodbye!"
    exit 0
    ;;
  *)
    echo "Invalid choice, please choose a valid option."
    ;;
esac
