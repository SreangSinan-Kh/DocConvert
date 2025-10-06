def main() -> None:
    # ត្រូវប្រាកដថាបានកំណត់ Webhook URL របស់អ្នក
    WEBHOOK_URL = "YOUR_RENDER_URL" # ត្រូវជំនួសដោយ URL ពិតប្រាកដរបស់ Render របស់អ្នក (ឧ. https://my-telegram-bot.onrender.com)
    
    # ទទួលបាន PORT ពី Render environment, លំនាំដើមគឺ 8000
    PORT = int(os.environ.get("PORT", "8000"))
    
    application = Application.builder().token(BOT_TOKEN).read_timeout(30).build()
    
    # ... (Conversation Handler ដូចកូដដើមរបស់អ្នក) ...
    
    # --- Conversation Handler ដូចកូដដើមរបស់អ្នក ---
    # គ្រាន់តែចម្លង 'conv_handler' ពីកូដដើមរបស់អ្នកមកត្រង់នេះ

    conv_handler = ConversationHandler(
        entry_points=[
             CommandHandler("start", start),
             # ... (Command Handlers ដូចកូដដើម) ...
             CommandHandler("pdf_to_img", start_pdf_to_img_command),
             CommandHandler("merge_pdf", start_merge_command),
             CommandHandler("split_pdf", start_split_command),
             CommandHandler("compress_pdf", start_compress_command),
             CommandHandler("img_to_pdf", start_img_to_pdf_command),
             CommandHandler("img_to_text", start_img_to_text_command),
             CommandHandler("audio_converter", start_audio_converter_command),
             CommandHandler("video_converter", start_video_converter_command),
             CommandHandler("archive_manager", start_archive_manager_command),
        ],
        states={
             # ... (States ទាំងអស់ដូចកូដដើម) ...
             SELECT_ACTION: [
                 CallbackQueryHandler(start_pdf_to_img, pattern='^pdf_to_img$'),
                 CallbackQueryHandler(start_conversion_with_format, pattern='^fmt_'),
                 CallbackQueryHandler(start_merge, pattern='^merge_pdf$'),
                 CallbackQueryHandler(start_split, pattern='^split_pdf$'),
                 CallbackQueryHandler(start_compress, pattern='^compress_pdf$'),
                 CallbackQueryHandler(start_img_to_pdf, pattern='^img_to_pdf$'),
                 CallbackQueryHandler(start_img_to_text, pattern='^img_to_text$'),
                 CallbackQueryHandler(start_audio_converter, pattern='^audio_converter$'),
                 CallbackQueryHandler(select_audio_output, pattern='^audio_'),
                 CallbackQueryHandler(start_video_converter, pattern='^video_converter$'),
                 CallbackQueryHandler(select_video_output, pattern='^video_'),
                 CallbackQueryHandler(start_archive_manager, pattern='^archive_manager$'),
                 CallbackQueryHandler(start_create_zip, pattern='^archive_create$'),
                 CallbackQueryHandler(start_extract_archive, pattern='^archive_extract$'),
                 CallbackQueryHandler(start, pattern='^main_menu$'),
             ],
             WAITING_PDF_TO_IMG_FILE: [MessageHandler(filters.Document.PDF, receive_pdf_for_img)],
             WAITING_FOR_MERGE: [MessageHandler(filters.Document.PDF, receive_pdf_for_merge), CommandHandler('done', done_merging)],
             WAITING_FOR_SPLIT_FILE: [MessageHandler(filters.Document.PDF, receive_pdf_for_split)],
             WAITING_FOR_SPLIT_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_split_range)],
             WAITING_FOR_COMPRESS: [MessageHandler(filters.Document.PDF, receive_pdf_for_compress)],
             WAITING_FOR_IMG_TO_PDF: [MessageHandler(filters.PHOTO, receive_img_for_pdf), CommandHandler('done', done_img_to_pdf)],
             WAITING_FOR_IMG_TO_TEXT_FILE: [MessageHandler(filters.PHOTO | filters.Document.IMAGE, receive_img_for_text)],
             WAITING_FOR_AUDIO_FILE: [MessageHandler(filters.AUDIO | filters.Document.ALL, receive_audio_for_conversion)],
             WAITING_FOR_VIDEO_FILE: [MessageHandler(filters.VIDEO | filters.Document.ALL, receive_video_for_conversion)],
             WAITING_FOR_FILES_TO_ZIP: [MessageHandler(filters.Document.ALL, receive_file_for_zip), CommandHandler('done', done_zipping)],
             WAITING_FOR_ARCHIVE_TO_EXTRACT: [MessageHandler(filters.Document.ALL, receive_archive_to_extract)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    # -----------------------------------------------------------------------

    # --- ការដំណើរការ Webhook សម្រាប់ Render ---
    print(">>> Bot កំពុងដំណើរការដោយ Webhook នៅលើ Render!")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL + '/' + BOT_TOKEN
    )