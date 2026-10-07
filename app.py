import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
from datetime import datetime


# =========================================================
# 🔐 JEEVAN-ALERT LOGIN SYSTEM
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None


# =========================================================
# 👤 DEMO USERS
# =========================================================



   # =========================================================
# 🔐 JEEVAN-ALERT USER LOGIN + REGISTRATION
# =========================================================

import json

USER_FILE = "data/users.json"


# ---------------------------------------------------------
# CREATE USER FILE IF NOT EXISTS
# ---------------------------------------------------------

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(USER_FILE):

    default_users = {

        "admin": {
            "password": "admin123",
            "role": "Administrator",
            "name": "System Administrator"
        },

        "healthworker": {
            "password": "health123",
            "role": "Health Worker",
            "name": "Health Worker"
        }

    }

    with open(
        USER_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            default_users,
            f,
            indent=4
        )


# ---------------------------------------------------------
# LOAD USERS
# ---------------------------------------------------------

with open(
    USER_FILE,
    "r",
    encoding="utf-8"
) as f:

    USERS = json.load(f)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = None


if "user_role" not in st.session_state:

    st.session_state.user_role = None


# =========================================================
# LOGIN / REGISTER PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown(
        """
        <h1 style="text-align:center;">
        🔐 JEEVAN-ALERT
        </h1>

        <p style="text-align:center;">
        Smart Community Health Monitoring &
        Early Warning System
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()


    login_tab, register_tab = st.tabs(
        [
            "🔑 Login",
            "📝 Create Account"
        ]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader(
            "🔑 Login to JEEVAN-ALERT"
        )

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "🔓 Login",
            type="primary",
            use_container_width=True
        ):

            if login_username in USERS:

                stored_password = USERS[
                    login_username
                ]["password"]


                if login_password == stored_password:

                    st.session_state.logged_in = True

                    st.session_state.username = (
                        login_username
                    )

                    st.session_state.user_role = (
                        USERS[
                            login_username
                        ]["role"]
                    )

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Incorrect password."
                    )

            else:

                st.error(
                    "❌ Username does not exist."
                )


    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    with register_tab:

        st.subheader(
            "📝 Create New Account"
        )

        new_name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            key="new_name"
        )


        new_username = st.text_input(
            "Create Username",
            placeholder="Example: akhilesh123",
            key="new_username"
        )


        new_password = st.text_input(
            "Create Password",
            type="password",
            key="new_password"
        )


        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_password"
        )


        new_role = st.selectbox(
            "Select Account Type",
            [
                "Family",
                "Health Worker",
                "Administrator"
            ],
            key="new_role"
        )


        if st.button(
            "📝 Create Account",
            type="primary",
            use_container_width=True
        ):

            # ---------------------------------------------
            # VALIDATION
            # ---------------------------------------------

            if new_name.strip() == "":

                st.error(
                    "❌ Please enter your name."
                )

            elif new_username.strip() == "":

                st.error(
                    "❌ Please create a username."
                )

            elif new_password == "":

                st.error(
                    "❌ Please create a password."
                )

            elif new_password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif len(new_password) < 4:

                st.error(
                    "❌ Password must contain at least 4 characters."
                )

            elif new_username in USERS:

                st.error(
                    "❌ This username already exists."
                )

            else:

                # -----------------------------------------
                # SAVE NEW USER
                # -----------------------------------------

                USERS[new_username] = {

                    "password":
                        new_password,

                    "role":
                        new_role,

                    "name":
                        new_name

                }


                with open(
                    USER_FILE,
                    "w",
                    encoding="utf-8"
                ) as f:

                    json.dump(
                        USERS,
                        f,
                        indent=4
                    )


                st.success(
                    "✅ Account created successfully!"
                )

                st.info(
                    "Now go to the Login tab and login "
                    "with your new username and password."
                )


    # -----------------------------------------------------
    # DEMO ACCOUNTS
    # -----------------------------------------------------

    st.divider()

    st.info(
        """
🔐 DEMO ACCOUNTS

Administrator
Username: admin
Password: admin123

Health Worker
Username: healthworker
Password: health123

You can create your own Family account
from the "Create Account" tab.
"""
    )


    # -----------------------------------------------------
    # STOP MAIN APP
    # -----------------------------------------------------

    st.stop()


# =========================================================
# LOGGED-IN USER INFORMATION
# =========================================================

st.sidebar.success(
    f"👤 {st.session_state.username}"
)


st.sidebar.info(
    f"Role: {st.session_state.user_role}"
)


# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪 Logout"
):

    st.session_state.logged_in = False

    st.session_state.username = None

    st.session_state.user_role = None

    st.rerun()


# =========================================================
# 👤 LOGGED-IN USER
# =========================================================

st.sidebar.success(
    f"👤 {st.session_state.username}"
)

st.sidebar.info(
    f"Role: {st.session_state.user_role}"
)


# =========================================================
# 🚪 LOGOUT
# =========================================================

if st.sidebar.button(
    "🚪 Logout",
    key="main_logout_button"
):

    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None

    st.rerun()


# =========================================================
# 👇 TUMHARA PURANA CODE YAHAN SE CONTINUE HOGA
# =========================================================

# =========================================================
# OPTIONAL MAP
# =========================================================

try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart Community Health Monitoring & Early Warning System",
    page_icon="🏥",
    layout="wide"
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "village_data.csv"
)

MODEL_FILE = os.path.join(
    BASE_DIR,
    "ml",
    "disease_risk_model.pkl"
)

ALERT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "alert_history.csv"
)

WATER_HISTORY_FILE = os.path.join(
    BASE_DIR,
    "data",
    "household_water_history.csv"
)

FAMILY_ALERT_FILE = os.path.join(
    BASE_DIR,
    "data",
    "family_alert_history.csv"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.main-title{
font-size:42px;
font-weight:800;
color:#0F766E;
}

.subtitle{
font-size:20px;
color:#64748B;
margin-bottom:20px;
}

.card{
padding:20px;
border-radius:15px;
background:#F8FAFC;
border:1px solid #E5E7EB;
}

</style>
""",unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_FILE)
    df.columns = [str(x).strip() for x in df.columns]
    return df


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    loaded = joblib.load(MODEL_FILE)

    if hasattr(loaded,"predict"):
        return loaded

    if isinstance(loaded,dict):

        for key in loaded:

            value = loaded[key]

            if hasattr(value,"predict"):
                return value

    raise Exception("Model not found")


# =========================================================
# INITIAL LOAD
# =========================================================

try:

    data = load_data()
    model = load_model()

except Exception as e:

    st.error("Project load error")
    st.code(str(e))
    st.stop()


# =========================================================
# ENCODING
# =========================================================

def encode_water_quality(value):

    mapping={
        "Good":0,
        "Medium":1,
        "Poor":2
    }

    return mapping.get(str(value).title(),1)


def encode_flood(value):

    mapping={
        "No":0,
        "Yes":1
    }

    return mapping.get(str(value).title(),0)


# =========================================================
# MODEL FEATURES
# =========================================================

def create_features(row):

    features={
        "population":float(row["population"]),
        "rainfall":float(row["rainfall"]),
        "temperature":float(row["temperature"]),
        "humidity":float(row["humidity"]),
        "previous_cases":float(row["previous_cases"]),
        "sanitation_score":float(row["sanitation_score"]),
        "water_quality_encoded":encode_water_quality(row["water_quality"]),
        "flood_status_encoded":encode_flood(row["flood_status"])
    }

    if hasattr(model,"feature_names_in_"):

        cols=list(model.feature_names_in_)
        values=[]

        for c in cols:

            if c in features:
                values.append(features[c])
            elif c in row.index:
                values.append(float(row[c]))
            else:
                values.append(0)

        return pd.DataFrame([values],columns=cols)

    return pd.DataFrame([[
        features["population"],
        features["rainfall"],
        features["temperature"],
        features["humidity"],
        features["previous_cases"],
        features["sanitation_score"],
        features["water_quality_encoded"],
        features["flood_status_encoded"]
    ]],columns=[
        "population",
        "rainfall",
        "temperature",
        "humidity",
        "previous_cases",
        "sanitation_score",
        "water_quality_encoded",
        "flood_status_encoded"
    ])


# =========================================================
# FALLBACK AI
# =========================================================

def fallback_risk(row):

    score=0

    if str(row["water_quality"])=="Poor":
        score+=30
    elif str(row["water_quality"])=="Medium":
        score+=15

    if float(row["previous_cases"])>=20:
        score+=25
    elif float(row["previous_cases"])>=10:
        score+=15

    if float(row["rainfall"])>=150:
        score+=20
    elif float(row["rainfall"])>=100:
        score+=10

    if float(row["sanitation_score"])<50:
        score+=20
    elif float(row["sanitation_score"])<70:
        score+=10

    if str(row["flood_status"])=="Yes":
        score+=20

    if score>=60:
        risk="High"
    elif score>=30:
        risk="Medium"
    else:
        risk="Low"

    return risk,min(score/100,0.99)


# =========================================================
# AI PREDICTION
# =========================================================

def predict_risk(row):

    try:

        X=create_features(row)

        pred=model.predict(X)[0]

        risk=str(pred).title()

        probability=0.0

        if hasattr(model,"predict_proba"):

            probs=model.predict_proba(X)[0]
            probability=float(max(probs))

        if risk not in ["Low","Medium","High"]:
            return fallback_risk(row)

        # Keep displayed AI score consistent with the predicted risk level.
        if risk == "High":
            probability = max(0.60, probability)
        elif risk == "Medium":
            probability = min(0.59, max(0.30, probability))
        else:
            probability = min(0.29, max(0.0, probability))

        return risk,probability

    except:

        return fallback_risk(row)


# =========================================================
# ALERT FUNCTIONS
# =========================================================

def load_alert_history():

    columns = [
        "alert_id",
        "date_time",
        "village",
        "district",
        "risk_level",
        "ai_risk_score",
        "status"
    ]

    if os.path.exists(ALERT_FILE):

        try:
            df = pd.read_csv(ALERT_FILE)

            for c in columns:
                if c not in df.columns:
                    df[c] = ""

            return df[columns]

        except:
            pass

    return pd.DataFrame(columns=columns)


def save_alert(village,district,risk,score):

    df=load_alert_history()

    now=datetime.now()

    new=pd.DataFrame([{
        "alert_id":"ALT-"+now.strftime("%Y%m%d%H%M%S"),
        "date_time":now.strftime("%d-%m-%Y %H:%M:%S"),
        "village":village,
        "district":district,
        "risk_level":risk,
        "ai_risk_score":round(score,2),
        "status":"ACTIVE"
    }])

    df=pd.concat([df,new],ignore_index=True)

    df.to_csv(ALERT_FILE,index=False)


# =========================================================
# HOUSEHOLD WATER SAVE
# =========================================================

def load_water_history():

    if os.path.exists(WATER_HISTORY_FILE):

        try:
            return pd.read_csv(WATER_HISTORY_FILE)
        except:
            pass

    return pd.DataFrame()


def save_water_reading(record):

    df=load_water_history()

    df=pd.concat([
        df,
        pd.DataFrame([record])
    ],ignore_index=True)

    df.to_csv(WATER_HISTORY_FILE,index=False)


# =========================================================
# FAMILY ALERT SAVE
# =========================================================

def load_family_alerts():

    if os.path.exists(FAMILY_ALERT_FILE):

        try:
            return pd.read_csv(FAMILY_ALERT_FILE)
        except:
            pass

    return pd.DataFrame()


def save_family_alert(record):

    df=load_family_alerts()

    df=pd.concat([
        df,
        pd.DataFrame([record])
    ],ignore_index=True)

    df.to_csv(FAMILY_ALERT_FILE,index=False)


# =========================================================
# HEADER
# =========================================================

st.markdown(
'<div class="main-title">🏥 Smart Community Health Monitoring & Early Warning System</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">AI + IoT Based Water Quality and Community Health Monitoring Platform</div>',
unsafe_allow_html=True
)

st.divider()


# =========================================================
# VILLAGE AI SUMMARY
# =========================================================

results=[]

for _,row in data.iterrows():

    risk,prob=predict_risk(row)

    results.append({
        "village":row["village"],
        "district":row["district"],
        "risk":risk,
        "score":prob*100
    })

risk_df=pd.DataFrame(results)

high=len(risk_df[risk_df["risk"]=="High"])
medium=len(risk_df[risk_df["risk"]=="Medium"])
low=len(risk_df[risk_df["risk"]=="Low"])

c1,c2,c3,c4=st.columns(4)

c1.metric("Total Villages",len(data))
c2.metric("🔴 High",high)
c3.metric("🟡 Medium",medium)
c4.metric("🟢 Low",low)

st.divider()


# =========================================================
# MAP
# =========================================================

st.header("🗺️ Community Risk Map")

if MAP_AVAILABLE:

    center=[
        data["latitude"].mean(),
        data["longitude"].mean()
    ]

    m=folium.Map(location=center,zoom_start=6)

    for _,row in data.iterrows():

        rr=risk_df[risk_df["village"]==row["village"]].iloc[0]

        color="green"

        if rr["risk"]=="High":
            color="red"

        elif rr["risk"]=="Medium":
            color="orange"

        folium.Marker(
            [row["latitude"],row["longitude"]],
            popup=f"""
            <b>{row['village']}</b><br>
            District: {row['district']}<br>
            Risk: {rr['risk']}<br>
            Score: {rr['score']:.2f}%
            """,
            icon=folium.Icon(color=color)
        ).add_to(m)

    st_folium(m,width=1200,height=500)

else:

    st.info("Install folium and streamlit-folium for map.")


# =========================================================
# VILLAGE ANALYSIS
# =========================================================

st.divider()

st.header("🔎 Village AI Analysis")

selected_village=st.selectbox(
"Select Village",
data["village"].tolist()
)

selected=data[data["village"]==selected_village].iloc[0]

risk,prob=predict_risk(selected)

score=prob*100

a,b=st.columns(2)

with a:

    st.subheader(selected["village"])

    st.write("District :",selected["district"])
    st.write("Population :",selected["population"])
    st.write("Rainfall :",selected["rainfall"])
    st.write("Temperature :",selected["temperature"])
    st.write("Humidity :",selected["humidity"])

with b:

    st.subheader("AI Risk")

    st.metric("Risk Score",f"{score:.2f}%")

    if risk=="High":
        st.error("🔴 HIGH RISK")

    elif risk=="Medium":
        st.warning("🟡 MEDIUM RISK")

    else:
        st.success("🟢 LOW RISK")


# =========================================================
# HOUSEHOLD WATER MONITORING
# =========================================================

st.divider()

st.header("💧 Household Water Quality Monitoring")

st.write("Enter water sensor readings from any household.")

h1,h2,h3=st.columns(3)

with h1:

    house_id=st.text_input(
        "House ID",
        "HOUSE-001"
    )

with h2:

    household_village=st.text_input(
        "Village Name",
        selected_village
    )

with h3:

    water_source=st.selectbox(
        "Water Source",
        [
            "Tap Water",
            "Borewell",
            "Handpump",
            "Community Tank"
        ]
    )


st.subheader("Sensor Readings")

s1,s2,s3,s4=st.columns(4)

with s1:

    ph=st.number_input(
        "pH",
        0.0,
        14.0,
        7.0,
        0.1
    )

with s2:

    turbidity=st.number_input(
        "Turbidity",
        0.0,
        100.0,
        2.0,
        0.1
    )

with s3:

    tds=st.number_input(
        "TDS",
        0.0,
        2000.0,
        200.0,
        1.0
    )

with s4:

    temp=st.number_input(
        "Water Temp",
        0.0,
        100.0,
        25.0,
        0.5
    )


# =========================================================
# FAMILY AGE GROUP
# =========================================================

st.subheader("👨‍👩‍👧 Household Family")

f1,f2,f3,f4=st.columns(4)

with f1:

    age_0_5=st.number_input(
        "Age 0-5",
        0,
        20,
        0
    )

with f2:

    age_6_17=st.number_input(
        "Age 6-17",
        0,
        20,
        0
    )

with f3:

    age_18_59=st.number_input(
        "Age 18-59",
        0,
        20,
        1
    )

with f4:

    age_60=st.number_input(
        "Age 60+",
        0,
        20,
        0
    )


# =========================================================
# WATER AI ENGINE
# =========================================================

water_score=0
reasons=[]

if ph<6.5 or ph>8.5:

    water_score+=25
    reasons.append("Abnormal pH")

if turbidity>5:

    water_score+=30
    reasons.append("High Turbidity")

elif turbidity>1:

    water_score+=10
    reasons.append("Moderate Turbidity")

if tds>500:

    water_score+=25
    reasons.append("High TDS")

elif tds>300:

    water_score+=10
    reasons.append("Elevated TDS")

if temp>30:

    water_score+=10
    reasons.append("High Temperature")

water_score=min(water_score,100)

if water_score>=60:

    water_level="High"

elif water_score>=30:

    water_level="Medium"

else:

    water_level="Low"


# =========================================================
# AGE PRIORITY
# =========================================================

priority=[]

if water_level in ["Medium","High"]:

    if age_0_5>0:
        priority.append("Young Children (0-5)")

    if age_60>0:
        priority.append("Older Adults (60+)")

if water_level=="High" and age_6_17>0:

    priority.append("Children (6-17)")

if len(priority)==0:

    priority.append("General Household")


# =========================================================
# AGE VULNERABILITY SCORE
# =========================================================

vulnerability_score = 0

if age_0_5 > 0:
    vulnerability_score += 35

if age_6_17 > 0:
    vulnerability_score += 20

if age_60 > 0:
    vulnerability_score += 30

if age_18_59 > 0:
    vulnerability_score += 5

vulnerability_score = min(vulnerability_score,100)

combined_household_score = min(
    100,
    round(
        (water_score * 0.70) +
        (vulnerability_score * 0.30),
        2
    )
)


# =========================================================
# POSSIBLE HEALTH RISK
# =========================================================

if water_level=="High":

    health_category="Elevated water-related gastrointestinal illness risk"

elif water_level=="Medium":

    health_category="Moderate water-related health risk"

else:

    health_category="Low screening-level water risk"


# =========================================================
# DISPLAY RESULT
# =========================================================

st.divider()

st.header("🤖 AI Household Result")

r1,r2,r3=st.columns(3)

r1.metric(
"Water Score",
f"{water_score}/100"
)

r2.metric(
"Risk Level",
water_level
)

r3.metric(
"Health Risk Category",
health_category
)

if water_level=="High":

    st.error("🔴 HIGH WATER RISK")

elif water_level=="Medium":

    st.warning("🟡 MEDIUM WATER RISK")

else:

    st.success("🟢 LOW WATER RISK")


st.subheader("👶 Age Group Priority")

for p in priority:

    st.write("⚠️",p)


st.subheader("🔍 Explainable AI Factors")

if reasons:

    for x in reasons:

        st.warning(x)

else:

    st.success("No major water screening factor detected.")


# =========================================================
# AUTOMATIC MESSAGE
# =========================================================

st.subheader("📱 Automatic Family Alert")

message=f"""
House ID: {house_id}

Village: {household_village}

Water Source: {water_source}

Water Risk: {water_level}

Water Score: {water_score}/100

Priority Age Group:
{", ".join(priority)}

Health Guidance:
{health_category}

Recommendation:
Use safe treated drinking water.
Arrange laboratory water testing if required.
Continue household monitoring.
"""

st.code(message)


# =========================================================
# SAVE HOUSE DATA
# =========================================================

if st.button("💾 Save Household Reading",type="primary"):

    record={
        "date_time":datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "house_id":house_id,
        "village":household_village,
        "water_source":water_source,
        "ph":ph,
        "turbidity":turbidity,
        "tds":tds,
        "temperature":temp,
        "water_score":water_score,
        "risk_level":water_level,
        "priority_age":", ".join(priority),
        "vulnerability_score":vulnerability_score,
        "combined_priority_score":combined_household_score,
        "health_risk":health_category
    }

    save_water_reading(record)

    st.success("Household water reading saved successfully.")


# =========================================================
# SEND FAMILY ALERT
# =========================================================

if st.button("📨 Generate Family Alert"):

    alert={
        "date_time":datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "house_id":house_id,
        "village":household_village,
        "message":message
    }

    save_family_alert(alert)

    st.success("Automatic family alert generated and stored.")

    st.info(message)


# =========================================================
# HOUSE HISTORY
# =========================================================

st.divider()

st.header("📋 Household Water History")

history=load_water_history()

if len(history)>0:

    st.dataframe(
        history,
        use_container_width=True
    )

else:

    st.info("No household records yet.")


# =========================================================
# COMMUNITY CLUSTER DETECTION
# =========================================================

st.divider()

st.header("🚨 Community Water Risk Cluster Detection")

if len(history)>=3:

    village_history=history[
        history["village"]==household_village
    ]

    total=len(village_history)

    high=len(
        village_history[
            village_history["risk_level"]=="High"
        ]
    )

    medium=len(
        village_history[
            village_history["risk_level"]=="Medium"
        ]
    )

    low=len(
        village_history[
            village_history["risk_level"]=="Low"
        ]
    )

    c1,c2,c3=st.columns(3)

    c1.metric("Total Houses",total)
    c2.metric("High Risk",high)
    c3.metric("Medium Risk",medium)

    if high>=3:

        st.error(
        f"""
🚨 COMMUNITY ALERT

Village: {household_village}

Multiple households show HIGH water-risk readings.

Possible community water contamination cluster detected.

Recommended Action:

• Inspect common water source
• Collect laboratory samples
• Inform health authority
• Increase field surveillance
        """
        )

    elif high>=1 and medium>=2:

        st.warning(
        "Possible emerging community water-quality issue detected."
        )

    else:

        st.success(
        "No major community cluster detected."
        )

else:

    st.info(
    "Save at least 3 household readings for community analysis."
    )


# =========================================================
# COMMON WATER SOURCE ANALYSIS
# =========================================================

st.subheader("🚰 Common Water Source Risk")

if len(history)>0 and "water_source" in history.columns:

    source_summary = (
        history.groupby("water_source")
        .agg(
            households=("house_id","nunique"),
            high_risk=("risk_level", lambda x:
                       (x.astype(str).str.title()=="High").sum()),
            medium_risk=("risk_level", lambda x:
                         (x.astype(str).str.title()=="Medium").sum())
        )
        .reset_index()
    )

    source_summary["risk_ratio_%"] = (
        source_summary["high_risk"] /
        source_summary["households"].replace(0,np.nan) * 100
    ).round(2)

    st.dataframe(
        source_summary,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# HEALTH OFFICER ALERT
# =========================================================

st.divider()

st.header("🏥 Health Officer Alert")

if risk=="High":

    st.error(
    f"High village disease risk detected : {selected_village}"
    )

    if st.button("Generate Health Officer Alert"):

        save_alert(
            selected["village"],
            selected["district"],
            risk,
            score
        )

        st.success("Health Officer Alert Generated.")

else:

    st.info("Current village risk is not HIGH.")


# =========================================================
# ALERT HISTORY
# =========================================================

st.divider()

st.header("📂 Health Alert History")

alert_history=load_alert_history()

if len(alert_history)>0:

    st.dataframe(
        alert_history,
        use_container_width=True
    )

else:

    st.info("No alerts generated yet.")


# =========================================================
# 7 DAY FORECAST
# =========================================================

st.divider()

st.header("📈 7-Day Risk Forecast")

base=score

days=[
"Today",
"Day2",
"Day3",
"Day4",
"Day5",
"Day6",
"Day7"
]

forecast=[]

trend = [0,-1,0,1,2,3,2]

for i in range(7):

    value=max(
        0,
        min(
            100,
            base + trend[i]
        )
    )

    forecast.append(round(value,2))

forecast_df=pd.DataFrame({
    "Day":days,
    "Risk Score":forecast
})

st.line_chart(
forecast_df.set_index("Day")
)

st.dataframe(forecast_df)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption("""
Smart Community Health Monitoring & Early Warning System

AI + IoT Prototype for Water Quality Monitoring,
Household Risk Screening, Age-group Precaution Priority,
Community Cluster Detection and Early Warning Support.

For MVP demonstration and decision-support only.
""")
# =========================================================
# AUTOMATIC HOUSEHOLD ALERT SYSTEM
# =========================================================

st.divider()

st.header("📱 Automatic Household Alert System")

st.write(
    "The system automatically prepares a personalized "
    "health-safety alert based on household water risk."
)

# ---------------------------------------------------------
# ALERT STATUS
# ---------------------------------------------------------

if water_level == "High":

    alert_status = "🚨 URGENT ALERT"

    alert_message = f"""
🚨 WATER SAFETY ALERT

House ID: {house_id}
Village: {household_village}
Water Source: {water_source}

Water Risk Score: {water_score}/100
Risk Level: HIGH

Priority Age Group:
{", ".join(priority)}

Health Risk Category:
{health_category}

Recommended Action:

1. Use safe/treated drinking water.
2. Avoid consuming untreated water.
3. Arrange authorized/laboratory water testing.
4. Give additional precaution to the identified age groups.
5. Contact the appropriate health authority if symptoms occur.
"""

elif water_level == "Medium":

    alert_status = "⚠️ WARNING"

    alert_message = f"""
⚠️ WATER QUALITY WARNING

House ID: {house_id}
Village: {household_village}
Water Source: {water_source}

Water Risk Score: {water_score}/100
Risk Level: MEDIUM

Priority Age Group:
{", ".join(priority)}

Health Risk Category:
{health_category}

Recommended Action:

1. Prefer safe/treated drinking water.
2. Monitor water quality.
3. Consider authorized/laboratory testing.
4. Give additional precaution to vulnerable age groups.
"""

else:

    alert_status = "🟢 NORMAL"

    alert_message = f"""
🟢 WATER MONITORING UPDATE

House ID: {house_id}
Village: {household_village}
Water Source: {water_source}

Water Risk Score: {water_score}/100
Risk Level: LOW

Current screening result does not show a major
water-quality risk indicator.

Continue regular monitoring.
"""

# ---------------------------------------------------------
# SHOW ALERT
# ---------------------------------------------------------

st.subheader(alert_status)

st.code(
    alert_message,
    language="text"
)

# ---------------------------------------------------------
# AUTOMATIC ALERT GENERATION
# ---------------------------------------------------------

if water_level in ["High", "Medium"]:

    if st.button(
        "🚨 SEND / RECORD ALERT",
        type="primary"
    ):

        alert_record = {

            "date_time":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

            "house_id":
                house_id,

            "village":
                household_village,

            "water_source":
                water_source,

            "water_score":
                water_score,

            "risk_level":
                water_level,

            "priority_age_groups":
                ", ".join(priority),

            "health_risk":
                health_category,

            "vulnerability_score":
                vulnerability_score,

            "combined_priority_score":
                combined_household_score,

            "alert_status":
                "GENERATED",

            "message":
                alert_message
        }

        save_family_alert(
            alert_record
        )

        st.success(
            "✅ Alert generated and stored successfully."
        )

        st.info(
            "📱 In the production version, this alert "
            "can be connected to SMS, WhatsApp, or a "
            "mobile-app notification service."
        )

else:

    st.success(
        "🟢 No emergency alert is required at this time."
    )

# =========================================================
# ALERT HISTORY
# =========================================================

st.subheader("📋 Family Alert History")

family_alert_history = load_family_alerts()

if len(family_alert_history) > 0:

    st.dataframe(
        family_alert_history,
        use_container_width=True,
        hide_index=True
    )

    alert_csv = family_alert_history.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Family Alert History",
        data=alert_csv,
        file_name="family_alert_history.csv",
        mime="text/csv"
    )

else:

    st.info(
        "No family alerts have been generated yet."
    )

    # =========================================================
# 📡 IOT SENSOR MONITORING MODULE
# =========================================================

st.divider()

st.header("📡 IoT Household Sensor Monitoring")

st.write(
    "IoT-ready module for receiving household water-quality "
    "readings from sensors such as ESP32."
)

# ---------------------------------------------------------
# DEVICE INFORMATION
# ---------------------------------------------------------

i1, i2, i3 = st.columns(3)

with i1:

    device_id = st.text_input(
        "Sensor Device ID",
        "ESP32-HOUSE-001"
    )

with i2:

    sensor_house = st.text_input(
        "Connected House",
        house_id
    )

with i3:

    connection_status = st.selectbox(
        "Sensor Connection",
        [
            "🟢 Connected",
            "🟡 Intermittent",
            "🔴 Disconnected"
        ]
    )

# ---------------------------------------------------------
# SENSOR SIMULATOR
# ---------------------------------------------------------

st.subheader("🧪 Live Sensor Simulator")

st.caption(
    "For MVP demonstration. In the hardware version, "
    "these values will come directly from ESP32 sensors."
)

sim1, sim2, sim3, sim4 = st.columns(4)

with sim1:

    sensor_ph = st.slider(
        "pH",
        0.0,
        14.0,
        7.0,
        0.1,
        key="iot_ph"
    )

with sim2:

    sensor_turbidity = st.slider(
        "Turbidity",
        0.0,
        100.0,
        2.0,
        0.1,
        key="iot_turbidity"
    )

with sim3:

    sensor_tds = st.slider(
        "TDS",
        0,
        2000,
        200,
        10,
        key="iot_tds"
    )

with sim4:

    sensor_temp = st.slider(
        "Temperature",
        0.0,
        60.0,
        25.0,
        0.5,
        key="iot_temp"
    )

# ---------------------------------------------------------
# IOT RISK CALCULATION
# ---------------------------------------------------------

iot_score = 0

iot_factors = []

if sensor_ph < 6.5 or sensor_ph > 8.5:

    iot_score += 25

    iot_factors.append(
        "Abnormal pH detected"
    )

if sensor_turbidity > 5:

    iot_score += 30

    iot_factors.append(
        "High turbidity detected"
    )

elif sensor_turbidity > 1:

    iot_score += 10

    iot_factors.append(
        "Moderate turbidity detected"
    )

if sensor_tds > 500:

    iot_score += 25

    iot_factors.append(
        "High TDS detected"
    )

elif sensor_tds > 300:

    iot_score += 10

    iot_factors.append(
        "Elevated TDS detected"
    )

if sensor_temp > 30:

    iot_score += 10

    iot_factors.append(
        "High water temperature detected"
    )

iot_score = min(
    iot_score,
    100
)

# ---------------------------------------------------------
# RISK LEVEL
# ---------------------------------------------------------

if iot_score >= 60:

    iot_risk = "High"

elif iot_score >= 30:

    iot_risk = "Medium"

else:

    iot_risk = "Low"

# ---------------------------------------------------------
# DISPLAY LIVE RESULT
# ---------------------------------------------------------

st.subheader("🤖 Live AI Water Assessment")

x1, x2, x3 = st.columns(3)

x1.metric(
    "Water Risk Score",
    f"{iot_score}/100"
)

x2.metric(
    "Risk Level",
    iot_risk
)

x3.metric(
    "Sensor Status",
    connection_status
)

if iot_risk == "High":

    st.error(
        "🚨 HIGH WATER RISK DETECTED BY SENSOR"
    )

elif iot_risk == "Medium":

    st.warning(
        "⚠️ MEDIUM WATER RISK DETECTED BY SENSOR"
    )

else:

    st.success(
        "🟢 SENSOR SCREENING RESULT: LOW RISK"
    )

# ---------------------------------------------------------
# EXPLAINABLE SENSOR FACTORS
# ---------------------------------------------------------

st.subheader(
    "🔍 Sensor Explanation"
)

if iot_factors:

    for factor in iot_factors:

        st.warning(
            "⚠️ " + factor
        )

else:

    st.success(
        "No major sensor screening factor detected."
    )

# ---------------------------------------------------------
# SENSOR TIMESTAMP
# ---------------------------------------------------------

sensor_time = datetime.now().strftime(
    "%d-%m-%Y %H:%M:%S"
)

st.info(
    f"📡 Last sensor reading: {sensor_time}"
)

# ---------------------------------------------------------
# AUTOMATIC IOT ALERT
# ---------------------------------------------------------

if iot_risk == "High":

    st.error(
        f"""
🚨 AUTOMATIC IOT ALERT

Device: {device_id}
House: {sensor_house}

Water Risk: HIGH
Water Score: {iot_score}/100

Action:
Use safe/treated drinking water and
arrange authorized/laboratory testing.
"""
    )

elif iot_risk == "Medium":

    st.warning(
        f"""
⚠️ IOT WARNING

Device: {device_id}
House: {sensor_house}

Water Risk: MEDIUM
Water Score: {iot_score}/100

Continue monitoring and prefer safe/treated water.
"""
    )

else:

    st.success(
        f"""
🟢 IOT MONITORING UPDATE

Device: {device_id}
House: {sensor_house}

Water Risk: LOW
Water Score: {iot_score}/100

Continue regular monitoring.
"""
    )

# ---------------------------------------------------------
# IOT DEMO BUTTON
# ---------------------------------------------------------

if st.button(
    "📡 Record IoT Sensor Reading"
):

    iot_record = {

        "date_time":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

        "device_id":
            device_id,

        "house_id":
            sensor_house,

        "sensor_status":
            connection_status,

        "ph":
            sensor_ph,

        "turbidity":
            sensor_turbidity,

        "tds":
            sensor_tds,

        "temperature":
            sensor_temp,

        "water_score":
            iot_score,

        "risk_level":
            iot_risk,

        "source":
            "IoT Sensor Simulator"
    }

    save_water_reading(
        iot_record
    )

    st.success(
        "✅ IoT sensor reading recorded successfully."
    )

# ---------------------------------------------------------
# HARDWARE ROADMAP
# ---------------------------------------------------------

with st.expander(
    "🔧 Hardware Integration Roadmap"
):

    st.write(
        """
Future hardware version:

ESP32
↓
pH Sensor
↓
TDS Sensor
↓
Turbidity Sensor
↓
Temperature Sensor
↓
Wi-Fi
↓
JEEVAN-ALERT Server
↓
AI Risk Engine
↓
Household Alert
↓
Community Early Warning
"""
    )

    # =========================================================
# 🤖 AI HEALTH RISK INTELLIGENCE ENGINE
# =========================================================

st.divider()

st.header("🤖 AI Health Risk Intelligence")

st.write(
    "The system combines water-quality indicators, environmental "
    "conditions and household vulnerability to generate an "
    "early-warning health-risk screening result."
)

# ---------------------------------------------------------
# CURRENT ENVIRONMENTAL DATA
# ---------------------------------------------------------

health_rainfall = float(selected["rainfall"])
health_temperature = float(selected["temperature"])
health_humidity = float(selected["humidity"])
health_previous_cases = float(selected["previous_cases"])
health_sanitation = float(selected["sanitation_score"])

# ---------------------------------------------------------
# HEALTH RISK SCORE
# ---------------------------------------------------------

health_score = 0
health_factors = []

# Water quality contribution
health_score += water_score * 0.40

if water_score >= 60:
    health_factors.append(
        "High household water-quality screening risk"
    )
elif water_score >= 30:
    health_factors.append(
        "Moderate household water-quality screening risk"
    )

# Rainfall
if health_rainfall >= 150:
    health_score += 15
    health_factors.append(
        "High rainfall may increase environmental exposure risk"
    )
elif health_rainfall >= 100:
    health_score += 8
    health_factors.append(
        "Elevated rainfall"
    )

# Temperature
if health_temperature >= 30:
    health_score += 10
    health_factors.append(
        "High environmental temperature"
    )

# Humidity
if health_humidity >= 75:
    health_score += 10
    health_factors.append(
        "High humidity"
    )

# Previous cases
if health_previous_cases >= 20:
    health_score += 15
    health_factors.append(
        "High number of previous reported cases"
    )
elif health_previous_cases >= 10:
    health_score += 8
    health_factors.append(
        "Previous reported cases present"
    )

# Sanitation
if health_sanitation < 50:
    health_score += 15
    health_factors.append(
        "Low sanitation score"
    )
elif health_sanitation < 70:
    health_score += 8
    health_factors.append(
        "Moderate sanitation score"
    )

# Family vulnerability
health_score += vulnerability_score * 0.15

health_score = min(
    round(health_score, 2),
    100
)

# ---------------------------------------------------------
# HEALTH RISK LEVEL
# ---------------------------------------------------------

if health_score >= 70:

    health_level = "HIGH"

elif health_score >= 40:

    health_level = "MEDIUM"

else:

    health_level = "LOW"

# ---------------------------------------------------------
# RISK CATEGORIES
# ---------------------------------------------------------

risk_categories = []

if water_score >= 60:

    risk_categories.append(
        "Water-related gastrointestinal illness screening priority"
    )

if health_rainfall >= 100:

    risk_categories.append(
        "Post-rainfall water contamination monitoring"
    )

if health_temperature >= 30:

    risk_categories.append(
        "Heat-related water safety monitoring"
    )

if health_sanitation < 70:

    risk_categories.append(
        "Sanitation-related exposure monitoring"
    )

if not risk_categories:

    risk_categories.append(
        "General water and environmental health monitoring"
    )

# ---------------------------------------------------------
# DISPLAY RESULT
# ---------------------------------------------------------

st.subheader("🧠 AI Screening Result")

h1, h2, h3 = st.columns(3)

h1.metric(
    "Health Risk Score",
    f"{health_score}/100"
)

h2.metric(
    "Health Risk Level",
    health_level
)

h3.metric(
    "Priority Age Groups",
    len(
        [
            x for x in priority
            if x != "General Household"
        ]
    )
)

if health_level == "HIGH":

    st.error(
        "🚨 HIGH HEALTH-RISK SCREENING PRIORITY"
    )

elif health_level == "MEDIUM":

    st.warning(
        "⚠️ MEDIUM HEALTH-RISK SCREENING PRIORITY"
    )

else:

    st.success(
        "🟢 LOW HEALTH-RISK SCREENING PRIORITY"
    )

# ---------------------------------------------------------
# POSSIBLE HEALTH-RISK CATEGORIES
# ---------------------------------------------------------

st.subheader(
    "🩺 Health-Risk Screening Categories"
)

for category in risk_categories:

    st.write(
        "🔎",
        category
    )

# ---------------------------------------------------------
# EXPLAINABLE AI
# ---------------------------------------------------------

st.subheader(
    "🔍 Why did AI give this result?"
)

if health_factors:

    for factor in health_factors:

        st.warning(
            "• " + factor
        )

else:

    st.success(
        "No major contributing factor detected."
    )

# ---------------------------------------------------------
# AGE-WISE IMPACT
# ---------------------------------------------------------

st.subheader(
    "👨‍👩‍👧 Age-wise Vulnerability Analysis"
)

age_data = pd.DataFrame({

    "Age Group": [
        "0-5",
        "6-17",
        "18-59",
        "60+"
    ],

    "Family Members": [
        age_0_5,
        age_6_17,
        age_18_59,
        age_60
    ],

    "Priority": [
        "HIGH" if age_0_5 > 0 and water_level != "Low"
        else "NORMAL",

        "HIGH" if age_6_17 > 0 and water_level == "High"
        else "NORMAL",

        "NORMAL",

        "HIGH" if age_60 > 0 and water_level != "Low"
        else "NORMAL"
    ]
})

st.dataframe(
    age_data,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# AUTOMATIC HEALTH RECOMMENDATION
# ---------------------------------------------------------

st.subheader(
    "💡 AI Recommended Action"
)

if health_level == "HIGH":

    st.error(
        """
1. Prefer safe/treated drinking water.
2. Avoid untreated water.
3. Arrange authorized/laboratory water testing.
4. Give additional precaution to vulnerable age groups.
5. Increase household/community monitoring.
6. Seek qualified medical advice if symptoms occur.
"""
    )

elif health_level == "MEDIUM":

    st.warning(
        """
1. Prefer safe drinking water.
2. Continue water-quality monitoring.
3. Consider authorized water testing.
4. Pay additional attention to vulnerable age groups.
5. Monitor the local situation.
"""
    )

else:

    st.success(
        """
1. Continue safe water practices.
2. Continue regular monitoring.
3. Keep household water sources clean.
"""
    )

# ---------------------------------------------------------
# AUTOMATIC HEALTH OFFICER MESSAGE
# ---------------------------------------------------------

if health_level == "HIGH":

    officer_message = f"""
🚨 COMMUNITY HEALTH EARLY WARNING

Village: {selected_village}
District: {selected["district"]}

Health Risk Score: {health_score}/100
Health Risk Level: HIGH

Water Risk Score: {water_score}/100

Priority Age Groups:
{", ".join(priority)}

Screening Categories:
{", ".join(risk_categories)}

Important Factors:
{", ".join(health_factors)}

Recommended:
Verify the water source, arrange authorized/laboratory
testing and increase community monitoring.
"""

    st.subheader(
        "🏥 Health Officer Early-Warning Message"
    )

    st.code(
        officer_message,
        language="text"
    )

    if st.button(
        "🚨 Save AI Health Warning"
    ):

        save_alert(
            selected["village"],
            selected["district"],
            "High",
            health_score
        )

        st.success(
            "✅ AI health warning saved successfully."
        )

# ---------------------------------------------------------
# DISCLAIMER
# ---------------------------------------------------------

st.caption(
    "⚠️ This module provides an early-warning screening result, "
    "not a medical diagnosis. Disease confirmation requires "
    "appropriate laboratory testing and qualified healthcare professionals."
)
# =========================================================
# 📢 MULTI-LEVEL NOTIFICATION CENTER
# =========================================================

st.divider()

st.header("📢 Multi-Level Alert & Notification Center")

st.write(
    "The system automatically decides the appropriate alert "
    "level based on household and community health risk."
)

# ---------------------------------------------------------
# ALERT LEVEL
# ---------------------------------------------------------

if health_score >= 85 or water_score >= 85:

    notification_level = "CRITICAL"

elif health_score >= 70 or water_score >= 60:

    notification_level = "HIGH"

elif health_score >= 40 or water_score >= 30:

    notification_level = "MEDIUM"

else:

    notification_level = "LOW"


# ---------------------------------------------------------
# RECIPIENTS
# ---------------------------------------------------------

if notification_level == "CRITICAL":

    recipients = [
        "👨‍👩‍👧 Family",
        "🏥 Health Worker",
        "🏛️ Health Authority / Admin"
    ]

elif notification_level == "HIGH":

    recipients = [
        "👨‍👩‍👧 Family",
        "🏥 Health Worker"
    ]

elif notification_level == "MEDIUM":

    recipients = [
        "👨‍👩‍👧 Family"
    ]

else:

    recipients = [
        "📊 Monitoring Dashboard"
    ]


# ---------------------------------------------------------
# NOTIFICATION STATUS
# ---------------------------------------------------------

n1, n2, n3 = st.columns(3)

n1.metric(
    "Alert Level",
    notification_level
)

n2.metric(
    "Health Score",
    f"{health_score}/100"
)

n3.metric(
    "Water Score",
    f"{water_score}/100"
)


# ---------------------------------------------------------
# DISPLAY LEVEL
# ---------------------------------------------------------

if notification_level == "CRITICAL":

    st.error(
        "🚨 CRITICAL ALERT — Immediate attention required"
    )

elif notification_level == "HIGH":

    st.error(
        "🔴 HIGH PRIORITY ALERT"
    )

elif notification_level == "MEDIUM":

    st.warning(
        "🟡 MEDIUM PRIORITY ALERT"
    )

else:

    st.success(
        "🟢 NORMAL MONITORING"
    )


# ---------------------------------------------------------
# RECIPIENT LIST
# ---------------------------------------------------------

st.subheader(
    "📨 Alert Recipients"
)

for recipient in recipients:

    st.write(
        f"✅ {recipient}"
    )


# ---------------------------------------------------------
# FAMILY NOTIFICATION
# ---------------------------------------------------------

family_notification = f"""
👨‍👩‍👧 FAMILY HEALTH ALERT

House ID:
{house_id}

Village:
{household_village}

Water Source:
{water_source}

Water Risk:
{water_score}/100

Health Risk:
{health_score}/100

Alert Level:
{notification_level}

Priority Age Groups:
{", ".join(priority)}

Recommended Action:

Use safe/treated drinking water.
Avoid untreated water.
Continue water-quality monitoring.
Arrange authorized/laboratory testing when appropriate.

This is an early-warning screening message,
not a medical diagnosis.
"""


# ---------------------------------------------------------
# HEALTH WORKER NOTIFICATION
# ---------------------------------------------------------

health_worker_notification = f"""
🏥 HEALTH WORKER ALERT

Village:
{selected_village}

District:
{selected["district"]}

House:
{house_id}

Water Risk:
{water_score}/100

Health Risk:
{health_score}/100

Alert Level:
{notification_level}

Priority Age Groups:
{", ".join(priority)}

Possible Screening Categories:
{", ".join(risk_categories)}

Important Factors:
{", ".join(health_factors)}

Recommended Field Action:

1. Verify the reported household water condition.
2. Check nearby households.
3. Inspect possible common water source.
4. Arrange authorized/laboratory water testing.
5. Escalate according to local health procedures.
"""


# ---------------------------------------------------------
# ADMIN NOTIFICATION
# ---------------------------------------------------------

admin_notification = f"""
🚨 COMMUNITY HEALTH ADMIN ALERT

Village:
{selected_village}

District:
{selected["district"]}

Alert Level:
{notification_level}

Health Risk Score:
{health_score}/100

Water Risk Score:
{water_score}/100

Household:
{house_id}

Community Monitoring Action:

Review nearby household readings.
Check for possible water-risk clusters.
Verify common water sources.
Coordinate appropriate field/laboratory assessment.

Generated:
{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
"""


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "👨‍👩‍👧 Family",
        "🏥 Health Worker",
        "🏛️ Admin"
    ]
)


with tab1:

    st.subheader(
        "Family Notification"
    )

    st.code(
        family_notification,
        language="text"
    )


with tab2:

    st.subheader(
        "Health Worker Notification"
    )

    st.code(
        health_worker_notification,
        language="text"
    )


with tab3:

    st.subheader(
        "Admin Notification"
    )

    st.code(
        admin_notification,
        language="text"
    )


# ---------------------------------------------------------
# SAVE NOTIFICATION
# ---------------------------------------------------------

st.subheader(
    "📤 Notification Center"
)

if st.button(
    "📨 Generate Multi-Level Alert",
    type="primary"
):

    notification_record = {

        "date_time":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),

        "house_id":
            house_id,

        "village":
            household_village,

        "water_score":
            water_score,

        "health_score":
            health_score,

        "alert_level":
            notification_level,

        "recipients":
            ", ".join(recipients),

        "priority_age_groups":
            ", ".join(priority),

        "status":
            "GENERATED"
    }

    save_family_alert(
        notification_record
    )

    st.success(
        "✅ Multi-level alert generated successfully."
    )

    st.info(
        "MVP mode: notification is generated and stored. "
        "Production mode can connect this event to an "
        "SMS/WhatsApp/mobile notification provider."
    )


# ---------------------------------------------------------
# ALERT DECISION LOGIC
# ---------------------------------------------------------

with st.expander(
    "🧠 View AI Alert Decision Logic"
):

    st.write(
        f"""
Current Water Score: {water_score}/100

Current Health Score: {health_score}/100

Final Alert Level: {notification_level}

Recipients:

{chr(10).join(recipients)}

The system uses the combined screening scores
to decide the notification priority.
"""
    )


# ---------------------------------------------------------
# EMERGENCY ACTION
# ---------------------------------------------------------

if notification_level == "CRITICAL":

    st.error(
        """
🚨 CRITICAL COMMUNITY WARNING

The system has detected a very high screening priority.

Do not rely on this automated result as a disease diagnosis.
Verify the water condition through appropriate testing
and follow responsible local health procedures.
"""
    )

    if st.button(
        "🚨 SAVE CRITICAL INCIDENT"
    ):

        save_alert(
            selected["village"],
            selected["district"],
            "Critical",
            health_score
        )

        st.success(
            "Critical incident saved to alert history."
        )

       # =========================================================
# =========================================================
# 🔐 ROLE-BASED ACCESS DASHBOARD
# =========================================================

st.divider()

st.header("🔐 Role-Based Health Platform")

st.write(
    "Different users receive different information "
    "according to their role."
)

# =========================================================
# PREPARE DATA FOR ROLE DASHBOARDS
# =========================================================

# Village counts
high_villages = len(
    risk_df[
        risk_df["risk"].astype(str).str.title() == "High"
    ]
)

medium_villages = len(
    risk_df[
        risk_df["risk"].astype(str).str.title() == "Medium"
    ]
)

low_villages = len(
    risk_df[
        risk_df["risk"].astype(str).str.title() == "Low"
    ]
)


# Household history
role_history = load_water_history()


# Family alerts
role_family_alerts = load_family_alerts()


# Health alerts
role_health_alerts = load_alert_history()


# =========================================================
# HOUSEHOLD RISK COUNTS
# =========================================================

if (
    len(role_history) > 0
    and "risk_level" in role_history.columns
):

    role_high_households = len(
        role_history[
            role_history["risk_level"]
            .astype(str)
            .str.title() == "High"
        ]
    )

    role_medium_households = len(
        role_history[
            role_history["risk_level"]
            .astype(str)
            .str.title() == "Medium"
        ]
    )

    role_low_households = len(
        role_history[
            role_history["risk_level"]
            .astype(str)
            .str.title() == "Low"
        ]
    )

else:

    role_high_households = 0
    role_medium_households = 0
    role_low_households = 0


# Total unique households
if (
    len(role_history) > 0
    and "house_id" in role_history.columns
):

    role_total_households = (
        role_history["house_id"]
        .astype(str)
        .nunique()
    )

else:

    role_total_households = 0


# =========================================================
# ROLE SELECTION
# =========================================================

role = st.selectbox(
    "Select User Role",
    [
        "👨‍👩‍👧 Family",
        "🏥 Health Worker",
        "🏛️ Administrator"
    ],
    key="role_dashboard_selector"
)


# =========================================================
# 👨‍👩‍👧 FAMILY DASHBOARD
# =========================================================

if role == "👨‍👩‍👧 Family":

    st.subheader(
        "👨‍👩‍👧 Family Dashboard"
    )

    st.success(
        f"Welcome to household: {house_id}"
    )


    # -----------------------------------------------------
    # FAMILY METRICS
    # -----------------------------------------------------

    f1, f2, f3 = st.columns(3)

    f1.metric(
        "💧 Water Risk",
        f"{water_score}/100"
    )

    f2.metric(
        "🩺 Health Risk",
        f"{health_score}/100"
    )

    f3.metric(
        "🚨 Alert Level",
        notification_level
    )


    # -----------------------------------------------------
    # WATER STATUS
    # -----------------------------------------------------

    st.subheader(
        "💧 My Water Status"
    )

    if water_level == "High":

        st.error(
            "🔴 Your household water screening "
            "requires immediate attention."
        )

    elif water_level == "Medium":

        st.warning(
            "🟡 Your household water screening "
            "requires monitoring."
        )

    else:

        st.success(
            "🟢 Your household water screening "
            "is currently low risk."
        )


    # -----------------------------------------------------
    # FAMILY VULNERABILITY
    # -----------------------------------------------------

    st.subheader(
        "👨‍👩‍👧 Family Vulnerability"
    )

    v1, v2 = st.columns(2)

    v1.metric(
        "Vulnerability Score",
        f"{vulnerability_score}/100"
    )

    v2.metric(
        "Combined Priority",
        f"{combined_household_score}/100"
    )


    st.subheader(
        "👶 Priority Age Groups"
    )

    for group in priority:

        st.write(
            "⚠️",
            group
        )


    # -----------------------------------------------------
    # FAMILY HEALTH RISK
    # -----------------------------------------------------

    st.subheader(
        "🩺 Health Risk Category"
    )

    st.info(
        health_category
    )


    # -----------------------------------------------------
    # FAMILY NOTIFICATION
    # -----------------------------------------------------

    st.subheader(
        "📱 My Latest Health Notification"
    )

    st.code(
        family_notification,
        language="text"
    )


    st.info(
        "Production version will show only the "
        "logged-in family's private information."
    )


# =========================================================
# 🏥 HEALTH WORKER DASHBOARD
# =========================================================

elif role == "🏥 Health Worker":

    st.subheader(
        "🏥 Health Worker Dashboard"
    )


    # -----------------------------------------------------
    # HEALTH WORKER METRICS
    # -----------------------------------------------------

    w1, w2, w3, w4 = st.columns(4)

    w1.metric(
        "🏘️ Villages",
        len(data)
    )

    w2.metric(
        "🔴 High-Risk Villages",
        high_villages
    )

    w3.metric(
        "🏠 High-Risk Houses",
        role_high_households
    )

    w4.metric(
        "📱 Family Alerts",
        len(role_family_alerts)
    )


    # -----------------------------------------------------
    # VILLAGE PRIORITY
    # -----------------------------------------------------

    st.subheader(
        "🚨 Priority Villages"
    )

    priority_villages_worker = risk_df[
        risk_df["risk"]
        .astype(str)
        .str.title() == "High"
    ].sort_values(
        "score",
        ascending=False
    )


    if len(priority_villages_worker) > 0:

        st.dataframe(
            priority_villages_worker[
                [
                    "village",
                    "district",
                    "risk",
                    "score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "No high-risk villages currently detected."
        )


    # -----------------------------------------------------
    # HIGH-RISK HOUSEHOLDS
    # -----------------------------------------------------

    st.subheader(
        "🏠 High-Risk Households"
    )


    if len(role_history) > 0:

        high_households_df = role_history[
            role_history["risk_level"]
            .astype(str)
            .str.title() == "High"
        ]


        if len(high_households_df) > 0:

            st.dataframe(
                high_households_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No high-risk households recorded."
            )

    else:

        st.info(
            "No household readings available."
        )


    # -----------------------------------------------------
    # COMMUNITY CLUSTER
    # -----------------------------------------------------

    st.subheader(
        "🚨 Community Water Cluster Status"
    )


    if role_high_households >= 3:

        st.error(
            """
🚨 POSSIBLE COMMUNITY WATER-RISK CLUSTER

Multiple households are showing HIGH
water-screening risk.

Recommended:
• Check common water sources
• Increase household monitoring
• Arrange authorized/laboratory testing
• Inform appropriate health authorities
"""
        )

    elif role_high_households >= 1:

        st.warning(
            """
⚠️ EARLY WARNING

High-risk household(s) detected.

Monitor nearby households and
check possible common water sources.
"""
        )

    else:

        st.success(
            "🟢 No high-risk household cluster detected."
        )


    # -----------------------------------------------------
    # HEALTH WORKER NOTIFICATION
    # -----------------------------------------------------

    st.subheader(
        "📨 Health Worker Notification"
    )

    st.code(
        health_worker_notification,
        language="text"
    )


    # -----------------------------------------------------
    # RECENT FAMILY ALERTS
    # -----------------------------------------------------

    st.subheader(
        "📱 Recent Family Alerts"
    )

    if len(role_family_alerts) > 0:

        st.dataframe(
            role_family_alerts.tail(10),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No family alerts available."
        )


# =========================================================
# 🏛️ ADMINISTRATOR DASHBOARD
# =========================================================

else:

    st.subheader(
        "🏛️ Administrator Dashboard"
    )


    # -----------------------------------------------------
    # ADMIN METRICS
    # -----------------------------------------------------

    a1, a2, a3, a4, a5 = st.columns(5)

    a1.metric(
        "🏘️ Villages",
        len(data)
    )

    a2.metric(
        "🏠 Households",
        role_total_households
    )

    a3.metric(
        "🔴 High-Risk Houses",
        role_high_households
    )

    a4.metric(
        "🏥 Health Alerts",
        len(role_health_alerts)
    )

    a5.metric(
        "📱 Family Alerts",
        len(role_family_alerts)
    )


    # -----------------------------------------------------
    # OVERALL RISK SUMMARY
    # -----------------------------------------------------

    st.subheader(
        "📊 Overall Risk Summary"
    )


    admin_summary = pd.DataFrame({

        "Category": [

            "High Villages",
            "Medium Villages",
            "Low Villages",

            "High Houses",
            "Medium Houses",
            "Low Houses"

        ],

        "Count": [

            high_villages,
            medium_villages,
            low_villages,

            role_high_households,
            role_medium_households,
            role_low_households

        ]
    })


    st.dataframe(
        admin_summary,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------------------------------
    # VILLAGE RISK CHART
    # -----------------------------------------------------

    st.subheader(
        "📈 Village Risk Distribution"
    )

    admin_village_chart = pd.DataFrame({

        "Risk Level": [
            "High",
            "Medium",
            "Low"
        ],

        "Villages": [
            high_villages,
            medium_villages,
            low_villages
        ]
    })


    st.bar_chart(
        admin_village_chart.set_index(
            "Risk Level"
        )
    )


    # -----------------------------------------------------
    # HOUSEHOLD RISK CHART
    # -----------------------------------------------------

    st.subheader(
        "💧 Household Water Risk Distribution"
    )

    admin_house_chart = pd.DataFrame({

        "Risk Level": [
            "High",
            "Medium",
            "Low"
        ],

        "Households": [
            role_high_households,
            role_medium_households,
            role_low_households
        ]
    })


    if admin_house_chart["Households"].sum() > 0:

        st.bar_chart(
            admin_house_chart.set_index(
                "Risk Level"
            )
        )

    else:

        st.info(
            "No household readings available yet."
        )


    # -----------------------------------------------------
    # HEALTH ALERT HISTORY
    # -----------------------------------------------------

    st.subheader(
        "🚨 Health Alert History"
    )


    if len(role_health_alerts) > 0:

        st.dataframe(
            role_health_alerts,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No health alerts generated."
        )


    # -----------------------------------------------------
    # FAMILY ALERT HISTORY
    # -----------------------------------------------------

    st.subheader(
        "📱 Family Alert History"
    )


    if len(role_family_alerts) > 0:

        st.dataframe(
            role_family_alerts,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No family alerts generated."
        )


    # -----------------------------------------------------
    # ADMIN ACTION
    # -----------------------------------------------------

    st.subheader(
        "🏛️ Administrative Recommendation"
    )


    if role_high_households >= 3:

        st.error(
            """
🚨 PRIORITY COMMUNITY ACTION

Multiple households show high
water-screening risk.

Recommended:

1. Verify common water sources.
2. Arrange authorized/laboratory testing.
3. Increase community surveillance.
4. Review nearby household readings.
5. Coordinate with appropriate health authorities.
"""
        )

    elif role_high_households >= 1:

        st.warning(
            """
⚠️ EARLY ACTION

A high-risk household has been detected.

Increase monitoring of nearby households.
"""
        )

    else:

        st.success(
            "🟢 No immediate community-level action indicated."
        )


# =========================================================
# 🏗️ SYSTEM ARCHITECTURE
# =========================================================

with st.expander(
    "🏗️ View Complete System Architecture"
):

    st.code(
        """
🏠 HOUSEHOLD
      ↓
📡 IoT WATER SENSORS
      ↓
💧 pH / TDS / TURBIDITY / TEMPERATURE
      ↓
🤖 AI WATER RISK ENGINE
      ↓
👨‍👩‍👧 FAMILY VULNERABILITY ANALYSIS
      ↓
🩺 HEALTH RISK INTELLIGENCE
      ↓
📢 MULTI-LEVEL ALERT ENGINE
      ↓
┌─────────────────────────────────────┐
│                                     │
│  👨‍👩‍👧 FAMILY                      │
│          ↓                          │
│  🏥 HEALTH WORKER                   │
│          ↓                          │
│  🏛️ ADMINISTRATOR                   │
│                                     │
└─────────────────────────────────────┘
      ↓
🚨 COMMUNITY CLUSTER DETECTION
      ↓
📊 EARLY WARNING
        """,
        language="text"
    )


# =========================================================
# FINAL DISCLAIMER
# =========================================================

st.caption(
    "⚠️ This platform is an early-warning and decision-support "
    "prototype. Sensor readings cannot diagnose a disease. "
    "Disease confirmation requires appropriate laboratory testing "
    "and qualified healthcare professionals."
)
# =========================================================
# 📲 JEEVAN-ALERT NOTIFICATION CENTER
# =========================================================

st.divider()

st.header("📲 Household Notification Center")

st.write(
    "This module prepares personalized household alerts "
    "and stores notification records for future SMS, "
    "WhatsApp, or mobile-app integration."
)


# =========================================================
# FILE PATHS
# =========================================================

CONTACT_FILE = "data/household_contacts.csv"
NOTIFICATION_FILE = "data/notification_history.csv"


# =========================================================
# CREATE DATA FOLDER
# =========================================================

if not os.path.exists("data"):
    os.makedirs("data")


# =========================================================
# CONTACT FILE
# =========================================================

if not os.path.exists(CONTACT_FILE):

    contact_columns = [
        "house_id",
        "name",
        "mobile",
        "village",
        "created_at"
    ]

    pd.DataFrame(
        columns=contact_columns
    ).to_csv(
        CONTACT_FILE,
        index=False
    )


# =========================================================
# NOTIFICATION FILE
# =========================================================

if not os.path.exists(NOTIFICATION_FILE):

    notification_columns = [
        "date_time",
        "house_id",
        "name",
        "mobile",
        "village",
        "water_source",
        "water_score",
        "risk_level",
        "priority_age_groups",
        "health_risk",
        "notification_type",
        "status",
        "message"
    ]

    pd.DataFrame(
        columns=notification_columns
    ).to_csv(
        NOTIFICATION_FILE,
        index=False
    )


# =========================================================
# LOAD CURRENT HOUSEHOLD INFORMATION
# =========================================================

current_house_id = str(
    globals().get(
        "house_id",
        "HOUSE-001"
    )
)

current_village = str(
    globals().get(
        "household_village",
        "Unknown"
    )
)

current_water_source = str(
    globals().get(
        "water_source",
        "Unknown"
    )
)

current_water_score = float(
    globals().get(
        "water_score",
        0
    )
)

current_water_level = str(
    globals().get(
        "water_level",
        "Low"
    )
)

current_health_category = str(
    globals().get(
        "health_category",
        "Low"
    )
)


# =========================================================
# PRIORITY AGE GROUPS
# =========================================================

current_priority = globals().get(
    "priority",
    []
)

if isinstance(
    current_priority,
    list
):

    if len(current_priority) > 0:

        priority_text = ", ".join(
            current_priority
        )

    else:

        priority_text = "No specific priority group"

else:

    priority_text = str(
        current_priority
    )


# =========================================================
# RISK LEVEL
# =========================================================

if current_water_score >= 70:

    notification_risk = "High"

elif current_water_score >= 40:

    notification_risk = "Medium"

else:

    notification_risk = "Low"


# Use existing risk level when available
if current_water_level in [
    "High",
    "Medium",
    "Low"
]:

    notification_risk = current_water_level


# =========================================================
# CONTACT REGISTRATION
# =========================================================

st.subheader(
    "👨‍👩‍👧 Household Contact Registration"
)

c1, c2 = st.columns(2)


with c1:

    notification_name = st.text_input(
        "👤 Family / Household Name",
        key="notification_family_name",
        placeholder="Enter family name"
    )


with c2:

    notification_mobile = st.text_input(
        "📱 Mobile Number",
        key="notification_mobile_number",
        placeholder="Enter 10-digit mobile number"
    )


st.text_input(
    "🏠 House ID",
    value=current_house_id,
    disabled=True,
    key="notification_house_id_display"
)

st.text_input(
    "🏘️ Village",
    value=current_village,
    disabled=True,
    key="notification_village_display"
)


# =========================================================
# SAVE CONTACT
# =========================================================

if st.button(
    "💾 SAVE HOUSEHOLD CONTACT",
    type="primary",
    key="save_household_contact_button"
):

    clean_mobile = (
        notification_mobile
        .replace(" ", "")
        .replace("-", "")
        .replace("+91", "")
    )

    if notification_name.strip() == "":

        st.error(
            "❌ Please enter the household/family name."
        )

    elif not clean_mobile.isdigit():

        st.error(
            "❌ Mobile number must contain digits only."
        )

    elif len(clean_mobile) != 10:

        st.error(
            "❌ Please enter a valid 10-digit mobile number."
        )

    else:

        contacts_df = pd.read_csv(
            CONTACT_FILE
        )

        new_contact = pd.DataFrame(
            [
                {
                    "house_id":
                        current_house_id,

                    "name":
                        notification_name.strip(),

                    "mobile":
                        clean_mobile,

                    "village":
                        current_village,

                    "created_at":
                        datetime.now().strftime(
                            "%d-%m-%Y %H:%M:%S"
                        )
                }
            ]
        )

        contacts_df = pd.concat(
            [
                contacts_df,
                new_contact
            ],
            ignore_index=True
        )

        contacts_df.to_csv(
            CONTACT_FILE,
            index=False
        )

        st.success(
            "✅ Household contact saved successfully."
        )


# =========================================================
# CURRENT RISK SUMMARY
# =========================================================

st.subheader(
    "💧 Current Household Risk"
)

r1, r2, r3, r4 = st.columns(4)


r1.metric(
    "Water Score",
    f"{current_water_score:.1f}/100"
)


r2.metric(
    "Risk Level",
    notification_risk
)


r3.metric(
    "Health Risk",
    current_health_category
)


r4.metric(
    "Water Source",
    current_water_source
)


# =========================================================
# PERSONALIZED MESSAGE
# =========================================================

st.subheader(
    "📩 Personalized Alert Message"
)


if notification_risk == "High":

    notification_type = (
        "HIGH WATER RISK ALERT"
    )

    notification_message = f"""
🚨 JEEVAN-ALERT HIGH RISK ALERT

House ID: {current_house_id}
Village: {current_village}

Water Source:
{current_water_source}

Water Risk Score:
{current_water_score:.1f}/100

Risk Level:
HIGH

Priority Age Group:
{priority_text}

Health Risk:
{current_health_category}

Recommended Actions:

1. Avoid consuming untreated water.
2. Prefer safe/treated drinking water.
3. Give additional precaution to vulnerable age groups.
4. Arrange appropriate water-quality testing.
5. Contact the appropriate health authority if required.

This is an early-warning screening alert,
not a medical diagnosis.
"""


elif notification_risk == "Medium":

    notification_type = (
        "WATER QUALITY WARNING"
    )

    notification_message = f"""
⚠️ JEEVAN-ALERT WATER QUALITY WARNING

House ID: {current_house_id}
Village: {current_village}

Water Source:
{current_water_source}

Water Risk Score:
{current_water_score:.1f}/100

Risk Level:
MEDIUM

Priority Age Group:
{priority_text}

Health Risk:
{current_health_category}

Recommended Actions:

1. Prefer safe/treated drinking water.
2. Monitor water quality.
3. Consider appropriate water testing.
4. Give additional precaution to vulnerable groups.

This is an early-warning screening alert,
not a medical diagnosis.
"""


else:

    notification_type = (
        "WATER MONITORING UPDATE"
    )

    notification_message = f"""
🟢 JEEVAN-ALERT WATER MONITORING UPDATE

House ID: {current_house_id}
Village: {current_village}

Water Source:
{current_water_source}

Water Risk Score:
{current_water_score:.1f}/100

Risk Level:
LOW

Priority Age Group:
{priority_text}

Health Risk:
{current_health_category}

Current screening does not indicate
a major water-quality risk.

Continue regular monitoring.
"""


st.code(
    notification_message,
    language="text"
)


# =========================================================
# RECIPIENT SELECTION
# =========================================================

st.subheader(
    "📢 Notification Recipients"
)

recipient_options = [
    "👨‍👩‍👧 Family",
    "🏥 Health Worker",
    "🏛️ Administrator"
]


if notification_risk == "High":

    default_recipients = [
        "👨‍👩‍👧 Family",
        "🏥 Health Worker"
    ]

elif notification_risk == "Medium":

    default_recipients = [
        "👨‍👩‍👧 Family"
    ]

else:

    default_recipients = [
        "👨‍👩‍👧 Family"
    ]


recipients = st.multiselect(
    "Select who should receive this notification",
    recipient_options,
    default=default_recipients,
    key="notification_recipients"
)


# =========================================================
# SEND / RECORD NOTIFICATION
# =========================================================

if st.button(
    "📲 SEND / RECORD NOTIFICATION",
    type="primary",
    key="send_notification_button"
):

    if notification_name.strip() == "":

        st.error(
            "❌ Please enter the family/household name first."
        )

    elif notification_mobile.strip() == "":

        st.error(
            "❌ Please enter a mobile number first."
        )

    elif len(recipients) == 0:

        st.error(
            "❌ Please select at least one recipient."
        )

    else:

        notification_df = pd.read_csv(
            NOTIFICATION_FILE
        )

        recipient_text = ", ".join(
            recipients
        )

        notification_record = {

            "date_time":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),

            "house_id":
                current_house_id,

            "name":
                notification_name.strip(),

            "mobile":
                notification_mobile.strip(),

            "village":
                current_village,

            "water_source":
                current_water_source,

            "water_score":
                current_water_score,

            "risk_level":
                notification_risk,

            "priority_age_groups":
                priority_text,

            "health_risk":
                current_health_category,

            "notification_type":
                f"{notification_type} → {recipient_text}",

            "status":
                "GENERATED / RECORDED",

            "message":
                notification_message
        }


        notification_df = pd.concat(
            [
                notification_df,
                pd.DataFrame(
                    [notification_record]
                )
            ],
            ignore_index=True
        )


        notification_df.to_csv(
            NOTIFICATION_FILE,
            index=False
        )


        st.success(
            "✅ Notification generated and recorded successfully."
        )

        st.info(
            f"""
📲 Notification Status: RECORDED

Recipients:
{recipient_text}

Mobile:
{notification_mobile}

Risk:
{notification_risk}

In the production version, this same
notification can be connected to an
SMS, WhatsApp, or mobile-app service.
"""
        )


# =========================================================
# NOTIFICATION HISTORY
# =========================================================

st.subheader(
    "📋 Notification History"
)


notification_history_df = pd.read_csv(
    NOTIFICATION_FILE
)


if len(notification_history_df) > 0:

    st.dataframe(
        notification_history_df,
        use_container_width=True,
        hide_index=True
    )


    notification_csv = (
        notification_history_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        "⬇️ Download Notification History",
        data=notification_csv,
        file_name="notification_history.csv",
        mime="text/csv",
        key="admin_download_notification_history"
    )

else:

    st.info(
        "No notifications have been recorded yet."
    )


# =========================================================
# PRODUCTION NOTIFICATION ROADMAP
# =========================================================

with st.expander(
    "🚀 Future Real-Time Notification Integration"
):

    st.write(
        """
Current MVP:
Water Risk
     ↓
AI Analysis
     ↓
Personalized Message
     ↓
Notification Record

Future Production System:
Water Sensor
     ↓
ESP32
     ↓
Internet / Wi-Fi
     ↓
JEEVAN-ALERT Server
     ↓
AI Risk Engine
     ↓
Notification Engine
     ↓
SMS / WhatsApp / Mobile App
     ↓
Family / Health Worker / Administrator
"""
    )

# =========================================================
# 🚨 COMMUNITY RISK COMMAND CENTER
# =========================================================

st.divider()

st.header("🚨 Community Risk Command Center")

st.write(
    "A centralized dashboard for identifying household, "
    "village, water-source and community-level risk patterns."
)


# =========================================================
# LOAD HOUSEHOLD DATA
# =========================================================

try:

    command_history = load_water_history()

except Exception:

    command_history = pd.DataFrame()


# =========================================================
# LOAD NOTIFICATION DATA
# =========================================================

try:

    command_notifications = pd.read_csv(
        "data/notification_history.csv"
    )

except Exception:

    command_notifications = pd.DataFrame()


# =========================================================
# PREPARE DATA
# =========================================================

if len(command_history) > 0:

    command_history = command_history.copy()

    if "risk_level" in command_history.columns:

        command_history["risk_level_clean"] = (
            command_history["risk_level"]
            .astype(str)
            .str.strip()
            .str.title()
        )

    else:

        command_history["risk_level_clean"] = "Low"

else:

    command_history = pd.DataFrame()


# =========================================================
# COMMUNITY METRICS
# =========================================================

if len(command_history) > 0:

    total_readings = len(
        command_history
    )

    if "house_id" in command_history.columns:

        total_houses = (
            command_history["house_id"]
            .astype(str)
            .nunique()
        )

    else:

        total_houses = 0


    high_risk_houses = len(
        command_history[
            command_history["risk_level_clean"]
            == "High"
        ]
    )


    medium_risk_houses = len(
        command_history[
            command_history["risk_level_clean"]
            == "Medium"
        ]
    )


    low_risk_houses = len(
        command_history[
            command_history["risk_level_clean"]
            == "Low"
        ]
    )

else:

    total_readings = 0
    total_houses = 0
    high_risk_houses = 0
    medium_risk_houses = 0
    low_risk_houses = 0


# =========================================================
# TOP METRICS
# =========================================================

st.subheader(
    "📊 Community Overview"
)

m1, m2, m3, m4, m5 = st.columns(5)


m1.metric(
    "🏠 Households",
    total_houses
)

m2.metric(
    "📋 Readings",
    total_readings
)

m3.metric(
    "🔴 High Risk",
    high_risk_houses
)

m4.metric(
    "🟡 Medium Risk",
    medium_risk_houses
)

m5.metric(
    "🟢 Low Risk",
    low_risk_houses
)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

st.subheader(
    "📈 Household Risk Distribution"
)


risk_distribution = pd.DataFrame({

    "Risk Level": [
        "High",
        "Medium",
        "Low"
    ],

    "Households": [
        high_risk_houses,
        medium_risk_houses,
        low_risk_houses
    ]
})


if risk_distribution["Households"].sum() > 0:

    st.bar_chart(
        risk_distribution.set_index(
            "Risk Level"
        )
    )

else:

    st.info(
        "No household readings available yet."
    )


# =========================================================
# VILLAGE HOTSPOT ANALYSIS
# =========================================================

st.subheader(
    "🔥 Village Risk Hotspots"
)


if (
    len(command_history) > 0
    and "village" in command_history.columns
):

    village_analysis = (
        command_history
        .groupby("village")
        .agg(
            households=(
                "house_id",
                "nunique"
            )
            if "house_id" in command_history.columns
            else (
                "risk_level_clean",
                "count"
            ),

            high_risk=(
                "risk_level_clean",
                lambda x:
                (
                    x == "High"
                ).sum()
            ),

            medium_risk=(
                "risk_level_clean",
                lambda x:
                (
                    x == "Medium"
                ).sum()
            )
        )
        .reset_index()
    )


    village_analysis["high_risk_ratio_%"] = (
        village_analysis["high_risk"]
        /
        village_analysis["households"]
        .replace(0, np.nan)
        * 100
    ).round(2)


    village_analysis = (
        village_analysis
        .sort_values(
            "high_risk_ratio_%",
            ascending=False
        )
    )


    st.dataframe(
        village_analysis,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "Village data will appear after household readings are saved."
    )


# =========================================================
# WATER SOURCE HOTSPOT
# =========================================================

st.subheader(
    "🚰 Water Source Risk Analysis"
)


if (
    len(command_history) > 0
    and "water_source" in command_history.columns
):

    source_analysis = (
        command_history
        .groupby("water_source")
        .agg(
            households=(
                "house_id",
                "nunique"
            )
            if "house_id" in command_history.columns
            else (
                "risk_level_clean",
                "count"
            ),

            high_risk=(
                "risk_level_clean",
                lambda x:
                (
                    x == "High"
                ).sum()
            ),

            medium_risk=(
                "risk_level_clean",
                lambda x:
                (
                    x == "Medium"
                ).sum()
            )
        )
        .reset_index()
    )


    source_analysis["risk_ratio_%"] = (
        source_analysis["high_risk"]
        /
        source_analysis["households"]
        .replace(0, np.nan)
        * 100
    ).round(2)


    source_analysis = (
        source_analysis
        .sort_values(
            "risk_ratio_%",
            ascending=False
        )
    )


    st.dataframe(
        source_analysis,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "Water-source analysis will appear after household readings are saved."
    )


# =========================================================
# COMMUNITY HOTSPOT DECISION
# =========================================================

st.subheader(
    "🧠 AI-Assisted Community Risk Status"
)


if high_risk_houses >= 5:

    st.error(
        """
🚨 HIGH COMMUNITY RISK

Multiple high-risk household readings have been detected.

Recommended priority:

• Investigate affected households
• Check common water sources
• Increase community monitoring
• Arrange appropriate water-quality testing
• Inform relevant health authorities when required
"""
    )

elif high_risk_houses >= 3:

    st.warning(
        """
⚠️ POSSIBLE COMMUNITY HOTSPOT

Several households are showing high-risk
water-screening results.

Nearby households and common water sources
should receive increased monitoring.
"""
    )

elif high_risk_houses >= 1:

    st.info(
        """
🔎 EARLY WARNING

A high-risk household has been detected.

Continue monitoring nearby households
and review the relevant water source.
"""
    )

else:

    st.success(
        """
🟢 COMMUNITY STATUS: NORMAL

No high-risk household cluster has
been detected in the available readings.
"""
    )


# =========================================================
# RISK TREND
# =========================================================

st.subheader(
    "📈 Community Risk Trend"
)


if (
    len(command_history) > 0
    and "date_time" in command_history.columns
):

    trend_data = command_history.copy()

    trend_data["date_time"] = pd.to_datetime(
        trend_data["date_time"],
        errors="coerce",
        dayfirst=True
    )


    if "water_score" in trend_data.columns:

        trend_data["water_score"] = pd.to_numeric(
            trend_data["water_score"],
            errors="coerce"
        )


        trend_data = trend_data.dropna(
            subset=[
                "date_time",
                "water_score"
            ]
        )


        if len(trend_data) > 0:

            daily_trend = (
                trend_data
                .groupby(
                    trend_data[
                        "date_time"
                    ].dt.date
                )[
                    "water_score"
                ]
                .mean()
                .reset_index()
            )


            daily_trend.columns = [
                "Date",
                "Average Water Risk"
            ]


            st.line_chart(
                daily_trend.set_index(
                    "Date"
                )
            )

        else:

            st.info(
                "More valid readings are required for trend analysis."
            )

    else:

        st.info(
            "Water-score data is not available yet."
        )

else:

    st.info(
        "Save household readings to generate the community trend."
    )


# =========================================================
# NOTIFICATION STATISTICS
# =========================================================

st.subheader(
    "📢 Notification Statistics"
)


if len(command_notifications) > 0:

    n_total = len(
        command_notifications
    )


    if "risk_level" in command_notifications.columns:

        n_high = len(
            command_notifications[
                command_notifications["risk_level"]
                .astype(str)
                .str.title()
                == "High"
            ]
        )

        n_medium = len(
            command_notifications[
                command_notifications["risk_level"]
                .astype(str)
                .str.title()
                == "Medium"
            ]
        )

    else:

        n_high = 0
        n_medium = 0

else:

    n_total = 0
    n_high = 0
    n_medium = 0


n1, n2, n3 = st.columns(3)


n1.metric(
    "📱 Total Notifications",
    n_total
)

n2.metric(
    "🔴 High-Risk Notifications",
    n_high
)

n3.metric(
    "🟡 Medium-Risk Notifications",
    n_medium
)


# =========================================================
# PRIORITY ACTION TABLE
# =========================================================

st.subheader(
    "🎯 Priority Action Center"
)


priority_actions = pd.DataFrame({

    "Risk Situation": [

        "High-risk household",
        "Multiple high-risk households",
        "Common-source concern",
        "Increasing risk trend"

    ],

    "Recommended Priority": [

        "Monitor household",
        "Investigate community cluster",
        "Check water source",
        "Increase surveillance"

    ],

    "Responsible Stakeholder": [

        "Family / Health Worker",
        "Health Worker",
        "Health Worker / Authority",
        "Health Worker / Administrator"

    ]
})


st.dataframe(
    priority_actions,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# COMMAND CENTER SUMMARY
# =========================================================

with st.expander(
    "🧠 How JEEVAN-ALERT Makes a Community Decision"
):

    st.code(
        """
HOUSEHOLD READINGS
        ↓
WATER RISK SCORE
        ↓
FAMILY VULNERABILITY
        ↓
MULTIPLE HOUSEHOLD ANALYSIS
        ↓
VILLAGE HOTSPOT
        ↓
COMMON WATER SOURCE
        ↓
COMMUNITY EARLY WARNING
        ↓
PRIORITY ACTION
        ↓
HEALTH WORKER / ADMINISTRATOR
        """,
        language="text"
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.caption(
    "⚠️ Community risk indicators are screening and "
    "decision-support outputs. They do not confirm disease "
    "or contamination and should be verified through "
    "appropriate testing and qualified authorities."
)
# =========================================================
# 📡 JEEVAN-ALERT IoT DEVICE MANAGEMENT
# =========================================================

st.divider()

st.header("📡 IoT Water Sensor Network")

st.write(
    "Manage household water-monitoring devices and "
    "view their latest sensor status."
)


# =========================================================
# FILE PATH
# =========================================================

IOT_FILE = "data/iot_devices.csv"


# =========================================================
# CREATE FILE
# =========================================================

if not os.path.exists("data"):
    os.makedirs("data")


if not os.path.exists(IOT_FILE):

    iot_columns = [
        "device_id",
        "house_id",
        "village",
        "status",
        "pH",
        "TDS",
        "turbidity",
        "temperature",
        "last_update"
    ]

    pd.DataFrame(
        columns=iot_columns
    ).to_csv(
        IOT_FILE,
        index=False
    )


# =========================================================
# LOAD DEVICES
# =========================================================

iot_devices = pd.read_csv(
    IOT_FILE
)


# =========================================================
# DEVICE REGISTRATION
# =========================================================

st.subheader(
    "➕ Register Water Sensor"
)

c1, c2 = st.columns(2)

with c1:

    device_id = st.text_input(
        "📡 Device ID",
        placeholder="Example: ESP32-H001",
        key="iot_device_id"
    )

    iot_house_id = st.text_input(
        "🏠 House ID",
        placeholder="Example: H001",
        key="iot_house_id"
    )


with c2:

    iot_village = st.text_input(
        "🏘️ Village",
        placeholder="Enter village",
        key="iot_village"
    )

    iot_status = st.selectbox(
        "🔌 Device Status",
        [
            "Connected",
            "Disconnected",
            "Maintenance"
        ],
        key="iot_status"
    )


if st.button(
    "📡 REGISTER SENSOR",
    type="primary",
    key="register_iot_device"
):

    if device_id.strip() == "":

        st.error(
            "❌ Please enter Device ID."
        )

    elif iot_house_id.strip() == "":

        st.error(
            "❌ Please enter House ID."
        )

    elif iot_village.strip() == "":

        st.error(
            "❌ Please enter village."
        )

    else:

        devices = pd.read_csv(
            IOT_FILE
        )

        existing = devices[
            devices["device_id"].astype(str)
            == device_id.strip()
        ]

        if len(existing) > 0:

            st.warning(
                "⚠️ This device is already registered."
            )

        else:

            new_device = pd.DataFrame(
                [
                    {
                        "device_id":
                            device_id.strip(),

                        "house_id":
                            iot_house_id.strip(),

                        "village":
                            iot_village.strip(),

                        "status":
                            iot_status,

                        "pH":
                            None,

                        "TDS":
                            None,

                        "turbidity":
                            None,

                        "temperature":
                            None,

                        "last_update":
                            "Not available"
                    }
                ]
            )

            devices = pd.concat(
                [
                    devices,
                    new_device
                ],
                ignore_index=True
            )

            devices.to_csv(
                IOT_FILE,
                index=False
            )

            st.success(
                "✅ IoT sensor registered successfully."
            )


# =========================================================
# DEVICE SUMMARY
# =========================================================

st.subheader(
    "📊 Sensor Network Status"
)

total_devices = len(iot_devices)

connected_devices = len(
    iot_devices[
        iot_devices["status"]
        .astype(str)
        .str.lower()
        == "connected"
    ]
)

disconnected_devices = len(
    iot_devices[
        iot_devices["status"]
        .astype(str)
        .str.lower()
        == "disconnected"
    ]
)


d1, d2, d3 = st.columns(3)

d1.metric(
    "📡 Total Devices",
    total_devices
)

d2.metric(
    "🟢 Connected",
    connected_devices
)

d3.metric(
    "🔴 Disconnected",
    disconnected_devices
)


# =========================================================
# REGISTERED DEVICE TABLE
# =========================================================

st.subheader(
    "📋 Registered Sensors"
)


if len(iot_devices) > 0:

    st.dataframe(
        iot_devices,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No IoT sensors registered yet."
    )


# =========================================================
# SIMULATE LIVE SENSOR READING
# =========================================================

st.subheader(
    "🧪 IoT Sensor Reading Simulator"
)

st.info(
    "This simulator represents the data that will "
    "later be received automatically from ESP32 sensors."
)


if len(iot_devices) > 0:

    selected_device = st.selectbox(
        "Select Sensor Device",
        iot_devices["device_id"].tolist(),
        key="selected_iot_device"
    )


    s1, s2 = st.columns(2)

    with s1:

        sensor_ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=7.0,
            step=0.1,
            key="iot_sensor_ph"
        )

        sensor_tds = st.number_input(
            "TDS",
            min_value=0.0,
            max_value=5000.0,
            value=300.0,
            step=10.0,
            key="iot_sensor_tds"
        )


    with s2:

        sensor_turbidity = st.number_input(
            "Turbidity",
            min_value=0.0,
            max_value=1000.0,
            value=1.0,
            step=0.1,
            key="iot_sensor_turbidity"
        )

        sensor_temperature = st.number_input(
            "Temperature °C",
            min_value=-10.0,
            max_value=80.0,
            value=25.0,
            step=0.1,
            key="iot_sensor_temperature"
        )


    if st.button(
        "📡 SEND SENSOR READING",
        type="primary",
        key="send_iot_reading"
    ):

        devices = pd.read_csv(
            IOT_FILE
        )

        device_index = devices[
            devices["device_id"].astype(str)
            == selected_device
        ].index


        if len(device_index) > 0:

            idx = device_index[0]

            devices.loc[
                idx,
                "pH"
            ] = sensor_ph

            devices.loc[
                idx,
                "TDS"
            ] = sensor_tds

            devices.loc[
                idx,
                "turbidity"
            ] = sensor_turbidity

            devices.loc[
                idx,
                "temperature"
            ] = sensor_temperature

            devices.loc[
                idx,
                "status"
            ] = "Connected"

            devices.loc[
                idx,
                "last_update"
            ] = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            devices.to_csv(
                IOT_FILE,
                index=False
            )

            st.success(
                "✅ Sensor reading received successfully."
            )


# =========================================================
# IOT WORKFLOW
# =========================================================

with st.expander(
    "🔄 Future Real-Time IoT Workflow"
):

    st.code(
        """
pH Sensor
     +
TDS Sensor
     +
Turbidity Sensor
     +
Temperature Sensor
     ↓
ESP32
     ↓
Wi-Fi / Internet
     ↓
JEEVAN-ALERT API
     ↓
Water Risk Engine
     ↓
AI Health-Risk Screening
     ↓
Household Alert
     ↓
Community Risk Detection
        """,
        language="text"
    )


st.caption(
    "Current module uses simulated sensor readings. "
    "Real ESP32 hardware integration will be added in "
    "the next development phase."
)
# =========================================================
# 🤖 AUTOMATIC IoT → AI RISK ENGINE
# =========================================================

st.divider()

st.header("🤖 Automatic IoT Risk Analysis")

st.write(
    "This module converts IoT sensor readings into "
    "an automatic water-risk and health-risk screening result."
)


# =========================================================
# LOAD IoT DEVICES
# =========================================================

try:

    auto_iot_devices = pd.read_csv(
        "data/iot_devices.csv"
    )

except Exception:

    auto_iot_devices = pd.DataFrame()


# =========================================================
# CHECK DEVICES
# =========================================================

if len(auto_iot_devices) == 0:

    st.info(
        "📡 No IoT devices are available yet. "
        "Register a sensor first."
    )

else:

    # =====================================================
    # SELECT DEVICE
    # =====================================================

    selected_auto_device = st.selectbox(
        "📡 Select IoT Device",
        auto_iot_devices["device_id"].astype(str).tolist(),
        key="automatic_iot_device"
    )


    selected_rows = auto_iot_devices[
        auto_iot_devices["device_id"].astype(str)
        == selected_auto_device
    ]


    if len(selected_rows) > 0:

        sensor_row = selected_rows.iloc[0]


        # =================================================
        # GET SENSOR VALUES
        # =================================================

        sensor_ph = pd.to_numeric(
            sensor_row["pH"],
            errors="coerce"
        )

        sensor_tds = pd.to_numeric(
            sensor_row["TDS"],
            errors="coerce"
        )

        sensor_turbidity = pd.to_numeric(
            sensor_row["turbidity"],
            errors="coerce"
        )

        sensor_temperature = pd.to_numeric(
            sensor_row["temperature"],
            errors="coerce"
        )


        sensor_house = str(
            sensor_row["house_id"]
        )

        sensor_village = str(
            sensor_row["village"]
        )


        # =================================================
        # SHOW SENSOR DATA
        # =================================================

        st.subheader(
            "📡 Latest Sensor Reading"
        )


        a1, a2, a3, a4 = st.columns(4)


        a1.metric(
            "pH",
            "N/A"
            if pd.isna(sensor_ph)
            else f"{sensor_ph:.2f}"
        )


        a2.metric(
            "TDS",
            "N/A"
            if pd.isna(sensor_tds)
            else f"{sensor_tds:.0f}"
        )


        a3.metric(
            "Turbidity",
            "N/A"
            if pd.isna(sensor_turbidity)
            else f"{sensor_turbidity:.2f}"
        )


        a4.metric(
            "Temperature",
            "N/A"
            if pd.isna(sensor_temperature)
            else f"{sensor_temperature:.1f} °C"
        )


        # =================================================
        # VALIDATE READING
        # =================================================

        valid_reading = all(
            [
                not pd.isna(sensor_ph),
                not pd.isna(sensor_tds),
                not pd.isna(sensor_turbidity),
                not pd.isna(sensor_temperature)
            ]
        )


        if not valid_reading:

            st.warning(
                "⚠️ Complete sensor readings are not "
                "available for this device."
            )

        else:

            # =============================================
            # WATER RISK CALCULATION
            # =============================================

            risk_points = 0


            # pH screening
            if sensor_ph < 6.5 or sensor_ph > 8.5:

                risk_points += 30


            elif sensor_ph < 6.8 or sensor_ph > 8.2:

                risk_points += 15


            # TDS screening
            if sensor_tds > 1000:

                risk_points += 30


            elif sensor_tds > 500:

                risk_points += 15


            # Turbidity screening
            if sensor_turbidity > 10:

                risk_points += 30


            elif sensor_turbidity > 5:

                risk_points += 15


            # Temperature screening
            if sensor_temperature > 35:

                risk_points += 10


            elif sensor_temperature > 30:

                risk_points += 5


            # Keep score within 0–100
            automatic_water_score = min(
                risk_points,
                100
            )


            # =============================================
            # RISK LEVEL
            # =============================================

            if automatic_water_score >= 60:

                automatic_risk = "High"

            elif automatic_water_score >= 30:

                automatic_risk = "Medium"

            else:

                automatic_risk = "Low"


            # =============================================
            # DISPLAY WATER RISK
            # =============================================

            st.subheader(
                "💧 Automatic Water Risk"
            )


            b1, b2 = st.columns(2)


            b1.metric(
                "Water Risk Score",
                f"{automatic_water_score}/100"
            )


            b2.metric(
                "Risk Level",
                automatic_risk
            )


            if automatic_risk == "High":

                st.error(
                    "🚨 HIGH WATER RISK DETECTED"
                )

            elif automatic_risk == "Medium":

                st.warning(
                    "⚠️ MEDIUM WATER RISK DETECTED"
                )

            else:

                st.success(
                    "🟢 LOW WATER RISK"
                )


            # =============================================
            # RISK FACTORS
            # =============================================

            st.subheader(
                "🔍 Risk Factors"
            )


            risk_factors = []


            if sensor_ph < 6.5 or sensor_ph > 8.5:

                risk_factors.append(
                    f"pH is outside the screening range ({sensor_ph:.2f})"
                )


            if sensor_tds > 1000:

                risk_factors.append(
                    f"TDS is high ({sensor_tds:.0f})"
                )


            elif sensor_tds > 500:

                risk_factors.append(
                    f"TDS is elevated ({sensor_tds:.0f})"
                )


            if sensor_turbidity > 10:

                risk_factors.append(
                    f"Turbidity is high ({sensor_turbidity:.2f})"
                )


            elif sensor_turbidity > 5:

                risk_factors.append(
                    f"Turbidity is elevated ({sensor_turbidity:.2f})"
                )


            if sensor_temperature > 35:

                risk_factors.append(
                    f"Water temperature is high ({sensor_temperature:.1f} °C)"
                )


            if len(risk_factors) > 0:

                for factor in risk_factors:

                    st.write(
                        "• " + factor
                    )

            else:

                st.write(
                    "✅ No major screening indicator detected."
                )


            # =============================================
            # AUTOMATIC RECOMMENDATION
            # =============================================

            st.subheader(
                "💡 Recommended Action"
            )


            if automatic_risk == "High":

                recommendation = """
🚨 Immediate precaution is recommended.

• Avoid consuming untreated water.
• Prefer safe/treated drinking water.
• Arrange appropriate water-quality testing.
• Review vulnerable household members.
• Consider notifying the responsible health worker.
"""

            elif automatic_risk == "Medium":

                recommendation = """
⚠️ Increased monitoring is recommended.

• Prefer safe/treated drinking water.
• Monitor water quality.
• Consider appropriate water testing.
• Give additional precaution to vulnerable groups.
"""

            else:

                recommendation = """
🟢 Continue regular monitoring.

• Maintain normal water-safety practices.
• Continue periodic water-quality checks.
• Monitor for changes in sensor readings.
"""


            st.info(
                recommendation
            )


            # =============================================
            # AUTOMATIC ALERT RECORD
            # =============================================

            if automatic_risk in [
                "High",
                "Medium"
            ]:

                if st.button(
                    "🚨 RECORD IoT ALERT",
                    type="primary",
                    key="record_iot_risk_alert"
                ):

                    iot_alert_file = (
                        "data/iot_alert_history.csv"
                    )


                    if os.path.exists(
                        iot_alert_file
                    ):

                        iot_alerts = pd.read_csv(
                            iot_alert_file
                        )

                    else:

                        iot_alerts = pd.DataFrame(
                            columns=[
                                "date_time",
                                "device_id",
                                "house_id",
                                "village",
                                "pH",
                                "TDS",
                                "turbidity",
                                "temperature",
                                "water_score",
                                "risk_level",
                                "status"
                            ]
                        )


                    new_alert = pd.DataFrame(
                        [
                            {
                                "date_time":
                                    datetime.now().strftime(
                                        "%d-%m-%Y %H:%M:%S"
                                    ),

                                "device_id":
                                    selected_auto_device,

                                "house_id":
                                    sensor_house,

                                "village":
                                    sensor_village,

                                "pH":
                                    sensor_ph,

                                "TDS":
                                    sensor_tds,

                                "turbidity":
                                    sensor_turbidity,

                                "temperature":
                                    sensor_temperature,

                                "water_score":
                                    automatic_water_score,

                                "risk_level":
                                    automatic_risk,

                                "status":
                                    "GENERATED"
                            }
                        ]
                    )


                    iot_alerts = pd.concat(
                        [
                            iot_alerts,
                            new_alert
                        ],
                        ignore_index=True
                    )


                    iot_alerts.to_csv(
                        iot_alert_file,
                        index=False
                    )


                    st.success(
                        "✅ IoT risk alert recorded successfully."
                    )


            # =============================================
            # SENSOR → AI → ALERT FLOW
            # =============================================

            with st.expander(
                "🔄 View Automatic Decision Flow"
            ):

                st.code(
                    f"""
IoT Device
    ↓
{selected_auto_device}
    ↓
House: {sensor_house}
    ↓
pH / TDS / Turbidity / Temperature
    ↓
Water Risk Score: {automatic_water_score}/100
    ↓
Risk Level: {automatic_risk}
    ↓
AI Health-Risk Screening
    ↓
Household Vulnerability Analysis
    ↓
Automatic Alert
    ↓
Family / Health Worker / Administrator
""",
                    language="text"
                )


st.caption(
    "⚠️ Sensor-based results are screening indicators "
    "and do not confirm contamination or disease. "
    "Appropriate laboratory testing and qualified "
    "health authorities should be used for confirmation."
)
# =========================================================
# 🚨 JEEVAN-ALERT AUTOMATIC ALERT BRIDGE
# IoT Risk → Notification → Stakeholder
# =========================================================

st.divider()

st.header("🚨 Automatic Alert Bridge")

st.write(
    "Automatically converts a detected IoT water-risk event "
    "into a stakeholder notification."
)


# =========================================================
# FILE PATHS
# =========================================================

IOT_ALERT_FILE = "data/iot_alert_history.csv"
NOTIFICATION_FILE = "data/notification_history.csv"
CONTACT_FILE = "data/household_contacts.csv"


# =========================================================
# CHECK IOT ALERT HISTORY
# =========================================================

if not os.path.exists(IOT_ALERT_FILE):

    st.info(
        "No IoT risk alerts are available yet. "
        "Generate an IoT risk alert first."
    )

else:

    bridge_alerts = pd.read_csv(
        IOT_ALERT_FILE
    )

    if len(bridge_alerts) == 0:

        st.info(
            "No IoT risk alerts are available yet."
        )

    else:

        st.subheader(
            "📋 Detected IoT Risk Events"
        )

        st.dataframe(
            bridge_alerts,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # SELECT ALERT
        # =================================================

        alert_options = []

        for index, row in bridge_alerts.iterrows():

            alert_label = (
                f"{index} | "
                f"{row.get('house_id', 'Unknown')} | "
                f"{row.get('risk_level', 'Unknown')} | "
                f"{row.get('date_time', 'Unknown')}"
            )

            alert_options.append(
                alert_label
            )


        selected_alert_label = st.selectbox(
            "Select Risk Event",
            alert_options,
            key="bridge_selected_alert"
        )


        selected_index = int(
            selected_alert_label.split("|")[0].strip()
        )


        selected_alert = bridge_alerts.iloc[
            selected_index
        ]


        # =================================================
        # EXTRACT DATA
        # =================================================

        bridge_house_id = str(
            selected_alert.get(
                "house_id",
                "Unknown"
            )
        )

        bridge_village = str(
            selected_alert.get(
                "village",
                "Unknown"
            )
        )

        bridge_risk = str(
            selected_alert.get(
                "risk_level",
                "Low"
            )
        ).title()

        bridge_score = float(
            pd.to_numeric(
                selected_alert.get(
                    "water_score",
                    0
                ),
                errors="coerce"
            )
            if not pd.isna(
                pd.to_numeric(
                    selected_alert.get(
                        "water_score",
                        0
                    ),
                    errors="coerce"
                )
            )
            else 0
        )

        bridge_device = str(
            selected_alert.get(
                "device_id",
                "Unknown"
            )
        )

        bridge_ph = selected_alert.get(
            "pH",
            "N/A"
        )

        bridge_tds = selected_alert.get(
            "TDS",
            "N/A"
        )

        bridge_turbidity = selected_alert.get(
            "turbidity",
            "N/A"
        )

        bridge_temperature = selected_alert.get(
            "temperature",
            "N/A"
        )


        # =================================================
        # SHOW EVENT
        # =================================================

        st.subheader(
            "🔍 Selected Risk Event"
        )

        e1, e2, e3, e4 = st.columns(4)

        e1.metric(
            "House",
            bridge_house_id
        )

        e2.metric(
            "Risk Score",
            f"{bridge_score:.0f}/100"
        )

        e3.metric(
            "Risk Level",
            bridge_risk
        )

        e4.metric(
            "Device",
            bridge_device
        )


        # =================================================
        # AUTOMATIC RECIPIENT LOGIC
        # =================================================

        if bridge_risk == "Critical":

            bridge_recipients = [
                "Family",
                "Health Worker",
                "Administrator"
            ]

        elif bridge_risk == "High":

            bridge_recipients = [
                "Family",
                "Health Worker"
            ]

        elif bridge_risk == "Medium":

            bridge_recipients = [
                "Family"
            ]

        else:

            bridge_recipients = [
                "Monitoring Dashboard"
            ]


        st.subheader(
            "📢 Automatic Recipients"
        )

        st.write(
            " → ".join(
                bridge_recipients
            )
        )


        # =================================================
        # AUTOMATIC MESSAGE
        # =================================================

        if bridge_risk == "High":

            bridge_title = (
                "🚨 HIGH WATER RISK ALERT"
            )

            bridge_action = """
• Avoid untreated drinking water.
• Prefer safe/treated drinking water.
• Arrange appropriate water-quality testing.
• Review vulnerable household members.
• Health worker investigation is recommended.
"""

        elif bridge_risk == "Medium":

            bridge_title = (
                "⚠️ WATER QUALITY WARNING"
            )

            bridge_action = """
• Prefer safe/treated drinking water.
• Monitor water quality.
• Consider appropriate water testing.
• Give additional precaution to vulnerable groups.
"""

        elif bridge_risk == "Critical":

            bridge_title = (
                "🚨 CRITICAL WATER RISK ALERT"
            )

            bridge_action = """
• Avoid untreated drinking water.
• Use safe/treated drinking water.
• Arrange appropriate testing urgently.
• Notify the responsible health worker.
• Escalate to the appropriate authority when required.
"""

        else:

            bridge_title = (
                "🟢 WATER MONITORING UPDATE"
            )

            bridge_action = """
• Continue regular monitoring.
• Maintain normal water-safety practices.
"""


        bridge_message = f"""
{bridge_title}

House ID: {bridge_house_id}
Village: {bridge_village}

IoT Device: {bridge_device}

Water Risk Score:
{bridge_score:.0f}/100

Risk Level:
{bridge_risk}

Sensor Snapshot:

pH: {bridge_ph}
TDS: {bridge_tds}
Turbidity: {bridge_turbidity}
Temperature: {bridge_temperature} °C

Recommended Actions:

{bridge_action}

This is an early-warning screening result,
not a medical diagnosis.
"""


        st.subheader(
            "📩 Generated Notification"
        )

        st.code(
            bridge_message,
            language="text"
        )


        # =================================================
        # SEND / RECORD AUTOMATIC ALERT
        # =================================================

        if st.button(
            "🚨 GENERATE STAKEHOLDER ALERT",
            type="primary",
            key="generate_stakeholder_alert"
        ):

            # ---------------------------------------------
            # LOAD NOTIFICATION FILE
            # ---------------------------------------------

            if os.path.exists(
                NOTIFICATION_FILE
            ):

                notification_df = pd.read_csv(
                    NOTIFICATION_FILE
                )

            else:

                notification_df = pd.DataFrame(
                    columns=[
                        "date_time",
                        "house_id",
                        "name",
                        "mobile",
                        "village",
                        "water_source",
                        "water_score",
                        "risk_level",
                        "priority_age_groups",
                        "health_risk",
                        "notification_type",
                        "status",
                        "message"
                    ]
                )


            # ---------------------------------------------
            # FIND HOUSEHOLD CONTACT
            # ---------------------------------------------

            family_name = "Household Resident"
            family_mobile = "Not Registered"


            if os.path.exists(
                CONTACT_FILE
            ):

                contact_df = pd.read_csv(
                    CONTACT_FILE
                )

                if (
                    len(contact_df) > 0
                    and "house_id"
                    in contact_df.columns
                ):

                    matching_contacts = contact_df[
                        contact_df[
                            "house_id"
                        ].astype(str)
                        == bridge_house_id
                    ]

                    if len(matching_contacts) > 0:

                        latest_contact = (
                            matching_contacts.iloc[-1]
                        )

                        family_name = str(
                            latest_contact.get(
                                "name",
                                "Household Resident"
                            )
                        )

                        family_mobile = str(
                            latest_contact.get(
                                "mobile",
                                "Not Registered"
                            )
                        )


            # ---------------------------------------------
            # CREATE NOTIFICATION RECORD
            # ---------------------------------------------

            new_bridge_notification = pd.DataFrame(
                [
                    {
                        "date_time":
                            datetime.now().strftime(
                                "%d-%m-%Y %H:%M:%S"
                            ),

                        "house_id":
                            bridge_house_id,

                        "name":
                            family_name,

                        "mobile":
                            family_mobile,

                        "village":
                            bridge_village,

                        "water_source":
                            "IoT Sensor",

                        "water_score":
                            bridge_score,

                        "risk_level":
                            bridge_risk,

                        "priority_age_groups":
                            "Requires household vulnerability lookup",

                        "health_risk":
                            "Early-warning screening",

                        "notification_type":
                            " → ".join(
                                bridge_recipients
                            ),

                        "status":
                            "GENERATED",

                        "message":
                            bridge_message
                    }
                ]
            )


            notification_df = pd.concat(
                [
                    notification_df,
                    new_bridge_notification
                ],
                ignore_index=True
            )


            notification_df.to_csv(
                NOTIFICATION_FILE,
                index=False
            )


            # ---------------------------------------------
            # SUCCESS
            # ---------------------------------------------

            st.success(
                "✅ Stakeholder alert generated successfully."
            )

            st.info(
                f"""
📢 Alert Flow

{bridge_house_id}
↓
IoT Risk: {bridge_risk}
↓
{bridge_score:.0f}/100
↓
{" → ".join(bridge_recipients)}

Family Contact:
{family_mobile}

Status:
GENERATED / RECORDED

Production version can connect this event
to SMS, WhatsApp, email or a mobile application.
"""
            )


# =========================================================
# COMPLETE AUTOMATION FLOW
# =========================================================

st.subheader(
    "🔄 Complete JEEVAN-ALERT Automation"
)

st.code(
    """
HOUSEHOLD
   ↓
IoT WATER SENSOR
   ↓
ESP32
   ↓
pH / TDS / TURBIDITY / TEMPERATURE
   ↓
WATER RISK ENGINE
   ↓
AI HEALTH-RISK SCREENING
   ↓
HOUSEHOLD VULNERABILITY
   ↓
COMMUNITY CLUSTER ANALYSIS
   ↓
RISK LEVEL
   ↓
┌───────────────┐
│ SMART ALERT   │
└───────────────┘
   ↓
Family / Health Worker / Administrator
   ↓
Preventive Action
""",
    language="text"
)


st.caption(
    "⚠️ Notifications generated by this MVP are "
    "screening and decision-support outputs. "
    "Actual disease or contamination confirmation "
    "requires appropriate testing and qualified authorities."
)
# =========================================================
# 🧠 JEEVAN-ALERT PERSONALIZED HEALTH-RISK ENGINE
# =========================================================

st.divider()

st.header("🧠 Personalized Household Health-Risk Analysis")

st.write(
    "This module combines water risk with household age-group "
    "vulnerability to generate a personalized early-warning "
    "screening result."
)


# =========================================================
# SELECT HOUSEHOLD
# =========================================================

st.subheader("🏠 Household Information")

h1, h2 = st.columns(2)

with h1:

    health_house_id = st.text_input(
        "House ID",
        placeholder="Example: H001",
        key="health_engine_house_id"
    )

with h2:

    health_village = st.text_input(
        "Village",
        placeholder="Example: Village A",
        key="health_engine_village"
    )


# =========================================================
# FAMILY AGE GROUPS
# =========================================================

st.subheader("👨‍👩‍👧 Household Age Composition")

a1, a2, a3, a4 = st.columns(4)

with a1:

    children_0_5 = st.number_input(
        "👶 Age 0–5",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        key="health_age_0_5"
    )

with a2:

    children_6_17 = st.number_input(
        "🧒 Age 6–17",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        key="health_age_6_17"
    )

with a3:

    adults_18_59 = st.number_input(
        "👨 Age 18–59",
        min_value=0,
        max_value=20,
        value=1,
        step=1,
        key="health_age_18_59"
    )

with a4:

    elderly_60_plus = st.number_input(
        "👴 Age 60+",
        min_value=0,
        max_value=20,
        value=0,
        step=1,
        key="health_age_60_plus"
    )


# =========================================================
# VULNERABILITY CALCULATION
# =========================================================

vulnerability_score = 0

priority_groups = []


if children_0_5 > 0:

    vulnerability_score += (
        children_0_5 * 20
    )

    priority_groups.append(
        "Young Children (0–5)"
    )


if children_6_17 > 0:

    vulnerability_score += (
        children_6_17 * 10
    )

    priority_groups.append(
        "Children (6–17)"
    )


if elderly_60_plus > 0:

    vulnerability_score += (
        elderly_60_plus * 20
    )

    priority_groups.append(
        "Older Adults (60+)"
    )


# Limit vulnerability score

vulnerability_score = min(
    vulnerability_score,
    100
)


# =========================================================
# VULNERABILITY LEVEL
# =========================================================

if vulnerability_score >= 60:

    vulnerability_level = "High"

elif vulnerability_score >= 30:

    vulnerability_level = "Medium"

else:

    vulnerability_level = "Low"


# =========================================================
# WATER RISK INPUT
# =========================================================

st.subheader(
    "💧 Current Water Risk"
)

water_input_score = st.slider(
    "Water Risk Score",
    min_value=0,
    max_value=100,
    value=30,
    step=1,
    key="health_engine_water_score"
)


if water_input_score >= 70:

    water_input_level = "High"

elif water_input_score >= 40:

    water_input_level = "Medium"

else:

    water_input_level = "Low"


# =========================================================
# HEALTH-RISK CALCULATION
# =========================================================

health_risk_score = (
    water_input_score * 0.70
    +
    vulnerability_score * 0.30
)


health_risk_score = round(
    min(
        health_risk_score,
        100
    ),
    2
)


# =========================================================
# HEALTH-RISK LEVEL
# =========================================================

if health_risk_score >= 70:

    health_risk_level = "High"

elif health_risk_score >= 40:

    health_risk_level = "Medium"

else:

    health_risk_level = "Low"


# =========================================================
# DISPLAY RESULTS
# =========================================================

st.subheader(
    "📊 Personalized Risk Result"
)

r1, r2, r3, r4 = st.columns(4)

r1.metric(
    "Water Risk",
    f"{water_input_score}/100"
)

r2.metric(
    "Vulnerability",
    f"{vulnerability_score}/100"
)

r3.metric(
    "Health Risk",
    f"{health_risk_score}/100"
)

r4.metric(
    "Risk Level",
    health_risk_level
)


# =========================================================
# PRIORITY GROUPS
# =========================================================

if len(priority_groups) > 0:

    st.warning(
        "👥 Priority Age Groups: "
        +
        ", ".join(priority_groups)
    )

else:

    st.success(
        "👥 No specific vulnerable age group identified."
    )


# =========================================================
# RISK MESSAGE
# =========================================================

if health_risk_level == "High":

    st.error(
        """
🚨 HIGH PERSONALIZED HEALTH-RISK SCREENING

This household requires increased precaution.

Recommended actions:

• Prefer safe/treated drinking water.
• Avoid consuming untreated water.
• Give additional precaution to vulnerable members.
• Arrange appropriate water-quality testing.
• Consider informing the responsible health worker.
"""
    )

elif health_risk_level == "Medium":

    st.warning(
        """
⚠️ MEDIUM PERSONALIZED HEALTH-RISK SCREENING

Increased monitoring is recommended.

Recommended actions:

• Prefer safe drinking water.
• Monitor water quality.
• Give additional precaution to vulnerable groups.
• Consider appropriate water testing.
"""
    )

else:

    st.success(
        """
🟢 LOW PERSONALIZED HEALTH-RISK SCREENING

Continue regular water-safety practices
and periodic monitoring.
"""
    )


# =========================================================
# EXPLANATION
# =========================================================

st.subheader(
    "🧠 Why This Household Received This Risk?"
)

st.write(
    f"""
Household: {health_house_id or "Not specified"}

Village: {health_village or "Not specified"}

Water Risk Score:
{water_input_score}/100

Household Vulnerability:
{vulnerability_score}/100

Personalized Health-Risk Screening:
{health_risk_score}/100

Risk Level:
{health_risk_level}
"""
)


# =========================================================
# DECISION FLOW
# =========================================================

with st.expander(
    "🔄 View AI Decision Flow"
):

    st.code(
        f"""
WATER RISK
{water_input_score}/100
        ↓
HOUSEHOLD VULNERABILITY
{vulnerability_score}/100
        ↓
PRIORITY AGE GROUPS
{", ".join(priority_groups)
if priority_groups
else "None"}
        ↓
PERSONALIZED HEALTH-RISK SCREENING
{health_risk_score}/100
        ↓
RISK LEVEL
{health_risk_level}
        ↓
PREVENTIVE ACTION
        """,
        language="text"
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.caption(
    "⚠️ This is an early-warning screening and "
    "decision-support system. It does not diagnose "
    "disease or confirm contamination. Appropriate "
    "laboratory testing and qualified medical/health "
    "authorities are required for confirmation."
)
# =========================================================
# 🧠 JEEVAN-ALERT UNIFIED EARLY WARNING DASHBOARD
# =========================================================

st.divider()

st.header("🧠 Unified Early Warning Dashboard")

st.write(
    "A single decision-support view combining water quality, "
    "household vulnerability, health-risk screening and "
    "community-level warning indicators."
)


# =========================================================
# INPUT SECTION
# =========================================================

st.subheader("🏠 Household & Environmental Information")

u1, u2, u3 = st.columns(3)

with u1:

    unified_house_id = st.text_input(
        "House ID",
        placeholder="H001",
        key="unified_house_id"
    )

with u2:

    unified_village = st.text_input(
        "Village",
        placeholder="Village A",
        key="unified_village"
    )

with u3:

    unified_source = st.selectbox(
        "Water Source",
        [
            "Tap Water",
            "Borewell",
            "Handpump",
            "Community Tank",
            "River",
            "Other"
        ],
        key="unified_water_source"
    )


# =========================================================
# WATER QUALITY
# =========================================================

st.subheader("💧 Water Quality")

w1, w2, w3, w4 = st.columns(4)

with w1:

    unified_ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1,
        key="unified_ph"
    )

with w2:

    unified_tds = st.number_input(
        "TDS",
        min_value=0.0,
        max_value=5000.0,
        value=300.0,
        step=10.0,
        key="unified_tds"
    )

with w3:

    unified_turbidity = st.number_input(
        "Turbidity",
        min_value=0.0,
        max_value=1000.0,
        value=1.0,
        step=0.1,
        key="unified_turbidity"
    )

with w4:

    unified_temperature = st.number_input(
        "Temperature °C",
        min_value=-10.0,
        max_value=80.0,
        value=25.0,
        step=0.1,
        key="unified_temperature"
    )


# =========================================================
# WATER RISK
# =========================================================

unified_water_score = 0


if unified_ph < 6.5 or unified_ph > 8.5:

    unified_water_score += 30

elif unified_ph < 6.8 or unified_ph > 8.2:

    unified_water_score += 15


if unified_tds > 1000:

    unified_water_score += 30

elif unified_tds > 500:

    unified_water_score += 15


if unified_turbidity > 10:

    unified_water_score += 30

elif unified_turbidity > 5:

    unified_water_score += 15


if unified_temperature > 35:

    unified_water_score += 10

elif unified_temperature > 30:

    unified_water_score += 5


unified_water_score = min(
    unified_water_score,
    100
)


if unified_water_score >= 60:

    unified_water_level = "High"

elif unified_water_score >= 30:

    unified_water_level = "Medium"

else:

    unified_water_level = "Low"


# =========================================================
# FAMILY VULNERABILITY
# =========================================================

st.subheader("👨‍👩‍👧 Family Vulnerability")

v1, v2, v3, v4 = st.columns(4)

with v1:

    unified_age_0_5 = st.number_input(
        "Age 0–5",
        min_value=0,
        max_value=20,
        value=0,
        key="unified_age_0_5"
    )

with v2:

    unified_age_6_17 = st.number_input(
        "Age 6–17",
        min_value=0,
        max_value=20,
        value=0,
        key="unified_age_6_17"
    )

with v3:

    unified_age_18_59 = st.number_input(
        "Age 18–59",
        min_value=0,
        max_value=20,
        value=1,
        key="unified_age_18_59"
    )

with v4:

    unified_age_60 = st.number_input(
        "Age 60+",
        min_value=0,
        max_value=20,
        value=0,
        key="unified_age_60"
    )


unified_vulnerability = 0

unified_priority_groups = []


if unified_age_0_5 > 0:

    unified_vulnerability += (
        unified_age_0_5 * 20
    )

    unified_priority_groups.append(
        "Young Children"
    )


if unified_age_6_17 > 0:

    unified_vulnerability += (
        unified_age_6_17 * 10
    )

    unified_priority_groups.append(
        "Children"
    )


if unified_age_60 > 0:

    unified_vulnerability += (
        unified_age_60 * 20
    )

    unified_priority_groups.append(
        "Older Adults"
    )


unified_vulnerability = min(
    unified_vulnerability,
    100
)


# =========================================================
# ENVIRONMENTAL FACTORS
# =========================================================

st.subheader("🌦️ Environmental Factors")

e1, e2, e3, e4 = st.columns(4)

with e1:

    unified_rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=0.0,
        step=1.0,
        key="unified_rainfall"
    )

with e2:

    unified_humidity = st.number_input(
        "Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0,
        key="unified_humidity"
    )

with e3:

    unified_previous_cases = st.number_input(
        "Previous Cases",
        min_value=0,
        max_value=10000,
        value=0,
        step=1,
        key="unified_previous_cases"
    )

with e4:

    unified_sanitation = st.selectbox(
        "Sanitation Condition",
        [
            "Good",
            "Moderate",
            "Poor"
        ],
        key="unified_sanitation"
    )


# =========================================================
# ENVIRONMENTAL RISK
# =========================================================

environment_score = 0


if unified_rainfall > 100:

    environment_score += 25

elif unified_rainfall > 50:

    environment_score += 10


if unified_humidity > 80:

    environment_score += 15


if unified_previous_cases > 10:

    environment_score += 30

elif unified_previous_cases > 5:

    environment_score += 15


if unified_sanitation == "Poor":

    environment_score += 30

elif unified_sanitation == "Moderate":

    environment_score += 15


environment_score = min(
    environment_score,
    100
)


# =========================================================
# UNIFIED HEALTH RISK
# =========================================================

unified_health_score = (

    unified_water_score * 0.50

    +

    unified_vulnerability * 0.20

    +

    environment_score * 0.30

)


unified_health_score = round(
    min(
        unified_health_score,
        100
    ),
    2
)


# =========================================================
# FINAL RISK LEVEL
# =========================================================

if unified_health_score >= 70:

    unified_final_risk = "Critical"

elif unified_health_score >= 50:

    unified_final_risk = "High"

elif unified_health_score >= 30:

    unified_final_risk = "Medium"

else:

    unified_final_risk = "Low"


# =========================================================
# RESULTS
# =========================================================

st.subheader(
    "🚨 Unified Risk Assessment"
)

r1, r2, r3, r4 = st.columns(4)

r1.metric(
    "💧 Water Risk",
    f"{unified_water_score}/100"
)

r2.metric(
    "👨‍👩‍👧 Vulnerability",
    f"{unified_vulnerability}/100"
)

r3.metric(
    "🌦️ Environmental Risk",
    f"{environment_score}/100"
)

r4.metric(
    "🩺 Final Health Risk",
    f"{unified_health_score}/100"
)


# =========================================================
# FINAL STATUS
# =========================================================

if unified_final_risk == "Critical":

    st.error(
        "🚨 CRITICAL EARLY-WARNING STATUS"
    )

elif unified_final_risk == "High":

    st.error(
        "🔴 HIGH EARLY-WARNING STATUS"
    )

elif unified_final_risk == "Medium":

    st.warning(
        "🟡 MEDIUM EARLY-WARNING STATUS"
    )

else:

    st.success(
        "🟢 LOW EARLY-WARNING STATUS"
    )


# =========================================================
# PRIORITY GROUPS
# =========================================================

if len(unified_priority_groups) > 0:

    st.info(
        "👥 Priority Groups: "
        +
        ", ".join(
            unified_priority_groups
        )
    )


# =========================================================
# AUTOMATIC ACTION
# =========================================================

st.subheader(
    "🎯 Recommended Action"
)


if unified_final_risk == "Critical":

    unified_action = """
🚨 Immediate escalation recommended.

• Avoid untreated drinking water.
• Use safe/treated drinking water.
• Arrange appropriate water-quality testing.
• Prioritize vulnerable household members.
• Inform the responsible health worker.
• Consider escalation to the appropriate authority.
"""

elif unified_final_risk == "High":

    unified_action = """
🔴 High-priority monitoring recommended.

• Prefer safe/treated drinking water.
• Review vulnerable household members.
• Arrange appropriate water-quality testing.
• Notify the responsible health worker.
"""

elif unified_final_risk == "Medium":

    unified_action = """
🟡 Increased monitoring recommended.

• Prefer safe drinking water.
• Continue monitoring water quality.
• Give additional precaution to vulnerable groups.
• Consider appropriate water testing.
"""

else:

    unified_action = """
🟢 Continue regular monitoring.

• Maintain normal water-safety practices.
• Continue periodic water-quality checks.
"""


st.info(
    unified_action
)


# =========================================================
# DECISION EXPLANATION
# =========================================================

with st.expander(
    "🧠 Why did the system generate this risk?"
):

    st.write(
        f"""
Household:
{unified_house_id or "Not specified"}

Village:
{unified_village or "Not specified"}

Water Source:
{unified_source}

Water Risk:
{unified_water_score}/100

Household Vulnerability:
{unified_vulnerability}/100

Environmental Risk:
{environment_score}/100

Final Health-Risk Screening:
{unified_health_score}/100

Final Risk Level:
{unified_final_risk}
"""
    )


# =========================================================
# COMPLETE SYSTEM FLOW
# =========================================================

st.subheader(
    "🔄 JEEVAN-ALERT End-to-End Flow"
)

st.code(
    """
HOUSEHOLD
   ↓
WATER SENSORS
   ↓
pH / TDS / TURBIDITY / TEMPERATURE
   ↓
WATER RISK ANALYSIS
   ↓
FAMILY VULNERABILITY
   ↓
ENVIRONMENTAL CONDITIONS
   ↓
AI HEALTH-RISK SCREENING
   ↓
COMMUNITY PATTERN DETECTION
   ↓
FINAL EARLY-WARNING LEVEL
   ↓
SMART NOTIFICATION
   ↓
FAMILY / HEALTH WORKER / ADMIN
   ↓
PREVENTIVE ACTION
""",
    language="text"
)


st.caption(
    "⚠️ This platform provides early-warning screening "
    "and decision support. It does not diagnose disease "
    "or confirm contamination. Appropriate laboratory "
    "testing and qualified authorities are required "
    "for confirmation."
)
# =========================================================
# 🏘️ JEEVAN-ALERT COMMUNITY EARLY-WARNING DASHBOARD
# =========================================================

st.divider()

st.header("🏘️ Community Early-Warning Dashboard")

st.write(
    "This dashboard aggregates household-level risk information "
    "to identify possible village and community-level warning signals."
)


# =========================================================
# LOAD WATER HISTORY
# =========================================================

try:

    community_data = load_water_history()

except Exception:

    community_data = pd.DataFrame()


# =========================================================
# CHECK DATA
# =========================================================

if len(community_data) == 0:

    st.info(
        "No household water readings are available yet. "
        "Please save some household readings first."
    )

else:

    community_data = community_data.copy()


    # =====================================================
    # STANDARDIZE COLUMNS
    # =====================================================

    if "risk_level" in community_data.columns:

        community_data["risk_level_clean"] = (
            community_data["risk_level"]
            .astype(str)
            .str.strip()
            .str.title()
        )

    else:

        community_data["risk_level_clean"] = "Low"


    if "water_score" in community_data.columns:

        community_data["water_score_numeric"] = pd.to_numeric(
            community_data["water_score"],
            errors="coerce"
        )

    else:

        community_data["water_score_numeric"] = 0


    # =====================================================
    # COMMUNITY SUMMARY
    # =====================================================

    st.subheader(
        "📊 Community Overview"
    )


    total_readings = len(
        community_data
    )


    if "house_id" in community_data.columns:

        total_households = (
            community_data["house_id"]
            .astype(str)
            .nunique()
        )

    else:

        total_households = 0


    if "village" in community_data.columns:

        total_villages = (
            community_data["village"]
            .astype(str)
            .nunique()
        )

    else:

        total_villages = 0


    high_count = len(
        community_data[
            community_data["risk_level_clean"]
            == "High"
        ]
    )


    medium_count = len(
        community_data[
            community_data["risk_level_clean"]
            == "Medium"
        ]
    )


    low_count = len(
        community_data[
            community_data["risk_level_clean"]
            == "Low"
        ]
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    c1.metric(
        "🏠 Households",
        total_households
    )


    c2.metric(
        "🏘️ Villages",
        total_villages
    )


    c3.metric(
        "🔴 High Risk",
        high_count
    )


    c4.metric(
        "🟡 Medium Risk",
        medium_count
    )


    c5.metric(
        "🟢 Low Risk",
        low_count
    )


    # =====================================================
    # VILLAGE RISK SCORE
    # =====================================================

    st.subheader(
        "🏘️ Village-Level Risk Analysis"
    )


    if "village" in community_data.columns:

        village_summary = (
            community_data
            .groupby("village")
            .agg(

                households=(
                    "house_id",
                    "nunique"
                )
                if "house_id"
                in community_data.columns
                else (
                    "risk_level_clean",
                    "count"
                ),

                average_water_score=(
                    "water_score_numeric",
                    "mean"
                ),

                high_risk_count=(
                    "risk_level_clean",
                    lambda x:
                    (
                        x == "High"
                    ).sum()
                ),

                medium_risk_count=(
                    "risk_level_clean",
                    lambda x:
                    (
                        x == "Medium"
                    ).sum()
                ),

                low_risk_count=(
                    "risk_level_clean",
                    lambda x:
                    (
                        x == "Low"
                    ).sum()
                )
            )
            .reset_index()
        )


        village_summary[
            "average_water_score"
        ] = village_summary[
            "average_water_score"
        ].round(2)


        # -----------------------------------------------
        # VILLAGE RISK CLASSIFICATION
        # -----------------------------------------------

        def classify_village(row):

            if row["high_risk_count"] >= 3:

                return "Critical"

            elif row["high_risk_count"] >= 1:

                return "High"

            elif row["medium_risk_count"] >= 2:

                return "Medium"

            else:

                return "Low"


        village_summary[
            "community_risk"
        ] = village_summary.apply(
            classify_village,
            axis=1
        )


        # -----------------------------------------------
        # SORT BY RISK
        # -----------------------------------------------

        risk_order = {
            "Critical": 0,
            "High": 1,
            "Medium": 2,
            "Low": 3
        }


        village_summary[
            "risk_order"
        ] = village_summary[
            "community_risk"
        ].map(
            risk_order
        )


        village_summary = (
            village_summary
            .sort_values(
                "risk_order"
            )
            .drop(
                columns=["risk_order"]
            )
        )


        st.dataframe(
            village_summary,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "Village information is not available."
        )


    # =====================================================
    # RISK DISTRIBUTION
    # =====================================================

    st.subheader(
        "📈 Community Risk Distribution"
    )


    risk_chart = pd.DataFrame({

        "Risk Level": [
            "High",
            "Medium",
            "Low"
        ],

        "Readings": [
            high_count,
            medium_count,
            low_count
        ]
    })


    if risk_chart["Readings"].sum() > 0:

        st.bar_chart(
            risk_chart.set_index(
                "Risk Level"
            )
        )


    # =====================================================
    # WATER SOURCE ANALYSIS
    # =====================================================

    st.subheader(
        "🚰 Common Water-Source Risk"
    )


    if "water_source" in community_data.columns:

        source_summary = (
            community_data
            .groupby("water_source")
            .agg(

                total_readings=(
                    "risk_level_clean",
                    "count"
                ),

                high_risk=(
                    "risk_level_clean",
                    lambda x:
                    (
                        x == "High"
                    ).sum()
                ),

                average_score=(
                    "water_score_numeric",
                    "mean"
                )
            )
            .reset_index()
        )


        source_summary[
            "average_score"
        ] = source_summary[
            "average_score"
        ].round(2)


        source_summary[
            "high_risk_percentage"
        ] = (
            source_summary["high_risk"]
            /
            source_summary["total_readings"]
            .replace(0, np.nan)
            * 100
        ).round(2)


        source_summary = source_summary.sort_values(
            "high_risk_percentage",
            ascending=False
        )


        st.dataframe(
            source_summary,
            use_container_width=True,
            hide_index=True
        )


    else:

        st.info(
            "Water-source data is not available."
        )


    # =====================================================
    # POSSIBLE COMMUNITY CLUSTERS
    # =====================================================

    st.subheader(
        "🚨 Possible Community Risk Clusters"
    )


    if "village" in community_data.columns:

        cluster_table = (
            community_data[
                community_data["risk_level_clean"]
                == "High"
            ]
            .groupby("village")
            .agg(

                high_risk_households=(
                    "house_id",
                    "nunique"
                )
                if "house_id"
                in community_data.columns
                else (
                    "risk_level_clean",
                    "count"
                )
            )
            .reset_index()
        )


        cluster_table = cluster_table[
            cluster_table[
                "high_risk_households"
            ] >= 2
        ]


        if len(cluster_table) > 0:

            st.warning(
                "⚠️ Possible community-level "
                "risk patterns detected."
            )


            st.dataframe(
                cluster_table,
                use_container_width=True,
                hide_index=True
            )

            st.write(
                """
Recommended response:

• Review nearby households.
• Check common water sources.
• Increase monitoring.
• Arrange appropriate water-quality testing.
• Inform the responsible health authority when required.
"""
            )

        else:

            st.success(
                "🟢 No possible high-risk cluster "
                "detected in the available data."
            )


    # =====================================================
    # COMMUNITY EARLY-WARNING STATUS
    # =====================================================

    st.subheader(
        "🧠 Community Early-Warning Status"
    )


    if high_count >= 5:

        community_status = "CRITICAL"

        st.error(
            """
🚨 CRITICAL COMMUNITY EARLY WARNING

Multiple high-risk readings have been detected.

Priority actions:
• Investigate affected households.
• Review common water sources.
• Increase community surveillance.
• Arrange appropriate testing.
• Escalate to relevant health authorities when required.
"""
        )


    elif high_count >= 3:

        community_status = "HIGH"

        st.error(
            """
🔴 HIGH COMMUNITY RISK

Several households are showing high-risk
water-screening results.

Priority actions:
• Investigate affected households.
• Check nearby water sources.
• Increase monitoring.
"""
        )


    elif high_count >= 1:

        community_status = "WATCH"

        st.warning(
            """
🟡 COMMUNITY WATCH

At least one high-risk household has been detected.

Continue monitoring nearby households and
review the relevant water source.
"""
        )


    else:

        community_status = "NORMAL"

        st.success(
            """
🟢 COMMUNITY STATUS NORMAL

No high-risk household pattern has been
detected in the available readings.
"""
        )


    # =====================================================
    # PRIORITY VILLAGE
    # =====================================================

    if (
        "village" in community_data.columns
        and len(community_data) > 0
    ):

        village_high = (
            community_data[
                community_data[
                    "risk_level_clean"
                ] == "High"
            ]
            .groupby("village")
            .size()
            .sort_values(
                ascending=False
            )
        )


        if len(village_high) > 0:

            priority_village = (
                village_high.index[0]
            )

            priority_count = (
                village_high.iloc[0]
            )


            st.info(
                f"""
🎯 Priority Monitoring Area

Village: {priority_village}

High-risk readings:
{priority_count}

This area should receive increased monitoring
and appropriate field verification.
"""
            )


    # =====================================================
    # COMMUNITY DECISION FLOW
    # =====================================================

    with st.expander(
        "🔄 Community Decision Flow"
    ):

        st.code(
            """
HOUSEHOLD WATER READINGS
          ↓
INDIVIDUAL WATER RISK
          ↓
MULTIPLE HOUSEHOLDS
          ↓
VILLAGE RISK ANALYSIS
          ↓
COMMON WATER SOURCE ANALYSIS
          ↓
POSSIBLE COMMUNITY CLUSTER
          ↓
EARLY WARNING
          ↓
HEALTH WORKER / ADMINISTRATOR
          ↓
PREVENTIVE ACTION
""",
            language="text"
        )


    # =====================================================
    # DISCLAIMER
    # =====================================================

    st.caption(
        "⚠️ Community-level indicators are screening "
        "and decision-support outputs. They do not "
        "confirm disease outbreaks or contamination. "
        "Appropriate laboratory testing and qualified "
        "authorities are required for confirmation."
    )
    # =========================================================
# 👨‍👩‍👧 JEEVAN-ALERT AUTOMATIC HOUSEHOLD PROFILE
# =========================================================

st.divider()

st.header("👨‍👩‍👧 Household Profile")

st.write(
    "Family information is stored once and can be "
    "automatically reused for future risk analysis."
)

PROFILE_FILE = "data/household_profiles.csv"

# ---------------------------------------------------------
# CREATE FILE
# ---------------------------------------------------------

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(PROFILE_FILE):

    profile_columns = [
        "house_id",
        "family_name",
        "mobile",
        "village",
        "water_source",
        "age_0_5",
        "age_6_17",
        "age_18_59",
        "age_60_plus",
        "created_at"
    ]

    pd.DataFrame(
        columns=profile_columns
    ).to_csv(
        PROFILE_FILE,
        index=False
    )


# ---------------------------------------------------------
# PROFILE FORM
# ---------------------------------------------------------

st.subheader("📝 Register Household")

p1, p2 = st.columns(2)

with p1:

    profile_house_id = st.text_input(
        "🏠 House ID",
        placeholder="H001",
        key="profile_house_id"
    )

    profile_family_name = st.text_input(
        "👤 Family Name",
        placeholder="Enter family name",
        key="profile_family_name"
    )

    profile_mobile = st.text_input(
        "📱 Mobile Number",
        placeholder="10-digit mobile number",
        key="profile_mobile"
    )


with p2:

    profile_village = st.text_input(
        "🏘️ Village",
        placeholder="Enter village",
        key="profile_village"
    )

    profile_water_source = st.selectbox(
        "🚰 Main Water Source",
        [
            "Tap Water",
            "Borewell",
            "Handpump",
            "Community Tank",
            "River",
            "Other"
        ],
        key="profile_water_source"
    )


# ---------------------------------------------------------
# AGE GROUPS
# ---------------------------------------------------------

st.subheader("👨‍👩‍👧 Family Members")

a1, a2, a3, a4 = st.columns(4)

with a1:

    profile_age_0_5 = st.number_input(
        "👶 Age 0–5",
        min_value=0,
        max_value=20,
        value=0,
        key="profile_age_0_5"
    )

with a2:

    profile_age_6_17 = st.number_input(
        "🧒 Age 6–17",
        min_value=0,
        max_value=20,
        value=0,
        key="profile_age_6_17"
    )

with a3:

    profile_age_18_59 = st.number_input(
        "👨 Age 18–59",
        min_value=0,
        max_value=20,
        value=1,
        key="profile_age_18_59"
    )

with a4:

    profile_age_60_plus = st.number_input(
        "👴 Age 60+",
        min_value=0,
        max_value=20,
        value=0,
        key="profile_age_60_plus"
    )


# ---------------------------------------------------------
# SAVE PROFILE
# ---------------------------------------------------------

if st.button(
    "💾 SAVE HOUSEHOLD PROFILE",
    type="primary",
    key="save_household_profile"
):

    clean_mobile = (
        profile_mobile
        .replace(" ", "")
        .replace("-", "")
        .replace("+91", "")
    )

    if profile_house_id.strip() == "":

        st.error(
            "❌ Please enter House ID."
        )

    elif profile_family_name.strip() == "":

        st.error(
            "❌ Please enter family name."
        )

    elif not clean_mobile.isdigit():

        st.error(
            "❌ Please enter a valid mobile number."
        )

    elif len(clean_mobile) != 10:

        st.error(
            "❌ Mobile number must contain 10 digits."
        )

    elif profile_village.strip() == "":

        st.error(
            "❌ Please enter village."
        )

    else:

        profiles = pd.read_csv(
            PROFILE_FILE
        )

        # -------------------------------------------------
        # CHECK EXISTING HOUSE
        # -------------------------------------------------

        existing_profile = profiles[
            profiles["house_id"]
            .astype(str)
            ==
            profile_house_id.strip()
        ]

        new_profile = pd.DataFrame(
            [
                {
                    "house_id":
                        profile_house_id.strip(),

                    "family_name":
                        profile_family_name.strip(),

                    "mobile":
                        clean_mobile,

                    "village":
                        profile_village.strip(),

                    "water_source":
                        profile_water_source,

                    "age_0_5":
                        profile_age_0_5,

                    "age_6_17":
                        profile_age_6_17,

                    "age_18_59":
                        profile_age_18_59,

                    "age_60_plus":
                        profile_age_60_plus,

                    "created_at":
                        datetime.now().strftime(
                            "%d-%m-%Y %H:%M:%S"
                        )
                }
            ]
        )

        if len(existing_profile) > 0:

            # Update existing household
            profiles = profiles[
                profiles["house_id"]
                .astype(str)
                !=
                profile_house_id.strip()
            ]

            profiles = pd.concat(
                [
                    profiles,
                    new_profile
                ],
                ignore_index=True
            )

            st.success(
                "✅ Household profile updated successfully."
            )

        else:

            profiles = pd.concat(
                [
                    profiles,
                    new_profile
                ],
                ignore_index=True
            )

            st.success(
                "✅ Household profile created successfully."
            )

        profiles.to_csv(
            PROFILE_FILE,
            index=False
        )


# ---------------------------------------------------------
# PROFILE LIST
# ---------------------------------------------------------

st.subheader(
    "📋 Registered Households"
)

try:

    profile_data = pd.read_csv(
        PROFILE_FILE
    )

except Exception:

    profile_data = pd.DataFrame()


if len(profile_data) > 0:

    st.dataframe(
        profile_data,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No household profiles registered yet."
    )


# ---------------------------------------------------------
# AUTOMATIC PROFILE LOOKUP
# ---------------------------------------------------------

st.subheader(
    "🔎 Automatic Household Lookup"
)

if len(profile_data) > 0:

    lookup_house = st.selectbox(
        "Select House ID",
        profile_data[
            "house_id"
        ].astype(str).tolist(),
        key="automatic_house_lookup"
    )

    selected_profile = profile_data[
        profile_data["house_id"]
        .astype(str)
        ==
        lookup_house
    ]

    if len(selected_profile) > 0:

        family = selected_profile.iloc[-1]

        total_members = (
            int(family["age_0_5"])
            +
            int(family["age_6_17"])
            +
            int(family["age_18_59"])
            +
            int(family["age_60_plus"])
        )

        vulnerable_members = (
            int(family["age_0_5"])
            +
            int(family["age_60_plus"])
        )

        q1, q2, q3, q4 = st.columns(4)

        q1.metric(
            "👨‍👩‍👧 Family",
            str(family["family_name"])
        )

        q2.metric(
            "👥 Total Members",
            total_members
        )

        q3.metric(
            "🛡️ Vulnerable Members",
            vulnerable_members
        )

        q4.metric(
            "🚰 Water Source",
            str(family["water_source"])
        )

        st.info(
            f"""
🏠 House ID: {family["house_id"]}

🏘️ Village: {family["village"]}

📱 Mobile: {family["mobile"]}

👶 Age 0–5: {int(family["age_0_5"])}

🧒 Age 6–17: {int(family["age_6_17"])}

👨 Age 18–59: {int(family["age_18_59"])}

👴 Age 60+: {int(family["age_60_plus"])}
"""
        )


# ---------------------------------------------------------
# AUTOMATION FLOW
# ---------------------------------------------------------

with st.expander(
    "🤖 How Household Data Will Be Used Automatically"
):

    st.code(
        """
HOUSEHOLD PROFILE
       ↓
Saved Once
       ↓
Water Sensor Reading
       ↓
AI Risk Analysis
       ↓
Automatically Load Family Profile
       ↓
Age-Wise Vulnerability
       ↓
Personalized Risk
       ↓
Automatic Alert
       ↓
Family / Health Worker / Admin
""",
        language="text"
    )


st.caption(
    "Household profile information is stored for "
    "MVP demonstration. Production deployment should "
    "use secure authentication, encryption and "
    "appropriate privacy controls."
)
# =========================================================
# 🤖 JEEVAN-ALERT ONE-CLICK AUTOMATIC HOUSEHOLD ANALYSIS
# =========================================================

st.divider()

st.header("🤖 Automatic Household Risk Pipeline")

st.write(
    "Select a registered household and automatically combine "
    "its family vulnerability with the latest IoT water reading."
)


PROFILE_FILE = "data/household_profiles.csv"
IOT_FILE = "data/iot_devices.csv"


# =========================================================
# CHECK REQUIRED FILES
# =========================================================

if not os.path.exists(PROFILE_FILE):

    st.warning(
        "⚠️ No household profiles found. "
        "Please register a household first."
    )

elif not os.path.exists(IOT_FILE):

    st.warning(
        "⚠️ No IoT devices found. "
        "Please register an IoT device first."
    )

else:

    profiles = pd.read_csv(
        PROFILE_FILE
    )

    devices = pd.read_csv(
        IOT_FILE
    )


    if len(profiles) == 0:

        st.info(
            "No household profiles available."
        )

    elif len(devices) == 0:

        st.info(
            "No IoT devices available."
        )

    else:

        # =================================================
        # SELECT HOUSEHOLD
        # =================================================

        st.subheader(
            "🏠 Select Household"
        )

        household_list = (
            profiles["house_id"]
            .astype(str)
            .unique()
            .tolist()
        )

        selected_house = st.selectbox(
            "House ID",
            household_list,
            key="pipeline_house_id"
        )


        # =================================================
        # LOAD FAMILY PROFILE
        # =================================================

        family_rows = profiles[
            profiles["house_id"]
            .astype(str)
            ==
            selected_house
        ]


        if len(family_rows) == 0:

            st.error(
                "❌ Household profile not found."
            )

        else:

            family = family_rows.iloc[-1]


            # =============================================
            # DISPLAY PROFILE
            # =============================================

            st.subheader(
                "👨‍👩‍👧 Automatically Loaded Family Profile"
            )

            p1, p2, p3, p4 = st.columns(4)

            p1.metric(
                "Family",
                str(family["family_name"])
            )

            p2.metric(
                "Village",
                str(family["village"])
            )

            p3.metric(
                "Mobile",
                str(family["mobile"])
            )

            p4.metric(
                "Water Source",
                str(family["water_source"])
            )


            # =============================================
            # FAMILY VULNERABILITY
            # =============================================

            age_0_5 = int(
                family["age_0_5"]
            )

            age_6_17 = int(
                family["age_6_17"]
            )

            age_18_59 = int(
                family["age_18_59"]
            )

            age_60_plus = int(
                family["age_60_plus"]
            )


            vulnerability_score = 0

            priority_groups = []


            if age_0_5 > 0:

                vulnerability_score += (
                    age_0_5 * 20
                )

                priority_groups.append(
                    "Young Children (0–5)"
                )


            if age_6_17 > 0:

                vulnerability_score += (
                    age_6_17 * 10
                )

                priority_groups.append(
                    "Children (6–17)"
                )


            if age_60_plus > 0:

                vulnerability_score += (
                    age_60_plus * 20
                )

                priority_groups.append(
                    "Older Adults (60+)"
                )


            vulnerability_score = min(
                vulnerability_score,
                100
            )


            # =============================================
            # FIND HOUSEHOLD SENSOR
            # =============================================

            household_devices = devices[
                devices["house_id"]
                .astype(str)
                ==
                selected_house
            ]


            if len(household_devices) == 0:

                st.warning(
                    "⚠️ No IoT sensor is linked to this household."
                )

            else:

                # Use latest registered device
                sensor = household_devices.iloc[-1]


                device_id = str(
                    sensor["device_id"]
                )


                # =========================================
                # SENSOR VALUES
                # =========================================

                sensor_ph = pd.to_numeric(
                    sensor["pH"],
                    errors="coerce"
                )

                sensor_tds = pd.to_numeric(
                    sensor["TDS"],
                    errors="coerce"
                )

                sensor_turbidity = pd.to_numeric(
                    sensor["turbidity"],
                    errors="coerce"
                )

                sensor_temperature = pd.to_numeric(
                    sensor["temperature"],
                    errors="coerce"
                )


                # =========================================
                # SENSOR STATUS
                # =========================================

                st.subheader(
                    "📡 Latest IoT Reading"
                )

                s1, s2, s3, s4 = st.columns(4)

                s1.metric(
                    "pH",
                    "N/A"
                    if pd.isna(sensor_ph)
                    else f"{sensor_ph:.2f}"
                )

                s2.metric(
                    "TDS",
                    "N/A"
                    if pd.isna(sensor_tds)
                    else f"{sensor_tds:.0f}"
                )

                s3.metric(
                    "Turbidity",
                    "N/A"
                    if pd.isna(sensor_turbidity)
                    else f"{sensor_turbidity:.2f}"
                )

                s4.metric(
                    "Temperature",
                    "N/A"
                    if pd.isna(sensor_temperature)
                    else f"{sensor_temperature:.1f} °C"
                )


                # =========================================
                # AUTOMATIC ANALYSIS BUTTON
                # =========================================

                st.subheader(
                    "🧠 Automatic Analysis"
                )


                if st.button(
                    "🚀 RUN COMPLETE RISK ANALYSIS",
                    type="primary",
                    key="run_complete_pipeline"
                ):

                    # =====================================
                    # VALIDATE SENSOR DATA
                    # =====================================

                    valid = all(
                        [
                            not pd.isna(sensor_ph),
                            not pd.isna(sensor_tds),
                            not pd.isna(sensor_turbidity),
                            not pd.isna(sensor_temperature)
                        ]
                    )


                    if not valid:

                        st.error(
                            "❌ Complete IoT sensor readings "
                            "are required."
                        )

                    else:

                        # =================================
                        # WATER RISK
                        # =================================

                        water_score = 0


                        if (
                            sensor_ph < 6.5
                            or sensor_ph > 8.5
                        ):

                            water_score += 30

                        elif (
                            sensor_ph < 6.8
                            or sensor_ph > 8.2
                        ):

                            water_score += 15


                        if sensor_tds > 1000:

                            water_score += 30

                        elif sensor_tds > 500:

                            water_score += 15


                        if sensor_turbidity > 10:

                            water_score += 30

                        elif sensor_turbidity > 5:

                            water_score += 15


                        if sensor_temperature > 35:

                            water_score += 10

                        elif sensor_temperature > 30:

                            water_score += 5


                        water_score = min(
                            water_score,
                            100
                        )


                        # =================================
                        # WATER LEVEL
                        # =================================

                        if water_score >= 60:

                            water_level = "High"

                        elif water_score >= 30:

                            water_level = "Medium"

                        else:

                            water_level = "Low"


                        # =================================
                        # PERSONALIZED HEALTH SCORE
                        # =================================

                        health_score = (

                            water_score * 0.70

                            +

                            vulnerability_score * 0.30
                        )


                        health_score = round(
                            min(
                                health_score,
                                100
                            ),
                            2
                        )


                        # =================================
                        # FINAL RISK
                        # =================================

                        if health_score >= 70:

                            final_risk = "Critical"

                        elif health_score >= 50:

                            final_risk = "High"

                        elif health_score >= 30:

                            final_risk = "Medium"

                        else:

                            final_risk = "Low"


                        # =================================
                        # DISPLAY RESULT
                        # =================================

                        st.subheader(
                            "🚨 Automatic Risk Result"
                        )


                        r1, r2, r3 = st.columns(3)


                        r1.metric(
                            "💧 Water Risk",
                            f"{water_score}/100"
                        )


                        r2.metric(
                            "👨‍👩‍👧 Vulnerability",
                            f"{vulnerability_score}/100"
                        )


                        r3.metric(
                            "🩺 Final Risk",
                            f"{health_score}/100"
                        )


                        if final_risk == "Critical":

                            st.error(
                                "🚨 CRITICAL RISK"
                            )

                        elif final_risk == "High":

                            st.error(
                                "🔴 HIGH RISK"
                            )

                        elif final_risk == "Medium":

                            st.warning(
                                "🟡 MEDIUM RISK"
                            )

                        else:

                            st.success(
                                "🟢 LOW RISK"
                            )


                        # =================================
                        # PRIORITY GROUPS
                        # =================================

                        if len(priority_groups) > 0:

                            st.info(
                                "👥 Priority Groups: "
                                +
                                ", ".join(
                                    priority_groups
                                )
                            )


                        # =================================
                        # AUTOMATIC ACTION
                        # =================================

                        if final_risk in [
                            "Critical",
                            "High"
                        ]:

                            action = """
🚨 HIGH PRIORITY ACTION

• Prefer safe/treated drinking water.
• Avoid untreated drinking water.
• Give additional precaution to vulnerable members.
• Arrange appropriate water-quality testing.
• Consider notifying the responsible health worker.
"""

                        elif final_risk == "Medium":

                            action = """
⚠️ MONITORING ACTION

• Prefer safe drinking water.
• Monitor water quality.
• Give additional precaution to vulnerable groups.
• Consider appropriate water testing.
"""

                        else:

                            action = """
🟢 NORMAL MONITORING

• Continue normal water-safety practices.
• Continue periodic water-quality monitoring.
"""


                        st.info(
                            action
                        )


                        # =================================
                        # AUTOMATIC DECISION SUMMARY
                        # =================================

                        st.subheader(
                            "🧠 System Decision"
                        )

                        st.code(
                            f"""
HOUSEHOLD
{selected_house}

        ↓

IoT DEVICE
{device_id}

        ↓

WATER RISK
{water_score}/100

        ↓

FAMILY VULNERABILITY
{vulnerability_score}/100

        ↓

PERSONALIZED HEALTH RISK
{health_score}/100

        ↓

FINAL RISK
{final_risk}

        ↓

PRIORITY GROUPS
{", ".join(priority_groups)
if priority_groups
else "None"}

        ↓

RECOMMENDED ACTION
Preventive monitoring / appropriate testing
""",
                            language="text"
                        )


                        st.success(
                            "✅ Complete household risk "
                            "analysis finished successfully."
                        )


# =========================================================
# AUTOMATION VISION
# =========================================================

with st.expander(
    "🤖 Future Fully Automatic Mode"
):

    st.code(
        """
REAL WATER SENSOR
       ↓
ESP32
       ↓
AUTOMATIC DATA TRANSMISSION
       ↓
HOUSE ID IDENTIFICATION
       ↓
HOUSEHOLD PROFILE LOADED
AUTOMATICALLY
       ↓
WATER RISK
       +
FAMILY VULNERABILITY
       ↓
HEALTH-RISK SCREENING
       ↓
COMMUNITY ANALYSIS
       ↓
AUTOMATIC ALERT
       ↓
FAMILY / HEALTH WORKER / ADMIN
""",
        language="text"
    )


st.caption(
    "⚠️ This MVP provides screening and decision support. "
    "It does not diagnose disease or confirm contamination. "
    "Appropriate testing and qualified authorities are "
    "required for confirmation."
)
# =========================================================
# 🦠 JEEVAN-ALERT WATER-BORNE DISEASE RISK SCREENING
# =========================================================

st.divider()

st.header("🦠 Water-Borne Disease Risk Screening")

st.write(
    "The system screens for potential water-borne disease "
    "risk categories using water, environmental and "
    "household-level indicators."
)


# =========================================================
# INPUTS
# =========================================================

st.subheader("📊 Risk Factors")

d1, d2 = st.columns(2)

with d1:

    disease_water_score = st.slider(
        "💧 Water Risk Score",
        0,
        100,
        30,
        key="disease_water_score"
    )

    disease_previous_cases = st.number_input(
        "🩺 Previous Water-Borne Cases",
        min_value=0,
        max_value=1000,
        value=0,
        step=1,
        key="disease_previous_cases"
    )

    disease_rainfall = st.number_input(
        "🌧️ Recent Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=0.0,
        step=1.0,
        key="disease_rainfall"
    )


with d2:

    disease_sanitation = st.selectbox(
        "🚰 Sanitation Condition",
        [
            "Good",
            "Moderate",
            "Poor"
        ],
        key="disease_sanitation"
    )

    disease_vulnerability = st.slider(
        "👨‍👩‍👧 Household Vulnerability",
        0,
        100,
        20,
        key="disease_vulnerability"
    )

    disease_cluster = st.selectbox(
        "🏘️ Community Risk Pattern",
        [
            "No Known Cluster",
            "Possible Cluster",
            "High-Risk Cluster"
        ],
        key="disease_cluster"
    )


# =========================================================
# CALCULATE ENVIRONMENTAL SCORE
# =========================================================

disease_environment_score = 0


if disease_rainfall >= 100:

    disease_environment_score += 30

elif disease_rainfall >= 50:

    disease_environment_score += 15


if disease_previous_cases >= 10:

    disease_environment_score += 30

elif disease_previous_cases >= 5:

    disease_environment_score += 15


if disease_sanitation == "Poor":

    disease_environment_score += 30

elif disease_sanitation == "Moderate":

    disease_environment_score += 15


if disease_cluster == "High-Risk Cluster":

    disease_environment_score += 30

elif disease_cluster == "Possible Cluster":

    disease_environment_score += 15


disease_environment_score = min(
    disease_environment_score,
    100
)


# =========================================================
# COMBINED SCREENING SCORE
# =========================================================

disease_screening_score = (

    disease_water_score * 0.45

    +

    disease_environment_score * 0.30

    +

    disease_vulnerability * 0.25
)


disease_screening_score = round(
    min(
        disease_screening_score,
        100
    ),
    2
)


# =========================================================
# RISK LEVEL
# =========================================================

if disease_screening_score >= 70:

    disease_risk_level = "High"

elif disease_screening_score >= 40:

    disease_risk_level = "Medium"

else:

    disease_risk_level = "Low"


# =========================================================
# SCREENING CATEGORY
# =========================================================

if disease_risk_level == "High":

    disease_category = (
        "High potential risk of water-borne illness"
    )

elif disease_risk_level == "Medium":

    disease_category = (
        "Moderate potential risk of water-borne illness"
    )

else:

    disease_category = (
        "Low potential risk of water-borne illness"
    )


# =========================================================
# RESULT
# =========================================================

st.subheader(
    "🧠 AI Screening Result"
)


x1, x2, x3 = st.columns(3)

x1.metric(
    "Water Risk",
    f"{disease_water_score}/100"
)

x2.metric(
    "Environmental Risk",
    f"{disease_environment_score}/100"
)

x3.metric(
    "Screening Score",
    f"{disease_screening_score}/100"
)


if disease_risk_level == "High":

    st.error(
        f"🚨 {disease_category}"
    )

elif disease_risk_level == "Medium":

    st.warning(
        f"⚠️ {disease_category}"
    )

else:

    st.success(
        f"🟢 {disease_category}"
    )


# =========================================================
# POSSIBLE RISK CATEGORIES
# =========================================================

st.subheader(
    "🔎 Potential Health-Risk Categories"
)

st.write(
    "The system uses risk categories rather than "
    "claiming a confirmed diagnosis."
)


risk_categories = []


if disease_water_score >= 40:

    risk_categories.append(
        "Gastrointestinal / diarrhoeal illness risk"
    )


if disease_rainfall >= 50:

    risk_categories.append(
        "Post-rainfall water-contamination concern"
    )


if disease_sanitation in [
    "Moderate",
    "Poor"
]:

    risk_categories.append(
        "Sanitation-related water-borne illness concern"
    )


if disease_cluster in [
    "Possible Cluster",
    "High-Risk Cluster"
]:

    risk_categories.append(
        "Community-level water-borne illness concern"
    )


if len(risk_categories) > 0:

    for category in risk_categories:

        st.write(
            "• " + category
        )

else:

    st.write(
        "• No specific risk category triggered."
    )


# =========================================================
# AGE-WISE PRIORITY
# =========================================================

st.subheader(
    "👨‍👩‍👧 Vulnerability Priority"
)

if disease_vulnerability >= 60:

    st.warning(
        """
High household vulnerability detected.

Additional precaution should be considered
for vulnerable household members.
"""
    )

elif disease_vulnerability >= 30:

    st.info(
        """
Moderate household vulnerability detected.

Continue increased monitoring.
"""
    )

else:

    st.success(
        """
Low household vulnerability score.
Continue routine monitoring.
"""
    )


# =========================================================
# RECOMMENDATION
# =========================================================

st.subheader(
    "🎯 Recommended Preventive Action"
)


if disease_risk_level == "High":

    disease_action = """
🚨 HIGH PRIORITY

• Use safe/treated drinking water.
• Avoid untreated water.
• Review vulnerable household members.
• Arrange appropriate water-quality testing.
• Increase monitoring of nearby households.
• Inform the responsible health worker when appropriate.
"""

elif disease_risk_level == "Medium":

    disease_action = """
⚠️ MODERATE PRIORITY

• Prefer safe drinking water.
• Monitor water quality.
• Review household vulnerability.
• Consider appropriate water testing.
• Continue community monitoring.
"""

else:

    disease_action = """
🟢 ROUTINE MONITORING

• Continue normal water-safety practices.
• Continue periodic monitoring.
• Observe changes in water quality.
"""


st.info(
    disease_action
)


# =========================================================
# DECISION EXPLANATION
# =========================================================

with st.expander(
    "🧠 Why was this risk generated?"
):

    st.write(
        f"""
Water Risk:
{disease_water_score}/100

Environmental Risk:
{disease_environment_score}/100

Household Vulnerability:
{disease_vulnerability}/100

Previous Cases:
{disease_previous_cases}

Rainfall:
{disease_rainfall} mm

Sanitation:
{disease_sanitation}

Community Pattern:
{disease_cluster}

Final Screening Score:
{disease_screening_score}/100

Final Risk:
{disease_risk_level}
"""
    )


# =========================================================
# FUTURE AI MODEL
# =========================================================

with st.expander(
    "🤖 Future Machine-Learning Model"
):

    st.code(
        """
Historical Water Data
        +
Weather Data
        +
Sanitation Data
        +
Health Surveillance Data
        +
Household Vulnerability
        +
Community Patterns
        ↓
Machine Learning Model
        ↓
Risk Probability
        ↓
Early Warning Category
        ↓
Preventive Action
""",
        language="text"
    )


# =========================================================
# DISCLAIMER
# =========================================================

st.caption(
    "⚠️ This module provides an early-warning screening "
    "category only. It does not diagnose or confirm any "
    "disease. Disease confirmation requires appropriate "
    "clinical/laboratory evaluation and qualified health "
    "professionals."
)
# =========================================================
# 📈 JEEVAN-ALERT RISK TREND INTELLIGENCE
# =========================================================

st.divider()

st.header("📈 Risk Trend & Early-Warning Intelligence")

st.write(
    "Automatically analyzes historical water-risk readings "
    "to identify whether household risk is increasing, "
    "stable, or decreasing."
)


# =========================================================
# LOAD HISTORY
# =========================================================

try:

    trend_history = load_water_history()

except Exception:

    trend_history = pd.DataFrame()


# =========================================================
# CHECK DATA
# =========================================================

if len(trend_history) == 0:

    st.info(
        "No historical water readings are available yet."
    )

else:

    trend_history = trend_history.copy()


    # =====================================================
    # DATE CONVERSION
    # =====================================================

    if "date_time" in trend_history.columns:

        trend_history["trend_date"] = pd.to_datetime(
            trend_history["date_time"],
            errors="coerce",
            dayfirst=True
        )

    else:

        trend_history["trend_date"] = pd.NaT


    # =====================================================
    # WATER SCORE
    # =====================================================

    if "water_score" in trend_history.columns:

        trend_history["trend_score"] = pd.to_numeric(
            trend_history["water_score"],
            errors="coerce"
        )

    else:

        trend_history["trend_score"] = np.nan


    trend_history = trend_history.dropna(
        subset=[
            "trend_date",
            "trend_score"
        ]
    )


    if len(trend_history) < 2:

        st.info(
            "At least two historical readings are required "
            "to calculate a risk trend."
        )

    else:

        # =================================================
        # HOUSEHOLD SELECTION
        # =================================================

        st.subheader(
            "🏠 Household Trend"
        )


        if "house_id" in trend_history.columns:

            available_houses = (
                trend_history["house_id"]
                .astype(str)
                .unique()
                .tolist()
            )

            selected_trend_house = st.selectbox(
                "Select House ID",
                available_houses,
                key="trend_house_selector"
            )

            household_trend = trend_history[
                trend_history["house_id"]
                .astype(str)
                ==
                selected_trend_house
            ].copy()

        else:

            selected_trend_house = "All"

            household_trend = trend_history.copy()


        # =================================================
        # SORT DATA
        # =================================================

        household_trend = household_trend.sort_values(
            "trend_date"
        )


        # =================================================
        # TREND GRAPH
        # =================================================

        st.subheader(
            "📊 Historical Water-Risk Trend"
        )


        graph_data = household_trend[
            [
                "trend_date",
                "trend_score"
            ]
        ].copy()


        graph_data.columns = [
            "Date",
            "Water Risk Score"
        ]


        graph_data = graph_data.set_index(
            "Date"
        )


        st.line_chart(
            graph_data
        )


        # =================================================
        # TREND CALCULATION
        # =================================================

        if len(household_trend) >= 2:

            latest_score = float(
                household_trend[
                    "trend_score"
                ].iloc[-1]
            )

            previous_score = float(
                household_trend[
                    "trend_score"
                ].iloc[-2]
            )

            score_change = round(
                latest_score
                -
                previous_score,
                2
            )


            # ---------------------------------------------
            # TREND STATUS
            # ---------------------------------------------

            if score_change >= 10:

                trend_status = "Increasing"

            elif score_change <= -10:

                trend_status = "Decreasing"

            else:

                trend_status = "Stable"


        else:

            latest_score = 0

            previous_score = 0

            score_change = 0

            trend_status = "Insufficient Data"


        # =================================================
        # DISPLAY TREND
        # =================================================

        t1, t2, t3, t4 = st.columns(4)


        t1.metric(
            "Latest Risk",
            f"{latest_score:.0f}/100"
        )


        t2.metric(
            "Previous Risk",
            f"{previous_score:.0f}/100"
        )


        t3.metric(
            "Change",
            f"{score_change:+.0f}"
        )


        t4.metric(
            "Trend",
            trend_status
        )


        # =================================================
        # TREND WARNING
        # =================================================

        if trend_status == "Increasing":

            st.error(
                """
🚨 EARLY WARNING: RISK IS INCREASING

The latest water-risk score is higher than
the previous reading.

Recommended:
• Increase monitoring frequency.
• Review the water source.
• Check nearby households.
• Consider appropriate water-quality testing.
"""
            )


        elif trend_status == "Decreasing":

            st.success(
                """
🟢 RISK TREND IS IMPROVING

The latest water-risk score is lower
than the previous reading.

Continue regular monitoring.
"""
            )


        elif trend_status == "Stable":

            st.info(
                """
🔵 RISK TREND IS STABLE

No major change has been detected
between the latest readings.
"""
            )


        # =================================================
        # COMMUNITY TREND
        # =================================================

        st.subheader(
            "🏘️ Community Risk Trend"
        )


        community_trend = (
            trend_history
            .groupby(
                trend_history[
                    "trend_date"
                ].dt.date
            )[
                "trend_score"
            ]
            .mean()
            .reset_index()
        )


        community_trend.columns = [
            "Date",
            "Average Community Risk"
        ]


        community_trend = (
            community_trend
            .set_index("Date")
        )


        if len(community_trend) >= 2:

            st.line_chart(
                community_trend
            )


            latest_community = float(
                community_trend[
                    "Average Community Risk"
                ].iloc[-1]
            )

            previous_community = float(
                community_trend[
                    "Average Community Risk"
                ].iloc[-2]
            )


            community_change = round(
                latest_community
                -
                previous_community,
                2
            )


            if community_change >= 10:

                st.error(
                    f"""
🚨 COMMUNITY RISK IS INCREASING

Average risk increased by
{community_change:.1f} points.

Health workers should review
the affected areas and water sources.
"""
                )

            elif community_change <= -10:

                st.success(
                    f"""
🟢 COMMUNITY RISK IS DECREASING

Average risk decreased by
{abs(community_change):.1f} points.

Continue routine monitoring.
"""
                )

            else:

                st.info(
                    """
🔵 COMMUNITY RISK IS RELATIVELY STABLE
"""
                )


        else:

            st.info(
                "More community readings are required "
                "to calculate a trend."
            )


        # =================================================
        # AUTOMATIC PRIORITY
        # =================================================

        st.subheader(
            "🎯 Automatic Monitoring Priority"
        )


        if (
            latest_score >= 70
            and trend_status == "Increasing"
        ):

            priority_level = "CRITICAL"

            priority_action = """
🚨 Highest Priority

• Review household immediately.
• Review the associated water source.
• Check nearby households.
• Arrange appropriate water-quality testing.
• Notify the responsible health worker.
"""


        elif (
            latest_score >= 50
            or trend_status == "Increasing"
        ):

            priority_level = "HIGH"

            priority_action = """
🔴 High Priority

• Increase monitoring.
• Review water-source conditions.
• Check vulnerable household members.
• Consider appropriate testing.
"""


        elif latest_score >= 30:

            priority_level = "MEDIUM"

            priority_action = """
🟡 Medium Priority

• Continue increased monitoring.
• Prefer safe drinking water.
• Review changes in water quality.
"""


        else:

            priority_level = "LOW"

            priority_action = """
🟢 Low Priority

• Continue routine monitoring.
"""


        st.metric(
            "Monitoring Priority",
            priority_level
        )


        st.info(
            priority_action
        )


        # =================================================
        # DECISION FLOW
        # =================================================

        with st.expander(
            "🤖 Automatic Trend Decision Flow"
        ):

            st.code(
                f"""
Historical Readings
        ↓
Water Risk Scores
        ↓
Latest Score
{latest_score:.0f}/100
        ↓
Previous Score
{previous_score:.0f}/100
        ↓
Change
{score_change:+.0f}
        ↓
Trend
{trend_status}
        ↓
Monitoring Priority
{priority_level}
        ↓
Preventive Action
""",
                language="text"
            )


# =========================================================
# DISCLAIMER
# =========================================================

st.caption(
    "⚠️ Trend analysis is an early-warning and "
    "decision-support feature. It does not confirm "
    "contamination or disease."
)
# =========================================================
# 🌦️ JEEVAN-ALERT ENVIRONMENTAL RISK ENGINE
# =========================================================

st.divider()

st.header("🌦️ Environmental Risk Intelligence")

st.write(
    "Environmental conditions are combined with water and "
    "household risk to strengthen early-warning decisions."
)


# =========================================================
# ENVIRONMENT DATA
# =========================================================

st.subheader("🌦️ Environmental Conditions")

e1, e2, e3, e4 = st.columns(4)

with e1:

    env_rainfall = st.number_input(
        "🌧️ Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        value=0.0,
        step=1.0,
        key="env_rainfall"
    )

with e2:

    env_humidity = st.number_input(
        "💧 Humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0,
        key="env_humidity"
    )

with e3:

    env_temperature = st.number_input(
        "🌡️ Temperature (°C)",
        min_value=-10.0,
        max_value=60.0,
        value=25.0,
        step=0.5,
        key="env_temperature"
    )

with e4:

    env_sanitation = st.selectbox(
        "🚰 Sanitation",
        [
            "Good",
            "Moderate",
            "Poor"
        ],
        key="env_sanitation"
    )


# =========================================================
# ENVIRONMENTAL SCORE
# =========================================================

environmental_score = 0


# Rainfall

if env_rainfall >= 150:

    environmental_score += 35

elif env_rainfall >= 75:

    environmental_score += 20

elif env_rainfall >= 30:

    environmental_score += 10


# Humidity

if env_humidity >= 85:

    environmental_score += 20

elif env_humidity >= 70:

    environmental_score += 10


# Temperature

if env_temperature >= 35:

    environmental_score += 20

elif env_temperature >= 30:

    environmental_score += 10


# Sanitation

if env_sanitation == "Poor":

    environmental_score += 25

elif env_sanitation == "Moderate":

    environmental_score += 10


environmental_score = min(
    environmental_score,
    100
)


# =========================================================
# ENVIRONMENT LEVEL
# =========================================================

if environmental_score >= 60:

    environmental_level = "High"

elif environmental_score >= 30:

    environmental_level = "Medium"

else:

    environmental_level = "Low"


# =========================================================
# DISPLAY ENVIRONMENT RISK
# =========================================================

st.subheader(
    "📊 Environmental Risk Result"
)

r1, r2 = st.columns(2)

r1.metric(
    "Environmental Risk Score",
    f"{environmental_score}/100"
)

r2.metric(
    "Environmental Risk Level",
    environmental_level
)


if environmental_level == "High":

    st.error(
        "🚨 HIGH ENVIRONMENTAL RISK"
    )

elif environmental_level == "Medium":

    st.warning(
        "⚠️ MODERATE ENVIRONMENTAL RISK"
    )

else:

    st.success(
        "🟢 LOW ENVIRONMENTAL RISK"
    )


# =========================================================
# RISK FACTORS
# =========================================================

st.subheader(
    "🔍 Detected Environmental Factors"
)

environment_factors = []


if env_rainfall >= 75:

    environment_factors.append(
        "High recent rainfall may increase water-contamination concerns."
    )


if env_humidity >= 70:

    environment_factors.append(
        "High humidity detected."
    )


if env_temperature >= 30:

    environment_factors.append(
        "Higher environmental temperature detected."
    )


if env_sanitation in [
    "Moderate",
    "Poor"
]:

    environment_factors.append(
        "Sanitation condition requires additional monitoring."
    )


if len(environment_factors) > 0:

    for factor in environment_factors:

        st.write(
            "• " + factor
        )

else:

    st.write(
        "✅ No major environmental warning factor detected."
    )


# =========================================================
# PREVENTIVE ACTION
# =========================================================

st.subheader(
    "🎯 Environmental Preventive Action"
)


if environmental_level == "High":

    st.info(
        """
🚨 Increase monitoring.

• Review local water sources.
• Check affected households.
• Prefer safe/treated drinking water.
• Consider appropriate water-quality testing.
• Increase community surveillance.
"""
    )

elif environmental_level == "Medium":

    st.info(
        """
⚠️ Moderate environmental concern.

• Continue water-quality monitoring.
• Review sanitation conditions.
• Monitor changes after rainfall.
"""
    )

else:

    st.success(
        """
🟢 Continue routine environmental monitoring.
"""
    )


# =========================================================
# COMBINED ENVIRONMENT + WATER RISK
# =========================================================

st.subheader(
    "🤖 Combined Environmental + Water Risk"
)


combined_water_score = st.slider(
    "💧 Current Water Risk Score",
    min_value=0,
    max_value=100,
    value=30,
    step=1,
    key="combined_water_score"
)


combined_score = round(
    (
        combined_water_score * 0.65
        +
        environmental_score * 0.35
    ),
    2
)


if combined_score >= 70:

    combined_level = "High"

elif combined_score >= 40:

    combined_level = "Medium"

else:

    combined_level = "Low"


c1, c2 = st.columns(2)

c1.metric(
    "Combined Risk Score",
    f"{combined_score}/100"
)

c2.metric(
    "Combined Risk Level",
    combined_level
)


if combined_level == "High":

    st.error(
        "🚨 Water + Environmental conditions "
        "indicate HIGH early-warning priority."
    )

elif combined_level == "Medium":

    st.warning(
        "⚠️ Water + Environmental conditions "
        "indicate MODERATE early-warning priority."
    )

else:

    st.success(
        "🟢 Water + Environmental conditions "
        "indicate LOW early-warning priority."
    )


# =========================================================
# FUTURE AUTOMATION
# =========================================================

with st.expander(
    "🤖 Future Automatic Environmental Data"
):

    st.code(
        """
Village / Location
       ↓
Weather / Environmental Data Service
       ↓
Rainfall
Humidity
Temperature
       ↓
Environmental Risk Engine
       ↓
+
IoT Water Sensor
       ↓
Combined Risk
       ↓
Household + Community Analysis
       ↓
Automatic Early Warning
""",
        language="text"
    )


st.caption(
    "⚠️ Environmental indicators support early-warning "
    "and decision-making. They do not independently "
    "confirm contamination or disease."
)
# =========================================================
# 🧠 JEEVAN-ALERT FINAL UNIFIED RISK ENGINE
# =========================================================

st.divider()

st.header("🧠 Final Unified AI Risk Engine")

st.write(
    "Combines water quality, household vulnerability, "
    "environmental conditions and community risk into "
    "one early-warning score."
)





# =========================================================
# AUTOMATIC RISK INPUTS
# =========================================================

st.subheader("📥 Automatic Risk Inputs")

PROFILE_FILE = "data/household_profiles.csv"
IOT_FILE = "data/iot_devices.csv"

if not os.path.exists(PROFILE_FILE):

    st.warning("⚠️ Household profile file not found.")

    final_water_score = 0
    final_vulnerability_score = 0
    final_environment_score = 0
    final_community_score = 0

else:

    profiles = pd.read_csv(PROFILE_FILE)

    if len(profiles) == 0:

        st.warning("⚠️ No household profile available.")

        final_water_score = 0
        final_vulnerability_score = 0
        final_environment_score = 0
        final_community_score = 0

    else:

        # -------------------------------------------------
        # SELECT HOUSEHOLD
        # -------------------------------------------------

        household_list = (
            profiles["house_id"]
            .astype(str)
            .unique()
            .tolist()
        )

        selected_final_house = st.selectbox(
            "🏠 Select Household",
            household_list,
            key="final_engine_house_id"
        )

        family_rows = profiles[
            profiles["house_id"].astype(str)
            == selected_final_house
        ]

        family = family_rows.iloc[-1]

        village = str(family["village"])

        # -------------------------------------------------
        # HOUSEHOLD VULNERABILITY
        # -------------------------------------------------

        age_0_5 = int(family["age_0_5"])
        age_6_17 = int(family["age_6_17"])
        age_60_plus = int(family["age_60_plus"])

        final_vulnerability_score = 0

        final_vulnerability_score += age_0_5 * 20
        final_vulnerability_score += age_6_17 * 10
        final_vulnerability_score += age_60_plus * 20

        final_vulnerability_score = min(
            final_vulnerability_score,
            100
        )

        # -------------------------------------------------
        # WATER RISK FROM IoT
        # -------------------------------------------------

        final_water_score = 0

        if os.path.exists(IOT_FILE):

            devices = pd.read_csv(IOT_FILE)

            household_devices = devices[
                devices["house_id"].astype(str)
                == selected_final_house
            ]

            if len(household_devices) > 0:

                sensor = household_devices.iloc[-1]

                ph = pd.to_numeric(
                    sensor["pH"],
                    errors="coerce"
                )

                tds = pd.to_numeric(
                    sensor["TDS"],
                    errors="coerce"
                )

                turbidity = pd.to_numeric(
                    sensor["turbidity"],
                    errors="coerce"
                )

                temperature = pd.to_numeric(
                    sensor["temperature"],
                    errors="coerce"
                )

                # pH
                if not pd.isna(ph):

                    if ph < 6.5 or ph > 8.5:
                        final_water_score += 30

                    elif ph < 6.8 or ph > 8.2:
                        final_water_score += 15

                # TDS
                if not pd.isna(tds):

                    if tds > 1000:
                        final_water_score += 30

                    elif tds > 500:
                        final_water_score += 15

                # Turbidity
                if not pd.isna(turbidity):

                    if turbidity > 10:
                        final_water_score += 30

                    elif turbidity > 5:
                        final_water_score += 15

                # Temperature
                if not pd.isna(temperature):

                    if temperature > 35:
                        final_water_score += 10

                    elif temperature > 30:
                        final_water_score += 5

        final_water_score = min(
            final_water_score,
            100
        )

        # -------------------------------------------------
        # ENVIRONMENT RISK
        # -------------------------------------------------

        # Existing Environmental Risk Engine ka
        # calculated score automatically use hoga.

        # ---------------------------------------------------------
# AUTOMATIC ENVIRONMENT RISK
# ---------------------------------------------------------

final_environment_score = 0

try:

    # Existing village dataset
    if "selected" in globals():

        env_rainfall = pd.to_numeric(
            selected["rainfall"],
            errors="coerce"
        )

        env_humidity = pd.to_numeric(
            selected["humidity"],
            errors="coerce"
        )

        env_temperature = pd.to_numeric(
            selected["temperature"],
            errors="coerce"
        )

        env_sanitation = pd.to_numeric(
            selected["sanitation_score"],
            errors="coerce"
        )

        if not pd.isna(env_rainfall):

            if env_rainfall >= 150:
                final_environment_score += 35

            elif env_rainfall >= 75:
                final_environment_score += 20

            elif env_rainfall >= 30:
                final_environment_score += 10

        if not pd.isna(env_humidity):

            if env_humidity >= 85:
                final_environment_score += 20

            elif env_humidity >= 70:
                final_environment_score += 10

        if not pd.isna(env_temperature):

            if env_temperature >= 35:
                final_environment_score += 20

            elif env_temperature >= 30:
                final_environment_score += 10

        if not pd.isna(env_sanitation):

            if env_sanitation < 50:
                final_environment_score += 25

            elif env_sanitation < 70:
                final_environment_score += 10

except Exception:
 
      final_environment_score = 0


final_environment_score = min(
    final_environment_score,
    100
)

        # -------------------------------------------------
        # COMMUNITY RISK
        # -------------------------------------------------

final_community_score = 0

try:

            community_history = load_water_history()

            if (
                len(community_history) > 0
                and "village" in community_history.columns
            ):

                village_data = community_history[
                    community_history["village"].astype(str)
                    == village
                ]

                if len(village_data) > 0:

                    if "combined_priority_score" in village_data.columns:

                        final_community_score = pd.to_numeric(
                            village_data[
                                "combined_priority_score"
                            ],
                            errors="coerce"
                        ).mean()

                    elif "water_score" in village_data.columns:

                        final_community_score = pd.to_numeric(
                            village_data[
                                "water_score"
                            ],
                            errors="coerce"
                        ).mean()
  
except Exception:

    final_community_score = 0

    if pd.isna(final_community_score):

            final_community_score = 0

    final_community_score = min(
            float(final_community_score),
            100
        )

        # -------------------------------------------------
        # SHOW AUTOMATIC INPUTS
        # -------------------------------------------------

a1, a2, a3, a4 = st.columns(4)

a1.metric(
     "💧 Water Risk",
        f"{final_water_score:.1f}/100"
        )
a2.metric(
            "👨‍👩‍👧 Vulnerability",
            f"{final_vulnerability_score:.1f}/100"
        )

a3.metric(
     "🌦️ Environment",
            f"{final_environment_score:.1f}/100"
        )

a4.metric(
            "🏘️ Community",
            f"{final_community_score:.1f}/100"
        )

st.info(
            f"🏠 Household: {selected_final_house}  |  "
            f"📍 Village: {village}"
        ) 


# =========================================================
# WEIGHTED RISK CALCULATION
# =========================================================

final_risk_score = (

    final_water_score * 0.40

    +

    final_vulnerability_score * 0.20

    +

    final_environment_score * 0.20

    +

    final_community_score * 0.20
)


final_risk_score = round(
    min(
        final_risk_score,
        100
    ),
    
)


# =========================================================
# FINAL RISK LEVEL
# =========================================================

if final_risk_score >= 75:

    final_risk_level = "Critical"

elif final_risk_score >= 55:

    final_risk_level = "High"

elif final_risk_score >= 30:

    final_risk_level = "Medium"

else:

    final_risk_level = "Low"


# =========================================================
# DISPLAY FINAL SCORE
# =========================================================

st.subheader(
    "🚨 Final Early-Warning Result"
)


f1, f2, f3 = st.columns(3)


f1.metric(
    "🧠 Final Risk Score",
    f"{final_risk_score}/100"
)


f2.metric(
    "🚨 Risk Level",
    final_risk_level
)


f3.metric(
    "🎯 Priority",
    (
        "Immediate"
        if final_risk_level == "Critical"
        else
        "High"
        if final_risk_level == "High"
        else
        "Monitor"
    )
)


# =========================================================
# STATUS
# =========================================================

if final_risk_level == "Critical":

    st.error(
        """
🚨 CRITICAL EARLY WARNING

Multiple risk factors combine to produce
a very high priority screening result.
"""
    )

elif final_risk_level == "High":

    st.error(
        """
🔴 HIGH EARLY WARNING

The household/community requires
increased monitoring and preventive action.
"""
    )

elif final_risk_level == "Medium":

    st.warning(
        """
🟡 MODERATE EARLY WARNING

Continue increased monitoring and
review changing risk factors.
"""
    )

else:

    st.success(
        """
🟢 LOW RISK

Continue routine monitoring.
"""
    )


# =========================================================
# RISK CONTRIBUTION
# =========================================================

st.subheader(
    "📊 Risk Contribution"
)


contribution_df = pd.DataFrame(
    {
        "Risk Factor": [
            "Water Quality",
            "Household Vulnerability",
            "Environment",
            "Community"
        ],

        "Score": [
            final_water_score,
            final_vulnerability_score,
            final_environment_score,
            final_community_score
        ],

        "Weight (%)": [
            40,
            20,
            20,
            20
        ]
    }
)


contribution_df[
    "Weighted Contribution"
] = (

    contribution_df["Score"]
    *
    contribution_df["Weight (%)"]
    /
    100
)


st.dataframe(
    contribution_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# MAIN RISK DRIVER
# =========================================================

risk_values = {
    "Water Quality":
        final_water_score,

    "Household Vulnerability":
        final_vulnerability_score,

    "Environment":
        final_environment_score,

    "Community":
        final_community_score
}


main_driver = max(
    risk_values,
    key=risk_values.get
)


st.info(
    f"""
🔎 Main Risk Driver:

{main_driver}

Score:
{risk_values[main_driver]}/100

The system can prioritize this factor
for further investigation.
"""
)


# =========================================================
# AUTOMATIC ACTION
# =========================================================

st.subheader(
    "🎯 Automatic Recommended Action"
)


if final_risk_level == "Critical":

    final_action = """
🚨 IMMEDIATE PRIORITY

1. Prefer safe/treated drinking water.
2. Avoid untreated drinking water.
3. Review vulnerable household members.
4. Review the relevant water source.
5. Arrange appropriate water-quality testing.
6. Notify the responsible health worker.
7. Review nearby households for similar patterns.
"""

elif final_risk_level == "High":

    final_action = """
🔴 HIGH PRIORITY

1. Prefer safe/treated drinking water.
2. Review vulnerable household members.
3. Increase water-quality monitoring.
4. Review the local water source.
5. Consider appropriate testing.
6. Consider notifying the responsible health worker.
"""

elif final_risk_level == "Medium":

    final_action = """
🟡 MODERATE PRIORITY

1. Prefer safe drinking water.
2. Continue monitoring.
3. Review changing environmental conditions.
4. Give additional precaution to vulnerable groups.
5. Consider appropriate testing if concerns persist.
"""

else:

    final_action = """
🟢 ROUTINE PRIORITY

1. Continue normal water-safety practices.
2. Continue periodic monitoring.
3. Watch for changes in water quality.
"""


st.info(
    final_action
)


# =========================================================
# AUTOMATIC ALERT TYPE
# =========================================================

if final_risk_level == "Critical":

    alert_type = (
        "🚨 FAMILY + HEALTH WORKER + ADMIN"
    )

elif final_risk_level == "High":

    alert_type = (
        "🔴 FAMILY + HEALTH WORKER"
    )

elif final_risk_level == "Medium":

    alert_type = (
        "🟡 FAMILY MONITORING ALERT"
    )

else:

    alert_type = (
        "🟢 DASHBOARD MONITORING"
    )


st.subheader(
    "📢 Automatic Alert Routing"
)

st.write(
    alert_type
)


# =========================================================
# COMPLETE DECISION FLOW
# =========================================================

with st.expander(
    "🤖 Complete AI Decision Flow"
):

    st.code(
        f"""
💧 WATER QUALITY
{final_water_score}/100
        ↓
👨‍👩‍👧 HOUSEHOLD VULNERABILITY
{final_vulnerability_score}/100
        ↓
🌦️ ENVIRONMENT
{final_environment_score}/100
        ↓
🏘️ COMMUNITY
{final_community_score}/100
        ↓
        🧠
FINAL RISK ENGINE
        ↓
{final_risk_score}/100
        ↓
{final_risk_level.upper()}
        ↓
📢 {alert_type}
        ↓
🎯 PREVENTIVE ACTION
""",
        language="text"
    )


# =========================================================
# FUTURE AUTOMATION
# =========================================================

with st.expander(
    "⚙️ Final Production Automation"
):

    st.code(
        """
ESP32 SENSOR
     ↓
AUTOMATIC WATER DATA
     ↓
HOUSE ID
     ↓
HOUSEHOLD PROFILE
     ↓
WEATHER / ENVIRONMENT
     ↓
COMMUNITY DATABASE
     ↓
AI RISK ENGINE
     ↓
FINAL RISK SCORE
     ↓
AUTOMATIC ALERT
     ↓
FAMILY
HEALTH WORKER
ADMINISTRATOR
""",
        language="text"
    )


st.caption(
    "⚠️ The score is an early-warning decision-support "
    "indicator, not a medical diagnosis or confirmation "
    "of contamination or disease."
)
# =========================================================
# 📢 JEEVAN-ALERT SMART NOTIFICATION CENTER
# =========================================================

st.divider()

st.header("📢 Smart Notification Center")

st.write(
    "Automatically routes early-warning alerts to the "
    "appropriate stakeholders according to risk level."
)


# =========================================================
# FILE
# =========================================================

NOTIFICATION_FILE = "data/notification_history.csv"


if not os.path.exists("data"):
    os.makedirs("data")


# =========================================================
# CREATE NOTIFICATION FILE
# =========================================================

if not os.path.exists(NOTIFICATION_FILE):

    notification_columns = [
        "date_time",
        "house_id",
        "family_name",
        "mobile",
        "village",
        "risk_score",
        "risk_level",
        "recipient",
        "channel",
        "message",
        "status"
    ]

    pd.DataFrame(
        columns=notification_columns
    ).to_csv(
        NOTIFICATION_FILE,
        index=False
    )


# =========================================================
# LOAD HISTORY
# =========================================================

notification_history = pd.read_csv(
    NOTIFICATION_FILE
)


# =========================================================
# ALERT INPUT
# =========================================================

st.subheader(
    "🚨 Generate Smart Notification"
)


n1, n2 = st.columns(2)


with n1:

    notify_house_id = st.text_input(
        "🏠 House ID",
        placeholder="H001",
        key="notify_house_id"
    )

    notify_family_name = st.text_input(
        "👤 Family Name",
        placeholder="Family name",
        key="notify_family_name"
    )

    notify_mobile = st.text_input(
        "📱 Mobile Number",
        placeholder="9876543210",
        key="notify_mobile"
    )


with n2:

    notify_village = st.text_input(
        "🏘️ Village",
        placeholder="Village A",
        key="notify_village"
    )

    notify_risk_score = st.number_input(
        "🧠 Risk Score",
        min_value=0,
        max_value=100,
        value=50,
        step=1,
        key="notify_risk_score"
    )


# =========================================================
# AUTOMATIC RISK LEVEL
# =========================================================

if notify_risk_score >= 75:

    notify_risk_level = "Critical"

elif notify_risk_score >= 55:

    notify_risk_level = "High"

elif notify_risk_score >= 30:

    notify_risk_level = "Medium"

else:

    notify_risk_level = "Low"


st.metric(
    "🚨 Automatic Risk Level",
    notify_risk_level
)


# =========================================================
# AUTOMATIC RECIPIENT ROUTING
# =========================================================

if notify_risk_level == "Critical":

    recipients = [
        "Family",
        "Health Worker",
        "Administrator"
    ]

elif notify_risk_level == "High":

    recipients = [
        "Family",
        "Health Worker"
    ]

elif notify_risk_level == "Medium":

    recipients = [
        "Family"
    ]

else:

    recipients = [
        "Dashboard"
    ]


st.subheader(
    "🎯 Automatic Alert Routing"
)

st.write(
    " → ".join(recipients)
)


# =========================================================
# AUTOMATIC MESSAGE
# =========================================================

if notify_risk_level == "Critical":

    notification_message = f"""
🚨 CRITICAL WATER-SAFETY ALERT

House ID: {notify_house_id}
Family: {notify_family_name}
Village: {notify_village}

Risk Score: {notify_risk_score}/100
Risk Level: CRITICAL

Immediate precaution is recommended.

• Prefer safe/treated drinking water.
• Avoid untreated drinking water.
• Review vulnerable household members.
• Arrange appropriate water-quality testing.
• Contact the responsible health worker.
"""

elif notify_risk_level == "High":

    notification_message = f"""
🔴 HIGH WATER-SAFETY ALERT

House ID: {notify_house_id}
Family: {notify_family_name}
Village: {notify_village}

Risk Score: {notify_risk_score}/100
Risk Level: HIGH

Recommended actions:

• Prefer safe/treated drinking water.
• Avoid untreated water.
• Review vulnerable household members.
• Consider appropriate water-quality testing.
• Health-worker review may be required.
"""

elif notify_risk_level == "Medium":

    notification_message = f"""
⚠️ WATER QUALITY WARNING

House ID: {notify_house_id}
Family: {notify_family_name}
Village: {notify_village}

Risk Score: {notify_risk_score}/100
Risk Level: MEDIUM

Recommended actions:

• Prefer safe drinking water.
• Continue water-quality monitoring.
• Review vulnerable household members.
• Consider appropriate testing.
"""

else:

    notification_message = f"""
🟢 WATER MONITORING UPDATE

House ID: {notify_house_id}
Family: {notify_family_name}
Village: {notify_village}

Risk Score: {notify_risk_score}/100
Risk Level: LOW

Continue regular water-safety practices
and periodic monitoring.
"""


# =========================================================
# PREVIEW
# =========================================================

st.subheader(
    "📩 Notification Preview"
)

st.code(
    notification_message,
    language="text"
)


# =========================================================
# GENERATE NOTIFICATIONS
# =========================================================

if st.button(
    "📢 GENERATE AUTOMATIC NOTIFICATIONS",
    type="primary",
    key="generate_notifications"
):

    if notify_house_id.strip() == "":

        st.error(
            "❌ Please enter House ID."
        )

    elif notify_family_name.strip() == "":

        st.error(
            "❌ Please enter Family Name."
        )

    elif notify_village.strip() == "":

        st.error(
            "❌ Please enter Village."
        )

    else:

        new_records = []


        # -----------------------------------------------
        # CREATE ONE RECORD PER RECIPIENT
        # -----------------------------------------------

        for recipient in recipients:

            if recipient == "Family":

                channel = "SMS / WhatsApp"

            elif recipient == "Health Worker":

                channel = "Health Dashboard / SMS"

            elif recipient == "Administrator":

                channel = "Admin Dashboard / Email"

            else:

                channel = "Dashboard"


            new_records.append(
                {
                    "date_time":
                        datetime.now().strftime(
                            "%d-%m-%Y %H:%M:%S"
                        ),

                    "house_id":
                        notify_house_id.strip(),

                    "family_name":
                        notify_family_name.strip(),

                    "mobile":
                        notify_mobile.strip(),

                    "village":
                        notify_village.strip(),

                    "risk_score":
                        notify_risk_score,

                    "risk_level":
                        notify_risk_level,

                    "recipient":
                        recipient,

                    "channel":
                        channel,

                    "message":
                        notification_message,

                    "status":
                        "GENERATED"
                }
            )


        new_notification_df = pd.DataFrame(
            new_records
        )


        notification_history = pd.concat(
            [
                notification_history,
                new_notification_df
            ],
            ignore_index=True
        )


        notification_history.to_csv(
            NOTIFICATION_FILE,
            index=False
        )


        st.success(
            f"✅ {len(recipients)} notification(s) "
            "generated successfully."
        )


        # -----------------------------------------------
        # SHOW ROUTING
        # -----------------------------------------------

        st.subheader(
            "📡 Notification Routing"
        )

        for recipient in recipients:

            if recipient == "Family":

                st.write(
                    "👨‍👩‍👧 Family → SMS / WhatsApp"
                )

            elif recipient == "Health Worker":

                st.write(
                    "🏥 Health Worker → Health Dashboard / SMS"
                )

            elif recipient == "Administrator":

                st.write(
                    "🏛️ Administrator → Admin Dashboard / Email"
                )

            else:

                st.write(
                    "📊 Dashboard → Monitoring"
                )


# =========================================================
# NOTIFICATION STATISTICS
# =========================================================

st.subheader(
    "📊 Notification Statistics"
)


total_notifications = len(
    notification_history
)


critical_notifications = len(
    notification_history[
        notification_history["risk_level"]
        .astype(str)
        ==
        "Critical"
    ]
)


high_notifications = len(
    notification_history[
        notification_history["risk_level"]
        .astype(str)
        ==
        "High"
    ]
)


medium_notifications = len(
    notification_history[
        notification_history["risk_level"]
        .astype(str)
        ==
        "Medium"
    ]
)


q1, q2, q3, q4 = st.columns(4)


q1.metric(
    "📢 Total",
    total_notifications
)

q2.metric(
    "🚨 Critical",
    critical_notifications
)

q3.metric(
    "🔴 High",
    high_notifications
)

q4.metric(
    "🟡 Medium",
    medium_notifications
)


# =========================================================
# HISTORY
# =========================================================

st.subheader(
    "📋 Notification History"
)


if len(notification_history) > 0:

    st.dataframe(
        notification_history,
        use_container_width=True,
        hide_index=True
    )


    notification_csv = (
        notification_history
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        "⬇️ Download Notification History",
        data=notification_csv,
        file_name="notification_history.csv",
        mime="text/csv",
        key="download_notification_history"
    )

else:

    st.info(
        "No notifications generated yet."
    )


# =========================================================
# PRODUCTION INTEGRATION
# =========================================================

with st.expander(
    "🔌 Production Notification Integration"
):

    st.code(
        """
AI RISK ENGINE
       ↓
RISK LEVEL
       ↓
┌─────────────────────────────┐
│ AUTOMATIC ROUTING ENGINE    │
└─────────────────────────────┘
       ↓
       ├── Family
       │     ↓
       │   SMS / WhatsApp
       │
       ├── Health Worker
       │     ↓
       │   Health Dashboard
       │
       └── Administrator
             ↓
          Admin Dashboard
          / Email

Future APIs can connect these
channels automatically.
""",
        language="text"
    )


st.caption(
    "⚠️ Current MVP generates and records notification "
    "events. Actual SMS/WhatsApp delivery requires "
    "integration with an authorized messaging service."
)
# =========================================================
# 🏛️ JEEVAN-ALERT ADMIN COMMAND CENTER
# =========================================================

st.divider()

st.header("🏛️ JEEVAN-ALERT Admin Command Center")

st.write(
    "Central monitoring dashboard for household, IoT, "
    "water-risk, alert and community-level information."
)


# =========================================================
# FILE PATHS
# =========================================================

PROFILE_FILE = "data/household_profiles.csv"
IOT_FILE = "data/iot_devices.csv"
ALERT_FILE = "data/iot_alert_history.csv"
NOTIFICATION_FILE = "data/notification_history.csv"


# =========================================================
# SAFE DATA LOADING FUNCTION
# =========================================================

def safe_load_csv_admin(file_path):

    try:

        if os.path.exists(file_path):

            return pd.read_csv(file_path)

        return pd.DataFrame()

    except Exception:

        return pd.DataFrame()


admin_profiles = safe_load_csv_admin(
    PROFILE_FILE
)

admin_iot = safe_load_csv_admin(
    IOT_FILE
)

admin_alerts = safe_load_csv_admin(
    ALERT_FILE
)

admin_notifications = safe_load_csv_admin(
    NOTIFICATION_FILE
)


# =========================================================
# HOUSEHOLD COUNT
# =========================================================

if (
    len(admin_profiles) > 0
    and "house_id" in admin_profiles.columns
):

    admin_households = (
        admin_profiles["house_id"]
        .astype(str)
        .nunique()
    )

else:

    admin_households = 0


# =========================================================
# SENSOR COUNT
# =========================================================

admin_total_sensors = len(
    admin_iot
)


if (
    len(admin_iot) > 0
    and "status" in admin_iot.columns
):

    admin_connected_sensors = len(
        admin_iot[
            admin_iot["status"]
            .astype(str)
            .str.lower()
            == "connected"
        ]
    )

else:

    admin_connected_sensors = 0


# =========================================================
# ALERT COUNT
# =========================================================

admin_total_alerts = len(
    admin_alerts
)


if (
    len(admin_alerts) > 0
    and "risk_level" in admin_alerts.columns
):

    admin_high_alerts = len(
        admin_alerts[
            admin_alerts["risk_level"]
            .astype(str)
            .str.title()
            .isin(
                [
                    "High",
                    "Critical"
                ]
            )
        ]
    )

else:

    admin_high_alerts = 0


# =========================================================
# NOTIFICATION COUNT
# =========================================================

admin_total_notifications = len(
    admin_notifications
)


# =========================================================
# MAIN KPI CARDS
# =========================================================

st.subheader(
    "📊 System Overview"
)


k1, k2, k3, k4, k5 = st.columns(5)


k1.metric(
    "🏠 Households",
    admin_households
)


k2.metric(
    "📡 Sensors",
    admin_total_sensors
)


k3.metric(
    "🟢 Connected",
    admin_connected_sensors
)


k4.metric(
    "🚨 High/Critical Alerts",
    admin_high_alerts
)


k5.metric(
    "📢 Notifications",
    admin_total_notifications
)


# =========================================================
# SENSOR HEALTH
# =========================================================

st.subheader(
    "📡 IoT Network Health"
)


if admin_total_sensors > 0:

    disconnected = (
        admin_total_sensors
        -
        admin_connected_sensors
    )

    sensor_health_percentage = round(
        (
            admin_connected_sensors
            /
            admin_total_sensors
        )
        * 100,
        1
    )

else:

    disconnected = 0

    sensor_health_percentage = 0


s1, s2, s3 = st.columns(3)


s1.metric(
    "Total Sensors",
    admin_total_sensors
)


s2.metric(
    "Connected",
    admin_connected_sensors
)


s3.metric(
    "Disconnected",
    disconnected
)


if admin_total_sensors == 0:

    st.info(
        "No IoT sensors registered yet."
    )

elif sensor_health_percentage >= 80:

    st.success(
        f"🟢 IoT Network Health: "
        f"{sensor_health_percentage}% connected"
    )

elif sensor_health_percentage >= 50:

    st.warning(
        f"🟡 IoT Network Health: "
        f"{sensor_health_percentage}% connected"
    )

else:

    st.error(
        f"🔴 IoT Network Health: "
        f"{sensor_health_percentage}% connected"
    )


# =========================================================
# ALERT RISK DISTRIBUTION
# =========================================================

st.subheader(
    "🚨 Alert Risk Distribution"
)


if (
    len(admin_alerts) > 0
    and "risk_level" in admin_alerts.columns
):

    admin_risk_counts = (
        admin_alerts["risk_level"]
        .astype(str)
        .str.title()
        .value_counts()
    )


    risk_names = [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]


    risk_values = []

    for risk_name in risk_names:

        risk_values.append(
            admin_risk_counts.get(
                risk_name,
                0
            )
        )


    admin_risk_chart = pd.DataFrame(
        {
            "Risk Level":
                risk_names,

            "Alerts":
                risk_values
        }
    )


    st.bar_chart(
        admin_risk_chart.set_index(
            "Risk Level"
        )
    )

else:

    st.info(
        "No risk alerts available yet."
    )


# =========================================================
# VILLAGE PRIORITY
# =========================================================

st.subheader(
    "🏘️ Priority Villages"
)


if (
    len(admin_alerts) > 0
    and "village" in admin_alerts.columns
):

    village_priority = (
        admin_alerts
        .assign(
            risk_clean=
            admin_alerts[
                "risk_level"
            ]
            .astype(str)
            .str.title()
        )
    )


    village_priority = village_priority[
        village_priority["risk_clean"]
        .isin(
            [
                "High",
                "Critical"
            ]
        )
    ]


    if len(village_priority) > 0:

        village_table = (
            village_priority
            .groupby("village")
            .size()
            .reset_index(
                name="High/Critical Alerts"
            )
            .sort_values(
                "High/Critical Alerts",
                ascending=False
            )
        )


        st.dataframe(
            village_table,
            use_container_width=True,
            hide_index=True
        )


        top_village = (
            village_table.iloc[0]["village"]
        )

        top_village_alerts = (
            village_table.iloc[0]
            ["High/Critical Alerts"]
        )


        st.warning(
            f"""
🎯 Priority Area:

{top_village}

High/Critical alerts:
{top_village_alerts}

Recommended: Review households and
water sources in this area.
"""
        )

    else:

        st.success(
            "🟢 No high/critical village hotspot detected."
        )

else:

    st.info(
        "Village alert data is not available yet."
    )


# =========================================================
# WATER SOURCE ANALYSIS
# =========================================================

st.subheader(
    "🚰 Water Source Risk Monitoring"
)


if (
    len(admin_profiles) > 0
    and "water_source" in admin_profiles.columns
):

    source_counts = (
        admin_profiles[
            "water_source"
        ]
        .astype(str)
        .value_counts()
        .reset_index()
    )


    source_counts.columns = [
        "Water Source",
        "Households"
    ]


    st.dataframe(
        source_counts,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Water-source information is not available."
    )


# =========================================================
# RECENT ALERTS
# =========================================================

st.subheader(
    "📋 Recent Alerts"
)


if len(admin_alerts) > 0:

    recent_alerts = (
        admin_alerts
        .tail(10)
        .iloc[::-1]
    )


    st.dataframe(
        recent_alerts,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No alerts generated yet."
    )


# =========================================================
# RECENT NOTIFICATIONS
# =========================================================

st.subheader(
    "📢 Recent Notifications"
)


if len(admin_notifications) > 0:

    recent_notifications = (
        admin_notifications
        .tail(10)
        .iloc[::-1]
    )


    st.dataframe(
        recent_notifications,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No notifications generated yet."
    )


# =========================================================
# ADMIN DECISION SUPPORT
# =========================================================

st.subheader(
    "🎯 Administrator Decision Support"
)


if admin_high_alerts >= 5:

    admin_status = "CRITICAL"

    admin_action = """
🚨 Immediate attention required.

• Review high-risk households.
• Identify common water sources.
• Review priority villages.
• Increase monitoring.
• Coordinate appropriate testing.
• Notify responsible health authorities when required.
"""


elif admin_high_alerts >= 3:

    admin_status = "HIGH"

    admin_action = """
🔴 High-priority monitoring required.

• Review affected households.
• Check water-source patterns.
• Increase community surveillance.
"""


elif admin_high_alerts >= 1:

    admin_status = "WATCH"

    admin_action = """
🟡 Community watch activated.

• Monitor affected households.
• Review water-source conditions.
• Continue collecting data.
"""


else:

    admin_status = "NORMAL"

    admin_action = """
🟢 System status normal.

• Continue routine monitoring.
• Continue collecting household and sensor data.
"""


a1, a2 = st.columns(2)


a1.metric(
    "🏛️ Community Status",
    admin_status
)


a2.metric(
    "🚨 High/Critical Alerts",
    admin_high_alerts
)


st.info(
    admin_action
)


# =========================================================
# COMPLETE SYSTEM MAP
# =========================================================

with st.expander(
    "🧠 JEEVAN-ALERT Complete System Architecture"
):

    st.code(
        """
                HOUSEHOLDS
                    ↓
              HOUSE ID
                    ↓
        ┌─────────────────────┐
        │  HOUSEHOLD PROFILE  │
        └─────────────────────┘
                    ↓
              IoT SENSOR
                    ↓
        pH / TDS / Turbidity
          / Temperature
                    ↓
             WATER RISK
                    ↓
        ┌─────────────────────┐
        │ FAMILY VULNERABILITY│
        └─────────────────────┘
                    ↓
        ┌─────────────────────┐
        │ ENVIRONMENTAL RISK  │
        └─────────────────────┘
                    ↓
        ┌─────────────────────┐
        │ COMMUNITY ANALYSIS  │
        └─────────────────────┘
                    ↓
               🧠 AI ENGINE
                    ↓
             FINAL RISK SCORE
                    ↓
              EARLY WARNING
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      FAMILY   HEALTH WORKER   ADMIN
        ↓           ↓           ↓
       📱          🏥          🏛️
                    ↓
            PREVENTIVE ACTION
"""
        ,
        language="text"
    )


# =========================================================
# DOWNLOAD ADMIN REPORT
# =========================================================

st.subheader(
    "📥 Admin Data Export"
)


admin_report = pd.DataFrame(
    {
        "Metric": [
            "Total Households",
            "Total IoT Sensors",
            "Connected Sensors",
            "High/Critical Alerts",
            "Total Notifications",
            "Community Status"
        ],

        "Value": [
            admin_households,
            admin_total_sensors,
            admin_connected_sensors,
            admin_high_alerts,
            admin_total_notifications,
            admin_status
        ]
    }
)


admin_csv = (
    admin_report
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    "⬇️ Download Admin Summary",
    data=admin_csv,
    file_name="jeevan_alert_admin_summary.csv",
    mime="text/csv",
    key="download_admin_summary"
)


st.caption(
    "⚠️ This dashboard provides early-warning and "
    "decision-support information. It does not diagnose "
    "disease or confirm contamination."
)

