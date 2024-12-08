import pandas as pd
import numpy as np
import polars as pl
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import importlib

from src.utils import keywords
from src.utils import analysis_tools

#adding num_comments to the metadata dataframe
num_comments = pl.read_csv('./data/num_comments.csv')
metadata = metadata.drop('num_comms_right')

#view counts in the previous metadata dataframe was found to have been saved wrongly as an int.
#we did not have time to fix this issue yet, but this is a dirty solution that allows for the rest of the code to work.
views = pl.read_csv(path_final_yt_metadata_feather)[['view_count','display_id']]
metadata = metadata.drop('view_count')
metadata = metadata.join(views, on='display_id')

#rename channel id columns to all have the same name
channels_df = channels_df.rename({'channel':'channel_id'})
timeseries_df = timeseries_df.rename({'channel':'channel_id'})

#----------------- Compute Public Response Metrics

#extract starting features from feather dataset
response_metrics = metadata.drop(['categories','channel_id','upload_date', 'duration','tags','description','title','crawl_date'])

#add a column for likes/dislikes ratio
response_metrics = response_metrics.with_columns((pl.col('like_count')/pl.col('dislike_count')).alias('Likes/Dislikes'))
response_metrics = response_metrics.drop(['like_count','dislike_count'])

#remove the entries with infinite like/dislike ratio, and set the NaNs to zero
print ('Number of entries before treating the Like/Dislike column:', len(response_metrics))
response_metrics = response_metrics.with_columns(pl.col('Likes/Dislikes').replace(np.NaN, 0))
response_metrics = response_metrics.filter(pl.col('Likes/Dislikes') != np.inf)
print ('Number of entries after treating the Like/Dislike column:', len(response_metrics))

# Number of entries before treating the Like/Dislike column: 2324376
# Number of entries after treating the Like/Dislike column: 1516647



# load a sample comments dataset
path_final_comments = 'data/filtered_youtube_comments_example.tsv'

df_comments = pl.read_csv(path_final_comments, separator=",", has_header=True)

replies_metrics = analysis_tools.comment_replies_metrics(df_comments)
response_metrics = response_metrics.join(replies_metrics, on="video_id", how="inner")
response_metrics

#------------------------------Compute Correlation between Video Features and Response Metrics

#join the features and metric dataframes together
features_and_metrics = vid_features.join(response_metrics, on='display_id')

corr_1 = plot_correlation_matrix_features_and_metrics(features_and_metrics,7)

