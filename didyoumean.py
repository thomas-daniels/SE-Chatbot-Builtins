from __future__ import division
from Module import Command

module_name = "didyoumean"
suggestions = {}


def unique_sorted(s):
    return ''.join(sorted(set(s)))


def did_you_mean(given, cmd_name_list):
    highest_ranked = ("", 0)
    given = unique_sorted(given.lower())
    for name in cmd_name_list:
        nameu = unique_sorted(name)
        score = 0
        for c in given:
            if c in nameu:
                score += 1
        if score >= len(name) / 2 and score > highest_ranked[1]:
            highest_ranked = (name, score)
    if highest_ranked[1] == 0:
        return None
    else:
        return highest_ranked[0]


def command_yes(cmd, bot, args, msg, event):
    if event.user.id in suggestions and suggestions[event.user.id] is not None:
        return bot.command(suggestions[event.user.id])
    else:
        return "There are no command suggestions for you (anymore)."


def command_no(cmd, bot, args, msg, event):
    if event.user.id in suggestions and suggestions[event.user.id] is not None:
        suggestions[event.user.id] = None
        return "Command suggestion cleared."
    else:
        return "Nothing to clear; there are no command suggestions stored for you."


def on_bot_load(bot):
    orig_method = bot.command

    def command_with_didyoumean(cmd, msg, event):
        result = orig_method(cmd, msg, event)
        if result == "Command not found.":
            dym = did_you_mean(cmd.split(' ')[0].lower(), [command.name for command in bot.modules.list_commands()])
            if dym is None:
                suggestions[event.user.id] = None
                return "Command not found."
            else:
                suggestions[event.user.id] = dym + " " + " ".join(cmd.split(cmd, " ")[1:])
                return "Command not found. Did you mean: `%s`?" % dym
        else:
            suggestions[event.user.id] = None
            return result

    bot.command = command_with_didyoumean

commands = [Command('yes', command_yes, "Executes the suggested command after a 'Did you mean?' response", False, False, None, None),
            Command('no', command_no, "Clears the command suggestion after a 'Did you mean?' response", False, False, None, None)]
