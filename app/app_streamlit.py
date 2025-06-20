import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# --- Load data and model ---
@st.cache_data
def load_data():
    return pd.read_csv(r'D:\Code\HR_Attrition_Analyzer\data\employee_cleaned.csv')

@st.cache_resource
def load_model():
    return joblib.load(r'D:\Code\HR_Attrition_Analyzer\models\rf_model.pkl')

df = load_data()
model = load_model()

# --- Sidebar for navigation ---
st.sidebar.title("📊 HR Attrition Analyzer")
page = st.sidebar.radio("Chọn chế độ", ["📌 Tổng quan dữ liệu", "🤖 Dự đoán nghỉ việc", "📈 Gợi ý giữ chân", "📊 Phân tích nâng cao"])

# --- Sidebar filters for data exploration ---
st.sidebar.markdown("---")
st.sidebar.subheader("Bộ lọc dữ liệu (Dành cho Tổng quan & Phân tích nâng cao)")

department_filter = st.sidebar.multiselect("Phòng ban", options=df['Department'].unique(), default=df['Department'].unique())
gender_filter = st.sidebar.multiselect("Giới tính", options=df['Gender'].unique(), default=df['Gender'].unique())
overtime_filter = st.sidebar.multiselect("Làm thêm giờ?", options=df['OverTime'].unique(), default=df['OverTime'].unique())

# Filtered DataFrame for analysis pages
df_filtered = df[
    (df['Department'].isin(department_filter)) &
    (df['Gender'].isin(gender_filter)) &
    (df['OverTime'].isin(overtime_filter))
]

# --- Page 1: Overview ---
if page == "📌 Tổng quan dữ liệu":
    st.title("📊 Tổng quan dữ liệu nhân sự")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Tỷ lệ nghỉ việc")
        attr_rate = df_filtered['Attrition'].value_counts(normalize=True).rename({0: "Không nghỉ", 1: "Nghỉ"})
        fig = px.pie(values=attr_rate.values, names=attr_rate.index, title="Tỷ lệ nghỉ việc", color=attr_rate.index,
                     color_discrete_map={"Nghỉ": "red", "Không nghỉ": "green"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📁 Tỷ lệ nghỉ việc theo phòng ban")
        dept_attr = df_filtered.groupby("Department")["Attrition"].mean().reset_index()
        fig = px.bar(dept_attr, x='Department', y='Attrition', color='Attrition',
                     color_continuous_scale='RdYlGn_r', title="Tỷ lệ nghỉ việc theo phòng ban")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("💰 Phân bố thu nhập")
    fig = px.histogram(df_filtered, x="MonthlyIncome", nbins=50, title="Phân bố thu nhập hàng tháng")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 So sánh thu nhập theo giới tính")
    fig = px.box(df_filtered, x='Gender', y='MonthlyIncome', color='Gender', title="Thu nhập theo giới tính")
    st.plotly_chart(fig, use_container_width=True)

# --- Page 2: Prediction ---
elif page == "🤖 Dự đoán nghỉ việc":
    st.title("🤖 Dự đoán khả năng nghỉ việc của nhân viên")

    st.write("🧾 Nhập thông tin nhân viên bên dưới:")

    # User inputs
    Age = st.slider("Tuổi", 18, 60, 30)
    MonthlyIncome = st.number_input("Thu nhập tháng (USD)", 1000, 20000, 5000)
    OverTime = st.selectbox("Làm thêm giờ?", ['Yes', 'No'])
    JobLevel = st.selectbox("Cấp bậc công việc", sorted(df['JobLevel'].unique()))
    JobRole = st.selectbox("Chức vụ", df['JobRole'].unique())
    Department = st.selectbox("Phòng ban", df['Department'].unique())
    Gender = st.selectbox("Giới tính", ['Male', 'Female'])
    EducationField = st.selectbox("Ngành học", df['EducationField'].unique())
    MaritalStatus = st.selectbox("Tình trạng hôn nhân", df['MaritalStatus'].unique())
    DistanceFromHome = st.slider("Khoảng cách đến công ty (km)", 1, 30, 5)

    # Encoding categorical variables
    encode = lambda col, val: df[col].astype('category').cat.categories.get_loc(val)
    input_dict = {
        'Age': Age,
        'BusinessTravel': 1,
        'DailyRate': 800,
        'Department': encode('Department', Department),
        'DistanceFromHome': DistanceFromHome,
        'Education': 3,
        'EducationField': encode('EducationField', EducationField),
        'EnvironmentSatisfaction': 3,
        'Gender': 1 if Gender == 'Male' else 0,
        'HourlyRate': 60,
        'JobInvolvement': 3,
        'JobLevel': JobLevel,
        'JobRole': encode('JobRole', JobRole),
        'JobSatisfaction': 3,
        'MaritalStatus': encode('MaritalStatus', MaritalStatus),
        'MonthlyIncome': MonthlyIncome,
        'MonthlyRate': 15000,
        'NumCompaniesWorked': 2,
        'OverTime': 1 if OverTime == 'Yes' else 0,
        'PercentSalaryHike': 12,
        'PerformanceRating': 3,
        'RelationshipSatisfaction': 3,
        'StockOptionLevel': 1,
        'TotalWorkingYears': 6,
        'TrainingTimesLastYear': 2,
        'WorkLifeBalance': 2,
        'YearsAtCompany': 3,
        'YearsInCurrentRole': 2,
        'YearsSinceLastPromotion': 1,
        'YearsWithCurrManager': 2
    }

    input_df = pd.DataFrame([input_dict])[model.feature_names_in_]

    if st.button("📌 Dự đoán"):
        proba = model.predict_proba(input_df)[0][1]
        st.metric("🔍 Xác suất nghỉ việc", f"{proba*100:.2f}%")
        if proba > 0.5:
            st.error("⚠️ Nhân viên có khả năng nghỉ việc cao!")
        else:
            st.success("✅ Nhân viên có khả năng ở lại.")

# --- Page 3: Retention suggestions ---
elif page == "📈 Gợi ý giữ chân":
    st.title("📈 Chiến lược giữ chân nhân viên")

    st.markdown("""
    ### 📊 Các yếu tố ảnh hưởng đến nghỉ việc:
    - 🔥 Làm thêm giờ (OverTime)
    - 📉 Thu nhập thấp
    - 📁 Cấp bậc thấp, vai trò nhàm chán
    - ⏳ Thiếu cơ hội thăng tiến, thời gian làm việc ngắn

    ### 💡 Gợi ý chiến lược:
    - Tăng lương và cơ hội thăng tiến cho nhóm có rủi ro cao
    - Giảm giờ làm thêm và cải thiện môi trường làm việc
    - Ưu tiên hỗ trợ nhóm chức vụ/phòng ban dễ nghỉ
    - Tận dụng phân tích để sớm nhận diện nhân sự rủi ro
    """)

# --- Page 4: Advanced analysis ---
elif page == "📊 Phân tích nâng cao":
    st.title("🔍 Phân tích dữ liệu nâng cao")

    # Select variable to analyze
    var_option = st.selectbox("Chọn biến để phân tích", options=[
        'Age', 'MonthlyIncome', 'DistanceFromHome', 'YearsAtCompany',
        'YearsInCurrentRole', 'YearsSinceLastPromotion', 'JobLevel'
    ])

    # Chart type selector
    chart_type = st.selectbox("Chọn loại biểu đồ", ['Histogram', 'Box Plot', 'Violin Plot', 'Scatter Plot'])

    # Plot charts with Plotly
    if chart_type == 'Histogram':
        fig = px.histogram(df_filtered, x=var_option, nbins=30, title=f"Phân bố {var_option}")
    elif chart_type == 'Box Plot':
        fig = px.box(df_filtered, y=var_option, color='Attrition',
                     title=f"Phân bố {var_option} theo nghỉ việc")
    elif chart_type == 'Violin Plot':
        fig = px.violin(df_filtered, y=var_option, color='Attrition', box=True,
                        title=f"Phân bố {var_option} theo nghỉ việc")
    elif chart_type == 'Scatter Plot':
        fig = px.scatter(df_filtered, x=var_option, y='MonthlyIncome',
                         color='Attrition', hover_data=['Department', 'JobRole'],
                         title=f"Scatter: {var_option} vs MonthlyIncome")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Feature importance chart
    st.subheader("🔑 Feature Importance của mô hình Random Forest")
    try:
        importances = model.feature_importances_
        feat_names = model.feature_names_in_
        fi_df = pd.DataFrame({'Feature': feat_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)
        fig_fi = px.bar(fi_df.head(15), x='Importance', y='Feature', orientation='h', title="Top 15 tính năng quan trọng", text='Importance')
        fig_fi.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        st.plotly_chart(fig_fi, use_container_width=True)
    except Exception as e:
        st.error("Không thể tải feature importance.")
        st.write(e)
