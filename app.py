from pathlib import Path

import streamlit as st
from PIL import Image


# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
resume_file = current_dir / "assets" / "CV_2024-09-20.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"


# --- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Basile Rommes"
PAGE_ICON = ":wave:"
NAME = "Basile Rommes"
DESCRIPTION = "Data Scientist, MSc. Bioinformatics"
EMAIL = "basilerommes@hotmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/basile-rommes/",
    "GitHub": "https://github.com/romba050",
}
PROJECTS = {
    "👁️ : Blood Vessel Segmentation Master Thesis - Leveraging DNN and Bayesian Modeling to find blood vessels": "https://github.com/romba050/MFN_RBV_segmentation",
    "🧬 Protein Superpositioning - Using Bayesian Inference to position protein strctures over each other": "https://github.com/romba050/Protein_Superpositioning_using_Bayesian_Inference",
    "🩻 Computer Tomography - Jupyter Notebook on how to use Fourrier Transform to calculate a CT": "https://nbviewer.org/github/romba050/computer_tomography/blob/master/ex3.ipynb",
    "🎵 Spotle Assist Project - The smart assistant to the Spotle artist guessing game": "https://spotle.streamlit.app/",
    "📊 NEAR Data Request - Plan your data application to conduct Aging Research": "https://near-data-request.streamlit.app/",
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
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label=" 📄 Download Resume",
        data=PDFbyte,
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    st.write("📫", EMAIL)


# --- SOCIAL LINKS ---
st.write('\n')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].link_button(f"{platform}", url=f"{link}")

# --- About ---
st.write("""
Data Scientist with Master's Degree in Bioinformatics and focus on machine learning, computer vision, structural bioinformatics and data visualization. 4 years of professional experience in Data Management and Data Harmonisation. Wide area of expertise including data analysis, WebDev and task automation.
"""
)


# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience & Qualifications")
st.write(
"""
- ✔️ 4 years experience in clinical data management
- ✔️ Strong hands on experience and knowledge in Python and R
- ✔️ Focus on Bioinformatics in Protein Structures and Medicla Image Analysis 
- ✔️ Good understanding of statistical principles and Machine Learning and their respective applications
- ✔️ Experience in WebDev using PHP, Wordpress or Python Libraries
""" #- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
)


# --- SKILLS ---
st.write('\n')
st.subheader("Hard Skills")
st.write(
    """
- 👩‍💻 Programming: Python (Scikit-learn, Pandas), R, Unix/Bash, C++, SQL, PHP
- 📊 Data Visulization: Matplotlib, Plotly, Streamlit
- 📚 Modeling: Convolutional Neural Networks, Bayesian Maximum a posteriori estimation, Logistic regression, Linear regression, Decision trees
- 🗄️ Databases and Cloud: MySQL, MariaDB, AWS
"""
)


# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History")
st.write("---")

# --- JOB 1
st.write("🚧", "**Software Developer | Karolinska Institutet**")
st.write("09/2022 - 09/2024")
st.write(
    """
- ► Data harmonization for Epidemiological Research
- ► Maintenance of the [NEAR database](https://neardb.near-aging.se/) and Website
- ► Building pipelines in R and python,
- ► WebDev in PHP and Wordpress
"""
)

# --- JOB 2
st.write('\n')
st.write("🚧", "**Research and Development Specialist| Luxembourg Centre for Systems Biomedicine**")
st.write("09/2020 - 08/2022")
st.write(
    """
- ► Data management and curation within the european BIOMAP and the luxembourgish CON-VINCE projects
- ► Using RedCAP to capture medical data
- ► Building re-usable data pipelines in KNIME
- ► Teaching Master of Data Science Course in Python and R Programming
"""
)

# --- Projects & Accomplishments ---
st.write('\n')
st.subheader("Projects & Accomplishments")
st.write("---")
for project, link in PROJECTS.items():
    st.write(f"[{project}]({link})")
