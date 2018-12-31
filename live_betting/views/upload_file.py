"""
Insta485 create view.

URLs include:
/accounts/create/
"""
import os
import tempfile
import shutil
import hashlib
import insta485


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


def upload_file(file):
    """Upload file to server."""
    # Save POST request's file object to a temp file
    dummy, temp_filename = tempfile.mkstemp()
    file.save(temp_filename)

    # Compute filename
    hash_txt = sha256sum(temp_filename)
    dummy, suffix = os.path.splitext(file.filename)
    hash_filename_basename = hash_txt + suffix
    hash_filename = os.path.join(
        insta485.app.config["UPLOAD_FOLDER"],
        hash_filename_basename
    )

    # Move temp file to permanent location
    shutil.copy(temp_filename, hash_filename)
    insta485.app.logger.debug("Saved %s", hash_filename_basename)

    return hash_filename, hash_filename_basename
