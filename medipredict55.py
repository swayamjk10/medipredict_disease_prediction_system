# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 19:42:14 2025

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
    page_icon=r"C:\Users\USer\Downloads\medipredictlogo.png",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling to match the attached UI
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
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        border: 1px solid #dee2e6;
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
        color: #333 !important; /* Default black for unselected */
        font-size: 16px !important;
    }
    .st-emotion-cache-1h7x7u9 .st-emotion-cache-1v0mbdj { /* Ensure unselected options stay black */
        color: #333 !important;
    }
    .st-emotion-cache-1h7x7u9:hover .st-emotion-cache-1v0mbdj { /* Hover effect for unselected */
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
    'heart': os.path.join(models_dir, 'heart_best_model.sav'),
    'breast_cancer': os.path.join(models_dir, 'breast_cancer_best_model.sav'),
    'hepatitis': os.path.join(models_dir, 'hepatitis_model (1).sav'),
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

# Disease information dictionary with detailed info like the Diabetes screenshot
disease_info = {
    'diabetes': {
        'description': "Diabetes mellitus is a chronic, metabolic disease characterized by elevated levels of blood glucose (or blood sugar), which leads over time to serious damage to the heart, blood vessels, eyes, kidneys, and nerves.",
        'risk_factors': "Risk factors include family history, obesity, unhealthy diet, physical inactivity, increasing age, high blood pressure, and ethnicity.",
        'prevention': "Prevention includes maintaining a healthy body weight, being physically active, eating a healthy diet, and avoiding tobacco use.",
        'remedies': "For more information, visit <a href='https://www.who.int/health-topics/diabetes#tab=tab_1' target='_blank'>World Health Organization (WHO)</a>.",
        'general_remedies': "- Monitor blood sugar levels regularly\n- Maintain a balanced diet\n- Exercise regularly\n- Avoid smoking"
    },
    'heart': {
        'description': "Cardiovascular disease (CVD) is a class of diseases that involve the heart or blood vessels, including coronary artery diseases like angina and myocardial infarction (heart attack).",
        'risk_factors': "Risk factors include high blood pressure, high blood cholesterol, diabetes, obesity, smoking, lack of physical activity, unhealthy diet, and excessive alcohol consumption.",
        'prevention': "Prevention includes quitting smoking, managing other health conditions like high blood pressure and diabetes, staying physically active, and eating a healthy diet.",
        'remedies': "For more information, visit <a href='https://www.heart.org/en/health-topics/heart-attack' target='_blank'>American Heart Association</a>.",
        'general_remedies': "- Take prescribed medications\n- Eat heart-healthy foods\n- Reduce stress\n- Maintain healthy weight"
    },
    'breast_cancer': {
        'description': "Breast cancer is cancer that forms in the cells of the breasts. After skin cancer, it’s the most common cancer diagnosed in women in the United States, but it can occur in men too.",
        'risk_factors': "Risk factors include increasing age, family history of breast cancer, obesity, exposure to radiation, early menstruation, and late menopause.",
        'prevention': "Prevention includes regular self-exams and mammograms, maintaining a healthy weight, and limiting alcohol consumption.",
        'remedies': "For more information, visit <a href='https://www.nationalbreastcancer.org/breast-cancer-facts' target='_blank'>National Breast Cancer Foundation, Inc.</a>.",
        'general_remedies': "- Follow medical treatment plan\n- Join support groups\n- Maintain nutrition\n- Gentle exercise"
    },
    'hepatitis': {
        'description': "Hepatitis C is a viral infection that causes liver inflammation, sometimes leading to serious liver damage. The hepatitis C virus (HCV) is usually spread through infected blood.",
        'risk_factors': "Risk factors include blood transfusions or organ transplants before 1992, injection drug use, hemodialysis, and being born to a mother with hepatitis C.",
        'prevention': "Prevention includes avoiding injection drug use, practicing safe hygiene, and ensuring safe blood transfusions and medical procedures.",
        'remedies': "For more information, visit <a href='https://www.cdc.gov/hepatitis/hcv/index.htm' target='_blank'>Centers for Disease Control and Prevention (CDC)</a>.",
        'general_remedies': "- Antiviral medications\n- Rest adequately\n- Healthy diet\n- Regular check-ups"
    },
    'kidney': {
        'description': "Chronic kidney disease (CKD) is a progressive loss in kidney function over months or years, leading to dangerous levels of fluid, electrolytes, and wastes building up in the body.",
        'risk_factors': "Risk factors include diabetes, high blood pressure, heart disease, family history of kidney disease, and older age.",
        'prevention': "Prevention includes managing diabetes and high blood pressure, maintaining a healthy weight, eating a healthy diet, and avoiding smoking and overuse of NSAIDs.",
        'remedies': "For more information, visit <a href='https://www.niddk.nih.gov/health-information/kidney-disease/chronic-kidney-disease-ckd' target='_blank'>National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)</a>.",
        'general_remedies': "- Follow dialysis if needed\n- Low-sodium diet\n- Medication adherence\n- Regular monitoring"
    }
}


# Enhanced sidebar navigation to match the attached UI
with st.sidebar:
    st.image(r"C:\Users\USer\Downloads\medipredictlogo.png", width=160)
    selected = option_menu(
        'MediPredict - Disease Prediction System',
        ['Diabetes Prediction', 'Heart Health Prediction', 'Breast Cancer Prediction', 
         'Hepatitis C Prediction', 'Kidney Disease Prediction'],
        icons=['droplet-fill', 'heart-pulse-fill', 'bandaid-fill', 'virus', 'meta'],
        menu_icon='hospital-fill',
        default_index=0)
    st.write("---")
    st.info("Select a prediction tool from above to begin")

# Function to create prediction section
def create_prediction_section(title, input_fields, model, prediction_logic, disease_key):
    st.title(f"{title} using ML")
    
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
            # Ensure all inputs are non-empty and convert to float, handle empty inputs gracefully
            cleaned_input = [float(x) for x in user_input if x and x.strip()]
            if len(cleaned_input) == len(input_fields):
                with st.spinner("Analyzing data..."):
                    prediction = model.predict([cleaned_input])
                    diagnosis = prediction_logic(prediction[0])
                    st.success(diagnosis)
                    
                    # Expanded disease info condition check
                    disease_keywords = [
                        "has", "diabetic", "malignant", "fibrosis", "cirrhosis", "hepatitis", 
                        "breast cancer", "kidney disease", "chronic kidney disease", "ckd", "hepatitis c"
                    ]
                    
                    if any(keyword in diagnosis.lower() for keyword in disease_keywords):
                        st.markdown(f"""
                            <div class='disease-info'>
                            <h3>More about {disease_key.capitalize()}</h3>
                            {disease_info[disease_key]['description']}<br><br>
                            <b>Risk Factors:</b><br>{disease_info[disease_key]['risk_factors']}<br><br>
                            <b>Prevention:</b><br>{disease_info[disease_key]['prevention']}<br><br>
                            <b>General Remedies:</b><br>{disease_info[disease_key]['general_remedies']}<br><br>
                            {disease_info[disease_key]['remedies']}
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("Please fill all fields with valid numerical values")
        except ValueError:
            st.error("Please enter valid numerical values")
    
    # Visualization
    with st.expander("Data Insights"):
        if submit_button and all(x.strip() for x in user_input if x):
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.barplot(x=list(input_fields.keys()), y=[float(x) for x in user_input if x])
            plt.xticks(rotation=45)
            st.pyplot(fig)



# Diabetes Prediction
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
        'diabetes'
    )

# Heart Health Prediction
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
        'heart'
    )

# Breast Cancer Prediction
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
        'breast_cancer'
    )

# Hepatitis C Prediction
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
        'hepatitis'
    )


# Kidney Disease Prediction
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
        'kidney'
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