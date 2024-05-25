#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Run the create_group command
echo "Running create_group command..."
python manage.py create_groups

# Start the server
echo "Starting server..."
exec "$@"
