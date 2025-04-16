"""
This module provides functions to work with files and directories.
"""

import grp
import os
import pwd
import re
from datetime import datetime
from typing import Optional, Pattern

# ---------------------------------------------------------------------------------------------------- #


def get_files(directory: str, pattern: Optional[str] = None, include_subdirs: bool = True) -> list[str]:
    """
    This function retrieves a list of files in the specified directory and all its subdirectories recursively.
    Optionally, it can filter files using a regex pattern.

    Args:
        directory (str): The path to the directory.
        pattern (Optional[str]): A regex pattern to filter files. If None, all files are returned.
        include_subdirs (bool): Whether to include files from subdirectories. Defaults to True.

    Returns:
        list[str]: A list of file paths.

    Raises:
        FileNotFoundError: If the directory does not exist.

    Example:
        >>> get_files('/path/to/directory')
        ['/path/to/directory/file1.txt', '/path/to/directory/subdir/file2.txt', '/path/to/directory/file3.py']
        >>> get_files('/path/to/directory', r'\.txt$')
        ['/path/to/directory/file1.txt', '/path/to/directory/subdir/file2.txt']
    """
    if not os.path.exists(directory) or not os.path.isdir(directory):
        raise FileNotFoundError(
            f"The directory '{directory}' does not exist.")

    # Compile regex pattern if provided
    regex: Optional[Pattern] = None
    if pattern is not None:
        regex = re.compile(pattern)

    files = []
    for root, dirnames, filenames in os.walk(directory):
        if not include_subdirs and root != directory:
            # If not including subdirectories, only process the top-level directory
            break  # Stop after the first directory

        # Include all subdirectories
        for dirname in dirnames:
            dir_path = os.path.join(root, dirname)
            # Apply regex filter if pattern was provided
            if regex is None or regex.search(dir_path):
                files.append(dir_path)

        # Include files in the current directory
        for filename in filenames:
            file_path = os.path.join(root, filename)
            # Apply regex filter if pattern was provided
            if regex is None or regex.search(file_path):
                files.append(file_path)
    return files

# ---------------------------------------------------------------------------------------------------- #


def get_file_or_dir_infos(path: str) -> dict:
    """
    Get file or directory information such as size, last modified date, and permissions.

    Args:
        path (str): Path to the file or directory.

    Returns:
        dict: Dictionary containing file information.
    Raises:
        FileNotFoundError: If the path does not exist.

    Example:
        >>> get_file_or_dir_infos('/path/to/file.txt')
        {
            'name': 'file.txt',
            'path': '/path/to/file.txt',
            'is_dir': False,
            'size': 1024,
            'last_modified': 'Oct 01 12:30',
            'permissions': '644',
            'inode': 123456,
            'device': 2050,
            'links': 1,
            'owner_id': 1000,
            'group_id': 1000,
            'owner': 'username',
            'group': 'groupname'
        }
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")

    file_stats = os.stat(path)

    # Format last modified date to 'MMM DD HH:MM' format if date is from less than a year
    # ago, otherwise use 'MMM DD YYYY' format
    last_modified = file_stats.st_mtime
    if (datetime.now() - datetime.fromtimestamp(last_modified)).days < 365:
        last_modified = datetime.fromtimestamp(
            last_modified).strftime("%h %d %H:%M")
    else:
        last_modified = datetime.fromtimestamp(
            last_modified).strftime("%h %d %Y")

    return {
        "name": os.path.basename(path),
        "path": path,
        "is_dir": os.path.isdir(path),
        "size": file_stats.st_size,
        "last_modified": last_modified,
        "permissions": oct(file_stats.st_mode)[-3:],
        "inode": file_stats.st_ino,
        "device": file_stats.st_dev,
        "links": file_stats.st_nlink,
        "owner_id": file_stats.st_uid,
        "group_id": file_stats.st_gid,
        "owner": pwd.getpwuid(file_stats.st_uid).pw_name,
        "group": grp.getgrgid(file_stats.st_gid).gr_name
    }

# ---------------------------------------------------------------------------------------------------- #


def permissions_to_string(permissions: int | str) -> str:
    """
    Convert file permissions from integer to string format.

    Args:
        permissions (int or str): File permissions in integer or string format.
        This is typically a 3-digit octal number (e.g., 755) or a string representation ('755').
        Note: The function assumes that the input `permissions` is a valid octal representation of file permissions.
    Returns:
        str: File permissions in string format (e.g., 'rwxr-xr-x').

    Example:
        >>> permissions_to_string(755)
        'rwxr-xr-x'
        >>> permissions_to_string('644')
        'rw-r--r--'
    """
    # Convert to integer if string was provided
    if isinstance(permissions, str):
        permissions = int(permissions, 8)

    formatted_permissions = ""
    for i in range(2, -1, -1):
        permission_set = (permissions >> (i * 3)) & 0b111
        formatted_permissions += "".join(
            ["r" if permission_set & 0b100 else "-",
             "w" if permission_set & 0b010 else "-",
             "x" if permission_set & 0b001 else "-"])
    return formatted_permissions

# ---------------------------------------------------------------------------------------------------- #
