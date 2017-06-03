# notify_labor

This is a [Twilio](https://www.twilio.com') application that utilizes [Flask](http://flask.pocoo.org/) and `sqlite3`.
It serves a unique purpose, but is written in a way that anyone can deploy it if they want to use it.

I wrote this out of a lack of desire to call anyone and everyone who may want to know when my wife has our baby.
Yes, I am that lazy. 
Users call the specified Twilio number and register their phone numbers with the application.
Then, when my wife (or whoever), has the baby, I (or the owner) can text a secret phrase to the number.
Upon receiving this text, the application will go through each of the registered numbers and call them to notify that the baby has been born.
It will also provide an option for the user receiving a call to leave a message for the woman/couple to listen to later. 
These recordings can then be downloaded by the owner and saved for later.
Alternatively, the user may get a text message.
When a user signs up for the service, he or she chooses to receive a phone call or a text message.
The message used is specified by the owner of the service when the notify text is sent.
If your secret phrase is "secret", then to begin the notification process you would text the number "secret your message goes here".

## Configuration

Create an account with Twilio and buy a number.
Create a server that is publicly accessible on the internet and download this repo to it.
Install the dependencies using `pip`: `pip install -r requirements.txt`.
You should ideally do this in a virtual environment using `virtualenv`.

Notice the file called `config_example.py`.
Fill in each of the values in that file then rename it to `config.py`.

**All of these values need to be set for the application to work.**

Finally, within Twilio you must provide the URL to use to connect to your application.
For the phone, enter `http://yourip:yourport/api/register` and for SMS enter `http://yourip:yourport/notify`, where `yourip` is the IP address of your
server and `yourport` is the port your application is running on as specified in the configuration file.
This can all be done under `Account -> Numbers -> The Number`.

## Use

Start the application with `python run.py`.
Then, hand out the Twilio number to those who you wish to have notified about the baby.
Finally, once it comes time, send your secret phrase in a text to the Twilio number and the application will handle notifying everyone who registered.
That's it!
Make sure once you have the baby you stop running your instance of the application: it will always allow for registration of numbers.

## License

See LICENSE.md

