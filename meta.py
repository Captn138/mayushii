"""Contain :class:`~meta.MetaInfo` class."""


class MetaInfo:
    """Store a bunch of values tu be called in other methods."""

    bot_version = "0.4.0"
    bot_invite_link = "https://discordapp.com/api/oauth2/authorize?client_id=479774802899501056&permissions=8&scope=bot"
    owner_server_invite_link = "https://discord.gg/qDJdDEn"
    embed_thumbnail_url = "https://cdn.discordapp.com/attachments/479409875860979712/492483239580008458/Mayuri_Shiina.png"
    owner_id = 202779792599285760

    def get_bot_version():
        """Get bot version.

        Returns:
            str: The bot version
        """
        return __class__.bot_version

    def get_bot_invite_link():
        """Get bot invite link.

        Returns:
            str: The bot invite link
        """
        return __class__.bot_invite_link

    def get_owner_server_invite_link():
        """Get owner server invite link.

        Returns:
            _tstrpe_: The owner server invite link
        """
        return __class__.owner_server_invite_link

    def get_embed_thumbnail_url():
        """Get thumbnail for embeds.

        Returns:
            str: The thumbnail for embeds
        """
        return __class__.embed_thumbnail_url

    def get_owner_id():
        """Get owner Discord ID.

        Returns:
            int: The owner Discord ID
        """
        return __class__.owner_id
