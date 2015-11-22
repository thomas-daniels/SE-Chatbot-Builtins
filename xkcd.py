from Module import Command

from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime

import string

module_name = "xkcd"

xkcd_comics = {
    "updated" : datetime(1900, 1, 1),
    "comics"  : []
}

def command_xkcdrandomnumber(cmd, bot, args, msg, event):
    return "[4 // Chosen by fair dice roll. Guaranteed to be random.](http://xkcd.com/221/)"

def command_xkcd(cmd, bot, args, msg, event):
    global xkcd_comics

    if len(args) < 1:
        return "Not enough arguments."

    # If the first parameter is an integer, assume it's the XKCD strip number.
    try:
        id = int(args[0])
        return "http://xkcd.com/{0}".format(id)
    except:
        pass

    # TODO It would be nice if we could also pull the alt-text
    if xkcd_comics["updated"] < datetime.today():
        page = request.urlopen("http://xkcd.com/archive/")
        soup = BeautifulSoup(page, 'html.parser')
        page.close()

        xkcd_comics["comics"] = []
        div = soup.find(id="middleContainer")

        for link in div.find_all("a"):
            for string in link.stripped_strings:
                xkcd_comics["comics"].append({ "id" : link["href"][1:-1], "title": string })

        xkcd_comics["updated"] = datetime.today()

    # Unfortunately we can't just return http://xkcd.com because the OneBox won't render it
    if args[0] == "latest":
        return "http://xkcd.com/{0}".format(xkcd_comics["comics"][0]["id"])

    results = []
    filter = " ".join(args[0:]).lower()

    for comic in xkcd_comics["comics"]:
        if comic["title"].lower().find(filter) > -1:
            results.append(comic)

    if len(results) == 0:
        return "No matching comic found."

    if len(results) == 1:
        return "http://xkcd.com/{0}".format(results[0]["id"])

    if len(results) > 5:
        return "Too many matching comics, be more specific please!"

    bot.room.send_message(":{0} More than one comic found; try `{1}xkcd <#>` with one of these numbers:".format(event.message.id, bot.prefix))
    for xkcd in results:
        bot.room.send_message("{0}: {1}".format(xkcd["id"], xkcd["title"]))

    return None

commands = [
    Command('xkcdrandomnumber', command_xkcdrandomnumber, "Returns a random number, based on an xkcd comic. Syntax: `$PREFIXxkcdrandomnumber`", False, False),
    Command('xkcd', command_xkcd, "Shows the specified xkcd comic. Syntax: `$PREFIXxkcd <id|title|'latest'>`", False, False)
]

