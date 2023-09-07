############ This is the update (current) code

import sqlite3
import yaml

# Load data from the YAML file
with open('all_responses_new.yaml', 'r') as file:
    data = yaml.safe_load(file)
    profile_data_list = data  # Assuming all_responses_new.yaml contains a list of profile data dictionaries

# Connect to the SQLite database
connection = sqlite3.connect('new_database.db')
cursor = connection.cursor()

# Create a table for users' information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        occupation TEXT,
        headline TEXT,
        summary TEXT,
        city TEXT,
        country TEXT
    )
''')

# Create a table for education data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        education_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Create a table for skills data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill_name TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

# Create a table for experiences data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS experiences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        experiences_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')


# Iterate through each profile data dictionary and insert into the respective tables
for profile_data in profile_data_list:
    # Insert the user information into the 'users' table
    user_query = '''
        INSERT INTO users
        (first_name, last_name, occupation, headline, summary, city, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''

    user_values = (
        profile_data['first_name'],
        profile_data['last_name'],
        profile_data['occupation'],
        profile_data['headline'],
        profile_data['summary'],
        profile_data['city'],
        profile_data['country']
    )

    cursor.execute(user_query, user_values)
    connection.commit()

    # Get the last inserted user id
    user_id = cursor.lastrowid

    # Insert the education data into the 'education' table
    education_query = '''
        INSERT INTO education
        (user_id, education_data)
        VALUES (?, ?)
    '''

    education_values = (
        user_id,
        yaml.dump(profile_data['education'])
    )

    cursor.execute(education_query, education_values)
    connection.commit()

    # # Insert the skills data into the 'skills' table
    # skills_query = '''
    #     INSERT INTO skills
    #     (user_id, skill_name)
    #     VALUES (?, ?)
    # '''

    # skills_values = (
    #     user_id,
    #     yaml.dump(profile_data['skills'])
    # )

    # cursor.execute(skills_query, skills_values)
    # connection.commit()

    for skill in profile_data['skills']:
        skills_query = '''
            INSERT INTO skills
            (user_id, skill_name)
            VALUES (?, ?)
        '''
        skills_values = (
            user_id,
            skill
        )
        
        cursor.execute(skills_query, skills_values)
        connection.commit()

    # Insert the experiences data into the 'experiences' table
    experiences_query = '''
        INSERT INTO experiences
        (user_id, experiences_data)
        VALUES (?, ?)
    '''

    experiences_values = (
        user_id,
        yaml.dump(profile_data['experiences'])
    )

    cursor.execute(experiences_query, experiences_values)
    connection.commit()

# Close the database connection
connection.close()

