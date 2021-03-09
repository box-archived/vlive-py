Custom variables
=================
User can customize variables used to connect with VLIVE



Override variable
-----------------
User can override variables by import and replace variable that starts with :code:`override_*` from vlivepy.variables package. This affects entire vlivepy workflow

This is the example of overriding user-agent.

.. code-block:: python

    from vlivepy.variables import override_user_agent

    override_user_agent = "<enter custom user agent>"

All customizable variables are below

override_gcc
------------
gcc is request parameter to specify user country. VLIVE server chooses cdn by this value.

The default value is :code:`KR`

override_locale
---------------
locale is request parameter to specify response language. VLIVE server chooses language of data (e.g Video title) by this value

The default value is :code:`ko_KR`

override_user_agent
-------------------
user-agent is request header to disguise as web browser. You can get it from your own browser by pasting :code:`console.log(navigator.userAgent)` to web browser's javascript console

The default value is :code:`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36`

override_accept_language
------------------------
accpet_language is request header to set webpage language. This value affects Upcoming object's language

The default value is :code:`ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7`
