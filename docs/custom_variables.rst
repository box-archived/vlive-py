Custom variables
=================
User can customize variables used to connect with vlive

override-able variables are start with :code:`override_*`

Override variable
-----------------
User can override variables with import vlivepy.variables package

.. code-block:: python

    from vlivepy.variables import override_user_agent

    override_user_agent = "<enter custom user agent>"

This affects entire vlivepy workflow

override_gcc
------------

override_locale
---------------

override_user_agent
-------------------

override_accept_language
------------------------
