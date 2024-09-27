# hexchat_onionshare.py
import hexchat
import subprocess
import re

__module_name__ = "OnionShare File Transfer"
__module_version__ = "1.0"
__module_description__ = "Script to send and receive files over OnionShare via Tor IRC chat"

def send_file(word, word_eol, userdata):
    if len(word) < 2:
        hexchat.prnt("Usage: /sendfile <file_path>")
        return hexchat.EAT_ALL

    file_path = word[1]
    try:
        result = subprocess.run(['onionshare', '--share', file_path], capture_output=True, text=True)
        match = re.search(r'http://[a-z0-9]+\.onion/[a-z0-9]+', result.stdout)
        if match:
            link = match.group(0)
            hexchat.command(f"MSG {hexchat.get_info('channel')} File available at: {link}")
        else:
            hexchat.prnt("Failed to generate OnionShare link.")
    except Exception as e:
        hexchat.prnt(f"Error: {e}")

    return hexchat.EAT_ALL

def receive_file(word, word_eol, userdata):
    if len(word) < 2:
        hexchat.prnt("Usage: /receivefile <onionshare_link>")
        return hexchat.EAT_ALL

    link = word[1]
    try:
        subprocess.run(['onionshare', '--receive', link])
        hexchat.prnt(f"File received from {link}")
    except Exception as e:
        hexchat.prnt(f"Error: {e}")

    return hexchat.EAT_ALL

hexchat.hook_command("sendfile", send_file, help="/sendfile <file_path> - Share a file using OnionShare")
hexchat.hook_command("receivefile", receive_file, help="/receivefile <onionshare_link> - Receive a file using OnionShare")

hexchat.prnt(f"{__module_name__} version {__module_version__} loaded")