class MetaInfo:

    bot_version = "0.3.1"
    bot_invite_link = "https://discordapp.com/api/oauth2/authorize?client_id=479774802899501056&permissions=8&scope=bot"
    owner_server_invite_link = "https://discord.gg/qDJdDEn"
    embed_thumbnail_url = "https://cdn.discordapp.com/attachments/479409875860979712/492483239580008458/Mayuri_Shiina.png"

    def get_bot_version():
        return __class__.bot_version

    def get_bot_invite_link():
        return __class__.bot_invite_link

    def get_owner_server_invite_link():
        return __class__.owner_server_invite_link

    def get_embed_thumbnail_url():
        return __class__.embed_thumbnail_url