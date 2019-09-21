
# SECTION 1: PROJECT TITLE
Intelligent Traffic Light Management System (ITLMS)
--

# SECTION 2: EXECUTIVE SUMMARY
Transportation is a core area of a country’s economy and functions, providing the means of quick and efficient movement of their population and goods through the country. Traffic lights are a critical component in road networks, directing the flow of vehicular and pedestrian traffic and ensure that transportation runs smoothly. Poor design and management of such traffic control systems may lead to traffic jams as well as road accidents, hampering economic activity and more importantly, the loss of citizens’ lives. In addition wait times are known to induce stress and affect psychological well-being for commuters, which may have adverse effects on health and work productivity.

Hence, there is a need for efficient and robust traffic control systems globally, including Singapore. Singapore as a geographically dense city-state, relies heavily on such systems to drive road transportation. In this project, we propose an intelligent traffic light management system which provides recommended green-light timings for different phases and directions in a single traffic junction. The system consists of a inference engine for assessing traffic conditions and processing traffic volume, a genetic optimization model to provide recommended green-light timings and a user interface that can be extended to include future road traffic sensor data.

# SECTION 3: CREDITS/PROJECT CONTRIBUTION

| Official Full Name|Student ID| Work Scope  |Email|
|:---------:|:-------------:|:-----:|:----:|
|Ang Boon Yew| A0096966E		|Chatbot Design, DialogFlow Configuration, Flask Backend App, Handling of Zomato APIs,Integration with Telegram, App Hosting on Heroku 	|boonyew@u.nus.edu|
|Kartik Chopra|A0198483L		|Initial survey for algorithm design, Algorithm Design, Question based knowledge system, Backend code for time calculation 	|kartik@u.nus.edu|
|Karamjot Singh|A0198470U		|Chatbot Design, DialogFlow Configuration, Flask Backend App, Handling of Zomato APIs, Backend Modules and Testing, Video Editing	|	singh@u.nus.edu|


# SECTION 4: VIDEO INTRODUCTION & USER GUIDE
<a href="https://github.com/validation7407/IRS-MR-2019-09-22-IS1FT-GRP-Validation7407-ITLMS/blob/master/ITLMS_Video.mp4" target="_blank"><img src="https://github.com/validation7407/IRS-MR-2019-09-22-IS1FT-GRP-Validation7407-ITLMS/blob/master/ITLMS_Video.jpg" 
alt="ITLMS" width="640" height="360" border="10" /></a>


# SECTION 5: USER GUIDE
The ITLMS comes with a web-based user interface in order to demonstrate the use of the system to estimate green-light timings at traffic junctions.


Follow below steps to setup ITLMS:
1. <u>Setting up the Flask Server
-   git clone  [https://github.com/validation7407/IRS-MR-RS-2019-09-22-IS1FT-GRP-Validation7407-ITLMS.git](https://github.com/validation7407/IRS-MR-RS-2019-09-22-IS1FT-GRP-Validation7407-ITLMS.git)
-  Open up command prompt for Windows or Terminal for Linux
- Navigate to the System sub-folder the cloned ITLMS repository folder
- Enter 'python app.py' in order to start the Flask server
-   Use your web browser to navigate to the ITLMS User Inteface [https://localhost:5000](https://localhost:5000)

2. <u>Using the ITLMS Demonstration Interface

- Select the type of junction: **"T-Junction"** or **"Cross-Junction"**
- For each of the possible directions as indicated in the figure on the left, enter the number of **Lanes**.
- Enter the current **No. of Vehicles** in each lane,separated by a comma e.g. Lanes: "2", No. of Cars: "3,4" or Lanes: "3", No of Cars: "5,10,15"
- Enter the arrival rates of cars in that direction (cars/sec) in **Arrival Rate**
- Enter in the number of vehicles in the right-turning lanes in **Right Lane**
- Click **"Submit"** to view the results.

Integration with external road traffic sensor systems or other inputs sources can also be done by passing these inputs to the Flask server through a HTTP POST request.

# SECTION 6: PROJECT REPORT
[https://github.com/validation7407/IRS-MR-RS-2019-09-22-IS1FT-GRP-Validation7407-ITLMS/blob/master/ITLMS_FinalReport_Group14.pdf]
