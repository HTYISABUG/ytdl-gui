class YTDLHelper(object):

    def __init__(self, ytdl_path, ffmpeg_path, process, text_process):
        self.ytdl_path = ytdl_path
        self.ffmpeg_path = ffmpeg_path
        self.process = process
        self.text_process = text_process

        self.default_params = ['--ffmpeg-location', self.ffmpeg_path]
        self.params = list(self.default_params)

    def update(self):
        self.process.start(self.ytdl_path, ['-U'])

    def split(self):
        self.params += ['-f', 'bestvideo,bestaudio']
        return self

    def audio_only(self):
        self.params += ['-f', 'bestaudio']
        return self

    def encoding(self, fmt):
        self.params += ['--merge-output-format', fmt]
        return self

    def thumbnail(self):
        self.params += ['--write-thumbnail']
        return self

    def output(self, template):
        self.params += ['-o', template]
        return self

    def exec(self, url):
        self.params += [url]
        self.process.start(self.ytdl_path, self.params)
        self.params = list(self.default_params)

    def get_real_url(self, url):
        self.text_process.start(self.ytdl_path, ['-f', 'best', '-g', url])
        self.text_process.waitForReadyRead()
        self.text_process.waitForFinished()

        url = self.text_process.readAll().data().decode().strip()

        return url

    def get_filename(self, url):
        self.text_process.start(
            self.ytdl_path, ['--get-filename', '-f', 'best', url])
        self.text_process.waitForReadyRead()
        self.text_process.waitForFinished()

        filename = self.text_process.readAll().data().decode(
            'big5', errors='replace').strip()

        return filename
