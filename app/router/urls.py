from app.router.path import Path
from app.router.views import *
from app.server.types import HttpMethod


urls = [
    Path('/', index),
    Path('/echo/', echo, start=True),
    Path('/user-agent', user_agent),
    Path('/files/', post_file, start=True,
         directory=True, method=HttpMethod.POST),
    Path('/files/', get_file, start=True, directory=True),
]
