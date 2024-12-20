
## Introduction
Journalism is often seen as the 4th pillar of democracy. It serves as a watchdog for the government, and keeps the public informed about events happening around the world. A century ago journalism was being reported mainly through newspapers, but today it has mostly migrated to the digital world. This shift made news more accessible than ever for the public, and signicicantly lowered the barrier to entry for independant journalists. In this datastory we dive into YouTube as a news source, analyzing how US news channels report on major geopolitical events and natural disasters using data provided by the [Youniverse](https://github.com/epfl-dlab/YouNiverse) dataset. 

But why focus on YouTube? As the world's larget video-sharing platform and the [second most](https://en.wikipedia.org/wiki/List_of_most-visited_websites) often visited website in the world, YouTube is a major player in daily content with more than **5 billion** hours of video [uploaded](https://www.madpenguin.org/how-many-youtube-videos-are-uploaded-every-day/) daily. Among this sea of content, the channels under category `News & Politics` have the third most videos out of all 15 categories, bolstering the role of Youtube as a substantial vessel of information and news. In fact, a 2020 study found that [26%](https://www.pewresearch.org/journalism/2020/09/28/many-americans-get-news-on-youtube-where-news-organizations-and-independent-producers-thrive-side-by-side/) of US adults get their news from YouTube. This number has a lot of room to grow given that the category getting comparatively few views compared to the amout of uploaded videos. With this in mind, investigating YouTube as a news source by examining how channels report on different events and how the subsequent public engagement offers valuable insights into how modern media affects the spread of news. The findings could help governments, NGOs, and media outlets optimize their use of YouTube during emergencies to maximize outreach and public response.

*** TALK ABBOUT TREND AND POSSIBLE PREDICTION PLOS ***

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


# for the readme / notebook #
Our goal is not only to study the spread of news, but to also examine how it is affected by the location of the event in question as well as its type. For this purpose, we consider three general regions to compare: the US, Europe, and Asia. As for the event type, we originally went for four classes: geopolotical conflicts (focusing on armed clashes), enviornmental disasters, economical crisis and political (mainly elections), with the goal of having two events per categories per location. However we later decided to reduce the number of event types and increase the number of videos per type to have a more accuracte and complete representation. 

***Geopolitical conflicts/ armed conflicts***

**US:**

- **Mosul Offensive (2016-2017) - Iraq:** A major urban battle where Iraqi security forces, backed by US-led coalition airpower and international special forces, launched a nine-month campaign to liberate Mosul from ISIS control. The conflict saw intense street-by-street fighting and significant civilian casualties, ending with the city’s recapture but leaving much of it in ruins.
- **Battle of Kobani (2014-2015) - Syria:** A key turning point in the war against ISIS, where Kurdish YPG forces, supported by US-led coalition airstrikes, defended the besieged city of Kobani near the Turkish border. The fierce, months-long battle significantly weakened ISIS and showcased the effectiveness of Kurdish and US-coalition collaboration.
- **Battle of Raqqa (June - October 2017) - Syria:** The climactic urban combat operation where the US-backed Syrian Democratic Forces (SDF) recaptured Raqqa, ISIS's self-declared capital. Supported by extensive US airstrikes, the battle resulted in heavy casualties and large-scale destruction, symbolizing the collapse of ISIS's territorial control.
- **Kunduz City Attack (2015) - Afghanistan:** Taliban forces launched a surprise assault on Kunduz, seizing the city for several days before being driven out by Afghan forces with US air support. The campaign drew international condemnation after a US airstrike mistakenly hit a Médecins Sans Frontières (MSF) hospital, causing significant civilian casualties.
- **Battle of Sirte (2016) - Libya:** Libyan government-aligned forces, with support from US airstrikes, fought for control of Sirte, ISIS’s North African stronghold. After months of intense street fighting, Libyan forces reclaimed the city, dealing a major blow to ISIS’s presence in the region.

**Asia:**

- **India-Pakistan Conflict / Kashmir Conflict (Pulwama and Balakot Airstrikes) (February 2019):** A suicide bombing by a Pakistan-based militant group in Pulwama killed 40 Indian paramilitary personnel, prompting retaliatory Indian airstrikes in Balakot. The incident triggered cross-border clashes, escalating tensions between the nuclear-armed neighbors.
- **Syrian Civil War (Aleppo Offensive (2016)):** In Aleppo, Syrian government forces, backed by Russian airstrikes, launched a brutal offensive against rebels, reclaiming the city after months of relentless bombardment.
- **Yemeni Civil War, battle of Hudayah (June - December 2018 ) -** The **Battle of Hudaydah (June - December 2018)** was the largest and most critical clash in the **Yemeni Civil War**. It involved a massive offensive by the **Saudi-led coalition** and Yemeni government forces against **Houthi rebels** to seize control of **Hudaydah Port**, Yemen's primary entry point for humanitarian aid and supplies. The battle saw **intense urban warfare**, **heavy airstrikes**, and **naval blockades**, resulting in thousands of casualties on both sides and severe civilian suffering. Fears of a **humanitarian disaster** due to potential disruptions in food and medical imports drew international condemnation. The fighting ultimately led to a **UN-brokered ceasefire** under the **Stockholm Agreement** in December 2018, halting the offensive and averting mass starvation in Yemen.

**Europe:**

- **Crimea Annexation and Conflict in Eastern Ukraine (2014):** Russia’s military annexation of Crimea and subsequent backing of separatist rebels in Ukraine’s Donbas region triggered an armed conflict with Ukrainian forces. The crisis led to thousands of deaths, economic sanctions against Russia, and a prolonged geopolitical standoff.
- **Nagorno-Karabakh Conflicts (Clashes (2016)) - Armenia-Azerbaijan:** A brief but intense escalation of hostilities over the disputed Nagorno-Karabakh region, featuring artillery duels, tank battles, and significant casualties on both sides. Despite a ceasefire, tensions between the two countries remain unresolved.

***Natural and human-caused environmental disasters***

- *US :*
    - **Hurricane Harvey (2017):** A Category 4 hurricane that caused catastrophic flooding in Texas, especially in Houston, becoming one of the costliest natural disasters in US history.
    - **California Wildfires (2018):** Including the Camp Fire, the deadliest and most destructive wildfire in California’s history, destroying entire towns like Paradise and causing widespread evacuation.
    - **Hurricane Maria (2017):** A powerful Category 5 hurricane that devastated Puerto Rico and nearby Caribbean islands, causing a prolonged humanitarian crisis and leaving much of the island without power for months.
    - **Hurricane Michael (2018):** A Category 5 hurricane that struck Florida, causing catastrophic damage with intense winds, storm surges, and widespread destruction in the southeastern US. It was one of the strongest hurricanes ever to hit the US mainland.
    
- *Asia :*
    - **Sulawesi Earthquake and Tsunami (2018):** A 7.5 magnitude earthquake triggered a devastating tsunami in Indonesia, killing thousands and flattening entire communities.
    - **Southeast Asian Haze (2015):** A massive transboundary haze caused by illegal agricultural fires in Indonesia, affecting millions across Southeast Asia with hazardous air quality.
    - **Nepal Earthquake (2015):** A 7.8 magnitude earthquake struck Nepal, causing widespread destruction, killing thousands, and severely damaging historical sites, including those in Kathmandu.
    - **Bangladesh Cyclone Mora (2017):** A strong cyclone that impacted densely populated coastal areas and refugee camps, displacing hundreds of thousands of people.
    - **India Floods (2018):** Severe monsoon flooding in Kerala, considered the worst in a century, displacing over a million people and causing massive economic and environmental damage.
    
- *Europe :*
    - **Heatwaves (2019):** Record-breaking heatwaves across Europe caused severe droughts, wildfires, and thousands of heat-related deaths, with temperatures exceeding 46°C in France.
    - **Portugal Wildfires (2017):** Massive wildfires in central Portugal, particularly in Pedrógão Grande, causing hundreds of deaths and devastating large areas of forest and rural communities.
    - **European Floods (2014):** Widespread flooding in the Balkans, including Bosnia, Serbia, and Croatia, caused by heavy rains and river overflows, displacing thousands and causing significant infrastructure damage.
    - **Greek Wildfires (2018):** Devastating wildfires near Athens, particularly in the town of Mati, causing significant loss of life, displacing thousands, and becoming one of Europe’s deadliest wildfire events in modern history.
    - **Italy Earthquakes (2016):** A series of powerful earthquakes hit central Italy, particularly in Amatrice, causing hundreds of deaths and massive destruction, including damage to historical towns and cultural landmarks.

The choice of events was rigorous, as we only wanted events that had a clear starting date that accurately represents the response to breaking news and that we can use for filtration. We also looked for the most popular and impactful events for each category, i.e. the ones that garnered the most reporting, to maximize the datapoints and best represent the event types.

To flag the related videos for each event, we looked for keywords in the titles and description of each video for any potential match. We define keywords and combinations of keywords that, if raise a match in either the title or description of the video, flag the video as relavant. For every event we define a list of lists, where each sublist has one or more keywords as strings. For a video to be flagged, at least one sublist has to match all its terms to the title or description. Finally we filter the results using upload time, where we only consider the time frame during which the specific event was occurring and still relevant.

######### end of readme paragraph

Our goal is not only to study the spread of news, but to also examine how it is affected by the location of the event in question as well as its type. For this purpose, we consider three general regions to compare: the US, Europe, and Asia. As for the event type, we settled on environmental disasters and geopolitical conflicts with a focus on armed clashes. For each category, we chose the largest and most impactful events to maximize the number of datapoints and have the most  accurate representation we could obtain. We flagged relavant videos for each event by searching for keywords in the titles and descriptions. We also added a second layer of filtering using the videos upload dates, where we only consider the time frame during which the specific event was occurring and still relevant.

**** point to tree plots for the events *****

plot with iframe without borders:

<iframe src="assets/plots/channels_activity_histogram.html" width="100%" height="400" style="border:none;"></iframe>

<iframe src="assets/plots/channel_filtering_steps.html" width="60%" height="400" style="border:none;"></iframe>

<iframe src="assets/plots/event_filtering_sankey.html" width="100%" height="600" style="border:none;"></iframe>

<span style="color: red;">Plots about the events and a first dumb analysis. Interactive plot with times series (upload) of each events, way to visualize keywords</span>

### Characteristics of videos
<span style="color: red;">

We define several video metrics that will be used to attempt to predict the audience's response. We consider factors that can be controlled by the video creator and that ideally can be optimized to maximize outreach. For every video, we compute and store: 

- video duration
- type of video (on ground footage or not). 
- frequency of uploads of the channel at time of video upload
- capitalization ratio of title
- appearance of specific keywords in the title: "breaking" and "update"
- Subjectivity score</span>

The video duration was taken directly from the YouNiverse dataset. The type of video reflects if it shows ground footage or not, and the filtering is done based on wether or not the word "footage" appears in the title. The frequeny of video uploads describles the average daily upload frequency of the specific channel in the 2 weeks surrounding the upload of that specific video. The video title are offer us a few metrics. The caplitalization of the title is the ratio of upper case letters in the title. The title is also used to sarch for common keywords, mainly "breaking" and "update". Finally we generate a subjectivity score for each title using OpenAI's API using the following promt:
"your task is to evaluate the subjectivity of news video titles and give each one a score from 0 neutral to 1 highly subjective. The topic does not matter but the phrasing of the reporting. As an example "Switzerland obliterates all other countries in quality of life" would be more subjective than "Switzerland exceeds other countries in quality of life". Only return the score"

Looking for repeating patterns, we visualize the most common words in the titles via the wordclouds below, separated by region and event type. For the US and Asia, subjectivity seems to be on average higher for geopolitical events, whereas we don't see significant difference in European events. 

<iframe src="assets/plots/wordclouds.html" width="100%" height="600" style="border:none;"></iframe>
<iframe src="assets\plots\plot_video_metrics_event_region.html" width="100%" height="600" style="border:none;"></iframe>
<iframe src="assets\plots\plot_video_metrics_event_type.html" width="100%" height="600" style="border:none;"></iframe>

We can look at the difference in distributions of these metrics based on location and event type.

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
<iframe src="assets\plots\correlation_matrix_events.html" width="100%" height="600" style="border:none;"></iframe>
<iframe src="assets\plots\correlation_matrix_regions.html" width="100%" height="600" style="border:none;"></iframe>

[insert normalized correlation plot form samuel here]


<iframe src="assets\plots\Linear_regression_final_plots.png" width="100%" height="600" style="border:none;"></iframe>




<span style="color: red;">Plot with statistics about each of those metrics where you can choose whether you want to group by region or event (or both?).</span>

<span style="color: red;">Again perform t-test for metrics which do show a difference and draw conclusion</span>

