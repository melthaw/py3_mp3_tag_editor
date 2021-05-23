import os
import time

from app import BASE_DIR


class Configuration:
    _settings = {}
    _tmp_dir = None
    _upload_dir = None
    _log_dir = None
    _version = None

    def update(self, **settings):
        self._settings.update(settings)

    @property
    def base_dir(self):
        return BASE_DIR

    @property
    def tmp_dir(self):
        if self._tmp_dir is None:
            tmp_dir = self._settings.get('tmp_dir', os.path.join(BASE_DIR, 'tmp/tmp'))
            self._tmp_dir = "/".join(tmp_dir.split("\\"))
        return self._tmp_dir

    @property
    def log_dir(self):
        if self._log_dir is None:
            log_dir = self._settings.get('log_dir', os.path.join(BASE_DIR, 'tmp/logs'))
            self._log_dir = "/".join(log_dir.split("\\"))
        return self._log_dir

    @property
    def log_file(self):
        return self._settings.get('log_file', 'main.log')

    @property
    def log_level(self):
        """

        :return:  DEBUG by default, and DEBUG, INFO, WARN, ERROR are supported
        """
        return self._settings.get('log_level', 'DEBUG')

    @property
    def log_rotating_type(self):
        """

        :return: size by default . size and time are supported,  if invalid type is set, warning message shown in console ,and default type is taking place.
        """
        return self._settings.get('log_rotating_type', 'size')

    @property
    def log_file_size(self):
        """taking place if log_rotating_type is size

        :return:
        """
        return self._settings.get('log_file_size', 16 * 1024 * 1024)

    @property
    def log_file_backups(self):
        """how many log files kept in history.

        :return: 10 by default.
        """
        return self._settings.get('log_file_history', 16)

    @property
    def version(self):
        if self._version is None:
            version = "unknown"
            version_file = os.path.join(os.getcwd(), ".version")
            if os.path.exists(version_file):
                try:
                    with open(version_file, "r") as f:
                        version_line = f.readline()
                        if version_line is not None:
                            time_local = time.localtime(int(version_line))
                            version = time.strftime("%Y%m%d %H:%M:%S", time_local)
                except Exception as e:
                    print(str(e))
                    pass
            self._version = version
        return self._version

    @property
    def mp3_home(self):
        return self._settings.get('mp3_home', None)

    @property
    def album(self):
        return self._settings.get('album', None)

    @property
    def title(self):
        return self._settings.get('title', None)

    @property
    def artist(self):
        return self._settings.get('artist', None)

    @property
    def endswith(self):
        return self._settings.get('endswith', '.mp3')

    @property
    def album_artist(self):
        return self._settings.get('album_artist', None)

    def validate(self):
        if self.mp3_home is None:
            raise Exception("mp3_home is required.")
        if not os.path.exists(self.mp3_home):
            raise Exception("%s not exists." % self.mp3_home)

        if self.album is None:
            raise Exception("album is required.")
        if self.artist is None:
            raise Exception("artist is required.")
        if self.album_artist is None:
            raise Exception("album_artist is required.")


configuration = Configuration()
