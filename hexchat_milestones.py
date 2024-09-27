# hexchat_milestones.py
import hexchat

__module_name__ = "Project Milestones Tracker"
__module_version__ = "1.0"
__module_description__ = "Script to track project milestones in HexChat"

milestones = {}

def add_milestone(word, word_eol, userdata):
    if len(word) < 2:
        hexchat.prnt("Usage: /addmilestone <milestone>")
        return hexchat.EAT_ALL

    milestone = word_eol[1]
    milestone_id = len(milestones) + 1
    milestones[milestone_id] = {'milestone': milestone, 'completed': False}
    hexchat.prnt(f"Milestone added: [{milestone_id}] {milestone}")

    return hexchat.EAT_ALL

def list_milestones(word, word_eol, userdata):
    if not milestones:
        hexchat.prnt("No milestones added.")
        return hexchat.EAT_ALL

    hexchat.prnt("Project Milestones:")
    for milestone_id, data in milestones.items():
        status = "Completed" if data['completed'] else "Pending"
        hexchat.prnt(f"[{milestone_id}] {data['milestone']} - {status}")

    return hexchat.EAT_ALL

def complete_milestone(word, word_eol, userdata):
    if len(word) < 2:
        hexchat.prnt("Usage: /completemilestone <milestone_id>")
        return hexchat.EAT_ALL

    try:
        milestone_id = int(word[1])
        if milestone_id in milestones:
            milestones[milestone_id]['completed'] = True
            hexchat.prnt(f"Milestone [{milestone_id}] marked as completed.")
        else:
            hexchat.prnt(f"Milestone ID {milestone_id} does not exist.")
    except ValueError:
        hexchat.prnt("Invalid milestone ID.")

    return hexchat.EAT_ALL

hexchat.hook_command("addmilestone", add_milestone, help="/addmilestone <milestone> - Add a new project milestone")
hexchat.hook_command("listmilestones", list_milestones, help="/listmilestones - List all project milestones")
hexchat.hook_command("completemilestone", complete_milestone, help="/completemilestone <milestone_id> - Mark a milestone as completed")

hexchat.prnt(f"{__module_name__} version {__module_version__} loaded")