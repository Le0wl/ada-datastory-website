
## Introduction
Journalism is often seen as the 4th pillar of democracy. It serves as a watchdog for the government, and keeps the public informed about events happening around the world. A century ago journalism was being reported mainly through newspapers, but today it has mostly migrated to the digital world. This shift made news more accessible than ever for the public, and signicicantly lowered the barrier to entry for independant journalists. In this datastory we dive into YouTube as a news source, analyzing how US news channels report on major geopolitical events and natural disasters using data provided by the [Youniverse](https://github.com/epfl-dlab/YouNiverse) dataset. 

But why focus on YouTube? As the world's larget video-sharing platform and the [second most](https://en.wikipedia.org/wiki/List_of_most-visited_websites) often visited website in the world, YouTube is a major player in daily content with more than **5 billion** hours of video [uploaded](https://www.madpenguin.org/how-many-youtube-videos-are-uploaded-every-day/) daily. Among this sea of content, the channels under category `News & Politics` have the third most videos out of all 15 categories, bolstering the role of Youtube as a substantial vessel of information and news. In fact, a 2020 study found that [26%](https://www.pewresearch.org/journalism/2020/09/28/many-americans-get-news-on-youtube-where-news-organizations-and-independent-producers-thrive-side-by-side/) of US adults get their news from YouTube. This number has a lot of room to grow given that the category getting comparatively few views compared to the amout of uploaded videos. With this in mind, investigating YouTube as a news source by examining how channels report on different events and how the subsequent public engagement offers valuable insights into how modern media affects the spread of news. The findings could help governments, NGOs, and media outlets optimize their use of YouTube during emergencies to maximize outreach and public response.

The plot below illustrates the result from the Youniverse Paper that inspired this analysis. News and politics is the third most uploaded video category with 12% of all uploaded videos, but when it comes to views, the currency of YouTube, News lacks far behind the rest with a meager 1% of total views. 
<iframe src="assets/plots/intro_pie.html" width="800" height="600" style="border:none;"></iframe>

## Research Questions

- How does the reporting of events by US news channels change with respect to the type of event as well as its location?
- How is the public’s response to an event affected by its nature, location, and video format through which it is presented?
- How does one make an effective news video to ellicit specific reactions and levels of interaction from the public?


# Methodology

### Dataset and preprocessing

The Youniverse dataset contains information about ~**73 million** of videos from more than **137'000** different channels. In addition there is metadata for over **8.6 billion** of comments. To get the videos we are interested in, we will filter the dataset in four steps.
1. We filter the dataset for videos from channels that are tagged with the category `News & Politics`.
2. We further filter for relevant channels by only considering the ones that have a high activity. The reason behind this is that we want to look into news _updates_ and thus channels posting sparsly are not interesting for use. We therefore set a minimum threshold of 4 videos per day.
  
By scrolling through the list of channels you might have noticed two things. First, the majority of the channels sound like legit news channels, but secondly there are some channels which do not seem to be English speaking. Even though the Youniverse dataset is supposed to only contain English speaking channels, especially Hindi and Arabic speaking channels were still present.

3. We filter for English-speaking US-based channels.

To fix this problem we used the [chatGPT-4o mini](https://openai.com/api/) to detect the language of a small sample of videos and filtered out all non-English channels. Further we used the [Youtube API](https://developers.google.com/youtube/v3/docs/channels/list) to get the country of the channel. We then only kept the channels that are from the US to get more comparable results.
After all this filtering process we end up with _149_ channels, _2.5 million_ videos and _xxx million_ of comments.

4. Then we get the relevant videos for our analysis by filtering for specific keywords related to each individual event.
   
To flag the related videos for each event, we looked for keywords in the titles and description of each video for any potential match. We define keywords and combinations of keywords that, if raise a match in either the title or description of the video, flag the video as relavant. For every event we define a list of lists, where each sublist has one or more keywords as strings. For a video to be flagged, at least one sublist has to match all its terms to the title or description. Finally we filter the results using upload time, where we only consider the time frame during which the specific event was occurring and still relevant.

Our goal is not only to study the spread of news, but to also examine how it is affected by the location of the event in question as well as its type. For this purpose, we consider three general regions to compare: the US, Europe, and Asia. As for the event type, we settled on environmental disasters and geopolitical conflicts with a focus on armed clashes. For each category, we chose the largest and most impactful events to maximize the number of datapoints and have the most  accurate representation we could obtain. We flagged relavant videos for each event by searching for keywords in the titles and descriptions. We also added a second layer of filtering using the videos upload dates, where we only consider the time frame during which the specific event was occurring and still relevant.


<iframe src="assets/plots/channels_activity_histogram.html" width="100%" height="400" style="border:none;"></iframe>
Here we can see our average activity cutoff on the distribution of news. The table of the righthand side makes it possible to have a look at the channels and their mean activity.
<iframe src="assets/plots/channel_filtering_steps.html" width="100%" height="400" style="border:none;"></iframe>
The plot above illustrades our pipepline for filtering the channesl in it's different steps. Howering above the plot gives some additional details. 
<iframe src="assets/plots/event_filtering_sankey.html" width="100%" height="600" style="border:none;"></iframe>

This plot illustrates the events that were chosen for this analysis. With the band thickness corresponding to the amount of videos found for each event.

<iframe src="assets\plots\time_series.html" width="100%" height="600" style="border:none;"></iframe>
Here we show the spike in videos connected to each event that was chosen for this analysis.

### Characteristics of videos

We define several video metrics that will be used to attempt to predict the audience's response. We consider factors that can be controlled by the video creator and that ideally can be optimized to maximize outreach. For every video, we compute and store: 

- video duration
- type of video (on ground footage or not). 
- frequency of uploads of the channel at time of video upload
- capitalization ratio of title
- appearance of specific keywords in the title: "breaking" and "update"
- Subjectivity score

The video duration was taken directly from the YouNiverse dataset. The type of video reflects if it shows ground footage or not, and the filtering is done based on wether or not the word "footage" appears in the title. The frequeny of video uploads describles the average daily upload frequency of the specific channel in the 2 weeks surrounding the upload of that specific video. The video title are offer us a few metrics. The caplitalization of the title is the ratio of upper case letters in the title. The title is also used to sarch for common keywords, mainly "breaking" and "update". Finally we generate a subjectivity score for each title using OpenAI's API using the following promt:

_"your task is to evaluate the subjectivity of news video titles and give each one a score from 0 neutral to 1 highly subjective. The topic does not matter but the phrasing of the reporting. As an example "Switzerland obliterates all other countries in quality of life" would be more subjective than "Switzerland exceeds other countries in quality of life". Only return the score"_

It is worth noting that subjectivity assessment is the most meaningful for geopolitical events, where personal agendas and political views might impact the reporting and the phrasing of video titles. For environmental events, this concept is not as potent or relavant, but will be assessed nontheless. 
With that being said, this approach to estimating subjectivity might not be very accurate and reliable, as it’s heavily dependent on the LLM used as well as the prompting. For that reason, the subjectivity score that we used should be interpreted with caution, however it might still reveal interesting insights, and could be further refined with a more robust model or prompt. 

Looking for repeating patterns, we visualize the most common words in the titles via the wordclouds below, separated by region and event type. 

<iframe src="assets/plots/wordclouds.html" width="100%" height="600" style="border:none;"></iframe>
This plot illustrates the most common words and phrased in the titles of the videos. The type of event and region can be selected, it shows what events are dominant within a category and the kind of langues used when discribing the event.

<iframe src="assets\plots\plot_video_metrics_event_region.html" width="100%" height="600" style="border:none;"></iframe>
Here we can see the distribution of video metrics for both environmental and geopolitical events grouped by region. 
<iframe src="assets\plots\keywords_by_region.png" width="100%" height="600" style="border:none; display: inline-block;"></iframe>
These pie charts show how many videos contain the keywords: breaking, update, and footage in the title based on the event region.

<iframe src="assets\plots\plot_video_metrics_event_type.html" width="100%" height="600" style="border:none;"></iframe>
Here we can see the distribution of video metrics for regions grouped by type of event. 

<iframe src="assets\plots\keywords_by_event.png" width="100%" height="600" style="border:none;"></iframe>

These pie charts show how many videos contain the keywords: breaking, update, and footage in the title based on the event type.

We can look at the difference in distributions of these metrics based on location and event type. or the US and Asia, subjectivity seems to be on average significantly higher for geopolitical events, whereas we don't see a massive difference in European events. Video duration seems to be longer for geopolitical events accross the board, potentially reflecting the general nature of reporting for such events where some analysis and discussion might typically follow the news update, providing more context and insights into the situation. Finally, in geopolitics, US-related events present higher subjectivity than Europe and Asia, as for environmental ones, Europe presents the highest subjectivity in reporting. 


### Public engagement

We now need metrics to quantify and describe the response of the public to videos. To do so, and after considering numerous options, we landed on the following four:

- views
- (likes - dislikes) / views
- number of comments / views
- average replies per comment
</span>

The choice of the first metric is quite straightforward. The second metric however is slightly more intricate. We interpret a like as a general desire of the user to see more of the same or similar content, and a dislike as a desire not to. Taking the difference gives us the net general interest of the users in this content. Given that likes and dislikes grow with views, we normalize this difference by view count. For the same reason, we normalize the number of comments by views to obtain the third metric.
This enables us to assess the extent to which a particular video entices people to discuss the videos' content in the comments. The comments/views ratio reflects how effectively a video captures public attention and prompts responses. If viewers are commenting frequently, the content likely resonates with concerns or prompts urgent reactions. By maximizing comments/views, NGOs and governments can drive awareness campaigns, ensuring key messages are reaching emotionally engaged audiences who are likely to spread critical information. Similarly, the last metric aims at capturing the degree of deeper discussion, debates and interactions taking place between the users. Maximizing replies per comment could create discussion hubs where people share resources, housing offers, or real-time situation updates, fostering a decentralized aid network. If an NGO posts a video about flood relief efforts and maximizes the comments/views ratio, more people will be exposed to the urgency of the situation, possibly prompting donations or volunteer sign-ups. Encouraging replies per comment fosters conversations where users can challenge misinformation, share verified updates, and provide corrections. By actively participating in these discussions, pinning accurate comments, and promoting trusted sources, organizations can create an interactive space where accurate information gains visibility, helping to reduce the spread of false or misleading content. In addition, high engagement indicates heightened public interest or concern, allowing governments and NGOs to assess whether crisis-related videos are raising awareness effectively.


<iframe src="assets\plots\plot_video_metrics_response_region.html" width="100%" height="600" style="border:none;"></iframe>
Here we can see the distribution of public response metrics for both environmental and geopolitical events grouped by region. 
<iframe src="assets\plots\plot_video_metrics_response_event_type.html" width="100%" height="600" style="border:none;"></iframe>
Here we can see the distribution of public response metrics for regions grouped by type of event. 


These metrics are all correlated to views because in order to interact with the video one has to click on it which qualifies as a view. Therefore in order to have more meaningfull data these metrics were normalized by the views of the video.

## Results and Analysis 

Having defined our video features and response metrics, we were now ready to relate them together. Our first simple approach was to calculate the pearsonr correlation coefficient between these variables. The PearsonR coefficient is an indicator of linear correlation, and therefore can reveal such linear relationships between our variables. We also computed the p-value corresponding to the null hypothesis that a random sample would give an equally strong correlation.

Next, we ploted the correlation between the features and metrics in order to find a way to link them together. We grouped them differently in order to observe the difference between events, event types, regions. The plots below show the results of the correlations along with p-values to indicate how significant the results are (note that for entries where the variance of the sample was zero, we mapped the correlation coefficient to zero, and the p-value to 1).

<iframe src="assets\plots\correlation_matrix_event_types.html" width="100%" height="600" style="border:none;"></iframe>
This is the correlation matrix between video features and response metrics for the videos grouped by event type.

<iframe src="assets\plots\correlation_matrix_events.html" width="100%" height="600" style="border:none;"></iframe>
This is the correlation matrix between video features and response metrics for each individual event.

<iframe src="assets\plots\correlation_matrix_regions.html" width="100%" height="600" style="border:none;"></iframe>
This is the correlation matrix between video features and response metrics for the videos grouped by region.

The distribution of the some of these metrics, mainly the categorical ones, as well as the number of videos per event category, are noticeably unbalanced, which may fail to capture the true underlying relationships, explaining some high p values and uncertainties in our results later on.
For the linear regression below, we standardize the continuous variables, i.e. the subjectivity, duration, channel activity, capitalization ratio. Statistical significance is considered for p values lower than 0.05. 

<iframe src="assets\plots\linear_regression_plot.html" width="100%" height="1000" style="border:none;"></iframe>


As you can see, all R2 values are hilariously low. However, this is okay because we are not trying to fully capture the entire distribution and variance of the response metrics. We only are looking for quantifying the effect of the video features on said metrics.

**View count**
We notice that all three categorical variables have high p values and uncertainties, so we cannot draw a meaningful relationship to the view count. Subjectivity also displays high p values. Duration, channel activity and capitalization ratio are all statistically significant for environmental events, unlike geopolitical ones where duration doesn’t seem to be significant. The highest coefficient in absolute value for both event types is being attributed to channel activity, followed by capitalization ratio, then duration. However channel activity is positively correlated with the view count for geopolitical events but negatively for environmental. Capitalization ratio has a positive correlation in both categories, and could be simply explained by plain old click baiting with all caps titles. 

**(Likes - dislikes)/views**
Duration, channel activity, and capitalization ratio are all statistically significant in their relation to the likes-dislikes metric for both event categories. Subjectivity and _breaking_ are only statistically significant for environmental events. _Update_ is only significant for geopolitical events, and is_footage is significant for neither types. The features with the most effect on the metric are _breaking_ and _update_ , followed by activity and capitalization ratio. The interpretation of this metric is tricker than the others, we will nonetheless attempt to explain the observation. A high coefficient for _breaking_, which is typically used for the first reporting of a natural disaster, likely includes the first “shocking” updates, which entices people to react and like the video in order to see more about it. On the other hand, _update_ has a negative coefficient for geopolitical events, potentially showing that people aren’t as interested in seeing updates of the same story compared to novel news and stories. 

**Replies per comment**
Looking at the replies per comment, we notice that capitalization ratio and channel activity are two statistically significant characteristics that affect replies per comment. For capitalization ratios, we see a positive coefficient with both event types. One possible explanation could be that videos with higher capitalization ratios can be ones with attention-grabbing titles, attracting more views, and thus more responses to the videos. This also is linked with the correlation of capitalization to view count.
We notice that the metric of channel activity has an inverse effect on replies per comment between Geopolitical events and environmental crises. Geopolitical events show a positive correlation for replies per comment, while environmental ones have a negative correlation. However, natural disasters may have fewer dynamic updates, so after receiving the first news of an event, viewers may not expect to see many new updates, so people may not be stirred to provide feedback. Another possible explanation for the inverse relation could be attention fatigue. The news of a natural disaster does not significantly change in nature with time from its first breaking news, and people might already anticipate the coming news. Hence, more videos from the channel covering the topic would be less likely to be viewed. 
Keyword update has a negative coefficient in geopolitical events. This is somewhat expected, since there is usually less to talk about and discuss in a story that has been going on for a while as opposed to a breaking one. Hence regular updates result in less discussion among the users.
We also see that videos with the keyword footage provide a significant positive correlation, with an uncertainty that puts it still in the positive domain. This could be attributed to the content of the videos. Geopolitical events are often ongoing with the potential for large shifts in the situation, such as losses in battles, and political decisions being made. Thus, new videos could spark users’ discussions in comments as they digest the ramifications of the updates. 
Along the same lines with impactful keywords, we see that the word “breaking” has a statistically significant positive correlation with the replies per comment. This could be because disasters are reported with “Breaking” in the title, which could be the initial reporting done. This initial reporting could evoke discussions about the state of the situation and the communication of people who may be in the wake of the disaster and those who are outside, who may be interested in further investigating it.

**Comments per views**
Capitalization ratio is statistically significant for both event types. For environmental, duration, channel activity and _breaking_ are also significant, and for geopolitical, only footage and _update_ are also significant. For geopolitical, once again footage has a positive coefficient with the metric, showing more engagement and discussions when the video has actual footage of the event reported on. And once again, keyword update has a negative coefficient, showing that old stories engage less than public and spark less discussions, as expected. As for environmental, keyword breaking has the highest impact on the metric, where breaking news result in a lot of comments per views. Similarly to the other metrics, channel activity has a high negative coefficient, which is inline with the general trends that recurrent news results in less engagement from the public.

## Conclusion
In this work we studied the spread of news in Youtube by examining the response of users to different video attributes for different event types and locations. The study was conducted on US-based, english speaking, high upload frequency channels. The assessment of the userbase's reaction is quantified through a set of four different metrics that aim at describing different types of response. Through regression, we observe two major trends. First, based on the features "channel activity", "_update_" and "_breaking_", we can notice that, in general, recurrent news, or news about an "old" story, gathers less engagement from and discusssion among the public compared to breaking ones and new stories. The second trend is based on the feature "is_footage", where videos consisting of footage about the reported event induces noticably more discussions and back and forth among the viewers.

Both these conclusions can be used by governments, NGO's and other public bodies to maximize the outreach and spread of information during crises.
