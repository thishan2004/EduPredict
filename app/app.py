import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="EduPredict",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Load Data and Models
# -----------------------------
@st.cache_data
def load_data():
    student_report = pd.read_csv("data/processed/student_risk_report.csv")
    risk_summary = pd.read_csv("data/processed/risk_summary.csv")
    risk_habit_summary = pd.read_csv("data/processed/risk_habit_summary.csv")
    feature_importance = pd.read_csv("data/processed/feature_importance.csv")
    regression_results = pd.read_csv("data/processed/regression_model_results.csv")
    classification_results = pd.read_csv("data/processed/classification_model_results.csv")
    return (
        student_report,
        risk_summary,
        risk_habit_summary,
        feature_importance,
        regression_results,
        classification_results
    )

@st.cache_resource
def load_models():
    exam_score_model = joblib.load("models/final_exam_score_model.pkl")
    category_model = joblib.load("models/final_performance_category_model.pkl")
    feature_columns = joblib.load("models/feature_columns.pkl")
    return exam_score_model, category_model, feature_columns


student_report, risk_summary, risk_habit_summary, feature_importance, regression_results, classification_results = load_data()
exam_score_model, category_model, feature_columns = load_models()

# -----------------------------
# Helper Functions
# -----------------------------
def assign_risk_level(score):
    if score >= 80:
        return "Low Risk"
    elif score >= 60:
        return "Medium Risk"
    else:
        return "High Risk"


def generate_recommendations(
    study_hours,
    social_media_hours,
    netflix_hours,
    attendance,
    sleep_hours,
    mental_health,
    exercise_frequency,
    diet_quality,
    internet_quality
):
    recommendations = []

    if study_hours < 2:
        recommendations.append("Increase daily study hours to at least 2-3 hours.")

    if social_media_hours > 3:
        recommendations.append("Reduce social media usage to improve focus.")

    if netflix_hours > 2:
        recommendations.append("Reduce entertainment screen time.")

    if attendance < 75:
        recommendations.append("Improve class attendance to at least 80%.")

    if sleep_hours < 6:
        recommendations.append("Improve sleep routine and aim for 7-8 hours of sleep.")

    if mental_health < 5:
        recommendations.append("Focus on mental well-being and seek support if needed.")

    if exercise_frequency < 2:
        recommendations.append("Increase weekly physical activity for better balance.")

    if diet_quality == "Poor":
        recommendations.append("Improve diet quality to support better academic performance.")

    if internet_quality == "Poor":
        recommendations.append("Improve internet access or use campus resources for online learning.")

    if len(recommendations) == 0:
        recommendations.append("Maintain current positive study and lifestyle habits.")

    return recommendations


def prepare_input(data):
    input_df = pd.DataFrame([data])
    input_encoded = pd.get_dummies(input_df)

    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0

    input_encoded = input_encoded[feature_columns]

    return input_encoded


# -----------------------------
# App Title
# -----------------------------
st.title("🎓 EduPredict")
st.subheader("AI-Powered Student Learning Analytics & Academic Success Platform")

tabs = st.tabs([
    "📊 Overview",
    "📈 Dataset Insights",
    "🤖 Model Performance",
    "🎯 Student Predictor",
    "💡 Recommendations"
])

# -----------------------------
# Overview Page
# -----------------------------
with tabs[0]:
    st.header("Project Overview")

    st.write(
        """
        EduPredict is a machine learning-powered academic success platform that analyzes
        student habits, lifestyle factors, and academic behavior to predict exam performance,
        identify risk levels, and provide personalized improvement recommendations.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Students Analyzed", len(student_report))

    with col2:
        st.metric("Features Used", len(feature_columns))

    with col3:
        st.metric("Best Classification F1", "82.5%")

    st.markdown("### Key Capabilities")
    st.write(
        """
        - Predict exact exam score using machine learning
        - Classify students into performance categories
        - Identify academic risk level
        - Analyze important performance factors
        - Generate personalized recommendations
        """
    )

# -----------------------------
# Dataset Insights Page
# -----------------------------
with tabs[1]:
    st.header("Dataset Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Academic Risk Distribution")
        fig = px.bar(
            risk_summary,
            x="Risk Level",
            y="Student Count",
            title="Student Count by Academic Risk Level"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Important Features")
        top_features = feature_importance.head(10)
        fig = px.bar(
            top_features,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top Factors Affecting Exam Score"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Habits by Risk Level")
    st.dataframe(risk_habit_summary)

# -----------------------------
# Model Performance Page
# -----------------------------
with tabs[2]:
    st.header("Model Performance")

    st.subheader("Regression Model Results")
    st.dataframe(regression_results)

    st.subheader("Classification Model Results")
    st.dataframe(classification_results)

    st.markdown(
        """
        **Final Selected Models**
        - Exam Score Prediction: Linear Regression
        - Performance Category Prediction: Logistic Regression
        """
    )

# -----------------------------
# Student Predictor Page
# -----------------------------
with tabs[3]:
    st.header("Student Performance Predictor")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 15, 30, 20)
        gender = st.selectbox("Gender", ["Male", "Female"])
        study_hours = st.slider("Study Hours per Day", 0.0, 10.0, 2.0)
        social_media_hours = st.slider("Social Media Hours per Day", 0.0, 10.0, 2.0)
        netflix_hours = st.slider("Netflix Hours per Day", 0.0, 10.0, 1.0)
        part_time_job = st.selectbox("Part-Time Job", ["No", "Yes"])

    with col2:
        attendance = st.slider("Attendance Percentage", 0.0, 100.0, 80.0)
        sleep_hours = st.slider("Sleep Hours", 0.0, 12.0, 7.0)
        diet_quality = st.selectbox("Diet Quality", ["Poor", "Fair", "Good"])
        exercise_frequency = st.slider("Exercise Frequency per Week", 0, 7, 2)
        parental_education_level = st.selectbox(
            "Parental Education Level",
            ["High School", "Bachelor", "Master"]
        )
        internet_quality = st.selectbox("Internet Quality", ["Poor", "Average", "Good"])
        mental_health = st.slider("Mental Health Rating", 1, 10, 6)
        extracurricular = st.selectbox("Extracurricular Participation", ["No", "Yes"])

    if st.button("Predict Student Performance"):
        input_data = {
            "age": age,
            "gender": gender,
            "study_hours_per_day": study_hours,
            "social_media_hours": social_media_hours,
            "netflix_hours": netflix_hours,
            "part_time_job": part_time_job,
            "attendance_percentage": attendance,
            "sleep_hours": sleep_hours,
            "diet_quality": diet_quality,
            "exercise_frequency": exercise_frequency,
            "parental_education_level": parental_education_level,
            "internet_quality": internet_quality,
            "mental_health_rating": mental_health,
            "extracurricular_participation": extracurricular
        }

        model_input = prepare_input(input_data)

        predicted_score = exam_score_model.predict(model_input)[0]
        predicted_category = category_model.predict(model_input)[0]
        risk_level = assign_risk_level(predicted_score)

        st.success(f"Predicted Exam Score: {predicted_score:.2f}")
        st.info(f"Predicted Performance Category: {predicted_category}")
        st.warning(f"Academic Risk Level: {risk_level}")

# -----------------------------
# Recommendations Page
# -----------------------------
with tabs[4]:
    st.header("Personalized Academic Recommendations")

    st.write(
        """
        Enter a student profile to generate academic improvement recommendations.
        """
    )

    study_hours_r = st.slider("Study Hours per Day", 0.0, 10.0, 1.0, key="rec_study")
    social_media_r = st.slider("Social Media Hours", 0.0, 10.0, 4.0, key="rec_social")
    netflix_r = st.slider("Netflix Hours", 0.0, 10.0, 3.0, key="rec_netflix")
    attendance_r = st.slider("Attendance Percentage", 0.0, 100.0, 65.0, key="rec_attendance")
    sleep_r = st.slider("Sleep Hours", 0.0, 12.0, 5.0, key="rec_sleep")
    mental_health_r = st.slider("Mental Health Rating", 1, 10, 4, key="rec_mental")
    exercise_r = st.slider("Exercise Frequency per Week", 0, 7, 1, key="rec_exercise")
    diet_r = st.selectbox("Diet Quality", ["Poor", "Fair", "Good"], key="rec_diet")
    internet_r = st.selectbox("Internet Quality", ["Poor", "Average", "Good"], key="rec_internet")

    if st.button("Generate Recommendations"):
        recs = generate_recommendations(
            study_hours_r,
            social_media_r,
            netflix_r,
            attendance_r,
            sleep_r,
            mental_health_r,
            exercise_r,
            diet_r,
            internet_r
        )

        st.subheader("Recommended Actions")
        for rec in recs:
            st.write(f"✅ {rec}")