from main2 import app, db  # Import your Flask app and database

with app.app_context():
    db.create_all()  # Creates the database tables if they don't exist

print("Database created successfully!")
