from Module import Command, Module, MetaModule
from Module import MalformedModuleException, ModuleDoesNotExistException
import sys

def module(cmd, bot, args, msg, event):
    if len(args) < 1:
        return "Not enough arguments. Syntax: `module <action> <options...>`"
    if args[0] == "help":
        return "Contains controls for modules.\n`module enable <name>` - enables a module\n`module disable <name>` - " \
            "disables a module\n"
    elif args[0] == "enable":
        return module_enable(cmd, bot, args, msg, event)
    elif args[0] == "disable":
        return module_disable(cmd, bot, args, msg, event)


def module_disable(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."
    mod = args[1]
    mod_obj = bot.modules.find_module_by_name(mod)
    try:
        del bot.modules[mod_obj]
        return "Module disabled."
    except AttributeError:
        return "No such module."

def module_enable(cmd, bot, args, msg, event):
    if len(args) < 2:
        return "Not enough arguments."
    try:
        metamod = MetaModule([args[1]], bot, 'temp')
        bot.modules.modules.append(metamod.modules[0])
    except MalformedModuleException or ModuleDoesNotExistException, e:
        exc_type, exc_value, exc_trace = sys.exc_info()
        print '[ModuleControls] ERROR: Module could not be loaded: details follow.'
        print '               MESSAGE: ' + exc_value
        print exc_trace
        return "Module cannot be loaded - check the console for details."



commands = [
    Command("module", module, "Contains controls for modules. Run `module help` for details.", True, False)
]