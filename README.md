# Description
Analysing the health of system using panda,plotly and streamlit

### Install Process
1 - update the system 
    sudo apt update && sudo apt upgrade
2 - install python pip 
    sudo apt install python3 python3-pip
3 - Install pandas , streamlit and plotly
    pip3 install pandas streamlit plotly
4 - execute the code
    streamlit run dashboards.py

### Original Query Video Request
SELECT 
    Cast(coalesce(RV.request_id,"NULL") as char) as request, 
    Cast(coalesce(RV.account_id,"NULL") as char) as account, 
    Cast(coalesce(RV.dvr_id,"NULL") as char) as dvr,
    Cast(coalesce(RV.video_request_starttime,"NULL") as char) as start_time, 
    Cast(coalesce(RV.video_request_endtime,"NULL") as char) as end_time,
    Cast(coalesce(RV.requested_source,"NULL") as char) as source,
    Cast(coalesce(RV.filenames_received_from_device,"NULL") as char) as received, 
    Cast(coalesce(RV.videos_uploaded,"NULL") as char) as uploaded,
    Cast(coalesce(RV.timestamp,"NULL") as char) as timestamp,
    Cast(coalesce(IF(RV.retry_meta = "" or RV.retry_meta is null,0,1)) as char) as is_retry,
    COUNT(VFD.request_id) AS videos_details
FROM 
    Prod_Diomedes_schema.Request_Videos RV
LEFT JOIN 
    Video_File_Details VFD ON RV.request_id = VFD.request_id
WHERE 
    RV.timestamp >= DATE_FORMAT(CURDATE(),'%Y-%m-01 00:00:00') 
    AND RV.timestamp <= LAST_DAY(CURDATE()) + INTERVAL 23 HOUR + INTERVAL 59 MINUTE + INTERVAL 59 SECOND 
    AND RV.filenames_received_from_device NOT IN ('Device unavailable','Device Disabled') 
    AND RV.account_id IS NOT NULL 
    AND RV.vin_number IS NOT NULL
GROUP BY 
    RV.request_id
ORDER BY 
    RV.timestamp DESC
LIMIT 1000;

### Original Query Video File Details
select 
	Cast(coalesce(VFD.request_id,"NULL") as char) as request , 
    Cast(coalesce(VFD.dvr_id,"NULL") as char) as dvr,
    Cast(coalesce(VFD.file_name,"NULL") as char) as file,
	Cast(coalesce(VFD.upload_status,"NULL") as char) as status,
    Cast(coalesce(VFD.timestamp ,"NULL") as char) as timestamp,
    Cast(coalesce(VFD.video_upload_timestamp,"NULL") as char) as upload_timestamp,
	Cast(coalesce(ROUND(VFD.original_file_size/1024/1024),0) as char) as original_size , 
    Cast(coalesce(ROUND(VFD.converted_file_size/1024/1024),0) as char) as converted_size , 
	Cast(coalesce(VFD.origin_video_format,"NULL") as char) as format
FROM Video_File_Details VFD
INNER JOIN 
	Request_Videos RV on VFD.request_id = RV.request_id
where RV.timestamp >= DATE_FORMAT(CURDATE(),'%Y-%m-01 00:00:00') 
	AND RV.timestamp <= LAST_DAY(CURDATE()) + INTERVAL 23 HOUR + INTERVAL 59 MINUTE + INTERVAL 59 SECOND and VFD.request_id = RV.request_id
ORDER BY 
    VFD.timestamp DESC
limit 100000;

### Original Query Transaction Tracker
SELECT 
	Cast(coalesce(TT.request_id,"NULL") as char) as request ,
    Cast(coalesce(RV.dvr_id,"NULL") as char) as dvr ,
    Cast(coalesce(TT.timestamp ,"NULL") as char) as timestamp,
    Cast(coalesce(TT.transaction ,"NULL") as char) as trasaction,
    Cast(coalesce(TT.topic_name ,"NULL") as char) as topic,
    Cast(coalesce(replace(TT.data,',',';') ,"NULL") as char) as data
FROM Transaction_Tracker TT
INNER JOIN 
	Request_Videos RV on TT.request_id = RV.request_id
WHERE RV.timestamp >= DATE_FORMAT(CURDATE(),'%Y-%m-01 00:00:00') 
	AND RV.timestamp <= LAST_DAY(CURDATE()) + INTERVAL 23 HOUR + INTERVAL 59 MINUTE + INTERVAL 59 SECOND and TT.request_id = RV.request_id
ORDER BY 
    TT.timestamp DESC
limit 1000000;