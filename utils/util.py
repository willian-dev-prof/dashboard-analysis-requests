# pylint: disable=unused-argument
# pylint: disable=import-error
# pylint: disable=broad-exception-caught
import streamlit as st
import pandas as pd


def filter_general(df,vfd,tt):
    '''
    Filter the dataframes based on selected requests and DVRs from the sidebar multiselect widgets.

    Parameters:
    - df (pandas.DataFrame): The main dataframe containing the data to be filtered.
    - vfd (pandas.DataFrame): The VFD dataframe to be filtered based on requests and DVRs.
    - tt (pandas.DataFrame): The TT dataframe to be filtered based on requests and DVRs.

    Returns:
    - Tuple[pandas.DataFrame, pandas.DataFrame, pandas.DataFrame]: Filtered dataframes for df, vfd, and tt respectively.
    '''
    df["dvr"] = df["dvr"].astype(str)
    vfd["dvr"] = vfd["dvr"].astype(str)
    tt["dvr"] = tt["dvr"].astype(str)
    df["request"] = df["request"].str.strip()
    filter_by_request = df["request"].unique().tolist()
    request = st.sidebar.multiselect("Request",options=filter_by_request)

    df["dvr"] = df["dvr"].str.strip()
    filter_by_dvr = df["dvr"].unique().tolist()
    dvr = st.sidebar.multiselect("Dvr",options=filter_by_dvr)

    if len(request) > 0:
        df = df[df["request"].isin(request)]
        vfd = vfd[vfd["request"].isin(request)]
        tt = tt[tt["request"].isin(request)]

    if len(dvr) > 0:
        df = df[df["dvr"].isin(dvr)]
        vfd = vfd[vfd["dvr"].isin(dvr)]
        tt = tt[tt["dvr"].isin(dvr)]

    return df,vfd,tt

def filter_details(vfd):
    '''
    Filter details based on selected status and issue filters.

    Args:
        vfd (pandas.DataFrame): DataFrame containing details to be filtered.

    Returns:
        pandas.DataFrame: Filtered DataFrame based on selected status and issue filters.
    '''
    vfd["timestamp"] = vfd["timestamp"].str.strip()
    vfd["timestamp"] = pd.to_datetime(vfd["timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    vfd = vfd.sort_values("timestamp", ascending=False)

    vfd["Day"] = vfd["timestamp"].apply(lambda x: str(x.month) +"-"+str(x.day))

    vfd["status"] = vfd["status"].str.strip()
    filter_by_status_details = vfd["status"].unique().tolist()
    status_details = st.sidebar.multiselect("Status",options=filter_by_status_details)

    filter_by_issue_details = ["All","Date 1971","Duplicate"]
    issue_details = st.sidebar.multiselect("Issue",options=filter_by_issue_details)

    if len(status_details) > 0:
        vfd = vfd[vfd["status"].isin(status_details)]

    if "Date 1971" in issue_details:
        vfd = vfd[vfd["file"].str.contains("1971", na=False)]

    if  "Duplicate" in issue_details:
        vfd = vfd[vfd.duplicated(subset="file", keep=False)]

    return vfd

def filter_request_video(df):
    '''
    Filter the given DataFrame based on user-selected criteria such as day, source, account, 
    and specific issues. Return the filtered DataFrame.
    '''
    df["timestamp"] = df["timestamp"].str.strip()
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S", errors='coerce')
    df = df.sort_values("timestamp", ascending=False)

    df["Diference"] = abs(df["received"] - df["uploaded"])

    df["Day"] = df["timestamp"].apply(lambda x: str(x.month) +"-"+str(x.day))
    filter_by_day = df["Day"].unique().tolist()
    day = st.sidebar.multiselect("Day",options=filter_by_day)

    df["source"] = df["source"].str.strip()
    filter_by_source = df["source"].unique().tolist()
    source = st.sidebar.multiselect("Source",options=filter_by_source)

    df["account"] = df["account"].str.strip()
    filter_by_account = df["account"].unique().tolist()
    account = st.sidebar.multiselect("Account",options=filter_by_account)

    filter_by_problems = ["All","Diference Received x Uploaded",
                          "Video Details > 200","Video Details > 1000",
                          "Videos Uploaded > 200","Videos Uploaded > 1000"]
    issue = st.sidebar.multiselect("Issue",options=filter_by_problems)

    if len(day) > 0:
        df_filtered = df[df["Day"].isin(day)]
    else:
        df_filtered = df

    if len(source) > 0:
        df_filtered = df_filtered[df_filtered["source"].isin(source)]

    if len(account) > 0:
        df_filtered = df_filtered[df_filtered["account"].isin(account)]

    if "Diference Received x Uploaded" in issue:
        df_filtered = df_filtered[df_filtered["Diference"] > 0]

    if "Video Details > 200" in issue:
        df_filtered = df_filtered[df_filtered["videos_details"] > 200]

    if "Video Details > 1000" in issue:
        df_filtered = df_filtered[df_filtered["videos_details"] > 1000]

    if "Videos Uploaded > 200" in issue:
        df_filtered = df_filtered[df_filtered["uploaded"] > 200]

    if "Videos Uploaded > 1000" in issue:
        df_filtered = df_filtered[df_filtered["uploaded"] > 1000]

    return df_filtered
