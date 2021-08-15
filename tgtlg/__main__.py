#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
# modified by reaitten/orsixtyone


import io
import logging
import os
import sys
import traceback

from pyrogram import Client, filters, idle
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.raw.functions.bots import SetBotCommands
from pyrogram.raw.base import BotCommand

'''
from tgtlg import (
    API_HASH,
    APP_ID,
    AUTH_CHANNEL,
    CANCEL_COMMAND_G,
    CLEAR_THUMBNAIL,
    CLONE_COMMAND_G,
    DOWNLOAD_LOCATION,
    GET_SIZE_G,
    GLEECH_COMMAND,
    GLEECH_UNZIP_COMMAND,
    GLEECH_ZIP_COMMAND,
    LEECH_COMMAND,
    LEECH_UNZIP_COMMAND,
    LEECH_ZIP_COMMAND,
    LOG_COMMAND,
    LOGGER,
    PYTDL_COMMAND,
    RENEWME_COMMAND,
    RENAME_COMMAND,
    SAVE_THUMBNAIL,
    STATUS_COMMAND,
    TELEGRAM_LEECH_UNZIP_COMMAND,
    TELEGRAM_LEECH_COMMAND,
    TG_BOT_TOKEN,
    UPLOAD_COMMAND,
    YTDL_COMMAND,
    GYTDL_COMMAND,
    GPYTDL_COMMAND,
    TOGGLE_VID,
    TOGGLE_DOC,
)
'''

from tgtlg import (
    DOWNLOAD_LOCATION,
    LOGGER,
    app,
)

from tgtlg import bcmds
from tgtlg.bot_utils.bot_cmds import BotCommands
from tgtlg.helper_funcs.download import down_load_media_f
from tgtlg.plugins.call_back_button_handler import button

# the logging things
from tgtlg.plugins.choose_rclone_config import rclone_command_f
from tgtlg.plugins.custom_thumbnail import clear_thumb_nail, save_thumb_nail
from tgtlg.plugins.incoming_message_fn import (
    g_clonee,
    g_yt_playlist,
    incoming_message_f,
    incoming_purge_message_f,
    incoming_youtube_dl_f,
    rename_tg_file,
)

from tgtlg.plugins.new_join_fn import *
from tgtlg.plugins.rclone_size import check_size_g, g_clearme
from tgtlg.helper_funcs.fn.status_message_fn import (
    cancel_message_f,
    eval_message_f,
    exec_message_f,
    status_message_f,
    upload_document_f,
    upload_log_file,
    upload_as_doc,
    upload_as_video,
)
from tgtlg.modules.torrent import *

from tgtlg.helper_funcs.fn.nan_message_fn import (
    nan
)

if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    # start app
    app.start()
    # set bot cmds in __init__.py
    bcmds(app)
    # grab bot username from logged in user (app)
    buname = "@" + app.get_me().username
    # for main leech
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=filters.command(
            [
                BotCommands.LeechCommand,
                BotCommands.LeechCommand + buname,
                BotCommands.ExtractCommand + buname,
                BotCommands.ExtractCommand,
                BotCommands.ArchiveCommand + buname,
                BotCommands.ArchiveCommand,
                BotCommands.RcloneLeechCommand + buname,
                BotCommands.RcloneLeechCommand,
                BotCommands.RcloneLeechExtractCommand + buname,
                BotCommands.RcloneLeechExtractCommand,
                BotCommands.RcloneLeechArchiveCommand + buname,
                BotCommands.RcloneLeechArchiveCommand,
            ]
        )
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_message_handler)
    incoming_telegram_download_handler = MessageHandler(
        down_load_media_f,
        filters=filters.command([BotCommands.TelegramLeechCommand, BotCommands.TelegramLeechCommand + buname, BotCommands.TelegramLeechExtractCommand, BotCommands.TelegramLeechExtractCommand + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_telegram_download_handler)
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=filters.command([BotCommands.PurgeCommand, BotCommands.PurgeCommand + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_purge_message_handler)
    incoming_clone_handler = MessageHandler(
        g_clonee,
        filters=filters.command([f"{BotCommands.CloneCommand}", f"{BotCommands.CloneCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_clone_handler)
    incoming_size_checker_handler = MessageHandler(
        check_size_g,
        filters=filters.command([f"{BotCommands.GetRcloneSizeCommand}", f"{BotCommands.GetRcloneSizeCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_size_checker_handler)
    incoming_g_clear_handler = MessageHandler(
        g_clearme,
        filters=filters.command([f"{BotCommands.ReNewMeCommand}", f"{BotCommands.ReNewMeCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_g_clear_handler)
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=filters.command([BotCommands.YoutubeDownloaderCommand, BotCommands.YoutubeDownloaderCommand + buname, BotCommands.RcloneYoutubeDownloaderCommand, BotCommands.RcloneYoutubeDownloaderCommand + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_dl_handler)
    incoming_youtube_playlist_dl_handler = MessageHandler(
        g_yt_playlist,
        filters=filters.command([BotCommands.PlaylistYoutubeDownloaderCommand, BotCommands.PlaylistYoutubeDownloaderCommand + buname, BotCommands.RcloneYoutubeDownloaderCommand, BotCommands.RcloneYoutubeDownloaderCommand + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(incoming_youtube_playlist_dl_handler)
    status_message_handler = MessageHandler(
        status_message_f,
        filters=filters.command([f"{BotCommands.StatusCommand}", f"{BotCommands.StatusCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(status_message_handler)
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=filters.command([f"{BotCommands.CancelCommand}", f"{BotCommands.CancelCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(cancel_message_handler)
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=filters.command([f"{BotCommands.ExecuteCommand}", f"{BotCommands.ExecuteCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(exec_message_handler)
    eval_message_handler = MessageHandler(
        eval_message_f,
        filters=filters.command([f"{BotCommands.EvaluateCommand}", f"{BotCommands.EvaluateCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(eval_message_handler)
    rename_message_handler = MessageHandler(
        rename_tg_file,
        filters=filters.command([f"{BotCommands.RenameCommand}", f"{BotCommands.RenameCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(rename_message_handler)
    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=filters.command([f"{BotCommands.UploadCommand}", f"{BotCommands.UploadCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_document_handler)
    upload_log_handler = MessageHandler(
        upload_log_file,
        filters=filters.command([f"{BotCommands.LogCommand}", f"{BotCommands.LogCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(upload_log_handler)
    help_text_handler = MessageHandler(
        help_message_f,
        filters=filters.command([BotCommands.HelpCommand, BotCommands.HelpCommand + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(help_text_handler)
    start_text_handler = MessageHandler(
        start_message_f,
        filters=filters.command([BotCommands.StartCommand, BotCommands.StartCommand + buname]) & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(start_text_handler)
    call_back_button_handler = CallbackQueryHandler(button)
    app.add_handler(call_back_button_handler)
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=filters.command([f"{BotCommands.SaveThumbnailCommand}", f"{BotCommands.SaveThumbnailCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
)
    app.add_handler(save_thumb_nail_handler)
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=filters.command([f"{BotCommands.ClearThumbnailCommand}", f"{BotCommands.ClearThumbnailCommand}" + buname])
        & filters.chat(chats=AUTH_CHANNEL),
    )
    app.add_handler(clear_thumb_nail_handler)
    rclone_config_handler = MessageHandler(
        rclone_command_f, filters=filters.command([BotCommands.RcloneConfigCommand, BotCommands.RcloneConfigCommand + buname])
    )
    app.add_handler(rclone_config_handler)
    upload_as_doc_handler = MessageHandler(
        upload_as_doc,
        filters=filters.command([f"{BotCommands.ToggleDocumentCommand}", f"{BotCommands.ToggleDocumentCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL), 
    )
    app.add_handler(upload_as_doc_handler)
    upload_as_video_handler = MessageHandler(
        upload_as_video,
        filters=filters.command([f"{BotCommands.ToggleVideoCommand}", f"{BotCommands.ToggleVideoCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL), 
    )
    # torrent.py
    nyaa_search_handler = MessageHandler(
        nyaa_search, filters=filters.command([f"{BotCommands.NyaasiCommand}", f"{BotCommands.NyaasiCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(nyaa_search_handler)

    nyaa_search_sukebei_handler = MessageHandler(
        nyaa_search_sukebei, filters=filters.command([f"{BotCommands.SukebeiCommand}", f"{BotCommands.SukebeiCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(nyaa_search_sukebei_handler)

    searchhelp_handler = MessageHandler(
        searchhelp, filters=filters.command([f"{BotCommands.SearchHelpCommand}", f"{BotCommands.SearchHelpCommand}" + buname]) & filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(searchhelp_handler)
    # to here
    app.add_handler(nan)
    nan_handler = MessageHandler(
        nan
    )
    app.add_handler(nan_handler)
    LOGGER.info("Bot Started!")
    idle()

    '''
    # when a new user joins, have the bot send new_join_f from new_join_fn.py
    new_join_handler = MessageHandler(
        new_join_f, filters=~filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)

    # when a new user joins, have the bot send help_message_f from new_join_fn.py
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=filters.chat(chats=AUTH_CHANNEL) & filters.new_chat_members,
    )
    app.add_handler(group_new_join_handler)
    '''