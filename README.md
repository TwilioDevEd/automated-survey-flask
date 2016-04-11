# Automated survey for Python - Flask
[![Build Status](https://travis-ci.org/TwilioDevEd/automated-survey-flask.svg?branch=master)](https://travis-ci.org/TwilioDevEd/automated-survey-flask)

Learn how to use [Twilio Client](https://www.twilio.com/client) to conduct automated phone surveys.

**Full Tutorial:** [soon]

## Quickstart

### Local development

This project is built using the [Flask](http://flask.pocoo.org/) web framework. It runs on Python 2.7+ and Python 3.4+.

To run the app locally, first clone this repository and `cd` into its directory. Then:

1. Create a new virtual environment:
    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```
        virtualenv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```
        mkvirtualenv automated-survey
        ```

1. Install the requirements:

    ```
    pip install -r requirements.txt
    ```

1. Copy the `.env.example` file to `.env`, and edit it to match your database.
1. Run `source .env` to apply the environment variables (or even better, use [autoenv](https://github.com/kennethreitz/autoenv))

1. Run the migrations with:

    ```
    python manage.py db upgrade
    ```

1. Modify seed data:

   We have provided an example of name and phone number in the seed data. In order for
   the application to send sms notifications, you must edit this seed data providing
   a real phone number where you want the sms notifications to be received.

   In order to do this, you must modify
   [this file](https://github.com/TwilioDevEd/automated-survey-flask/blob/master/manage.py#L25)
   that is located at: `project_root/manage.py`

1. Seed the database:

   ```
   python manage.py dbseed
   ```

1. Start ngrok
   
    To actually forward incoming calls, your development server will need to be publicly accessible.
    [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).


   ```bash
   $ ngrok http 5000
   ```

    Once you have started ngrok, update your TwiML app's voice URL setting to use your ngrok hostname, so it will look something like this:

    ```
    http://88b37ada.ngrok.io/support/call
    ```

1. Start the development server:

    ```
    python manage.py runserver
    ```

Once Ngrok is running, open up your browser and go to your Ngrok URL. It will
look like this: `http://88b37ada.ngrok.io`

That's it!

### Configure Twilio to call your webhooks

You will also need to configure Twilio to call your application when
calls are received

You will need to provision at least one Twilio number with voice
capabilities so the application's users can take surveys. You can buy
a number
[right here](https://www.twilio.com/user/account/phone-numbers/search). Once
you have a number you need to configure your number to work with your
application. Open
[the number management page](https://www.twilio.com/user/account/phone-numbers/incoming)
and open a number's configuration by clicking on it.

![Open a number configuration](https://raw.github.com/TwilioDevEd/automated-survey-django/master/images/number-conf.png)

Next, edit the "Request URL" field under the "Voice" section and point
it towards your ngrok-exposed application `/automated-survey/first-survey/` route. Set
the HTTP method to POST. If you are trying the Heroku
application you need to point Twilio to
`http://<your-app-name>.herokuapp.com/automated-survey/first-survey/`. 

See the images
below for an example:

You can then visit the application at [http://localhost:8000/](http://localhost:8000/).

Mind the trailing slash.

![Webhook Voice configuration](https://raw.github.com/TwilioDevEd/automated-survey-django/master/images/webhook-conf-voice.png)

The same endpoint for Voice is being used for Messaging, so you can repeat this step on Messaging section.
![Webhook SMS configuration](https://raw.github.com/TwilioDevEd/automated-survey-django/master/images/webhook-conf-sms.png)


## Run the tests

You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

1. Run the tests:

    ```
    $ coverage run manage.py test
    ```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.
