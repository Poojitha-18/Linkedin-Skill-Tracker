import streamlit as st
import requests
import subprocess

import streamlit as st
import numpy as np
from itertools import combinations
from sentence_transformers import SentenceTransformer, util
import sqlite3
from streamlit.components.v1 import html
from streamlit import components


def generate_skill_suggestions(input_skills):
    available_skills = ['Python', 'JavaScript', 'Java', 'HTML', 'CSS', 'SQL','Data Analysis','Machine Learning']
    suggestions = []

    # Split the input skills by commas
    skills = [skill.strip() for skill in input_skills.split(',')]

    # Generate suggestions based on the available skills
    for skill in skills:
        matching_skills = [available_skill for available_skill in available_skills if skill.lower() in available_skill.lower()]
        suggestions.extend(matching_skills)

        # Add partial matches
        partial_matches = [available_skill for available_skill in available_skills if skill.lower() in available_skill.lower() and skill.lower() != available_skill.lower()]
        suggestions.extend(partial_matches)

    # Remove duplicates and sort the suggestions
    suggestions = sorted(list(set(suggestions)))

    return suggestions

# Function to start the Flask app
def start_flask_app():
    subprocess.Popen(['python', 'app.py'])

# Start the Flask app when the Streamlit app runs
if __name__ == '__main__':
    # Start Flask app as a separate process
    start_flask_app()

# Add banner with logo
col1, col2 = st.columns([1, 3])
with col1:
    logo_image = st.image("ust_logo.png", width=100)

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
    st.markdown('<h1 class="title">TALENT INSIGHT</h1>', unsafe_allow_html=True)

FLASK_URL = 'http://localhost:8080'

# Menu bar
# selected_page = st.sidebar.selectbox(
#     "Go to",
#     ("Home", "Skill Search", "Profile Management", "Job Description Match", "JD Creation", "Finding a Candidate",
#      "Interview Questions", "Similarity Score"),
# )


# Define the options with icons
options = {
    "Home": "<i class='fas fa-home'></i>",
    "Skill Search": "<i class='fas fa-search'></i>",
    "Profile Management": "<i class='fas fa-user'></i>",
    "Job Description Match": "<i class='fas fa-briefcase'></i>",
    "JD Creation": "<i class='fas fa-file-alt'></i>",
    "Finding a Candidate": "<i class='fas fa-users'></i>",
    "Interview Questions": "<i class='fas fa-question-circle'></i>",
    "Similarity Score": "<i class='fas fa-percent'></i>"
}

# Get the selected page
selected_page = st.sidebar.selectbox(
    "Go to",
    list(options.keys()),
    format_func=lambda page: html(options[page], parse_html=True)
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
        if st.button("Interview Questions", help="Interview questions generator"):
            selected_page = "Interview Questions"


    
if selected_page == "Skill Search":
    st.header("Skill Search")
    
    # Skills input
    skills = st.text_input('Skills (comma-separated)', help='Enter the skills to search for', key='skill_input_search')
    
    
    # Skill suggestions
    skill_suggestions = generate_skill_suggestions(skills)
    
    if skill_suggestions:
        st.write('Skill Suggestions:', ', '.join(skill_suggestions))

    if st.button('Search'):
        try:
            # Make a request to the Flask API endpoint
            response = requests.get(f'{FLASK_URL}/search', params={'skills': skills})
            
            if response.status_code == 200:
                # Display the search results
                results = response.json()
                
                if not results:  # Check if the results are empty
                    st.warning('No results found. Please try a different search.')
                else:
                    st.table(results)
            else:
                # Display an error message if the request fails
                st.error('An error occurred during the search. Please try again.')
        
        except requests.exceptions.RequestException as e:
            # Handle the exception if a request error occurs
            st.error('An error occurred during the search. Please try again.')
            
            
# elif selected_page == "Profile Management":
#     st.header("Profile Management Tool'")
#     user_id = st.text_input('Enter user ID', key='user_id')
#     if st.button('Get Profile and Skills'):
#             response_profile = requests.get(f'{FLASK_URL}/profile', params={'user_id': user_id})
#             response_skills = requests.get(f'{FLASK_URL}/skills', params={'user_id': user_id})
#             if response_profile.status_code == 200 and response_skills.status_code == 200:
#                 profile_data = response_profile.json()
#                 skills_data = response_skills.json()
#                 st.write('Profile Data:')
#                 st.write('First Name:', profile_data['first_name'])
#                 st.write('Last Name:', profile_data['last_name'])
#                 st.write('Skills Data:')
#                 st.write('Skills:', skills_data['skills'])
#             else:
#                 st.error('An error occurred while retrieving the profile and skills data. Please try again.')

elif selected_page == "Profile Management":
    st.header("Profile Management Tool")

    # Option to search by user ID, first name, last name, or both
    search_option = st.radio("Search by", ("User ID", "First Name", "Last Name", "Full Name"), index=0)

    if search_option == "User ID":
        user_identifier = st.text_input('Enter user ID', key='user_id')
    elif search_option == "First Name":
        user_identifier = st.text_input('Enter first name', key='first_name')
    elif search_option == "Last Name":
        user_identifier = st.text_input('Enter last name', key='last_name')
    else:
        first_name = st.text_input('Enter first name', key='first_name')
        last_name = st.text_input('Enter last name', key='last_name')
        user_identifier = first_name + " " + last_name

    if st.button('Get Profile and Skills'):
        connection = sqlite3.connect('new_database.db')
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
                WHERE first_name=?
            ''', (user_identifier,))
            user_data = cursor.fetchone()
        elif search_option == "Last Name":
            cursor.execute('''
                SELECT * FROM users
                WHERE last_name=?
            ''', (user_identifier,))
            user_data = cursor.fetchone()
        else:
            cursor.execute('''
                SELECT * FROM users
                WHERE first_name=? AND last_name=?
            ''', (first_name, last_name))
            user_data = cursor.fetchone()

        if user_data:
            user_id = user_data[0]

            # Retrieve profile data
            profile_data = {
                'first_name': user_data[1],
                'last_name': user_data[2],
                'occupation': user_data[3],
                'headline': user_data[4],
                'summary': user_data[5],
                'city': user_data[6],
                'country': user_data[7]
            }

            # Retrieve skills data
            cursor.execute('''
                SELECT skill_name FROM skills
                WHERE user_id=?
            ''', (user_id,))
            skills_data = cursor.fetchall()
            skills_list = [skill[0] for skill in skills_data]

            st.write('Profile Data:')
            st.write('First Name:', profile_data['first_name'])
            st.write('Last Name:', profile_data['last_name'])
            st.write('Occupation:', profile_data['occupation'])
            st.write('Headline:', profile_data['headline'])
            st.write('Summary:', profile_data['summary'])
            st.write('City:', profile_data['city'])
            st.write('Country:', profile_data['country'])

            st.write('Skills Data:')
            st.write('Skills:', skills_list)
        else:
            st.error('User not found.')

elif selected_page == "Job Description Match":
    st.header("Job Description Match")
    # Job Description Match endpoint
    job_description = st.text_area('Enter job description', key='job_description')
    if st.button('Match Candidates'):
        response_candidates = requests.post(f'{FLASK_URL}/match', json={'job_description': job_description})
        if response_candidates.status_code == 200:
            matching_candidates = response_candidates.json()
            st.table(matching_candidates)
        else:
            st.error('An error occurred during candidate matching. Please try again.')

elif selected_page == "JD Creation":
    st.header("JD Creation")
    # Add your JD creation content here
  
    st.subheader("Job Title and Department")
    job_title = st.text_input("Job Title", value="Streamlit Developer")
    department = st.text_input("Department", value="Software Development")

    st.subheader("Reporting Structure")
    reporting_structure = st.text_input("Reporting Structure", value="Reports to the Engineering Manager")

    st.subheader("Job Summary")
    job_summary = st.text_area("Job Summary", value="We are seeking a talented Streamlit Developer to join our Software Development team. The Streamlit Developer will be responsible for designing and developing interactive web applications using Streamlit framework. The ideal candidate should have a strong background in web development, proficiency in Python programming, and a passion for creating intuitive user interfaces.")

    st.subheader("Key Responsibilities")
    key_responsibilities = st.text_area("Key Responsibilities", value="Collaborate with cross-functional teams to gather requirements and understand application needs.\nDesign and develop web applications using Streamlit framework and Python programming language.\nCreate visually appealing and user-friendly interfaces that provide a seamless user experience.\nImplement data visualization and interactive features to enhance application functionality.\nIntegrate APIs and third-party services to fetch and display data within the applications.\nPerform testing and debugging of the applications to ensure proper functionality and fix any issues or bugs.\nOptimize and refactor code to improve performance and maintainability.\nStay up-to-date with the latest Streamlit developments and best practices in web development.\nCollaborate with team members to troubleshoot and resolve technical challenges.\nDocument code, processes, and application architectures for future reference.")

    st.subheader("Qualifications and Skills")
    qualifications = st.text_area("Qualifications and Skills", value="Bachelor's degree in Computer Science, Software Engineering, or a related field.\nProven experience in web development with a focus on Python.\nProficiency in Python programming and experience with frameworks such as Streamlit.\nStrong understanding of HTML, CSS, and JavaScript for building interactive web interfaces.\nFamiliarity with data visualization libraries, such as Matplotlib or Plotly, is a plus.\nExperience with version control systems, such as Git, for collaborative development.\nExcellent problem-solving and analytical skills.\nStrong communication and teamwork abilities.\nAbility to work in a fast-paced and agile development environment.")

    # Display the Job Description
    st.header("Job Description: " + job_title)
    st.subheader("Department: " + department)
    st.write(reporting_structure)
    st.write("---")
    st.subheader("Job Summary")
    st.write(job_summary)
    st.write("---")
    st.subheader("Key Responsibilities")
    for i, responsibility in enumerate(key_responsibilities.split("\n"), start=1):
        st.write(f"{i}. {responsibility}")
    st.write("---")
    st.subheader("Qualifications and Skills")
    for i, qualification in enumerate(qualifications.split("\n"), start=1):
        st.write(f"{i}. {qualification}")
    
elif selected_page== "Finding a Candidate":
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
    st.write("Carefully review the profiles of potential candidates to assess their suitability.")

    # Add more steps or content as needed
    # Example: Display a link to an external resource
    st.write("For more information, you can refer to the [LinkedIn Recruiter Guide](https://www.linkedin.com/recruiter/guide/overview)")

elif selected_page == "Interview Questions":
    st.header("Interview Questions")

    # Add your interview questions content here
    st.write("Here are some interview questions:")

    # Example: Display a list of questions
    questions = [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why do you want to work for our company?",
        "How do you handle challenges?",
    ]
    st.write(questions)

elif selected_page == "Similarity Score":
    st.header("Similarity Fitment Analysis")

    # Set page configuration
    #st.set_page_config(layout="wide")

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
        terms = [term.strip() for term in term_insertion.split(",") if term.strip() != ""]
    
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
            st.markdown("Similarity Score")

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
                    st.markdown("Skills are quite simillar - " + str(similar_val)[:4])
                elif 0.4 < similar_val <= 0.5:
                    st.markdown("Skills are disparate - " + str(similar_val)[:4])
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
