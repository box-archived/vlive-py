# -*- coding: utf-8 -*-

formatted_body_template = """<div id="vlivepy-post-html" style="width:728px;">
    <p><a href="###LINK###">###LINK###</a></p>
<div style="padding:15px 0;border-bottom:1px solid #f2f2f2">
    <span class="author" style="font-weight:600;color:#111;font-size:14px;display:block">###AUTHOR###</span>
    <span class="createdAt" style="color:#777;font-size:12px">###TIME###</span>
</div>
    <h2 class="title">###TITLE###</h2>
    <div class="post_content">
        ###POST###
    </div>
</div>"""

video_box_template = """<div style="position:relative;padding-top: 56.25%;background-color: #000;margin-bottom:10px">
    <div style="position: absolute;top: 0;right: 0;bottom: 0;left: 0;z-index: 0;">
        <div style="position:relative;z-index:1;height:100%;">
            <div class="container" style="overflow:hidden;height:100%">###VIDEO###</div>
            <div class="sizer"
                 style="position: absolute; inset: 0px; overflow: hidden; z-index: -1; visibility: hidden; opacity: 0;"></div>
        </div>
    </div>
</div>
"""