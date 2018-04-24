# -*- coding: utf8 -*-
import tempfile
import braincert
import urllib.request
import config
import re
from subprocess import call

def set_new_at_job(class_instance_id, time):
    """
    Sets new "at" job in Linux (man at for more)
    The job is to add students to the online class in Braincert and send them invitations in Telegram
    :param class_instance_id: id from Class_Instance DB
    :param time: time in HH:MM DD.MM.YYYY format
    :return: "at" command's job id / None if error occured
    """
    tmp = tempfile.NamedTemporaryFile(mode='r+t')
    # Actually, sender.py will send message
    command = 'echo python3 -c \'import braincert; braincert.join_braincert_class({0!s})\' | at {1!s}'.format(class_instance_id, time, text)
    # Because of some warnings, all data is sent to stderr instead of stdout.
    # But it's normal
    call(command, shell=True, stderr=tmp)
    print(command)
    tmp.seek(0)
    for line in tmp:
        if 'job' in line:
            return line.split()[1]
    tmp.close()
    return None

def download_from_url(file_url, file_name):
    """
    Downloads a file from a given url
    """

    # Remove redundant \\ characters in a Braincert-generated url like this:
    # https:\\/\\/d2i7n1mt3ez1zt.cloudfront.net\\/rkFr7hUOG.webm?Expires=1520000586&Signature=N~ClHyxTCLFVPtEcn30i5iExT7rgNjT4oPwV2Gay2uZjcpfYw5PLIFDj-UowVFyRT7I7bhd84Fx0bUg6vTBJh-0t7t63C2AsqXd0r4n8MDoozRSSeISS2ppWKekZ98d0CXlWrSILh~37RJg33IQT7LYcYiqPXDOj1t1UdgWMUJc_&Key-Pair-Id=APKAINGTP6O5WANPM7YQ
    updated_url = re.sub('\\\\','',file_url)

    full_file_path = config.download_path + file_name
    urllib.request.urlretrieve (updated_url, full_file_path)

    return(full_file_path)
