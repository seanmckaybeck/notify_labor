# notify_labor

This is a [Twilio](https://www.twilio.com') application that utilizes [Flask](http://flask.pocoo.org/) and `sqlite3`.
It serves a unique purpose, but is written in a way that anyone can deploy it if they want to use it.

I wrote this out of a lack of desire to call anyone and everyone who may want to know when my wife goes into labor.
Yes, I am that lazy. Users will call the specified Twilio number and register their phone numbers with the application.
Then, when my wife (or whoever), goes into labor I (or the owner) can text a secret phrase to the number. Upon receiving
this text, the application will go through each of the registered numbers and call them to notify that the woman has gone
into labor. It will also provide an option for the user receiving a call to leave a message for the woman/couple to listen
to later. These recordings can then be downloaded by the owner and saved for later!

## Configuration

Create an account with Twilio and buy a number. Create a server that is publicly accessible on the internet and
download this repo to it. Install the dependencies using `pip`: `pip install -r requirements.tx`. You should
ideally do this in a virtual environment using `virtualenv`.

Notice the file called `config.ini`. The following describes what each of the parameters should be:  
* `secret`: The secret phrase the owner sends the application to notify registered numbers that labor has started
* `deadline`: A Unix timestamp, representing the deadline for registration. Use the `deadline.py` script to generate this
* `number`: The Twilio number the application uses
* `port`: The port to run the application on
* `ip`: The public IP address of the server the application is running on
* `sid`: Your Twilio SID, found on your user account page
* `authtoken`: Your Twilio authentication token, found on your user account page

All of these values need to be set for the application to work.

### Deadline

I only want people to have the ability to register for a certain amount of time. The application handles this using
Unix timestamps. You must use `deadline.py` to generate a valid timestamp to put in the configuration file. As an example,
say I want the deadline to be July 25, 2015. Note that it assumes midnight for time.

> python deadline.py -y 2015 -m 7 -d 25

This will spit out the timestamp to save in the configuration file.

## Use

Start the application with `python app.py`. Then, hand out the Twilio number to those who you wish to have notified about
the beginning of labor. Finally, once it comes time, send your secret phrase in a text to the Twilio number and the
application will handle calling everyone who registered. That's it!

## License

See LICENSE.md
