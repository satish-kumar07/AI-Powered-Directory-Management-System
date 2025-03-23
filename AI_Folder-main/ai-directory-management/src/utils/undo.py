import os
import shutil
import logging
import json

def undo_last_operation():
    """Revert the last file operation."""
    try:
        if not os.path.exists('operations.log'):
            logging.info("No operations to undo.")
            return

        with open('operations.log', 'r') as log_file:
            lines = log_file.readlines()
        if not lines:
            logging.info("No operations to undo.")
            return
        last_operation = json.loads(lines[-1])
        operation = last_operation['operation']
        details = last_operation['details']

        if operation == 'move':
            source = details['source']
            target = details['target']
            shutil.move(target, source)
            logging.info(f"Undid move operation: Moved {target} back to {source}")
        elif operation == 'copy':
            target = details['target']
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)
            logging.info(f"Undid copy operation: Deleted {target}")
        elif operation == 'delete':
            path = details['path']
            # Note: Undoing a delete operation is not straightforward without a backup.
            logging.warning(f"Cannot undo delete operation for {path}")

        # Remove the last operation from the log
        with open('operations.log', 'w') as log_file:
            log_file.writelines(lines[:-1])
    except Exception as e:
        logging.error(f"Error undoing last operation: {e}")