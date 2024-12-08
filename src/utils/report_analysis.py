import pandas as pd
import numpy as np
import polars as pl
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import importlib

from src.utils import keywords
from src.utils import analysis_tools

#--------------------- VIDEOS PER EVENT -----------------------------------------

# load data in such a way to avoid errors
metadata = pl.read_csv(path_final_yt_metadata,  schema_overrides={
                                "dislike_count": pl.Float64,
                                "like_count": pl.Float64},
                                ignore_errors = True)

# counting erroneous like/dislike and date entries
keywords.summarize_outliers(metadata)



# Total number of videos: 2,548,064
# Date Outlier Count: 164,271
# Like/Dislike Outlier Count (null elements): 223,686

# removing rows there the like or dislike entry is null, or where the date entry is erroneous (like "17")
metadata = keywords.filtering_bad_rows(metadata)

# Original metadata shape: (2,548,064, 12)
# New metadata shape: (2,324,376, 12)

keywords.summarize_outliers(metadata)

# Total number of videos: 2,324,376
# Date Outlier Count: 0
# Like/Dislike Outlier Count (null elements): 0

## removing the hour time from the upload_date since it's always 00:00:00
metadata = keywords.remove_hour(metadata)

# plot the evolution of upload frequency for each event

index = 11       # 0-11, chooses event to plot. List is found in keywords.py
keywords.plot_update_frequ(index, metadata, all_plots = True, grouping_mode = "daily")
# all_plots = True to plot for all the events, disregards chosen index. Else plot for the even corresponding to chosen index
# grouping_mode: "daily", "weekly", "monthly"

# Event: 2016 US elections
# Related videos found: 256,198
# ------------
# Event: 2019 indian elections
# Related videos found: 232,904
# ------------
# Event: 2019 EU elections
# Related videos found: 642
# ------------
# Event: Venezuela Hyperinflation in 2018
# Related videos found: 3,661
# ------------
# Event: US-China trade war 2018
# Related videos found: 156,707
# ------------
# Event: Greece Economic Crisis 2015
# Related videos found: 3,252
# ------------
# Event: Hurricane Harvey (2017)
# Related videos found: 2,573
# ------------
# Event: Sulawesi Earthquake and Tsunami (2018)
# Related videos found: 76
# ------------
# Event: European Heatwaves (2019)
# Related videos found: 314
# ------------
# Event: 2017 battle of Raqqa (by US-led coalition)
# Related videos found: 12,812
# ------------
# Event: 2019 India-Pakistan Conflict (Pulwama and Balakot Airstrikes)
# Related videos found: 118
# ------------
# Event: 2015-2017 Rise in ISIS Attacks in Europe
# Related videos found: 1,153
# ------------

#select the first features from the video metadata
#channel_id and display_id are for merging other dataframes
from src.utils.analysis_tools import *
timeseries_df = pl.read_csv(path_final_timeseries)
vid_features = metadata[['display_id','channel_id','duration']]

#compute general statistics on the timeseries dataframe and add join them together
counts, means, stds, meds  = get_general_ch_statistics(timeseries_df,['delta_videos','subs'])
joined = counts.join(means, on='channel_id').rename({'delta_videos':'mean_delta_videos','subs':'mean_subs' })
joined = joined.join(stds, on='channel_id').rename({'delta_videos':'std_delta_videos','subs':'std_subs' })
joined = joined.join(meds, on='channel_id').rename({'delta_videos':'median_delta_videos','subs':'median_subs' })

#merge the timeseries statistics with the video features daframe
vid_features = vid_features.join(joined, on='channel_id')
vid_features = vid_features.drop('channel_id')

#compute the capitalization ratio of the title for each video (number of capital letters/number of lowercase letters) and add it to the dataframe
titles = metadata[['display_id','title']]
ratio = cap_ratio(titles, 'title')
ratio = ratio.drop('title')
vid_features = vid_features.join(ratio, on='display_id')

#plotting numerical distributions
analysis_tools.plot_video_stat(metadata, 'view_count')
analysis_tools.plot_video_stat(metadata, 'duration')
analysis_tools.plot_video_stat(metadata, 'like_count')
analysis_tools.plot_video_stat(metadata, 'dislike_count')

#plotting common words
analysis_tools.plot_most_common_tags(metadata, 30)
analysis_tools.plot_most_common_words(metadata, 'title', 30)
analysis_tools.plot_most_common_words(metadata, 'description', 30)

#plotting the length of titles and discriptions
analysis_tools.plot_text_len_words(metadata, 'title')
analysis_tools.plot_text_len_words(metadata, 'description')

get_general_vid_statistics(metadata)

corr = plot_correlation_matrix(vid_features)

