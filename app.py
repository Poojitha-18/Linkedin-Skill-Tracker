# Required libraries
import streamlit as st
import requests
import subprocess
import streamlit as st
import numpy as np
from itertools import combinations
from sentence_transformers import SentenceTransformer, util
import sqlite3
import pandas as pd
import openai


def fetch_available_skills():
    # Database connection
    connection = sqlite3.connect('db/profiles.db')
    cursor = connection.cursor()

    # Fetching skills query execution
    cursor.execute('SELECT skill_name FROM skills')
    skills_data = cursor.fetchall()

    # Skills data extraction
    skills_list = [skill[0] for skill in skills_data]

    # Database connection closure
    connection.close()

    return skills_list


def generate_skill_suggestions(input_skills):
    """
    Generates a list of suggested skills based on the input skills.
    The suggestions are generated based on matching parts of the input skills
    with the available skills.

    Parameters:
    -----------
    input_skills (str): 
        A comma-separated string of input skills.

    Returns:
    --------
    List[str]:
        A sorted list of suggested skills without any duplicates.
    """
    available_skills = fetch_available_skills()
    suggestions = []

    # Splitting input skills by comma
    skills = [skill.strip() for skill in input_skills.split(',')]

    # Skill suggestion generation
    for skill in skills:
        matching_skills = [available_skill for available_skill in available_skills if skill.lower(
        ) in available_skill.lower()]
        suggestions.extend(matching_skills)

    # Duplicate removal and suggestion sorting
    suggestions = sorted(list(set(suggestions)))

    return suggestions

# # Function to generate screening interview questions
# def generate_interview_questions(job_role):
#     prompt = f"Generate screening interview questions for the job role: {job_role}"

#     # Generate the completion using OpenAI API
#     response = openai.Completion.create(
#         engine="davinci",
#         prompt=prompt,
#         max_tokens=100,
#         n=5,  # Generate 5 questions
#         stop=None,
#         temperature=0.7,
#         top_p=1,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#     )

#     # Extract the generated questions from the response
#     questions = [choice['text'].strip() for choice in response['choices']]

#     return questions

def generate_interview_questions_and_answers(job_role):
    prompt = f"Generate 10 screening interview questions and answers for the job role: {job_role}"

    openai.api_key = "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"
    # Generate the completion using OpenAI API
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response)

    # Convert the response to a JSON-compatible format
    response_json = response.to_dict()
    

    # Extract the generated questions and answers from the response
    questions = []
    answers = []
    for choice in response_json['choices']:
        text = choice['text'].strip()
        if text.startswith("Q:"):
            questions.append(text.replace("Q:", "").strip())
        elif text.startswith("A:"):
            answers.append(text.replace("A:", "").strip())

    return questions, answers, response_json

def generate_job_description(job_title, location, key_responsibilities=None, tools_skills=None, education_experience=None):

    prompt = prompt = f"Job Title: {job_title}\n\nDescription:\n{description}\n\nKey Responsibilities:\n{key_responsibilities}\n\nTools/Skills (hands-on experience is must):\n{tools_skills}\n\nEducation & Experience: -\n{education_experience}\n\nLocation: {location}\n\n"

    # Add the rest of your job description prompt here
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )
    jd = response.choices[0].text.strip()
    return jd

# Function to start the Flask app
def start_flask_app():
    subprocess.Popen(['python', 'code/utils.py'])


# Start the Flask app when the Streamlit app runs
if __name__ == '__main__':
    # Start Flask app as a separate process
    start_flask_app()

# Add banner with logo
col1, col2 = st.columns([1, 3])
with col1:
    logo_image = st.image("assets/ust_logo.png", width=100)

with col2:
    st.markdown(
        """
    <style>
    .title {
        text-align: left;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    st.markdown('<h1 class="title">TALENT INSIGHT</h1>',
                unsafe_allow_html=True)

FLASK_URL = 'http://localhost:8080'

# Menu bar
selected_page = st.sidebar.radio(
    "Go to",
    ("Home", "Skill Search", "Profile Management", "Job Description Match", "JD Creation", "Finding a Candidate",
     "Screening Interview Questions", "Skill Fitment Analysis"),
)

# Page content
if selected_page == "Home":
    st.header("Home")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Skill Search", help="Search for users by skills"):
            selected_page = "Skill Search"

    with col2:
        if st.button("Profile Management", help="Profile and skills management tool"):
            selected_page = "Profile Management"
    with col3:
        if st.button("Job Description Match", help="Match job descriptions with users"):
            selected_page = "Job Description Match"

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("JD Creation", help="Job descriptions generator"):
            selected_page = "JD Creation"
    with col5:
        if st.button("Finding a Candidate", help="Finding a Candidate"):
            selected_page = "Finding a Candidate"
    with col6:
        if st.button("Screening Interview Questions", help="Interview questions generator"):
            selected_page = "Screening Interview Questions"


if selected_page == "Skill Search":
    st.header("Skill Search")

    # Skill suggestions
    skill_suggestions = generate_skill_suggestions('')

    # Skills input
    skills = st.multiselect('Skills', options=skill_suggestions,
                            help='Enter the skills to search for', key='skill_input_search')

    if st.button('Search'):
        try:
            # Make a request to the Flask API endpoint
            response = requests.get(
                f'{FLASK_URL}/search', params={'skills': ','.join(skills)})

            if response.status_code == 200:
                # Display the search results
                results = response.json()

                if not results:  # Check if the results are empty
                    st.warning(
                        'No results found. Please try a different search.')
                else:
                    st.table(results)
            else:
                # Display an error message if the request fails
                st.error('An error occurred during the search. Please try again.')

        except requests.exceptions.RequestException as e:
            # Handle the exception if a request error occurs
            st.error('An error occurred during the search. Please try again.')


elif selected_page == "Profile Management":
    st.header("Profile Management Tool")

    # Option to search by user ID, first name, last name, or both
    search_option = st.radio(
        "Search by", ("User ID", "First Name", "Last Name", "Full Name"), index=0)

    if search_option == "User ID":
        user_identifier = st.text_input('Enter user ID', key='user_id')
    elif search_option == "First Name":
        user_identifier = st.text_input(
            'Enter first name', key='first_name').lower()
    elif search_option == "Last Name":
        user_identifier = st.text_input(
            'Enter last name', key='last_name').lower()
    else:
        first_name = st.text_input(
            'Enter first name', key='first_name').lower()
        last_name = st.text_input('Enter last name', key='last_name').lower()
        user_identifier = first_name + " " + last_name

    if st.button('Get Profile and Skills'):
        connection = sqlite3.connect('db/profiles.db')
        cursor = connection.cursor()

        if search_option == "User ID":
            cursor.execute('''
                SELECT * FROM users
                WHERE id=?
            ''', (user_identifier,))
            user_data = cursor.fetchone()
        elif search_option == "First Name":
            cursor.execute('''
                SELECT * FROM users
                WHERE LOWER(first_name)=?
            ''', (user_identifier,))
            user_data = cursor.fetchone()
        elif search_option == "Last Name":
            cursor.execute('''
                SELECT * FROM users
                WHERE LOWER(last_name)=?
            ''', (user_identifier,))
            user_data = cursor.fetchone()
        else:
            cursor.execute('''
                SELECT * FROM users
                WHERE LOWER(first_name)=? AND LOWER(last_name)=?
            ''', (first_name, last_name))
            user_data = cursor.fetchone()

        if user_data:
            user_id = user_data[0]

            # Retrieve profile data
            profile_data = {
                'First Name': user_data[1],
                'Last Name': user_data[2],
                'Occupation': user_data[3],
                'Headline': user_data[4],
                'Summary': user_data[5],
                'City': user_data[6],
                'Country': user_data[7]
            }

            # Retrieve skills data
            cursor.execute('''
                SELECT skill_name FROM skills
                WHERE user_id=?
            ''', (user_id,))
            skills_data = cursor.fetchall()
            skills_list = [skill[0] for skill in skills_data]

            col1, col2 = st.columns(2)  # Create two columns

            with col1:
                st.write('Profile Data:')
                st.dataframe(profile_data)

            with col2:
                st.write('Skills Data:')
                skills_df = pd.DataFrame({'Skills': skills_list})
                st.dataframe(skills_df)

            #below incomplete
            # Generate hyperlink for detailed user info page
            #st.markdown("### Detailed User Info:")
            #user_info_link = f"[Click here for detailed user info](https://yourwebsite.com/user/{user_id})"
            #st.markdown(user_info_link)
        else:
            st.error('User not found.')


elif selected_page == "Job Description Match":
    # Set up OpenAI API
    openai.api_key = "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"
    connection = sqlite3.connect('db/profiles.db')
    cursor = connection.cursor()

    def fetch_users():
        # Fetch the users and their information from the database
        query = '''
        SELECT u.id, u.first_name, u.last_name, u.occupation, u.headline, u.summary, u.city, u.country, (
            SELECT GROUP_CONCAT(s.skill_name)
            FROM skills s
            WHERE s.user_id = u.id
        ) AS skills
        FROM users u
        '''
        cursor = connection.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        return users

    def generate_best_suited_user(prompt):
        # Generate the completion using OpenAI API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the best suited user from the response
        generated_text = response.choices[0].text
        best_suited_user = generated_text.split('- ')[-1].split(',')[0].strip()
        return best_suited_user

    # Streamlit app
    def main():
        # Title and description
        st.title("Job Description Match")
        st.write("Enter the job description below and find the best suited candidate for the position.")

        # Input prompt
        prompt = st.text_area("Enter the job description")

        # Generate best suited user when button is clicked
        if st.button("Match"):
            if prompt:
                # Fetch users from the database
                users = fetch_users()

                # Construct the complete prompt
                complete_prompt = "This job description is from a company called UST, please match the job descriptions to the candidates you would think would be best suited for the position. Here are the candidates and their information:\n"
                for user in users:
                    _, first_name, _, occupation, _, _, city, _, skills = user
                    complete_prompt += f"- {first_name}, a {occupation} in {city}. Skills: {skills}\n"

                complete_prompt += '\n\"\"\"\n' + prompt + '\n\"\"\"'

                # Debugging 
                #st.write("Complete Prompt:")
                #st.write(complete_prompt)

                # Generate best suited user
                best_suited_user = generate_best_suited_user(complete_prompt)

                # Debugging 
                #st.write("Response from OpenAI:")
                #st.write(best_suited_user)

                for user in users:
                    _, first_name, last_name, occupation, _, _, city, country, skills = user
                    if best_suited_user.startswith(f"{first_name}"):
                        matching_user = user
                        break
                    
                # Display the best suited user generated by OpenAI
                st.subheader("Generated best suited user")
                st.write(best_suited_user)
            else:
                st.warning("Please enter a prompt.")

    main()

    # Close the database connection
    connection.close()
          
      
# elif selected_page == "JD Creation":
#     st.header("JD Creation")
#     # Add your JD creation content here

#     st.subheader("Job Title")
#     job_title = st.text_input("Job Title", value=" ")

#     if st.button('Create JD'):
#         # Perform your desired actions when the button is clicked
#         # Access the entered job title using the variable: job_title
#         # Generate the job description based on the job title
#         jd_template = f'''
#         Job Title: {job_title}

#         Department: Software Development

#         Reporting Structure: Reports to the Engineering Manager

#         Job Summary:
#         We are seeking a talented {job_title} to join our Software Development team. The {job_title} will be responsible for designing and developing interactive web applications using the Streamlit framework. The ideal candidate should have a strong background in web development, proficiency in Python programming, and a passion for creating intuitive user interfaces.

#         Key Responsibilities:
#         - Collaborate with cross-functional teams to gather requirements and understand application needs.
#         - Design and develop web applications using the Streamlit framework and Python programming language.
#         - Create visually appealing and user-friendly interfaces that provide a seamless user experience.
#         - Implement data visualization and interactive features to enhance application functionality.
#         - Integrate APIs and third-party services to fetch and display data within the applications.
#         - Perform testing and debugging of the applications to ensure proper functionality and fix any issues or bugs.
#         - Optimize and refactor code to improve performance and maintainability.
#         - Stay up-to-date with the latest Streamlit developments and best practices in web development.
#         - Collaborate with team members to troubleshoot and resolve technical challenges.
#         - Document code, processes, and application architectures for future reference.

#         Qualifications and Skills:
#         - Bachelor's degree in Computer Science, Software Engineering, or a related field.
#         - Proven experience in web development with a focus on Python.
#         - Proficiency in Python programming and experience with frameworks such as Streamlit.
#         - Strong understanding of HTML, CSS, and JavaScript for building interactive web interfaces.
#         - Familiarity with data visualization libraries, such as Matplotlib or Plotly, is a plus.
#         - Experience with version control systems, such as Git, for collaborative development.
#         - Excellent problem-solving and analytical skills.
#         - Strong communication and teamwork abilities.
#         - Ability to work in a fast-paced and agile development environment.

#         This is just a sample job description for a {job_title}.
#         '''

#         # Display the generated job description
#         st.subheader("Generated Job Description")
#         st.text(jd_template)

elif selected_page == "JD Creation":
    st.header("JD Creation")
    openai.api_key = "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"
    job_title = st.text_input("Job Title")
    description = st.text_area("Description")
    key_responsibilities = st.text_area("Key Responsibilities")
    tools_skills = st.text_area("Tools/Skills (hands-on experience is must)")
    education_experience = st.text_area("Education & Experience")
    location = st.text_input("Location")
    if st.button("Generate Job Description"):
        jd = generate_job_description(job_title, location,
                              key_responsibilities=key_responsibilities,
                              tools_skills=tools_skills,
                              education_experience=education_experience)
        st.markdown(f"## Job Description\n\n{jd}")

elif selected_page == "Finding a Candidate":
    st.header("Finding a Candidate")

    # Add your LinkedIn candidate content here
    st.write("To find a candidate on LinkedIn, you can follow these steps:")

    # Example: Display step-by-step instructions
    st.subheader("Step 1: Define your requirements")
    st.write("Clearly define the skills, experience, and qualifications you are looking for in a candidate.")

    st.subheader("Step 2: Use LinkedIn search")
    st.write("Use the search feature on LinkedIn to find potential candidates matching your requirements.")

    st.subheader("Step 3: Refine your search")
    st.write("Narrow down your search results using filters like location, industry, experience level, etc.")

    st.subheader("Step 4: Review candidate profiles")
    st.write(
        "Carefully review the profiles of potential candidates to assess their suitability.")

    # Add more steps or content as needed
    # Example: Display a link to an external resource
    st.write(
        "For more information, you can refer to the [LinkedIn Recruiter Guide](https://www.linkedin.com/recruiter/guide/overview)")

# elif selected_page == "Screening Interview Questions":
#     st.header("Screening Interview Questions")

#     # Add your interview questions content here
#     st.write("Here are some interview questions:")

#     # Example: Display a list of questions
#     questions = [
#         "Tell me about yourself.",
#         "What are your strengths and weaknesses?",
#         "Why do you want to work for our company?",
#         "How do you handle challenges?",
#     ]
#     st.write(questions)

# elif selected_page == "Screening Interview Questions":
#         st.header("Screening Interview Questions")

#         # Input job role
#         job_role = st.text_input("Enter the job role")
#         openai.api_key = "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"
#         # Generate questions when button is clicked
#         if st.button("Generate Questions"):
#             if job_role:
#                 # Generate interview questions
#                 questions = generate_interview_questions(job_role)

#                 # Display the generated questions
#                 st.subheader("Generated Interview Questions:")
#                 for i, question in enumerate(questions, 1):
#                     st.write(f"{i}. {question}")
#             else:
#                 st.warning("Please enter a job role.")

elif selected_page == "Screening Interview Questions":
    st.header("Screening Interview Questions")

    # Input job role
    job_role = st.text_input("Enter the job role")
    # openai.api_key = "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"

    # Generate questions and answers when button is clicked
    if st.button("Generate Questions"):
        if job_role:
            # Generate interview questions and answers
            questions, answers, response = generate_interview_questions_and_answers(job_role)

            # Display the generated questions and answers
            
            if response:
                st.subheader("Generated Questions and Answers:")
                # for i, (question, answer) in enumerate(zip(questions, answers), 1):
                #     st.write(f"Q{i}. {question}")
                #     st.write(f"A{i}. {answer}")
                for text in response:
                    if text=="choices":
                        rtext= response[text][0]['text']
                        st.code(rtext)
                    # rtext = [choice.get('text', '').strip() for choice in response['choices']]
                    # st.code('\n'.join(rtext))
            else:
                st.warning("No questions generated for the given job role.")

            # Display the OpenAI API response text
            # st.subheader("OpenAI API Response:")
            # for choice in response['choices']:
            #     text = choice['text'].strip()
            #     if text.startswith("Q:"):
            #         st.write(f"Q: {text.replace('Q:', '').strip()}")
            #     elif text.startswith("A:"):
            #         st.write(f"A: {text.replace('A:', '').strip()}")
            
        else:
            st.warning("Please enter a job role.")


elif selected_page == "Skill Fitment Analysis":
    st.header("Skill Fitment Analysis")

    # Set page configuration
    # st.set_page_config(layout="wide")

    # Define an empty list to store terms
    terms = []

    # Load the 'sentence-transformers/all-mpnet-base-v2' model
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    # Define the terms to compare
    term_insertion = st.text_input('Enter your terms separated by commas')

    # Create button to trigger result
    results = st.button("Result")

    # Process terms when the button is clicked
    if results:

        # if the list ends in a comma, remove it
        terms = [term.strip()
                 for term in term_insertion.split(",") if term.strip() != ""]

        # Define headers for displaying terms and similarity score
        col1, col2, col3 = st.columns([0.3, 0.3, 0.3])

        # Display term1 header
        with col1:
            st.markdown("Term1")

        # Display term2 header
        with col2:
            st.markdown("Term2")

        # Display similarity score header
        with col3:
            st.markdown("Skill Fitment Analysis")

        # Calculate the cosine similarity between all pairs of terms
        similarities = []
        combination = combinations(terms, 2)
        for value in combination:
            term1, term2 = value
            term1_encode = model.encode(term1)
            term2_encode = model.encode(term2)

            with col1:
                st.markdown(term1)
            with col2:
                st.markdown(term2)
            with col3:
                # Calculate cosine similarity score
                cosine_sim = util.cos_sim(term1_encode, term2_encode)[0][0]
                similar_val = float(str(cosine_sim)[7:-1])
                if similar_val > 0.6:
                    st.markdown("Skills are very simillar - " +
                                str(similar_val)[:4])
                elif 0.5 < similar_val < 0.6:
                    st.markdown("Skills are quite simillar - " +
                                str(similar_val)[:4])
                elif 0.4 < similar_val <= 0.5:
                    st.markdown("Skills are disparate - " +
                                str(similar_val)[:4])
                else:
                    st.markdown("Skills are highly disparate - " +
                                str(similar_val)[:4])
                similarities.append(similar_val)

        # Calculate the SSDI
        mean_similarity = np.mean(similarities)
        ssdi = np.std(similarities) / mean_similarity

        # Display the SSDI results
        if ssdi > 0.2:
            st.success("These skills are unlikely to be found in the same candidate '%s': %.2f" % (
                ", ".join(terms), ssdi))
        elif ssdi >= 0.1 and ssdi <= 0.2:
            st.success("These skills are likely to be found in the same candidate '%s': %.2f" % (
                ", ".join(terms), ssdi))
        elif ssdi < 0.15:
            st.success("Theseskills are highly likely to be found in the same candidate '%s': %.2f" % (
                ", ".join(terms), ssdi))
