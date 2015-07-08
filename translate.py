import thread
import requests
import random
import os
from Module import Command
from Config import Config

translation_languages = {}
end_lang = None
translation_chain_going_on = False
translation_switch_going_on = False
yandex_api_key = None


def command_detectlang(cmd, bot, args, msg, event):
    if yandex_api_key is None:
        return "Warning: no Yandex API Key found. Put one in `botdata/translate/yandex_api_key.txt`."
    detected = detect_lang(args[0])
    if detected[0] is False:
        return "Error code: %i" % (detected[0],)
    if len(detected[1]) == 0:
        return r"\[Powered by [Yandex Translate](https://translate.yandex.com)\] No language found."
    return r"\[Powered by [Yandex Translate](https://translate.yandex.com)\] Detected language: %s (%s)" % (detected[1], translation_languages[detected[1]])


def command_translationchain(cmd, bot, args, msg, event):
    global translation_languages
    global translation_chain_going_on
    if yandex_api_key is None:
        return "Warning: no Yandex API Key found. Put one in `botdata/translate/yandex_api_key.txt`."
    if event.user.id not in bot.owner_ids:
        return "The `translationchain` command is a command that posts many messages and it does not post all messages, and causes that some messages that have to be posted after the chain might not be posted, so it is an owner-only command now."
    if len(args) < 4:
        return "Not enough arguments."
    try:
        translation_count = int(args[0])
    except ValueError:
        return "Invalid arguments."
    if translation_count < 1:
        return "Invalid arguments."
    if not translation_chain_going_on:
        if not args[1] in translation_languages or not args[2] in translation_languages:
            return "Language not supported."
        translation_chain_going_on = True
        thread.start_new_thread(translationchain, (bot, args[3], args[1], args[2], translation_count))
        return "Translation chain started. Translation made by [Yandex Translate](https://translate.yandex.com). Some messages in the chain might not be posted due to a reason I don't know."
    else:
        return "There is already a translation chain going on."


def command_translationswitch(cmd, bot, args, msg, event):
    global translation_switch_going_on
    global translation_languages
    if yandex_api_key is None:
        return "Warning: no Yandex API Key found. Put one in `botdata/translate/yandex_api_key.txt`."
    if event.user.id not in bot.owner_ids:
        return "The `translationswitch` command is a command that posts many messages and it does not post all messages, and causes that some messages that have to be posted after the chain might not be posted, so it is an owner-only command now."
    if translation_switch_going_on:
        return "There is already a translation switch going on."
    if len(args) < 4:
        return "Not enough arguments."
    try:
        translation_count = int(args[0])
    except ValueError:
        return "Invalid arguments."
    if translation_count < 2:
        return "Invalid arguments."
    if (translation_count % 2) == 1:
        return "Translation count has to be an even number."
    if not args[1] in translation_languages or not args[2] in translation_languages:
        return "Language not supported."
    translation_switch_going_on = True
    thread.start_new_thread(translationswitch, (bot, args[3], args[1], args[2], translation_count))
    return "Translation switch started. Translation made by [Yandex Translate](https://translate.yandex.com). Some messages in the switch might not be posted due to a reason I don't know."


def command_translate(cmd, bot, args, msg, event):
    global translation_languages
    if yandex_api_key is None:
        return "Warning: no Yandex API Key found. Put one in `botdata/translate/yandex_api_key.txt`."
    if len(args) < 3:
        return "Not enough arguments."
    if args[0] == args[1]:
        return "There's no point in having the same input language as output language."
    if not args[0] in translation_languages or not args[1] in translation_languages:
        return "Language not supported."
    translated = translate(args[2], args[0], args[1])
    if translated[0] is True:
        return r"\[Powered by [Yandex Translate](https://translate.yandex.com)\] %s" % translated[1]
    else:
        return "Error code: %i" % (translated[1],)


def translationchain(bot, text, start_lang, end_lang, translation_count):
    global translation_languages
    global translation_chain_going_on
    i = 0
    curr_lang = start_lang
    next_lang = None
    curr_text = text
    choices = list(translation_languages)
    if start_lang == end_lang:
        choices.remove(start_lang)
    else:
        choices.remove(start_lang)
        choices.remove(end_lang)
    while i < translation_count - 1:
        if next_lang is not None:
            curr_lang = next_lang
        while True:
            next_lang = random.choice(choices)
            if next_lang != curr_lang:
                break
        result = translate(curr_text, curr_lang, next_lang)[1]
        curr_text = result
        bot.room.send_message("Translate %s-%s: %s" % (curr_lang, next_lang, result))
        i += 1
    final_result = translate(curr_text, next_lang, end_lang)[1]
    bot.room.send_message("Final translation result (%s-%s): %s" % (next_lang, end_lang, final_result))
    translation_chain_going_on = False


def translationswitch(bot, text, lang1, lang2, translation_count):
    global translation_switch_going_on
    i = 1
    curr_text = text
    while i <= translation_count:
        if (i % 2) == 0:
            lang_order = (lang2, lang1)
        else:
            lang_order = (lang1, lang2)
        curr_text = translate(curr_text, lang_order[0], lang_order[1])[1]
        msg_text = "Translate %s-%s: %s" if i != translation_count else "Final result (%s-%s): %s"
        bot.room.send_message(msg_text % (lang_order + (curr_text,)))
        i += 1
    translation_switch_going_on = False


def detect_lang(text):
    request_url = "https://translate.yandex.net/api/v1.5/tr.json/detect"
    params = {"key": yandex_api_key, "text": text}
    resp_json = requests.get(request_url, params).json()
    if resp_json["code"] != 200:
        return False, resp_json["code"]
    return True, resp_json["lang"]


def translate(text, start_lang, end_lang):
    request_url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    params = {"key": yandex_api_key, "lang": "%s-%s" % (start_lang, end_lang),
              "text": text}
    resp_json = requests.get(request_url, params).json()
    if resp_json["code"] != 200:
        return False, resp_json["code"]
    translated_text = " ".join(resp_json["text"])
    return True, translated_text


def trans_arg_parsing(full_cmd):
    cmd_args = full_cmd.split(' ')
    args = cmd_args[1:]
    to_translate = " ".join(args[2:])
    args = args[:2]
    args.append(to_translate)
    return args


def transcs_arg_parsing(full_cmd):
    cmd_args = full_cmd.split(' ')
    args = cmd_args[1:]
    to_translate = " ".join(args[3:])
    args = args[:3]
    args.append(to_translate)
    return args


def detectlang_arg_parsing(full_cmd):
    return [full_cmd.split(" ", 1)[1]]


def on_bot_load(bot):
    global translation_languages
    global yandex_api_key
    if not os.path.isfile("botdata/translate/yandex_api_key.txt"):
        print("Warning: no Yandex API Key found for the translation module. Put one in botdata/translate/yandex_api_key.txt")
        return
    with open("botdata/translate/yandex_api_key.txt") as f:
        yandex_api_key = f.read().strip()
    request_url = "https://translate.yandex.net/api/v1.5/tr.json/getLangs"
    params = {"key": yandex_api_key, "ui": "en"}
    resp_json = requests.get(request_url, params).json()
    translation_languages = resp_json["langs"]


commands = [
    Command('detectlang', command_detectlang, "Detects the language of a piece of text using [Yandex Translate](https://translate.yandex.com/). Syntax: `$PREFIXdetectlang Input text here`", False, False, False, detectlang_arg_parsing),
    Command('translate', command_translate, "Translates text using [Yandex Translate](https://translate.yandex.com/). Syntax: `$PREFIXtranslate input_lang output_lang Text to translate.`. `input_lang` and `output_lang` are language codes such as `en`, `fr` and `auto`.", False, False, False, trans_arg_parsing),
    Command('translationchain', command_translationchain, "Owner-only command. Creates a chain of translations using [Yandex Translate](https://translate.yandex.com/). Syntax: `$PREFIXtranslationchain steps_number input_lang output_lang Text to translate.`", False, True, False, transcs_arg_parsing),
    Command('translationswitch', command_translationswitch, "Owner-only command. Creates a chain of translations using [Yandex Translate](https://translate.yandex.com/), consisting of two languages. Syntax: `$PREFIXtranslationswitch steps_number lang1 lang2 Text to translate.`", False, True, False, transcs_arg_parsing)
]
module_name = "translate"
save_subdir = "translate"
