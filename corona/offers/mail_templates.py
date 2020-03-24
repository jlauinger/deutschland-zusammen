from django.utils.translation import gettext_lazy as _

CONTACT_MAIL_FROM = 'noreply@{domain}'
CONTACT_MAIL_SUBJECT = _('Neue Nachricht von {domain}')
CONTACT_MAIL_BODY = _("""Hallo {name}!

Du hast eine neue Anfrage nach Hilfe über {domain}!

Daten zur suchenden Person:
Name: {sender_name}
E-Mail: {sender_email}
Telefon: {sender_phone}

Nachricht:
{message}

Melde dich doch wenn du kannst schnellstmöglich zurück.

Liebe Grüße
dein Team von {domain}
""")

ACTIVATION_MAIL_FROM = 'noreply@{domain}'
ACTIVATION_MAIL_SUBJECT = _('Aktiviere deinen Account bei {domain}')
ACTIVATION_MAIL_BODY = _("""
Hallo {name}!

Bitte bestätige deine E-Mail-Adresse und aktiviere deinen Account bei {domain}. Klicke dazu einfach
auf den folgenden Link oder kopiere ihn in die Adressleiste deines Browsers:

{link}

Bis du deinen Account aktiviert hast können deine Angebote nicht gefunden werden.

Liebe Grüße
dein Team von {domain}
""")