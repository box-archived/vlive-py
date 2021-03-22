vlivepy
=======
**vlivepy** is a VLIVE(vlive.tv) parser for python.

Easily parse and explore VLIVE with vlivepy.

.. code-block:: python

    import vlivepy

    video = vlivepy.OfficialVideoPost(231176)
    print(video.title)
    # 연히랑 새해 따뜻하게 보내기❣

    print(video.channel_name)
    # Rocket Punch

Getting started
---------------
First, you need to install the vlivepy. Check out :doc:`how to install vlivepy </installation>`.
If you want to customize some settings? Read about :doc:`custom variables </custom_variables>`.

Oops. You've got trouble? Check all :doc:`exceptions </exceptions>` or
`create an issue <https://github.com/box-archived/vlive-py/issues>`_.
You can also ask for help on the `discussion <https://github.com/box-archived/vlive-py/discussions>`_

* **Getting started**:
  :doc:`Installation </installation>` |
  :doc:`Custom variables </custom_variables>` |
  :doc:`exceptions </exceptions>`

* **Supports**:
  `GitHub Issues <https://github.com/box-archived/vlive-py/issues>`_ |
  `GitHub Discussions <https://github.com/box-archived/vlive-py/discussions>`_

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Getting started

    installation
    custom_variables
    exceptions

Base Models & Objects
---------------------
This is the base model for grouping common properties of the objects.

Entire inheritance structure is down below.

* :doc:`DataModel </model/datamodel>`

    * :doc:`Channel </model/channel>`
    * :doc:`Comment </model/comment>`
    * :doc:`GroupedBoards </model/groupedboards>`

    * :doc:`OfficialVideoModel </model/officialvideomodel>`

        * :doc:`OfficialVideoLive </model/officialvideolive>`
        * :doc:`OfficialVideoVOD </model/officialvideovod>`

    * :doc:`PostModel </model/postmodel>`

        * :doc:`Post </model/post>`
        * :doc:`OfficialVideoPost </model/officialvideopost>`

    * :doc:`Schedule </model/schedule>`
* :doc:`Upcoming </model/upcoming>`
* :doc:`UserSession </model/usersession>`

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Base Models

    model/datamodel
    model/officialvideomodel
    model/postmodel

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Objects

    model/channel
    model/comment
    model/groupedboards
    model/post
    model/officialvideopost
    model/officialvideolive
    model/officialvideovod
    model/schedule
    model/upcoming
    model/usersession

Module & Functions
------------------
Check more :doc:`functions! </function/functions>`. Or you just can import modules and use core functions.

* **Functions**: :doc:`Functions </function/functions>`

* **Modules**:
  :doc:`vlivepy.board </function/board>` |
  :doc:`vlivepy.channel </function/channel>` |
  :doc:`vlivepy.comment </function/comment>` |
  :doc:`vlivepy.connections </function/connections>` |
  :doc:`vlivepy.parser </function/parser>` |
  :doc:`vlivepy.post </function/post>` |
  :doc:`vlivepy.schedule </function/schedule>` |
  :doc:`vlivepy.session </function/session>` |
  :doc:`vlivepy.upcoming </function/upcoming>` |
  :doc:`vlivepy.video </function/video>`

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Module & Functions

    function/functions
    function/board
    function/channel
    function/comment
    function/connections
    function/parser
    function/post
    function/schedule
    function/session
    function/upcoming
    function/video