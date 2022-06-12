from django.utils.timezone import now

BATON = {
    'SITE_HEADER': 'Digital Auction',
    'SITE_TITLE': 'Digital Auction',
    'INDEX_TITLE': 'System Admin',
    'SUPPORT_HREF': 'https://support.university-auction.marvelous-tech.com',
    'COPYRIGHT':
        f'Copyright © 2020 {now().year} '
        '<a href="https://university-auction.marvelous-tech.com">Marvelous Technologies</a>',
    'POWERED_BY': '<a href="https://www.marvelous-tech.com">Marvelous Technologies</a>',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MESSAGES_TOASTS': True,
    'GRAVATAR_DEFAULT_IMG': 'retro',
}
