import streamlit as st
import pandas as pd
import plotly.express as px

def filter_details(vfd):
    vfd["timestamp"] = vfd["timestamp"].str.strip()
    vfd["dvr"] = vfd["dvr"].astype(str)
    vfd["timestamp"] = pd.to_datetime(vfd["timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    vfd = vfd.sort_values("timestamp", ascending=False)

    vfd["Day"] = vfd["timestamp"].apply(lambda x: str(x.month) +"-"+str(x.day))
    vfd["dvr"] = vfd["dvr"].str.strip()
    filter_by_dvr_details = vfd["dvr"].unique().tolist()
    filter_by_dvr_details.append("All")
    default_index_dvr_details = len(filter_by_dvr_details) - 1
    dvr_details = st.sidebar.selectbox("Dvr",filter_by_dvr_details,index=default_index_dvr_details)

    vfd["request"] = vfd["request"].str.strip()
    filter_by_request_details = vfd["request"].unique().tolist()
    filter_by_request_details.append("All")
    default_index_request_details = len(filter_by_request_details) - 1
    request_details = st.sidebar.selectbox("Request",filter_by_request_details,index=default_index_request_details)

    vfd["status"] = vfd["status"].str.strip()
    filter_by_status_details = vfd["status"].unique().tolist()
    filter_by_status_details.append("All")
    default_index_status_details = len(filter_by_status_details) - 1
    status_details = st.sidebar.selectbox("Status",filter_by_status_details,index=default_index_status_details)

    filter_by_issue_details = ["All","Date 1971","Duplicate"]
    issue_details = st.sidebar.selectbox("Issue",filter_by_issue_details)

    if dvr_details != "All":
        vfd = vfd[vfd["dvr"] == dvr_details]

    if request_details != "All":
        vfd = vfd[vfd["request"] == request_details]

    if status_details != "All":
        vfd = vfd[vfd["status"] == status_details]

    if issue_details == "Date 1971":
        vfd = vfd[vfd["file"].str.contains("1971", na=False)]

    if issue_details == "Duplicate":
        vfd = vfd[vfd.duplicated(subset="file", keep=False)]

    return vfd

def filter_request_video(df):
    df["timestamp"] = df["timestamp"].str.strip()
    df["dvr"] = df["dvr"].astype(str)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    df = df.sort_values("timestamp", ascending=False)

    df["Diference"] = abs(df["received"] - df["uploaded"])
    
    df["Day"] = df["timestamp"].apply(lambda x: str(x.month) +"-"+str(x.day))
    filter_by_day = df["Day"].unique().tolist()
    filter_by_day.append("All")
    default_index_day = len(filter_by_day) - 1
    day = st.sidebar.selectbox("Day",filter_by_day,index=default_index_day)

    df["request"] = df["request"].str.strip()
    filter_by_request = df["request"].unique().tolist()
    filter_by_request.append("All")
    default_index_request = len(filter_by_request) - 1
    request = st.sidebar.selectbox("Request",filter_by_request,index=default_index_request)

    df["source"] = df["source"].str.strip()
    filter_by_source = df["source"].unique().tolist()
    filter_by_source.append("All")
    default_index_source = len(filter_by_source) - 1
    source = st.sidebar.selectbox("Source",filter_by_source,index=default_index_source)

    df["account"] = df["account"].str.strip()
    filter_by_Account = df["account"].unique().tolist()
    filter_by_Account.append("All")
    default_index_account = len(filter_by_Account) - 1
    account = st.sidebar.selectbox("Account",filter_by_Account,index=default_index_account)

    df["dvr"] = df["dvr"].str.strip()
    filter_by_dvr = df["dvr"].unique().tolist()
    filter_by_dvr.append("All")
    default_index_dvr = len(filter_by_dvr) - 1
    dvr = st.sidebar.selectbox("Dvr",filter_by_dvr,index=default_index_dvr)

    filter_by_problems = ["All","Diference Received x Uploaded"]
    issue = st.sidebar.selectbox("Issue",filter_by_problems)


    if day != "All":
        df_filtered = df[df["Day"] == day]
    else:
        df_filtered = df

    if source != "All":
        df_filtered = df_filtered[df_filtered["source"] == source]

    if account != "All":
        df_filtered = df_filtered[df_filtered["account"] == account]

    if dvr != "All":
        df_filtered = df_filtered[df_filtered["dvr"] == dvr]

    if issue == "Diference Received x Uploaded":
        df_filtered = df_filtered[df_filtered["Diference"] > 0]

    if request != "All":
        df_filtered = df_filtered[df_filtered["request"] == request]

    return df_filtered