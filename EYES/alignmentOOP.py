
"""
$ git clone https://github.com/ReadBeyond/aeneas.git
$ cd aeneas
$ sudo pip install -r requirements.txt
$ python setup.py build_ext --inplace
$ python aeneas_check_setup.py
"""

from aeneas.executetask import ExecuteTask
from aeneas.task import Task

class AudioTextAligner:
    def __init__(self, audio_file_path, text_file_path, sync_map_path, language='eng', text_type='plain', file_format='json'):
        self.audio_file_path = audio_file_path
        self.text_file_path = text_file_path
        self.sync_map_path = sync_map_path
        self.language = language
        self.text_type = text_type
        self.file_format = file_format
        self.task = None

    def create_task(self):
        config_string = u"task_language={}|is_text_type={}|os_task_file_format={}".format(
            self.language, self.text_type, self.file_format)
        self.task = Task(config_string=config_string)
        self.task.audio_file_path_absolute = self.audio_file_path
        self.task.text_file_path_absolute = self.text_file_path
        self.task.sync_map_file_path_absolute = self.sync_map_path

    def process_task(self):
        if self.task is None:
            self.create_task()
        ExecuteTask(self.task).execute()

    def output_sync_map(self):
        if self.task is not None:
            self.task.output_sync_map_file()
        else:
            print("Task not initialized or processed. Call process_task() first.")

if __name__ == "__main__":
    aligner = AudioTextAligner(
        audio_file_path="alingment_audio.mp3",
        text_file_path="alignment_text",
        sync_map_path="syncmap2.json"
    )
    aligner.process_task()
    aligner.output_sync_map()
