'''
Module for displaying various dashboards related to request videos, video file details, transaction tracking, and data consolidation.

Dependencies:
- streamlit
- pandas
- plotly.express
- utils.util.filter_details
- utils.util.filter_request_video
- utils.util.filter_general

Functions:
- request_videos(df_filtered): Display bar charts showing the number of videos uploaded, received, and the difference between received and uploaded per day.
- video_file_details(vfd): Display details of video files including total size, format distribution, and status distribution.
- transaction_tracker(tt): Display a DataFrame `tt` in the Streamlit app.
- consolidation(df_filtered, vfd): Display statistics such as total requests, errors, videos, completed videos, pending videos, and videos with errors. Generates pie charts to visualize data distribution by different categories.
'''
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.util import filter_details,filter_request_video,filter_general

def request_videos(df_filtered):
    '''
        Function to display request videos dashboard.

        Parameters:
            - df_filtered: DataFrame containing filtered data.

        Displays bar charts showing the number of videos uploaded, received, and the difference between received and uploaded per day.
    '''
    st.header("Request Videos")
    columns_to_drop = ["Diference", "Day"]
    st.dataframe(df_filtered.drop(columns=columns_to_drop))

    col1 , col2 , col3 = st.columns(3)
    Number_uploaded_by_day = px.bar(df_filtered, x="Day", y="uploaded",color="source",title="Number of Uploaded per Day")
    Number_received_by_day = px.bar(df_filtered, x="Day", y="received",color="source",title="Number of Received per Day")
    Number_diference_beetween_received_uploaded = px.bar(df_filtered, x="Day", y="Diference",color="source",title="Diference Between Received x Uploaded")
    col1.plotly_chart(Number_uploaded_by_day,use_container_width=True)
    col2.plotly_chart(Number_received_by_day,use_container_width=True)
    col3.plotly_chart(Number_diference_beetween_received_uploaded,use_container_width=True)

def video_file_details(vfd):
    '''
        Display details of video files including total size, format distribution, and status distribution.
    '''
    st.header("Details Videos")
    vfd["total_size"] = vfd["original_size"] + vfd["converted_size"]
    columns_to_drop = ["Day","total_size"]
    st.dataframe(vfd.drop(columns=columns_to_drop))
    col7 , col8 , col9 = st.columns(3)
    Number_temporary_size_day = px.bar(vfd, x="Day", y="total_size",title="Total MB in S3 Per Day")
    vfd_ts = vfd[vfd["format"] == "ts"].shape[0]
    vfd_h264 = vfd[vfd["format"] == "h264"].shape[0]
    Number_format_total = px.pie(vfd,names=["ts","h264"],values=[vfd_ts,vfd_h264],title="Video Format")
    vfd_conv_fail = vfd[vfd["status"] == "convFail"].shape[0]
    vfd_pending = vfd[vfd["status"] =="pending"].shape[0]
    vfd_completed = vfd[vfd["status"] =="completed"].shape[0]
    vfd_less_100 = vfd[vfd["status"] =="Less than 100.0 KiB"].shape[0]
    vfd_less_50 = vfd[vfd["status"] =="Less than 50.0 KiB"].shape[0]
    names = ["convFail","peding","completed","less than 100","less than 50"]
    values = [vfd_conv_fail,vfd_pending,vfd_completed,vfd_less_100,vfd_less_50]
    Number_status_total = px.pie(vfd,names=names,values=values,title="Video Status")

    col7.plotly_chart(Number_temporary_size_day,use_container_width=True)
    col8.plotly_chart(Number_format_total,use_container_width=True)
    col9.plotly_chart(Number_status_total,use_container_width=True)

def transaction_tracker(tt):
    '''
        Display a header "Transaction Tracker" using Streamlit.
        Display a DataFrame `tt` in the Streamlit app.
    '''
    st.header("Transaction Tracker")
    st.dataframe(tt)

def consolidation(df_filtered,vfd):
    '''
        Function to display the consolidation of request and video data.
        Calculates various statistics such as total requests, errors, videos, completed videos, pending videos, and videos with errors.
        Generates pie charts to visualize data distribution by different categories.
    '''
    st.header("Consolidation")
    total_requests = df_filtered.shape[0]
    total_requests_error = df_filtered[df_filtered["Diference"] > 0].shape[0]
    total_videos = vfd.shape[0]
    videos_completed = vfd[vfd["status"] =="completed"].shape[0]
    videos_pending = vfd[(
        vfd["status"] == "pending") & (vfd["file"].str.contains("1971", na=False))
    ].shape[0]
    error_statuses = ["Less than 100.0 KiB", "convFail", "Less than 50.0 KiB"]
    videos_error = vfd[
        vfd["status"].isin(error_statuses) | vfd["file"].str.contains("1971", na=False)
    ].shape[0]
    data = {
        'Total Request':[total_requests],
        'Total Request Error':[total_requests_error],
        'Total Videos':[total_videos],
        'Videos Completed': [videos_completed],
        'Videos Pending': [videos_pending],
        'Videos Error': [videos_error]
    }
    st.dataframe(data)
    col4 , col5 , col6 = st.columns(3)
    df_received = df_filtered["received"].sum()
    df_uploaded = df_filtered["uploaded"].sum()
    df_filtered_source_offline = df_filtered[df_filtered["source"] == "API_OFFLINE"].shape[0]
    df_filtered_source_online = df_filtered[df_filtered["source"] == "API"].shape[0]
    df_filtered_source_push = df_filtered[df_filtered["source"] == "Vehicle"].shape[0]
    labels = ["Received", "Uploaded"]
    colors_total = ['#636EFA', '#EF553B']
    values_total = [df_received,df_uploaded]
    Number_request_total = px.pie(df_filtered,names=labels,color_discrete_sequence=colors_total,
                              values=values_total,title="Received x Uploaded")
    labels_type = ["Offline", "Online","Vehicle"]
    colors_type = ['#636EFA', '#EF553B', '#FFFF00']
    values_type = [df_filtered_source_offline,df_filtered_source_online,df_filtered_source_push]
    Number_request_type = px.pie(df_filtered,names=labels_type,color_discrete_sequence=colors_type,
                             values=values_type,title="Request Videos By Type")
    labels_status = ["Error", "Pending","Completed"]
    colors_status = ['#EF553B', '#636EFA','#FFFF00']
    values_color = [videos_error,videos_pending,videos_completed]
    Number_videos_status = px.pie(df_filtered,names=labels_status,color_discrete_sequence=colors_status,
                              values=values_color,title="Videos by Status")
    col4.plotly_chart(Number_request_total,use_container_width=True)
    col5.plotly_chart(Number_request_type,use_container_width=True)
    col6.plotly_chart(Number_videos_status,use_container_width=True)

def handler():
    st.set_page_config(layout="wide")
    df = pd.read_csv("request_videos.CSV",sep=",")
    vfd = pd.read_csv("video_file_details.CSV",sep=",")
    tt = pd.read_csv("transaction_tracker.CSV",sep=",")

    st.sidebar.header("General Videos Filter")
    df,vfd,tt = filter_general(df,vfd,tt)

    st.sidebar.header("Request Videos Filter")
    df_filtered = filter_request_video(df)

    st.sidebar.header("Details Videos Filter")
    vfd = filter_details(vfd)

    # Information by Resquest_Videos
    request_videos(df_filtered)

    # Information by Video_File_Details
    video_file_details(vfd)

    # transaction tracker
    transaction_tracker(tt)

    # consolidation the data in end of the system
    consolidation(df_filtered,vfd)

handler()
