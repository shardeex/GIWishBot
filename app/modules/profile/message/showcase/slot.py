from app.loader import i18n


_ = i18n.lazy_gettext

def get() -> str:
    return _(
        'Please select showcase slot you want to edit.'
    ).value
