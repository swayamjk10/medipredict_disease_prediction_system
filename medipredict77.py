# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:17:06 2025

@author: USer
"""

import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration with enhanced styling
st.set_page_config(
    page_title="MediPredict",
    layout="wide",
    page_icon="medipredictlogo.png",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling to match the UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 0;
    }
    .stButton>button {
        background-color: #ff4d4d;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        padding: 8px;
        border: 1px solid #ccc;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .st-expander {
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 10px;
    }
    .disease-info {
        background-color: #e6f0fa; /* Light blue background like in the image */
        padding: 15px; /* Reduced padding for compactness */
        border-radius: 10px;
        margin-top: 10px; /* Reduced margin */
        border: 1px solid #b3d4fc; /* Subtle border */
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); /* Subtle shadow */
        font-family: Arial, sans-serif;
        color: #333;
        line-height: 1.4; /* Reduced line height for compactness */
    }
    .disease-info h3 {
        color: #333;
        font-size: 18px; /* Slightly smaller heading */
        margin-bottom: 8px; /* Reduced margin */
    }
    .disease-info p {
        margin: 5px 0; /* Reduced paragraph spacing */
    }
    .disease-info b {
        color: #555;
        font-weight: 600;
    }
    .disease-info a {
        color: #0066cc;
        text-decoration: underline;
    }
    .disease-info a:hover {
        color: #003366;
    }
    /* Sidebar menu styling */
    .st-emotion-cache-1t8cb1q {
        background-color: #ffffff !important;
    }
    .st-emotion-cache-1h7x7u9 {
        background-color: #ff4d4d !important;
        color: white !important;
        border-radius: 5px !important;
    }
    .st-emotion-cache-1h7x7u9:hover {
        background-color: #e43b3b !important;
    }
    .st-emotion-cache-1v0mbdj {
        color: #333 !important;
        font-size: 16px !important;
    }
    .st-emotion-cache-1h7x7u9 .st-emotion-cache-1v0mbdj {
        color: #333 !important;
    }
    .st-emotion-cache-1h7x7u9:hover .st-emotion-cache-1v0mbdj {
        color: #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Working directory and model loading
working_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(working_dir, 'models')

# Model paths
model_paths = {
    'diabetes': os.path.join(models_dir, 'best_model.sav'),
    'heart': os.path.join(models_dir, 'heart_excellent_model.sav'),
    'breast_cancer': os.path.join(models_dir, 'breast_cancer_best_model.sav'),
    'hepatitis': os.path.join(models_dir, 'hepatitis_model_new.sav'),
    'kidney': os.path.join(models_dir, 'model.sav')
}

# Load models with error handling
models = {}
for name, path in model_paths.items():
    try:
        models[name] = pickle.load(open(path, 'rb'))
    except FileNotFoundError:
        st.error(f"Error: Model file {path} not found!")
        st.stop()

# Disease information dictionary with compact general remedies
disease_info = {
    'diabetes': {
        'description': "Diabetes mellitus is a chronic, metabolic disease characterized by elevated levels of blood glucose (or blood sugar), which leads over time to serious damage to the heart, blood vessels, eyes, kidneys, and nerves.",
        'risk_factors': "Risk factors include family history, obesity, unhealthy diet, physical inactivity, increasing age, high blood pressure, and ethnicity.",
        'prevention': "Prevention includes maintaining a healthy body weight, being physically active, eating a healthy diet, and avoiding tobacco use.",
        'remedies': "For more information, visit <a href='https://www.who.int/health-topics/diabetes#tab=tab_1' target='_blank'>World Health Organization (WHO)</a>.",
        'general_remedies': "Monitor blood sugar levels regularly • Maintain a balanced diet • Exercise regularly • Avoid smoking"
    },
    'heart': {
        'description': "Cardiovascular disease (CVD) is a class of diseases that involve the heart or blood vessels, including coronary artery diseases like angina and myocardial infarction (heart attack).",
        'risk_factors': "Risk factors include high blood pressure, high blood cholesterol, diabetes, obesity, smoking, lack of physical activity, unhealthy diet, and excessive alcohol consumption.",
        'prevention': "Prevention includes quitting smoking, managing other health conditions like high blood pressure and diabetes, staying physically active, and eating a healthy diet.",
        'remedies': "For more information, visit <a href='https://www.heart.org/en/health-topics/heart-attack' target='_blank'>American Heart Association</a>.",
        'general_remedies': "Take prescribed medications • Eat heart-healthy foods • Reduce stress • Maintain healthy weight"
    },
    'breast_cancer': {
        'description': "Breast cancer is cancer that forms in the cells of the breasts. After skin cancer, it’s the most common cancer diagnosed in women in the United States, but it can occur in men too.",
        'risk_factors': "Risk factors include increasing age, family history of breast cancer, obesity, exposure to radiation, early menstruation, and late menopause.",
        'prevention': "Prevention includes regular self-exams and mammograms, maintaining a healthy weight, and limiting alcohol consumption.",
        'remedies': "For more information, visit <a href='https://www.nationalbreastcancer.org/breast-cancer-facts' target='_blank'>National Breast Cancer Foundation, Inc.</a>.",
        'general_remedies': "Follow medical treatment plan • Join support groups • Maintain nutrition • Gentle exercise"
    },
    'hepatitis': {
        'description': "Hepatitis C is a viral infection that causes liver inflammation, sometimes leading to serious liver damage. The hepatitis C virus (HCV) is usually spread through infected blood.",
        'risk_factors': "Risk factors include blood transfusions or organ transplants before 1992, injection drug use, hemodialysis, and being born to a mother with hepatitis C.",
        'prevention': "Prevention includes avoiding injection drug use, practicing safe hygiene, and ensuring safe blood transfusions and medical procedures.",
        'remedies': "For more information, visit <a href='https://www.cdc.gov/hepatitis/hcv/index.htm' target='_blank'>Centers for Disease Control and Prevention (CDC)</a>.",
        'general_remedies': "Antiviral medications • Rest adequately • Healthy diet • Regular check-ups"
    },
    'kidney': {
        'description': "Chronic kidney disease (CKD) is a progressive loss in kidney function over months or years, leading to dangerous levels of fluid, electrolytes, and wastes building up in the body.",
        'risk_factors': "Risk factors include diabetes, high blood pressure, heart disease, family history of kidney disease, and older age.",
        'prevention': "Prevention includes managing diabetes and high blood pressure, maintaining a healthy weight, eating a healthy diet, and avoiding smoking and overuse of NSAIDs.",
        'remedies': "For more information, visit <a href='https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd' target='_blank'>National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)</a>.",
        'general_remedies': "Follow dialysis if needed • Low-sodium diet • Medication adherence • Regular monitoring"
    }
}

# Enhanced sidebar navigation
with st.sidebar:
    st.image("medipredictlogo.png", width=160)
    selected = option_menu(
        'MediPredict - Disease Prediction System',
        ['Diabetes Prediction', 'Heart Health Prediction', 'Breast Cancer Prediction', 
         'Hepatitis C Prediction', 'Kidney Disease Prediction'],
        icons=['droplet-fill', 'heart-pulse-fill', 'bandaid-fill', 'virus', 'meta'],
        menu_icon='hospital-fill',
        default_index=0)
    st.write("---")
    st.info("Select a prediction tool from above to begin")

# Function to create prediction section with variable info expander
def create_prediction_section(title, input_fields, model, prediction_logic, disease_key, variable_info):
    st.title(f"{title} using ML")
    
    # Variable Information Expander
    with st.expander("Input Variables Explanation"):
        st.markdown("### Understanding the Input Parameters")
        for var_name, info in variable_info.items():
            st.markdown(f"**{var_name}** ({info['unit']}):")
            st.write(f"- {info['description']}")
            if 'encoding' in info:
                st.write(f"- Numerical Encoding: {info['encoding']}")
            st.write("---")
    
    st.subheader("Enter Patient Data")
    with st.form(key=f"{title.lower().replace(' ', '_')}_form"):
        cols = st.columns(min(len(input_fields), 4))
        user_input = []
        
        for i, (label, placeholder) in enumerate(input_fields.items()):
            with cols[i % 4]:
                value = st.text_input(label, placeholder=placeholder, key=f"{title}_{label}")
                user_input.append(value if value else "0")  # Default to "0" if empty
        
        submit_button = st.form_submit_button(label="Predict Result")
    
    if submit_button:
        try:
            cleaned_input = [float(x) for x in user_input if x and x.strip()]
            if len(cleaned_input) == len(input_fields):
                with st.spinner("Analyzing data..."):
                    prediction = model.predict([cleaned_input])
                    diagnosis = prediction_logic(prediction[0])
                    st.success(diagnosis)
                    
                    disease_keywords = [
                        "has", "diabetic", "malignant", "fibrosis", "cirrhosis", "hepatitis", 
                        "breast cancer", "kidney disease", "chronic kidney disease", "ckd", "hepatitis c"
                    ]
                    
                    if any(keyword in diagnosis.lower() for keyword in disease_keywords):
                        st.markdown(f"""
                            <div class='disease-info'>
                            <h3>More about {disease_key.capitalize()}</h3>
                            <p>{disease_info[disease_key]['description']}</p>
                            <p><b>Risk Factors:</b> {disease_info[disease_key]['risk_factors']}</p>
                            <p><b>Prevention:</b> {disease_info[disease_key]['prevention']}</p>
                            <p><b>General Remedies:</b> {disease_info[disease_key]['general_remedies']}</p>
                            <p>{disease_info[disease_key]['remedies']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Please fill all fields with valid numerical values")
        except ValueError:
            st.error("Please enter valid numerical values")
    
    with st.expander("Data Insights"):
        if submit_button and all(x.strip() for x in user_input if x):
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x=list(input_fields.keys()), y=[float(x) for x in user_input if x])
            plt.xticks(rotation=45)
            st.pyplot(fig)

# Diabetes Prediction Variables Info
diabetes_var_info = {
    "Pregnancies": {"unit": "count", "description": "Number of times pregnant"},
    "Glucose": {"unit": "mg/dL", "description": "Plasma glucose concentration after 2 hours in an oral glucose tolerance test"},
    "Blood Pressure": {"unit": "mmHg", "description": "Diastolic blood pressure"},
    "Skin Thickness": {"unit": "mm", "description": "Triceps skin fold thickness"},
    "Insulin": {"unit": "μU/mL", "description": "2-Hour serum insulin"},
    "BMI": {"unit": "kg/m²", "description": "Body mass index (weight in kg/(height in m)²)"},
    "Diabetes Pedigree": {"unit": "score", "description": "Diabetes pedigree function (genetic risk score)"},
    "Age": {"unit": "years", "description": "Patient's age"}
}

if selected == 'Diabetes Prediction':
    fields = {
        "Pregnancies": "e.g., 2",
        "Glucose": "e.g., 120",
        "Blood Pressure": "e.g., 70",
        "Skin Thickness": "e.g., 20",
        "Insulin": "e.g., 80",
        "BMI": "e.g., 32",
        "Diabetes Pedigree": "e.g., 0.5",
        "Age": "e.g., 33"
    }
    create_prediction_section(
        "Diabetes Prediction",
        fields,
        models['diabetes'],
        lambda x: "The person is diabetic" if x == 1 else "The person is not diabetic",
        'diabetes',
        diabetes_var_info
    )

# Heart Health Prediction Variables Info
heart_var_info = {
    "Age": {"unit": "years", "description": "Patient's age"},
    "Sex": {"unit": "binary", "description": "Patient's gender", "encoding": "0 = Female, 1 = Male"},
    "Chest Pain": {"unit": "type", "description": "Chest pain type", "encoding": "0 = Typical angina, 1 = Atypical angina, 2 = Non-anginal pain, 3 = Asymptomatic"},
    "Resting BP": {"unit": "mmHg", "description": "Resting blood pressure"},
    "Cholesterol": {"unit": "mg/dL", "description": "Serum cholesterol"},
    "Fasting BS": {"unit": "binary", "description": "Fasting blood sugar > 120 mg/dL", "encoding": "0 = False, 1 = True"},
    "Resting ECG": {"unit": "type", "description": "Resting electrocardiographic results", "encoding": "0 = Normal, 1 = ST-T wave abnormality, 2 = Left ventricular hypertrophy"},
    "Max HR": {"unit": "bpm", "description": "Maximum heart rate achieved"},
    "Exercise Angina": {"unit": "binary", "description": "Exercise-induced angina", "encoding": "0 = No, 1 = Yes"},
    "Oldpeak": {"unit": "mm", "description": "ST depression induced by exercise relative to rest"},
    "Slope": {"unit": "type", "description": "Slope of peak exercise ST segment", "encoding": "0 = Upsloping, 1 = Flat, 2 = Downsloping"},
    "CA": {"unit": "count", "description": "Number of major vessels (0-3) colored by fluoroscopy"},
    "Thal": {"unit": "type", "description": "Thalassemia", "encoding": "0 = Normal, 1 = Fixed defect, 2 = Reversible defect"}
}

if selected == 'Heart Health Prediction':
    fields = {
        "Age": "e.g., 55",
        "Sex": "0=Female, 1=Male",
        "Chest Pain": "0-3",
        "Resting BP": "e.g., 120",
        "Cholesterol": "e.g., 200",
        "Fasting BS": "0 or 1",
        "Resting ECG": "0-2",
        "Max HR": "e.g., 150",
        "Exercise Angina": "0 or 1",
        "Oldpeak": "e.g., 1.5",
        "Slope": "0-2",
        "CA": "0-3",
        "Thal": "0-2"
    }
    create_prediction_section(
        "Heart Health Prediction",
        fields,
        models['heart'],
        lambda x: "The person has heart disease" if x == 1 else "The person has a healthy heart",
        'heart',
        heart_var_info
    )

# Breast Cancer Prediction Variables Info
breast_cancer_var_info = {
    "Mean Radius": {"unit": "mm", "description": "Mean radius of cell nuclei"},
    "Mean Texture": {"unit": "std dev", "description": "Mean standard deviation of gray-scale values"},
    "Mean Perimeter": {"unit": "mm", "description": "Mean perimeter of cell nuclei"},
    "Mean Area": {"unit": "mm²", "description": "Mean area of cell nuclei"},
    "Mean Smoothness": {"unit": "score", "description": "Mean local variation in radius lengths"},
    "Mean Compactness": {"unit": "score", "description": "Mean perimeter²/area - 1.0"},
    "Mean Concavity": {"unit": "score", "description": "Mean severity of concave portions of contour"},
    "Mean Concave Points": {"unit": "count", "description": "Mean number of concave portions of contour"},
    "Mean Symmetry": {"unit": "score", "description": "Mean symmetry measure"},
    "Mean Fractal Dim": {"unit": "score", "description": "Mean coastline approximation - 1"},
    "Radius SE": {"unit": "mm", "description": "Standard error of radius of cell nuclei"},
    "Texture SE": {"unit": "std dev", "description": "Standard error of gray-scale values"},
    "Perimeter SE": {"unit": "mm", "description": "Standard error of perimeter of cell nuclei"},
    "Area SE": {"unit": "mm²", "description": "Standard error of area of cell nuclei"},
    "Smoothness SE": {"unit": "score", "description": "Standard error of local variation in radius lengths"},
    "Compactness SE": {"unit": "score", "description": "Standard error of perimeter²/area - 1.0"},
    "Concavity SE": {"unit": "score", "description": "Standard error of severity of concave portions"},
    "Concave Points SE": {"unit": "count", "description": "Standard error of number of concave portions"},
    "Symmetry SE": {"unit": "score", "description": "Standard error of symmetry measure"},
    "Fractal Dim SE": {"unit": "score", "description": "Standard error of coastline approximation - 1"},
    "Worst Radius": {"unit": "mm", "description": "Worst (largest) radius of cell nuclei"},
    "Worst Texture": {"unit": "std dev", "description": "Worst standard deviation of gray-scale values"},
    "Worst Perimeter": {"unit": "mm", "description": "Worst perimeter of cell nuclei"},
    "Worst Area": {"unit": "mm²", "description": "Worst area of cell nuclei"},
    "Worst Smoothness": {"unit": "score", "description": "Worst local variation in radius lengths"},
    "Worst Compactness": {"unit": "score", "description": "Worst perimeter²/area - 1.0"},
    "Worst Concavity": {"unit": "score", "description": "Worst severity of concave portions of contour"},
    "Worst Concave Points": {"unit": "count", "description": "Worst number of concave portions of contour"},
    "Worst Symmetry": {"unit": "score", "description": "Worst symmetry measure"},
    "Worst Fractal Dim": {"unit": "score", "description": "Worst coastline approximation - 1"}
}

if selected == 'Breast Cancer Prediction':
    fields = {
        "Mean Radius": "e.g., 17.99",
        "Mean Texture": "e.g., 10.38",
        "Mean Perimeter": "e.g., 122.8",
        "Mean Area": "e.g., 1001",
        "Mean Smoothness": "e.g., 0.118",
        "Mean Compactness": "e.g., 0.277",
        "Mean Concavity": "e.g., 0.300",
        "Mean Concave Points": "e.g., 0.147",
        "Mean Symmetry": "e.g., 0.241",
        "Mean Fractal Dim": "e.g., 0.078",
        "Radius SE": "e.g., 1.095",
        "Texture SE": "e.g., 0.905",
        "Perimeter SE": "e.g., 8.589",
        "Area SE": "e.g., 153.4",
        "Smoothness SE": "e.g., 0.006",
        "Compactness SE": "e.g., 0.049",
        "Concavity SE": "e.g., 0.053",
        "Concave Points SE": "e.g., 0.015",
        "Symmetry SE": "e.g., 0.030",
        "Fractal Dim SE": "e.g., 0.006",
        "Worst Radius": "e.g., 25.38",
        "Worst Texture": "e.g., 17.33",
        "Worst Perimeter": "e.g., 184.6",
        "Worst Area": "e.g., 2019",
        "Worst Smoothness": "e.g., 0.162",
        "Worst Compactness": "e.g., 0.665",
        "Worst Concavity": "e.g., 0.711",
        "Worst Concave Points": "e.g., 0.265",
        "Worst Symmetry": "e.g., 0.460",
        "Worst Fractal Dim": "e.g., 0.118"
    }
    create_prediction_section(
        "Breast Cancer Prediction",
        fields,
        models['breast_cancer'],
        lambda x: "The person has Breast Cancer (Malignant)" if x == 1 else "The person does not have Breast Cancer (Benign)",
        'breast_cancer',
        breast_cancer_var_info
    )

# Hepatitis C Prediction Variables Info
hepatitis_var_info = {
    "Age": {"unit": "years", "description": "Patient's age"},
    "Sex": {"unit": "category", "description": "Patient's gender", "encoding": "1 = Male, 2 = Female"},
    "Albumin": {"unit": "g/L", "description": "Albumin level in blood"},
    "Alkaline Phosphatase": {"unit": "U/L", "description": "Alkaline phosphatase enzyme level"},
    "ALT": {"unit": "U/L", "description": "Alanine aminotransferase enzyme level"},
    "AST": {"unit": "U/L", "description": "Aspartate aminotransferase enzyme level"},
    "Bilirubin": {"unit": "mg/dL", "description": "Bilirubin level in blood"}
}

if selected == 'Hepatitis C Prediction':
    fields = {
        "Age": "e.g., 45",
        "Sex": "1=Male, 2=Female",
        "Albumin": "e.g., 40",
        "Alkaline Phosphatase": "e.g., 85",
        "ALT": "e.g., 35",
        "AST": "e.g., 30",
        "Bilirubin": "e.g., 1.0"
    }
    create_prediction_section(
        "Hepatitis C Prediction",
        fields,
        models['hepatitis'],
        lambda x: f"Predicted Condition: {['Healthy', 'Fibrosis', 'Cirrhosis', 'Hepatitis'][x]}" if x in [0, 1, 2, 3] else "Unknown Category",
        'hepatitis',
        hepatitis_var_info
    )

# Kidney Disease Prediction Variables Info
kidney_var_info = {
    "Blood Pressure": {"unit": "mmHg", "description": "Diastolic blood pressure"},
    "Specific Gravity": {"unit": "ratio", "description": "Urine specific gravity"},
    "Albumin": {"unit": "g/dL", "description": "Albumin level in urine"},
    "Blood Glucose Random": {"unit": "mg/dL", "description": "Random blood glucose level"},
    "Blood Urea": {"unit": "mg/dL", "description": "Blood urea nitrogen level"},
    "Serum Creatinine": {"unit": "mg/dL", "description": "Serum creatinine level"},
    "Sodium": {"unit": "mEq/L", "description": "Sodium level in blood"},
    "Hemoglobin": {"unit": "g/dL", "description": "Hemoglobin level"},
    "Packed Cell Volume": {"unit": "%", "description": "Percentage of red blood cells in blood"},
    "Red Blood Cell Count": {"unit": "millions/cmm", "description": "Red blood cell count"},
    "Hypertension": {"unit": "binary", "description": "Presence of hypertension", "encoding": "0 = No, 1 = Yes"},
    "Diabetes Mellitus": {"unit": "binary", "description": "Presence of diabetes", "encoding": "0 = No, 1 = Yes"}
}

if selected == 'Kidney Disease Prediction':
    fields = {
        "Blood Pressure": "e.g., 80",
        "Specific Gravity": "e.g., 1.020",
        "Albumin": "e.g., 1",
        "Blood Glucose Random": "e.g., 150",
        "Blood Urea": "e.g., 35",
        "Serum Creatinine": "e.g., 1.2",
        "Sodium": "e.g., 135",
        "Hemoglobin": "e.g., 14.5",
        "Packed Cell Volume": "e.g., 42",
        "Red Blood Cell Count": "e.g., 5.2",
        "Hypertension": "0=No, 1=Yes",
        "Diabetes Mellitus": "0=No, 1=Yes"
    }
    create_prediction_section(
        "Kidney Disease Prediction",
        fields,
        models['kidney'],
        lambda x: "The person has Chronic Kidney Disease" if x == 1 else "The person does not have CKD",
        'kidney',
        kidney_var_info
    )

# Footer
st.markdown("""
    <div style='text-align: center; color: #666;'>
        MediPredict machine learning model can make mistakes. Check important info.
    </div>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Made with ❤️ in India | Powered by MediPredict | © 2025 | Built with Streamlit by Swayam Korgaonkar
    </div>
""", unsafe_allow_html=True)
