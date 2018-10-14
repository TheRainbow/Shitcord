<div align="center">
    <img src="https://user-images.githubusercontent.com/38182450/46910084-abad8d80-cf3e-11e8-9be3-09c9078b2c3a.png" width="400px" />
    <h1>~~ Shitcord ~~</h1>
    <strong>A shitty, probably not even that shitty Discord API wrapper.</strong>
    <br><br>
    <hr>
</div>

_Though this library is incomplete yet, contributions are very appreciated!_

# Installation
For now, you can only install the dev branch which is constantly updated.
```
pip install -U https://github.com/itsVale/Shitcord/archive/dev.zip
```

No documentation yet since the available code is not intended to be used by everyone.  

# Usage
```python
import shitcord
import logging

logger = logging.getLogger(__name__)
api = shitcord.API('Token')

# Some variables we need for a request.
channel_id = 12345678901234
content = "I'm using Shitcord and I'm proud of this!"

# Send a message to a given channel.
api.create_message(channel_id, content)
```

# Support
Need help with something or just want to hang out with more or less cool guys? [Join our cool Discord server!](https://discord.gg/HbKGrVTy)