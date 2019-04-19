from modules.__init__ import discord, commands, link

Bot = commands.Bot(command_prefix= "$")

def add_fie(emb, what):
        """ 
emb = Embed
What = where key = name, value = value
        """
        for field in what:
                emb.add_field(name= field, value= what[field])
        return emb 

def cemb(title, colour, author= None, a_author= None):
        """
title: title of the embed
colour: color of the embed
author: need to footer, if autor is none then footer now will be exist
        """
        global link
        emb = discord.Embed(title= title, colour= colour)
        if a_author is not None:
                emb.set_author(name= a_author.name, icon_url= a_author.avatar_url, url= link.format(a_author.id))
        if author is not None:
                emb.set_footer(text= "Запросил " + author.display_name, icon_url= author.avatar_url)
        return emb
