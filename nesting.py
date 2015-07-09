# The commands listed in this file can be read and loaded as a Module into a MetaModule by the load_module() function

# Add necessary import to this file, including:
# from Module import Command

# import SaveIO # For if you want to save and load objects for this module.
# save_subdir = '<subdir_name>' # Define a save subdirectory for this Module, must be unique in the project. If this is not set, saves and loads will fail.
# SaveIO.save(<object>, save_subdir, <filename>)  # Saves an object, filename does not need an extension.
# SaveIO.load(save_subdir, <filename>)  # Loads and returns an object, filename does not need an extension.

def nesting_deco(get_output):
    def check_nested(cmd_args, message, event):
        content = cmd_args
        final_content = ""
        temp_content = ""
        open_brackets = 0

        i = 0
        while i < len(content):
            to_add = content[i]
            if content[i]=='{' and i < len(content) - 1 and content[i+1]=='{':
                i += 1
                if open_brackets == 0:
                    to_add = ""
                else:
                    to_add += content[i]
                open_brackets += 1
            elif content[i]=='}' and i < len(content) - 1 and content[i+1]=='}':
                i += 1
                if open_brackets==1:
                    to_add = ""
                    final_content += check_nested(temp_content, message, event)
                    temp_content = ""
                else:
                    to_add += content[i]
                open_brackets -= 1
                if open_brackets < 0:
                    return "Your nesting brackets '{{' and '}}' don't match up"
            if open_brackets>0:
                temp_content += to_add
            else:
                final_content += to_add
            i += 1

        if open_brackets==0:
            print final_content
            return get_output(final_content, message, event)
        else:
           return "Your nesting brackets '{{' and '}}' don't match up"
    return check_nested

def on_bot_load(bot): # This will get called when the bot loads (after your module has been loaded in), use to perform additional setup for this module.
    bot.get_output = nesting_deco(bot.get_output)

# def on_bot_stop(bot): # This will get called when the bot is stopping.
#     pass

# def on_event(event, client, bot): # This will get called on any event (messages, new user entering the room, etc.)
#     pass

# Logic for the commands goes here.
#
# def <command exec name>(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
#     return "I'm in test1"
#
# def <command exec name>(cmd, bot, args, msg, event): # cmd refers to the Command you assign this function to
#     return "I'm in test1"
#
# ...


commands = [  # A list of all Commands in this Module.
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False), <owner only> (= False), <char check>(*) (= True), <special arg parsing method>(**) (= None) ),
    # Command( '<command name>', <command exec name>, '<help text>' (optional), <needs privilege> (= False), <owner only> (= False), <char check>(*) (= True), <special arg parsing method>(**) (= None) ),
    # ...
]

# (*) <char check> = the bot only allows a specific set of characters
# and if any character is used in a command outside this set, the bot would give you an error message.
# Setting this parameter to False avoids this char check.

# (**) <special arg parsing method> = Some commands require a non-default argument parsing method.
# Pass it there when necessary. It must return the array of arguments.

module_name = "nesting"
