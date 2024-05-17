import shutil
import os
import pathlib as pl
import tomli

# this is taken from: 
# https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory/13197763#13197763
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def read_template_file(swb_control_file_template_name):
    with open(swb_control_file_template_name) as f:
        contents = f.read()
    return contents

def write_control_file(control_file_text, control_filename):
    with open(control_filename, "w") as f:
        f.write(control_file_text)

def write_batch_file(batch_file_text, batch_filename):
    with open(batch_filename, "w") as f:
        f.write(batch_file_text)

def destroy_model_work_dir(work_dir):
    shutil.rmtree(work_dir, ignore_errors=True)

def create_model_work_dir(work_dir,
                          sub_dir,
                          output_dir,
                          logfile_dir):
    work_path = pl.Path(work_dir) / sub_dir
    logfile_path = work_path / logfile_dir
    output_path = work_path / output_dir 
    work_path.mkdir(parents=True, exist_ok=True)
    logfile_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)

def read_toml_file(filename):
    with open(filename, "rb") as f:
        toml_dict = tomli.load(f)
    return toml_dict
