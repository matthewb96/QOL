"""
    Module for interacting with git, contains functions for accessing tag information
    in order to automatically update project version numbers and a changelog based on
    tags.
"""

##### IMPORTS #####
# Standard imports
import subprocess as sp
from datetime import datetime

##### FUNCTIONS #####
def getVersion(path):
    """ Gets the full version number from a git tag using the git describe command.

    Parameters
    ----------
    path: pathlib.Path, optional
        Path to a file to save the version number and datetime.now()
        to, datetime will be saved in iso format. Defaults to None
        where no file is created.

    Returns
    -------
    version: str
        Output from git describe command.

    Warning
    -------
    Git must be installed and included in PATH for this function to work,
    and it must be inside a git respository.
    """
    gitOut = sp.check_output(['git', 'describe', '--tags', '--always'])
    version = gitOut.strip().decode('utf-8')

    # Create a version file if path is given
    if path is not None:
        out = f'{version}\n{datetime.now()}'
        with open(path, 'wt') as f:
            f.write(out)

    return version

def getAllTags():
    """ Gets the tag name, title and description for all the git tags.

    Use git tag commands to get the information.

    Returns
    -------
    names: list of str
        List of all the tag names.
    titles: list of str
        List of all the tag titles, same length as `names`.
    descs: list of str
        List of all the tag descriptions, same length as `names`.

    Warning
    -------
    Git must be installed and included in PATH for this function to work,
    and it must be inside a git respository.
    """
    # Get the basic tag info, with most recent at the top
    tags = sp.check_output(['git', 'tag', '-l', '-n1']).decode('utf-8').split('\n')
    tags.reverse()

    # Get the name, title and description for all the tags
    names, titles, descs = [], [], []
    for t in tags:
        if t.strip() == '':
            continue
        # Split t on the first space
        loc = t.find(' ')
        nm = t[:loc].strip()
        names.append(nm)
        titles.append(t[loc:].strip())
        # Get the description for this tag
        d = sp.check_output(['git', 'tag', '-l', f'{nm}', '-n100']).decode('utf-8')
        d = d[d.find('\n'):]
        d = [i.strip() for i in d.split('\n')]
        descs.append('\n'.join(d))

    return names, titles, descs
