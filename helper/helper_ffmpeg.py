class FFMPEGHelper(object):

    def __init__(self, ffmpeg_path, process):
        self.ffmpeg_path = ffmpeg_path
        self.process = process

        self.input_params = []
        self.output_params = []

    def start_time(self, timeoff):
        self.input_params += ['-ss', timeoff]
        return self

    def stop_time(self, timeoff):
        self.output_params += ['-copyts', '-to', timeoff]
        return self

    def duration(self, dur):
        self.output_params += ['-t', dur]
        return self

    def download(self, url, filename):
        self.process.start(self.ffmpeg_path, [
            *self.input_params,
            '-i', url,
            '-c', 'copy',
            *self.output_params,
            filename
        ])
        self.input_params = []
        self.output_params = []
