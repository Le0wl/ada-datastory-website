---
layout: page
cover-img: /assets/img/breaking.png
---

The old notebook minus the plots
## Table of Contents
* [1 Preprocessing and data filtering](#filter_data)
    * [1.1 Filter for Category 'News & Politics'](#filter_data-category)
    * [1.2 Filter for Active Channels](#filter_data-active)
    * [1.3 Get country of channel](#filter_data-country)
    * [1.4 Get if channel is english-speaking](#filter_data-english)
    * [1.5 Filter for language and country and save final data](#filter_data-save)
        * [1.5.1 Filtering relevant comments](#filter_data-comments)
* [2 How US News report on different events](#status_quo)
    * [2.1 Get relevant videos per event](#status_quo-videos_per_event)
    * [2.2 Extract video and channel features](#status_quo-features)
        * [2.2.1 Intial distribution of video metrics](#status_quo-features-distributions)
    * [2.3 Results and Comparison between Events](#status_quo-results)
* [3 How does the public response to events](#public_response)
    * [3.1 Compute Public Response Metrics](#public_response-metrics)
    * [3.2 Compute Correlation between Video Features and Response Metrics](#public_response-correlation)
    * [3.3 Compute F- and T-tests](#public_response-ttest)
* [4 Conclusion](#conclusion)

## 1 Preprocessing and data filtering  <a class="anchor" id="filter_data"></a>

### 1.1 Filter for Category 'News & Politics' <a class="anchor" id="filter_data-category"></a>
The first step for filtering our data is to select only the channels which have been categorized as 'News & Politics'. This is done using `df_channels_en.tsv`.

### 1.2 Filter for Active Channels <a class="anchor" id="filter_data-active"></a>
As we only want to focus on channels providing News Updates, we will compute the average activity of channel. This is defined as the average number of videos uploaded over two weeks and computed using the `df_timeseries_en.tsv`. We assumed that channels providing news *updates* will upload several videos per day. A manual review of some channels verified this assumption. To set a threshold we will plot the distribution to see if there is a clear separation between active and inactive channels. 

#### Test activity filter
Here we plot the distribution of the average number of videos uploaded over two weeks for all channels. 
![activity plot](assets\plots\channel_activity.png)
**Conclusion**: We cannot identify clusters of active and non-active channels. That's why we set the cutoff threshold manually choosing a reasonable activity as threshold as 4 videos per day. This was verified manually by checking channels above the threshold. They mainly correspond to the type of news channels we were looking for.
#### Filter channels by activity

#### Filter yt_metadata by channels obtained before
To reduce the size of the big datasets `yt_metadata_en.jsonl` and `yt_metadata_helper.feather` we will prefilter them using the channels we obtained before. This will reduce the size of the dataset and make it easier to work with in future.

### 1.3 Get country of channel <a class="anchor" id="filter_data-country"></a>
With the Youtube API we can query for the country information with the channel ID 

### 1.4 Get if channel is english-speaking with CHATGPT LLM API <a class="anchor" id="filter_data-english"></a>
Task: Use `filtered_yt_metadata.csv` and `high_activity_channels_with_country.csv` to filter for english videos

Since the youtube metadata dataset contains videos that are not from english speaking channels, we need to do further processing. We use the CHATGPT API to analyze 5 videos and descriptions and if any video is not classified as english, the channel is marked as non-english

### 1.5 Filter for language and country and save all the final dataframes <a class="anchor" id="filter_data-save"></a>
Now that we got all the information needed, we can filter all our dataframes and save them for future use. As a recall we are filtering for channels that are:
- categorized as 'News & Politics'
- active (more than 4 videos per day)
- english-speaking (predicted by CHATGPT API)
- from the US (fetched from the youtube API and completed manually)

#### 1.5.1 Filtering relevant comments <a class="anchor" id="filter_data-comments"></a> 
We want to filter out the comments related the videos in the df_final_yt_metadata. To do this, we initially tried using our personal PCs to filter out the youtube_comments.tsv.gz dataset, but found that it would take too long for the scope of the project. To address this, we use AWS resources for more computational resources. The code in the below 3 cells is running on Amazon Sagemaker and the dataset is stored in a S3 bucket.

## 2 How US News report on different events <a class="anchor" id="status_quo"></a>

### 2.1 Get relevant videos per event <a class="anchor" id="status_quo-videos_per_event"></a>
![plot of uploads per event](assets\plots\uploads_per_topic.png)
### 2.2 Extract video and channel features<a class="anchor" id="status_quo-features"></a>
![plot views](assets\plots\views.png)
![plot likes](assets\plots\likes.png)
![plot dislikes](assets\plots\dislikes.png)
![plot video length](assets\plots\duration.png)

![plot title word count](assets\plots\tiltle_words.png)
![plot most popular tilte words](assets\plots\title.png)

![plot discription word count](assets\plots\description_words.png)
![plot most popular discription words](assets\plots\description.png)

![plot most popular tags words](assets\plots\videotags.png)

#### 2.2.1 Initial distributions of video metrics <a class="anchor" id="status_quo-features-distributions"></a>
In this section we want to show the distributions of all available video metrics. These metrics will later be used to catergorize the videos and the user resopnse to them. The plots here below are show the overall distribution over the whole filtered dataset, they build the baseline we can compare the response to specific events against.

### 2.3 Results and Comparison between Events <a class="anchor" id="status_quo-results"></a>
Getting correlation between the video features and plotting them.

![correlation matirx of features](assets\plots\features_corr.png)

## 3 How does the public response to events <a class="anchor" id="public_response"></a>

### 3.1 Compute Public Response Metrics <a class="anchor" id="public_response-metrics"></a>
#### Replies to comments and number of comments

The number of comments per video is given in `final_num_comments.csv`, so no need to compute them. For average replies per comment per video, we can compute it using `final_yt_comments.csv`.

**Disclaimer**:
At this point of our project we have not yet filtered the comments for the videos we are interested in. Therefore we will only propose a pipeline for the computation of the metrics.

### 3.2 Compute Correlation between Video Features and Response Metrics <a class="anchor" id="public_response-correlation"></a>

### 3.3 Compute F- and T-tests <a class="anchor" id="public_response-ttest"></a>
After computing the correlation between the video features and the response variables, we can analyse the significance of the correlation with statistical tests. We have a pipeline designed and a few functions coded to perform this analysis.
We will implement those in order to determine which video features should be optimized in order to expect a better video performance in a given metric.

## 4 Conclusion <a class="anchor" id="conclusion"></a>
In this notebook, we filtered the channels, metadata and times-series by keeping the videos from US, English-speaking channels with the category of News and Politics, keeping only high activity channels. Filtering of the massive comments dataset from these channels will be done on AWS, and we will study the reporting of the different events, ultimate grouping them by event category and country of occurrence to draw meaningful patterns, and we will also study how different video formats, types, and other characteristics affect the response of the public in terms of virality as well as the breadth of discussions that are illicited in the comments. We were able to isolate the videos related to each event by writing a list of terms that are respectively relevant to said events (while minimizing overlapping with other events as to not flag irrelevant videos), and searching for them in the titles and descriptions.
