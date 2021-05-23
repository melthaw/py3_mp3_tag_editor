import os

import eyed3

from app.config import configuration


class Mp3Editor:

    def update_tag_all_under_mp3_home(self):
        files_under_mp3_home = os.listdir(configuration.mp3_home)
        mp3_iterator = filter(lambda f: f.endswith(configuration.endswith), files_under_mp3_home)
        mp3_iterator = sorted(mp3_iterator)

        for mp3 in mp3_iterator:
            mp3_file = eyed3.load(os.path.join(configuration.mp3_home, mp3))
            print(mp3_file)


mp3_editor = Mp3Editor()
