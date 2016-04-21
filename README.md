# Automated survey for Python - Flask
[![Build Status](https://travis-ci.org/TwilioDevEd/automated-survey-flask.svg?branch=master)](https://travis-ci.org/TwilioDevEd/automated-survey-flask)

Learn how to use [Twilio Client](https://www.twilio.com/client) to conduct automated phone surveys.

## Quickstart

### Local development

This project is built using the [Flask](http://flask.pocoo.org/) web framework. It runs on Python 2.7+ and Python 3.4+.

To run the app locally follow these steps:

1. Clone this repository and `cd` into it.

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

1. Install the requirements.

    ```
    pip install -r requirements.txt
    ```

1. Copy the `.env.example` file to `.env`, and edit it to match your database.

1. Run `source .env` to apply the environment variables (or even better, use [autoenv](https://github.com/kennethreitz/autoenv))

1. Run the migrations.

    ```
    python manage.py db upgrade
    ```

1. Seed the database.

   ```
   python manage.py dbseed
   ```

   Seeding will load `survey.json` into SQLite.

1. Expose your appliction to the wider internet using ngrok.

    To actually forward incoming calls, your development server will need to be publicly accessible.
    [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).


   ```bash
   $ ngrok http 5000
   ```

    Once you have started ngrok, update your TwiML app's voice URL setting to use your ngrok hostname.
    It will look something like this:

    ```
    http://88b37ada.ngrok.io/support/call
    ```

1. Start the development server.

    ```
    python manage.py runserver
    ```

Once ngrok is running, open up your browser and go to your ngrok URL. It will
look like this: `http://88b37ada.ngrok.io`

That's it!

### Configuring Twilio to call your webhooks

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

![Open a number configuration](https://raw.github.com/TwilioDevEd/automated-survey-flask/master/images/number-conf.png)

Next, edit the "Request URL" field under the "Voice" section and point
it towards your ngrok-exposed application `/voice/` route. Set
the HTTP method to GET.
Do the same with the "Messaging" section, but towards the `/message` route.

See the images below for an example:

![Webhook Voice configuration](https://raw.githubusercontent.com/TwilioDevEd/automated-survey-flask/master/images/webhook-conf.png)

You can then visit the application at [http://localhost:8000/](http://localhost:5000/).

Mind the trailing slash.

## Running the tests

You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

1. Run the tests.

    ```
    $ coverage run manage.py test
    ```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.
