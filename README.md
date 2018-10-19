<div align="center">
    <img src="https://user-images.githubusercontent.com/38182450/46910084-abad8d80-cf3e-11e8-9be3-09c9078b2c3a.png" width="400px" />
    <h1>~~ Shitcord ~~</h1>
    <strong>A shitty, probably not even that shitty Discord API wrapper.</strong>
    <br><br>
    <a href="https://www.codacy.com/app/itsVale/Shitcord?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=itsVale/Shitcord&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/b3ed9f02a50142bf9fd337978be88b24" /></a>
    &nbsp;
    <a href="https://travis-ci.com/itsVale/Shitcord"><img src="https://travis-ci.com/itsVale/Shitcord.svg?branch=dev" /></a>
    &nbsp;
    <a href="https://GitHub.com/itsVale/Shitcord/issues/"><img src="https://img.shields.io/github/issues/itsVale/Shitcord.svg" /></a>
    &nbsp;
    <a href="https://GitHub.com/itsVale/Shitcord/pulls/"><img src="https://img.shields.io/github/issues-pr/itsVale/Shitcord.svg" /></a>
    &nbsp;
    <a href="http://perso.crans.org/besson/LICENSE.html"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" /></a>
    <hr>
</div>

_Though this library is incomplete yet, contributions are very appreciated!_

# Installation
For now, you can only install the dev branch which is constantly updated.
```
pip install -U https://github.com/itsVale/Shitcord/archive/dev.zip
```

No documentation yet since the available code is not intended to be used by everyone.  
It requires you to read the source code to understand how the library works. At the moment it's just
a client to interact with the REST API. If there is an "official" client to interact with the REST API
and the Gateway, then there will be docs added.

# Usage
```python
from shitcord import *
import logging #Only use if you want to see the log

logger = logging.getLogger('shitcord') #Only use if you want to see the log
logger.level = logging.DEBUG #Only use if you want to see the log

Client().start("TOKEN")
```

# Support
Need help with something or just want to hang out with more or less cool guys? [Join our cool Discord server!](https://discord.gg/HbKGrVT)