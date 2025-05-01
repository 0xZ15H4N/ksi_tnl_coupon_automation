well I was bored so yeah i made automated py script that can extract coupons out of ksi video (try-not-to-laugh money edtion)

testimony :-
results.txt is the file where out video AI api send the text from the video and is written into results.txt 
![image](https://github.com/user-attachments/assets/dd489992-25f8-46a6-af6c-afca820c185b)
![image](https://github.com/user-attachments/assets/540eda68-cc8d-4aa5-93bc-164564882d3f)
![image](https://github.com/user-attachments/assets/ea64c3eb-cbb6-4c81-bf11-1a8bfa6717b5)
![image](https://github.com/user-attachments/assets/1e079f99-e284-430e-ac8b-af0b232f9332)
![image](https://github.com/user-attachments/assets/88cec207-a7f3-4848-aecc-f0b2d57ae16c)
![image](https://github.com/user-attachments/assets/475ae40b-c772-4bcc-878c-128256daa9d8)

here is the step by step guide on how you can setup this repo on you system so you can start mining 
 first like a good boy/girl clone the repo into ~/ , after that rename the repo to ksi_tnl with this command `mv ksi_tnl_coupon_automation ksi_tnl`
 cd into ksi_tnl ,before that copy that .envDemo to .env in the ~/ksi_tnl
 and you're done 

 now come to google cloud service click this link `https://cloud.google.com/free`
 awail the 300$ credits to get started! make sure you cancel the bill before 90 completes ( In India we get 300$ credits ) 
   
create an account for free , i have used google video intelegence and vision AI to extract text from images and video 

all you need to do is after completing the signup and signIN , go to search bar and search for `YOUTUBE DATA v3`
![image](https://github.com/user-attachments/assets/14312f08-3830-49eb-8d8b-1bf8f6295cb3)
 click on this and click enable  button its free so dont worry !
 
after enabling inthe place of enable button you'll see the manage button click on that , after that slide that left side panel and you will see this click on credentials
![image](https://github.com/user-attachments/assets/4e788295-6e98-4948-adee-4fa178acee88)

as you can see on the top bar you wil see `create credentials`, create one and you will get an api-key copy that , after that copy that api-key and paste it on the .env file 
where `API_KEY=""`
![image](https://github.com/user-attachments/assets/401f2e7a-dfd7-470d-9921-9f65d4103ce4)

then in the serach bar  ,type `cloud vision api` and same click on that and enable it , this time no need to create an api_key, just copy the same `api_key` you created earlier and 
paste it where you have `VISION_API=""`

after that click on the top left corner click on this three lines on the left of google cloud logo
![image](https://github.com/user-attachments/assets/50d7a209-0b2f-40ad-a62a-e94d5efa4956)

slide down to `cloud storage -> Bucket`
![image](https://github.com/user-attachments/assets/5ba9fc73-086c-4da0-aae4-ff8fe53e00d1)

click on `➕create` 
![image](https://github.com/user-attachments/assets/2ead2fea-a8c7-4684-908f-a156901543fc)

after that set the name of the Bucket and select the options if dont know chatgpt it this is what I used, and then create !  
![image](https://github.com/user-attachments/assets/9c662940-4c60-41bc-b8a5-2696403d7617)

copy the bucket name exactly go to .env and paste the bucket name where `BUCKET_NAME=""`

at last go to search bar and search `Cloud Video Intelligence API` , click on enable and then go to manage 
![image](https://github.com/user-attachments/assets/049cdd83-f807-4dba-8649-c6d6298148e5)

after that click on three lines on the top left corner and link on `IAM & admin-> service accounts`
![image](https://github.com/user-attachments/assets/d61ea04f-5c57-4490-b85b-df15ef89c6b2)


1 Fill in the details (name, description) and click Create and Continue.

2 Grant access to the service account:

3 Choose a role like Storage Admin (for full access) or a more limited role depending on your needs.

4 Click Done or Continue, then find your newly created account in the list.

5 Click on the service account name → Go to the “Keys” tab.

6 Click “Add Key” → “Create new key” → Choose JSON → Click Create.

7 The auth_key.json file will automatically download.

after that download the .json file in the ~/ksi_tnl and update the .env where `auth_key="./auth_key.json"`
after to automatically redeem that coupon i have create an amazon_bot for that all you need to do is fill the `phone='' and pass=''` with amazon account password 
after that also add the video path to `/<full-path>/ksi_tnl/temp_youtube_download/video.mp4.webm`

update the channel id with ksi channel id in .env

################## optional thing ##########################

 if you wish to get the email every time ksi drops a video just update the APP_PASS WITH you gmail app pass for that you can ask chatgpt its 2 minute works
 also update the email and client field with respective email (email from which the mail will be send and client which will recieve it )

note that : APP_PASS need that app-pass of email one which will send the mail hope you under stand what i am saying now you are all set 

all you need to do is now find a system that never sleep and  also donwload that the requirements.txt 

before running the init.py

if you are on linux then do this 
    run this command `python -m venv myenv`
    and after that run `source myenv/bin/activate `

after that run `pip install -r requirements.txt`

 now all you need to do is run init.py and start mining the coupons !
if you mine even one of them , please hit a star button and consider following !

or you can buy me a cofffe at  : https://buymeacoffee.com/0xz15h4n

  chao ~

