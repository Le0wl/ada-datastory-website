import pandas as pd
import numpy as np
import polars as pl
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import importlib

from src.utils import keywords
from src.utils import analysis_tools
from src.scripts import filters

path_df_channels_en = 'data/df_channels_en.tsv'
path_df_timeseries = 'data/df_timeseries_en.tsv'
path_yt_metadata_feather = 'data/yt_metadata_helper.feather'
path_yt_metadata_feather_filtered = 'data/filtered_yt_metadata_helper.feather.csv'

path_yt_metadata = 'data/yt_metadata_en.jsonl'
path_yt_metadata_filtered = 'data/filtered_yt_metadata.csv'

path_final_channels = 'data/final_channels.csv'
path_final_timeseries = 'data/final_timeseries.csv'
path_final_yt_metadata_feather = 'data/final_yt_metadata_helper.csv'
path_final_yt_metadata = 'data/final_yt_metadata.csv'


pl_df_f = pl.read_csv(path_df_channels_en, separator="\t")

filtered_df_ch = filters.filter_df(pl_df_f, column_name="category_cc", 
                                   value="News & Politics", cmpstr="==")

print(f"Number of channels in category 'News & Politics': {len(filtered_df_ch)}")

#------------------------------- FILTERING FOR ACTIVITY ---------------------------------------

df_timeseries = pl.read_csv(path_df_timeseries, separator="\t")

# filter timeseries for channels in category 'News & Politics'
filtered_df_timeseries = filters.filter_df_isin(df_timeseries, column_name="channel", 
                                                values=filtered_df_ch["channel"])
# compute the average activity for all channels
grouped_df = filtered_df_timeseries.group_by('channel').agg(pl.col('activity').mean().alias('mean_activity'))

mean_activities = grouped_df['mean_activity'].to_list()

# Plot histogram of the mean activity values
plt.hist(mean_activities, bins=100, edgecolor="black", alpha=0.7)
plt.xlabel('Mean Activity')
plt.ylabel('Frequency')
plt.title('Histogram of Mean Activity by Channel')
# plt.xscale("log")
plt.yscale("log")
plt.grid(True, which="both")
plt.show()

# merge with channels dataframe
filtered_df_ch = filtered_df_ch.join(grouped_df, on="channel", how="inner")

# 56 = 4 videos per day x 14 days
filtered_df_ch = filters.filter_df(filtered_df_ch, "mean_activity", 56, ">")

# filtered_df_ch.sort(by="mean_activity", descending=True).head(10)

print("Number of channels in category 'News & Politics' with more than 4 videos per",\
      f"day: {len(filtered_df_ch)}")


# Transform feather into csv to ease handling
df_vd_f = pd.read_feather(path_yt_metadata_feather)
# save to csv
df_vd_f.to_csv(path_yt_metadata_feather+".csv", sep="\t", index=False)

# filter yt_metadata_helper.feather.csv by highly active news channels
filters.df_filter_csv_batched(path_yt_metadata_feather+".csv", path_yt_metadata_feather_filtered,
                              column_name="channel_id", values=filtered_df_ch["channel"],
                              filter_method="is_in")

# Test if filtering worked by reading the previous saved file and printing the number of videos remaining
filtered_df_metadata_feather = pl.read_csv(path_yt_metadata_feather_filtered)
print("Number of videos from channels of interest (CoI): "\
      f"{len(filtered_df_metadata_feather)}")


# same process for yt_metadata_en.jsonl
# we will also transform this file into a csv to unify file formats
filters.df_filter_jsonl_batched(path_yt_metadata, path_yt_metadata_filtered, 
                                column_name="channel_id", 
                                values=filtered_df_ch["channel"],
                                sep="\t", batch_size=500)

#------------------------------- FILTERING FOR COUNTRY ---------------------------------------

high_activity_channels = filtered_df_ch.with_columns(
    pl.col("channel").map_elements(lambda channel_id:general_utils.get_channel_country(channel_id)).alias("Channel_country")
)

high_activity_channels.write_csv("data/high_activity_channels_with_country")
print(high_activity_channels.sample(10))

#------------------------------- FILTERING FOR ENGLISH ---------------------------------------

channels_df = pd.read_csv("data/high_activity_channels_with_country.csv") 
channel_ids = set(channels_df['channel'].unique())  
chunk_reader = pd.read_csv("data/filtered_yt_metadata.csv", chunksize=5000)

matching_videos = []
# dictionary to track how many videos are saved for each channel
channel_video_count = {channel_id: 0 for channel_id in channel_ids}

for chunk in chunk_reader:
    matching_rows = chunk[chunk['channel_id'].isin(channel_ids)]
    for channel_id, group in matching_rows.groupby('channel_id'):
        # if 5 videos are analyzed continue
        if channel_video_count[channel_id] >= 5:
            continue
        # get the first 5 videos for this channel, or fewer if there are less than 5
        first_5_videos = group.head(5 - channel_video_count[channel_id]) 
        channel_video_count[channel_id] += len(first_5_videos)
        matching_videos.append(first_5_videos)

final_df = pd.concat(matching_videos, ignore_index=True)
final_df.to_csv('data/matching_videos.csv', index=False)

## TESTING THE FUNCTION 
final_df = pd.read_csv("data/matching_videos.csv")
result = general_utils.check_channel_english(final_df, "UClMs26ViHFMy7MS897Alcxw")

high_activity_channels = high_activity_channels.with_columns(
    pl.col("channel").map_elements(lambda channel_id:general_utils.check_channel_english(final_df, channel_id)).alias("Is_English")
)

high_activity_channels.write_csv("data/high_activity_channels_country_and_english.csv")

filtered = pd.read_csv("data/high_activity_channels_country_and_english.csv")

english = filtered[filtered["Is_English"] == True]
print("English")
print(english["Channel_country"].value_counts())


df_final_channels = pl.read_csv("data/high_activity_channels_country_and_english.csv", separator=",")
df_final_channels = df_final_channels.filter((pl.col("Channel_country") == "US") & (pl.col("Is_English") == True))
df_final_channels = df_final_channels.rename({"Is_English": "is_english", "Channel_country": "channel_country"})

df_final_channels.write_csv(path_final_channels, include_header=True, separator=",")

# metadata feather
filters.df_filter_csv_batched(path_yt_metadata_feather_filtered, path_final_yt_metadata_feather,
                              column_name="channel_id", values=df_final_channels["channel"],
                              filter_method="is_in", sep_in="\t", sep_out=",")

# metadata
df_final_yt_metadata = pl.read_csv(path_yt_metadata_filtered, has_header=True, 
                                   separator="\t", infer_schema=False)
df_final_yt_metadata = filters.filter_df_isin(df_final_yt_metadata, "channel_id", df_final_channels["channel"])
df_final_yt_metadata.write_csv(path_final_yt_metadata, include_header=True, separator=",")

# timeseries
df_final_timeseries = pl.read_csv(path_df_timeseries, separator="\t", has_header=True)
df_final_timeseries = filters.filter_df_isin(df_final_timeseries, column_name="channel", 
                                                values=df_final_channels["channel"])
df_final_timeseries.write_csv(path_final_timeseries, include_header=True, separator=",")

print("Final Number of videos from channels of interest (CoI): "\
      f"{len(df_final_yt_metadata)}")

print("Final channels of interest (CoI): "\
      f"{len(df_final_channels)}")

#----------------------------- FILTERING COMMENTS ---------------------------------------

import boto3
import polars as pl
import pandas as pd
import s3fs
from urllib.parse import urlparse

# Define the S3 bucket name and any prefix you want to use
bucket_name = 'adaproject-lil0mohammedali'

# Initialize a session using Boto3
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

for obj in bucket.objects.filter():
    print(obj.key)

