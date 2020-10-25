import discord
import configuration.variables as variables

STAFFROLES = {
    variables.SERVEROWNER, # Role @Server Owner.
    variables.SERVERMODERATOR, # Role @Server Moderator.
}

BOTCHANNELS = {
    variables.BOTCOMMANDS, # Channel #bot-commands.
    variables.TRUSTEDCHAT, # Channel #trusted-chat.
    variables.MODERATORCHAT, # Channel #moderator-chat.
    variables.BOTDISCUSSION, # Channel #bot-discussion.
}

LOCKDOWNCHANNELS = {
    variables.GENERALCHAT, # Channel #general-chat.
    variables.RANDOMCHAT, # Channel #random-chat.
    variables.BOTCOMMANDS, # Channel #bot-commands.
    variables.SMASHGENERAL, # Channel #smash-general.
    variables.SMASHBATTLES, # Channel #smash-battles.
    variables.POKEMONGENERAL, # Channel #pokémon-general.
    variables.POKEMONTRADES, # Channel #pokémon-trades.
    variables.POKEMONBATTLES, # Channel #pokémon-battles.
}

UNFILTERCHANNELS = {
    variables.BOTDISCUSSION, # Channel #bot-discussion.
    variables.TRUSTEDCHAT, # Channel #trusted-chat.
    variables.MODERATORCHAT, # Channel #moderator-chat.
    variables.BOTLOGS, # Channel #bot-logs.
    variables.REQUESTLOGS, # Channel #request-logs.
    variables.ACTIONLOGS, # Channel #action-logs.
    variables.MESSAGELOGS, # Channel #message-logs.
    variables.SERVERLOGS, # Channel #server-logs.
}

MESSAGEFILTER = {
    "freeshop",
    "freshop",
    "freehop",
    "freesh0p",
    "threeshop",
    "freestore", # Variations of "freeshop."
    "ciangel",
    "tikdevil",
    "tikshop",
    "utikdownloadhelper",
    "utik", # Variation of "utikdownloadhelper."
    "funkii",
    "funk11",
    "funki",
    "funkey", # Variations of "funkii."
    "usbhelper",
    "villian3ds",
    "vi11ian3ds", # Variation of "villian3ds."
    "wareznx",
    "homebrewgeneralshop",
    "hbgshop", # Variation of "homebrewgeneralshop."
    "goldbrick",
    "3dsiso",
    "3dscia",
    "wiiuiso",
    "emuparadise",
    "loveroms",
    "coolroms",
    "doperoms",
    "vimm",
    "unbanmii",
    "easymode9",
    "sysconfig",
 } # The filter is mostly just piracy-related terms. I'll probably add more soon.

LOGCHANNELS = {
    variables.BOTLOGS, # Channel #bot-logs.
    variables.REQUESTLOGS, # Channel #request-logs.
    variables.ACTIONLOGS, # Channel #action-logs.
    variables.MESSAGELOGS, # Channel #message-logs.
    variables.SERVERLOGS, # Channel #server-logs.
}