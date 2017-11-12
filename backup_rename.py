import os
import sys
import re
import logging

from datetime import datetime


FOLDERS_LIST = os.path.join(os.path.dirname(sys.argv[0]),
                            'backup_rename_list.txt')
LOG_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'backup_rename.log')
LOG_FORMAT = r'%(asctime)s %(levelname)-8s %(message)s    [LINE:%(lineno)d]'


def rename_with_modification_date(directory):
    try:
        os.chdir(directory)
    except FileNotFoundError:
        logging.error(f"Error:\n'{directory}' can't be found. Skipped.")
        return
    except Exception:
        logging.error(sys.exc_info())
        return

    logging.info(f"Starting working on directory '{os.getcwd()}' ...")
    for filename in os.listdir('.'):
        if not os.path.isfile(filename):
            continue
        if not re.match(r'^\d{8}_\d{4}_.*', filename):
            file_modified = datetime.fromtimestamp(os.path.getmtime(filename))
            file_modified_str = file_modified.strftime("%Y%m%d_%H%M")
            filename_new = f'{file_modified_str}_{filename}'
            logging.info(f'{filename}\t\t--->>>\t\t{filename_new}')
            os.replace(filename, filename_new)
        else:
            logging.debug(f'{filename}\tskipped')
    logging.info(f"Directory processed.")


if __name__ == '__main__':

    logging.basicConfig(format=LOG_FORMAT, filename=LOG_PATH,
                        level=logging.INFO)

    logging.info('#################    Script started   #################')

    with open(FOLDERS_LIST) as folders_list:
        for folder in folders_list:
            folder = folder.strip()
            if folder:
                rename_with_modification_date(folder)

    logging.info('#################    Script stopped   #################')
