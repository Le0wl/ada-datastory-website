
## Introduction
Journalism is often seen as the 4th pillar of democracy. It serves as a watchdog for the government, and keeps the public informed about events happening around the world. A century ago journalism was being reported mainly through newspapers, but today it has mostly migrated to the digital world. This shift made news more accessible than ever for the public, and signicicantly lowered the barrier to entry for independant journalists. In this datastory we dive into YouTube as a news source, analyzing how US new channels report on major geopolitical events and natural disaster using data provided by the [Youniverse](https://github.com/epfl-dlab/YouNiverse) dataset. 

But why focus on YouTube? As the world's larget video-sharing platform and the [second most](https://en.wikipedia.org/wiki/List_of_most-visited_websites) often visited website in the world, YouTube is a major player in daily content with more than **5 billion** hours of video content [uploaded](https://www.madpenguin.org/how-many-youtube-videos-are-uploaded-every-day/) daily. Among this sea of content, the channels under category `News & Politics` have the most videos out of all categories, bolstering Youtube as a substantial vessel of information and news. In fact, a 2020 study found that [26%](https://www.pewresearch.org/journalism/2020/09/28/many-americans-get-news-on-youtube-where-news-organizations-and-independent-producers-thrive-side-by-side/) of US adults get their news from YouTube. This number has a lot of room to grow with the category getting comparatively few views compared to the amout of uploaded videos. With this mind studying YouTube as a news source, how channels report on about specific events and how the public engages with its content, offers valuable insights into how modern media affects the spread of news. The findings could help governments, NGOs, and media outlets optimize their use of YouTube during emergencies to maximize outreach and public response.

TALK ABBOUT TREND

<iframe src="assets/plots/videos_by_cat.html" width="800" height="600" style="border:none;"></iframe>

## Research Questions

- How does the reporting of events by US news channels change with respect to the type of event as well as its location?
- How is the public’s response to an event affected by its nature, location, and video format through which it is presented?
- How does one make an effective news video to ellicit specific reactions and levels of interaction from the public?


## Analysis and Findings

### What data we are looking at

The Youniverse dataset contains information about ~**73 million** of videos from more than **137'000** different channels. In addition there is metadata for over **8.6 billion** of comments. To get the videos we are interested in, we will filter the dataset in four steps.
1. We filter the dataset for videos that are tagged with the category `News & Politics`.
2. We further filter for relevant channels by only considering channels that have a high activity. The reasoning behind this idea is that we want to look into news _updates_ and thus channels posting less than 4 videos per day are not interesting for us.

By scrolling through the list of channels you might have noticed two things. First, the majority of the channels sound like legit news channels, but secondly there are some channels which do not seem to be English speaking. Even though the Youniverse dataset is supposed to only contain English speaking channels, especially Hindi and Arabic speaking channels were still present.

3. We filter for English-speaking US-based channles.

To fix this problem we used the [chatGPT-4o mini](https://openai.com/api/) to detect the language of a small sample of videos and filtered out all non-English channels. Further we used the [Youtube API](https://developers.google.com/youtube/v3/docs/channels/list) to get the country of the channel. We then only kept the channels that are from the US to get more comparable results.
After all this filter process we end up with _149_ channels, _2.5 million_ videos and _xxx million_ of comments.

4. Then we get the relevant videos for our analysis by filtering for specific keywords related to each individual event.

The choice of specific events to consider was a difficult one. The original plan was to consider the following event categories: political events, natural disasters, geopolitcal conflicts and economic crisis that happen in the US, Asia and Europe. This was then narrowed down further in order to include more events per category because we want it to representative of the event category rather than the specific events. The categories chosen are geopoitical conflicts and natural disasters in the US, Asia and Europe because in those categoriees it is easier to isolate single events. 

We filtered for videos that concern a certain event using different combinations of keywords that have to appear in the title of the discription of the video in question and within a certain timeframe of the event. 

plot with iframe without borders:

<iframe src="assets/plots/channels_activity_histogram.html" width="100%" height="400" style="border:none;"></iframe>


<iframe src="assets/plots/channel_filtering_steps.html" width="60%" height="400" style="border:none;"></iframe>

<span style="color: red;">Explanation on how we selected the events. Explain breakdowns of different events and on which ones we are focusing. </span>

<iframe src="assets/plots/event_filtering_sankey.html" width="100%" height="600" style="border:none;"></iframe>


<span style="color: red;">Plots about the events and a first dumb analysis. Interactive plot with times series (upload) of each events, way to visualize keywords</span>

### Characteristics of videos
<span style="color: red;">
Explain what characterizes a video, i.e. the variables the news channel can influence:

- video duration
- type of video (live footage/analysis)
- frequency of video uploads concerning the event at time of upload
- capitalization of title
- appearance of specific keywords (breaking news…)
- Subjectivity score</span>

The video duration was taken directly from the YouNiverse dataset. The type of video trying to identify live footage as opposed to studio recording, the distinction is based on weither the key word "footage" appears in the title. This keyword had the best performance compared to "live" that tended to also flag live streams and the verb live (as in I live here). The frequeny of video video uploads describles the average dayly upload in the 2 weeks surrounding the upload of that specific video. 
The video title are offer us a few metrics. The caplitalization of the title is the ratio of upper case to lower case letters in the title, then we look at recurring keywords in the titles to see if they affect response and for a more quantitative measure there is a subjectivity score that has been obtained using OpenAI's API using the following promt:

"your task is to evaluate the subjectivity of news video titles and give each one a score from 0 neutral to 1 highly subjective. The topic does not matter but the phrasing of the reporting. as an example "Switzerland obliterates all other countries in quality of life" would be more subjective than "Switzerland exceeds other countries in quality of life". only return the score"

To look at the titles for the different events the most common words and experesstions are ploted in the wordclouds below:
<iframe src="assets/plots/wordclouds.html" width="100%" height="600" style="border:none;"></iframe>

<iframe src="assets\plots\plot_video_metrics_event_region.html" width="100%" height="600" style="border:none;"></iframe>
<iframe src="assets\plots\plot_video_metrics_event_type.html" width="100%" height="600" style="border:none;"></iframe>

<span style="color: red;">Plot with statistics about each of those metrics where you can choose whether you want to group by region or event (or both?).</span>

<span style="color: red;">Pick metrics which show a difference in either region or event category for a specific metric and provide t-test of the difference. Draw some conclusion about your analysis.</span>

### Public engagement
<span style="color: red;">What we understand by public response. Why does it matter? (News spread, fake news, etc.)

Introduce our metrics for measuring the public response:

- views
- number of comments
- number of replies to comments
- ratio of like/dislike
</span>

These metrics were taken purely from the YouNiverse dataset and are conserning the news videos we chose to analyse above. 
[insert plot here showing off the responsemetrics]
<iframe src="assets\plots\plot_video_metrics_response_region.html" width="100%" height="600" style="border:none;"></iframe>
<iframe src="assets\plots\plot_video_metrics_response_event_type.html" width="100%" height="600" style="border:none;"></iframe>


These metrics are all correlated to views because in order to interact with the video one has to click on it which qualifies as a view. Therefore in order to have more meaningfull data these metrics were normalized by the views of the video.
[insert correlation plot form samuel here]
[insert normalized correlation plot form samuel here]





<span style="color: red;">Plot with statistics about each of those metrics where you can choose whether you want to group by region or event (or both?).</span>

<span style="color: red;">Again perform t-test for metrics which do show a difference and draw conclusion</span>

