from sys import stderr

from nextcord import Interaction, ApplicationCheckFailure, ApplicationError
from nextcord.ext import application_checks

from dragonbot import session, cfg, bot
from dragonbot.core.model import CoreUser, CoreACL


def check(level: CoreACL):
    def predicate(interaction: Interaction) -> bool:
        user: CoreUser = session.get(CoreUser, interaction.user.id)
        if not user:
            user = CoreUser(id=interaction.user.id, acl=CoreACL.DEFAULT.value)
            session.add(user)
            session.commit()
        return user.acl >= level.value

    if application_checks.has_role(cfg['access']['su_role']):
        return application_checks.has_role(cfg['access']['su_role'])
    else:
        return application_checks.check(predicate)



@bot.event
async def on_application_command_error(interaction: Interaction, error: ApplicationError):
    if isinstance(error, ApplicationCheckFailure):
        await interaction.send("K tomuto příkazu **nemáš** přístup!")
    else:
        await interaction.send("Chyba při vykonávání příkazu, kontaktuj správce serveru.")
    print(error, type(error), file=stderr)

