from pathlib import Path

import streamlit as st
from PIL import Image


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "CV_Short_Basile_Rommes_2025-07-02.pdf"
profile_pic = current_dir / "assets" / "profile-pic-2_2025-12-19.png" # "profile-pic-spiral.png"
# profile_pic = current_dir / "assets" / "profile-pic_2024-10-03.png"

# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Basile Rommes"
PAGE_ICON = ":wave:"
NAME = "Basile Rommes"
DESCRIPTION = " MSc Bioinformatics"
EMAIL = "basilerommes@hotmail.com"
LOCATION = "Stockholm, Sweden"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/basile-rommes/",
    "GitHub": "https://github.com/romba050",
}
PROJECTS = {
    "👁️ Blood Vessel Segmentation (Master Thesis) – Leveraging Neural Networks and Probability Theory to find blood vessels": "https://github.com/romba050/MFN_RBV_segmentation",
    "👁️ Blood Vessel Segmentation Webapp – Interactive webapp for vessel segmentation": "https://basile-rommes.com/bvs",
    "🧬 Protein Superpositioning – Using Bayesian Inference to position protein structures over each other": "https://github.com/romba050/Protein_Superpositioning_using_Bayesian_Inference",
    #"🩻 Computer Tomography – Jupyter Notebook on how to use Fourier Transform to calculate a CT": "https://nbviewer.org/github/romba050/computer_tomography/blob/master/ex3.ipynb",
    "🎵 Spotle Assist Project – The smart assistant to the Spotle artist guessing game": "https://basile-rommes.com/spotle/", # "https://spotle.streamlit.app/",
    "📊 NEAR Data Request Form – Plan your data application to conduct ageing research": "https://basile-rommes.com/near-data-request/", # "https://near-data-request.streamlit.app/",
    "🍰 Swedish Cake Day – Find out which cake is celebrated today in Sweden, the country of pastries": "https://basile-rommes.com/cake/", # "https://whatcakeday.streamlit.app/",
    "🤖 AI Art Turing Test – Test your ability to distinguish AI-generated images from human art": "https://basile-rommes.com/ai-art-quiz/",
}

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
    PDFbyte = pdf_file.read()
profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    # Create columns to position the image between left and center
    _, center_col, _ = st.columns([0.5, 2, 0.5])
    with center_col:
        st.image(profile_pic, use_column_width=True)
        # get original width with:
        # sips -g pixelWidth -g pixelHeight "assets/profile-pic_2024-10-03.png"


with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    ## Removed CV because it is too much work to change all the time
    # st.download_button(
    #     label=" 📄 Download Resume",
    #     data=PDFbyte,
    #     file_name=resume_file.name,
    #     mime="application/octet-stream",
    # )
    st.write("📫", EMAIL)
    st.write("📍", LOCATION)


# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    with cols[index]:
        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration: none;"><button style="background-color: #FFD700; color: black; border: none; padding: 12px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold;">{platform}</button></a>', unsafe_allow_html=True)
# cols = st.columns(len(SOCIAL_MEDIA))
# for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
#     with cols[index]:
#         container = st.container()
#         with container:
#             st.markdown(f'<div style="display: flex; justify-content: center;"><a href="{link}" target="_blank" style="text-decoration: none;"><button style="background-color: #ff4b4b; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">{platform}</button></a></div>', unsafe_allow_html=True)


# # --- About ---
# st.write("""
# Data scientist with a master's degree in bioinformatics and a focus on machine learning, computer vision, structural bioinformatics and data visualisation. 4 years of professional experience in data management and data harmonisation. Wide area of expertise, including data analysis, web development and task automation.
# """
# )

# --- Projects & Accomplishments ---
st.write('\n')
st.markdown('<h3 style="color: #FFD700;">Projects & WebApps</h3>', unsafe_allow_html=True)
st.write("---")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")


# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.markdown('<h3 style="color: #FFD700;">Experience & Qualifications</h3>', unsafe_allow_html=True)
st.write("---")
st.write(
"""
► 4 years of experience in clinical data management\n
► Strong hands-on experience and knowledge in Python and R\n
► Focus on bioinformatics in protein structures and medical image analysis\n
► Good understanding of statistical principles and machine learning and their respective applications\n
► Experience in WebDev using PHP, WordPress or Python libraries\n
""" #- ► Excellent team-player and displaying strong sense of initiative on task\n
)


# --- SKILLS ---
st.write('\n')
st.markdown('<h3 style="color: #FFD700;">Skills</h3>', unsafe_allow_html=True)
st.write("---")
st.write(
    """
👨🏻‍💻 Programming: Python (Scikit-learn, Pandas), R, Unix/Bash, C++, SQL, PHP\n
📊 Data Visualisation: Matplotlib, Plotly, Streamlit\n
🤖 Machine Learning: PyTorch, Keras\n
📚 Modeling: Convolutional Neural Networks, Bayesian Maximum a posteriori estimation, logistic regression, linear regression, decision trees\n
🗄️ Databases and Cloud: MySQL, MariaDB, AWS, Docker, InfluxDB, Grafana\n
"""
)
# # DevOps: Git, CI/CD

# --- WORK Experience ---
st.write('\n')
st.markdown('<h3 style="color: #FFD700;">Work Experience</h3>', unsafe_allow_html=True)
st.write("---")

# --- JOB 1
st.write("👨🏻‍💻", "**Software Developer | Karolinska Institutet**")
st.write("09/2022 - 09/2024")
st.write(
    """
- ► Data harmonisation for epidemiological research\n
- ► Maintenance of the [NEAR database](https://neardb.near-aging.se/) and Website\n
- ► Building pipelines in R and Python,\n
- ► WebDev in PHP and WordPress
"""
)

# --- JOB 2
st.write('\n')
st.write("👨🏻‍💻", "**Research and Development Specialist | Luxembourg Centre for Systems Biomedicine**")
st.write("09/2020 - 08/2022")
st.write(
    """
- ► Data management and curation within the european BIOMAP and the luxembourgish CON-VINCE projects\n
- ► Using RedCAP to capture medical data\n
- ► Building re-usable data pipelines in KNIME\n
- ► Teaching in the Master of Data Science Course "Python and R Programming"
"""
)
