import streamlit as st
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the trained model
model = joblib.load('ids_model1.joblib')

# Title
st.title("Intrusion Detection System (Packet Classification)")

# Input fields for packet parameters
st.header("Enter Packet Parameters")
parameters = {}

# Text inputs for numerical features
numerical_features = [
    'count', 'duration', 'src_bytes', 'dst_bytes', 'hot', 'srv_count',
    'dst_host_count', 'dst_host_srv_count', 'dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate','logged_in'
]

for feature in numerical_features:
    parameters[feature] = st.number_input(f"Enter {feature}:", value=0.0)

# Dropdowns for categorical features
parameters['protocol_type'] = st.selectbox("Protocol Type:", ['tcp', 'udp', 'icmp'])
parameters['service'] = st.selectbox("Service:", ['http', 'ftp', 'smtp', 'other'])  # Add services as per dataset
parameters['flag'] = st.selectbox("Flag:", ['SF', 'REJ', 'RSTO', 'SH'])  # Add flags as per dataset

# Encode categorical inputs
le_protocol = LabelEncoder()
le_service = LabelEncoder()
le_flag = LabelEncoder()

# Assume encodings are consistent with training
protocol_mapping = {'tcp': 0, 'udp': 1, 'icmp': 2}  # Replace with actual mapping
service_mapping = {'http': 0, 'ftp': 1, 'smtp': 2, 'other': 3}  # Replace with actual mapping
flag_mapping = {'SF': 0, 'REJ': 1, 'RSTO': 2, 'SH': 3}  # Replace with actual mapping

parameters['protocol_type'] = protocol_mapping[parameters['protocol_type']]
parameters['service'] = service_mapping[parameters['service']]
parameters['flag'] = flag_mapping[parameters['flag']]

# Standardize numerical features
scaler = StandardScaler()
numerical_values = np.array([parameters[feature] for feature in numerical_features]).reshape(1, -1)
scaled_numerical_values = scaler.fit_transform(numerical_values)  # Use same scaler used in training

final_input = np.array([
    parameters['src_bytes'], parameters['protocol_type'], parameters['dst_host_srv_count'], 
    parameters['dst_bytes'], parameters['hot'], parameters['service'], parameters['dst_host_diff_srv_rate'], 
    parameters['duration'], parameters['flag'], parameters['dst_host_count'], 
    parameters['dst_host_same_src_port_rate'], parameters['logged_in'], parameters['dst_host_rerror_rate'], 
    parameters['dst_host_srv_diff_host_rate'], parameters['dst_host_srv_serror_rate'], 
    parameters['srv_count'], parameters['count']
]).reshape(1, -1)


# Prediction
if st.button("Predict"):
    prediction = model.predict(final_input)
    if prediction[0] == 0:
        st.success("The packet is NORMAL.")
    else:
        st.error("The packet is ANOMALOUS.")
