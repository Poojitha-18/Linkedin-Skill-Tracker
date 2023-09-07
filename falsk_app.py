import logging
from flask import Flask, jsonify, request, has_request_context
import sqlite3
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

logger = app.logger

#logging formatter 
class NewFormatter(logging.Formatter): 
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote = request.remote_addr
        else:
            record.url = None
            record.remote = None
        return super().format(record)

logFormatter = NewFormatter("%(asctime)s - %(url)s - %(remote)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

#add console handler to the root logger
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#add file handler to the root logger 
fileHandler = RotatingFileHandler("logs.log", backupCount=100)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

#set the log level for the Flask app logger 
logger.setLevel(logging.INFO)

@app.route('/ping', methods=['GET'])
def ping():
    app.logger.info('Ping request received')
    return 'Pong!'

@app.route('/skills', methods=['GET'])
def get_skills():
    app.logger.info('Get skills request received')
    user_id = request.args.get('user_id')

    if not user_id:
        return 'No user_id provided', 400

    # Connect to the database
    connection = sqlite3.connect('new_database.db')
    cursor = connection.cursor()

    try:
        # Execute the query
        query = '''
            SELECT skill_name
            FROM skills
            WHERE user_id = ?;
        '''
        results = cursor.execute(query, (user_id,)).fetchall()

        # Format the results as a list of skill names
        skills = [row[0] for row in results]

        # Return the results as JSON
        return jsonify({'skills': skills})

    except Exception as e:
        return f'An error occurred: {str(e)}', 500

    finally:
        # Close the connection
        connection.close()

@app.route('/profile', methods=['GET'])
def get_profile():
    app.logger.info('Get profile request received')
    user_id = request.args.get('user_id')

    if not user_id:
        return 'No user_id provided', 400

    # Connect to the database
    connection = sqlite3.connect('new_database.db')
    cursor = connection.cursor()

    try:
        # Execute the query
        query = '''
            SELECT first_name, last_name
            FROM users
            WHERE id = ?;
        '''
        result = cursor.execute(query, (user_id,)).fetchone()

        # Format the result as a dictionary
        profile = {
            'first_name': result[0],
            'last_name': result[1],
        }

        # Return the result as JSON
        return jsonify(profile)

    except Exception as e:
        return f'An error occurred: {str(e)}', 500

    finally:
        # Close the connection
        connection.close()


@app.route('/search', methods=['GET'])
def search():
    # Get the skills from the request arguments and split by comma
    skills_to_search = request.args.get('skills')
    
    if not skills_to_search:
        return 'No skills provided', 400
    
    skills_to_search = skills_to_search.split(',')

    # Connect to the database
    connection = sqlite3.connect('new_database.db')
    cursor = connection.cursor()

    try:
        # Placeholder for the skills
        placeholders = ', '.join(['?'] * len(skills_to_search))

        # Execute the query
        query = f'''
            SELECT users.first_name, users.last_name, skills.skill_name
            FROM users
            INNER JOIN skills ON users.id = skills.user_id
            WHERE skills.skill_name IN ({placeholders});
        '''
        results = cursor.execute(query, skills_to_search).fetchall()

        # Format the results as a list of dictionaries
        users = [{'first_name': row[0], 'last_name': row[1], 'skill': row[2]} for row in results]

        # Return the results as JSON
        return jsonify(users)

    except Exception as e:
        return f'An error occurred: {str(e)}', 500

    finally:
        # Close the connection
        connection.close()


if __name__ == '__main__':
    app.run(port=8080)
    
