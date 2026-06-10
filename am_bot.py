import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

CONTACT = "@gmdashi"

MSG_WELCOME = (
    "👋 Bienvenue dans l'espace Ressources AM.\n\n"
    "Tu trouveras ici tous les process officiels de la structure, tes scripts d'approche "
    "et les guides de configuration pour cartonner sur tes volumes.\n\n"
    "Choisis une catégorie ci-dessous pour commencer :"
)

MSG_JOB = (
    "🎯 En quoi consiste ton job ?\n\n"
    "Ton rôle est de contacter, closer et manager des influenceurs pour qu'ils fassent la promotion "
    "de nos jeux de casino. C'est très facile, tu es formé de A à Z et nous avons de gros budgets "
    "fixes pour les rémunérer, ce qui rend le closing très simple.\n\n"
    "🎰 Le Produit :\n"
    "Nous faisons la promotion de mini-jeux de casino. Ils sont extrêmement populaires et génèrent "
    "beaucoup plus de FTD (First Time Deposit) que les casinos classiques.\n\n"
    "💰 Rémunération & Suivi :\n"
    "À la performance : Tu commences à 10 € / FTD.\n\n"
    "Suivi : Tout ton travail et tes résultats sont traqués en temps réel sur notre dashboard d'équipe.\n\n"
    "Rappel : J'ai juste besoin de gens déter pour bosser. Le potentiel de gain est énorme si tu es rigoureux.\n\n"
    f"❓ Problème ou question ? Contacte {CONTACT} sur Telegram."
)

MSG_SETUP = (
    "🛠️ I/ CRÉATION DES COMPTES\n\n"
    "📱 Matériel : Utilise un 2ème téléphone portable si possible.\n\n"
    "📡 Réseau (Règle d'or) : Toujours être en 4G/5G ou en partage de connexion pour utiliser le compte. Jamais de Wi-Fi.\n\n"
    "📧 Inscription : Crée le compte avec une adresse e-mail Gmail ou Outlook/Hotmail.\n\n"
    "✏️ Optimisation : Dès le début, configure le profil : nom, prénom, photo de profil (pfp) et bio.\n\n"
    "🔐 Sécurité : Active directement l'A2F (Double Authentification) via une application d'authentification (Google Authenticator).\n\n"
    "🔗 Account Center : Ne lie JAMAIS les Account Centers des différents comptes entre eux.\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "🔥 II/ LE WARMUP (La Chauffe du compte)\n\n"
    "Les premières 24h : Connecte-toi sur ton appareil, scrolle juste le compte 3-4 minutes de façon "
    "naturelle (regarder le feed, etc.) puis laisse-le reposer 24h sans trop l'utiliser.\n\n"
    "Si le compte est NON WARMUP : Suis un warmup classique pendant 5-6 jours. Connecte-toi quelques "
    "minutes par jour : scrolle, ouvre les commentaires, mais ne spamme pas les likes.\n\n"
    "Si le compte est DÉJÀ CHAUFFÉ : Laisse-le simplement 24h sur ton appareil avec une utilisation "
    "normale (scroll, like) avant de lancer des actions.\n\n"
    f"❓ Problème ou question ? Contacte {CONTACT} sur Telegram."
)

MSG_OUTREACH = (
    "💬 I/ RÈGLES DE L'OUTREACH\n\n"
    "✅ Disponibilité : Soyez toujours disponible pour répondre rapidement.\n\n"
    "🤝 Posture : Soyez toujours amical et proche des influenceurs.\n\n"
    "📸 Profil actif : Pour DM, tu dois toujours avoir une story active, simple et épurée. "
    "Tu peux aller prendre des exemples de stories sur ces comptes de référence : "
    "@loris.cataldo, @maxrusso.design, @julesfrankenn.\n\n"
    "💡 Hacks Réseaux :\n"
    "• Instagram : Quand la story d'un influenceur est active, réponds directement à sa story pour engager le DM.\n"
    "• TikTok : N'hésite pas à commenter ses vidéos publiques avec un message du genre : "
    "'Salut je t'ai envoyé un mp pour une collab ;)'\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "📈 II/ TABLEAU DE PROGRESSION DES DMS\n\n"
    "Une fois le warmup fini, commence à DM progressivement (2-3 le premier jour, puis 5-6...) "
    "jusqu'à atteindre l'objectif.\n\n"
    "Divise toujours tes sessions en 2 :\n"
    "Ex : si tu es à 30 DM/jour ➡️ 15 DM à 10h + 15 DM à 20h\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "🎯 III/ SCRIPTS D'APPROCHE (À copier/coller)\n\n"
    "Message de base :\n"
    "Salut (prénom)! On te propose 1500€ par semaine en partageant nos jeux, intéressé ?\n\n"
    "Variante 1 :\n"
    "Salut [Prénom] ! J'espère que tu vas bien. On propose 1 500 € par semaine juste pour partager nos jeux ça te dirait d'en discuter?\n\n"
    "Variante 2 :\n"
    "Salut [Prénom] ! Ça va? On propose 1 500 € par semaine pour partager nos jeux en ce moment, ça pourrait t'intéresser ?\n\n"
    "Variante 3 :\n"
    "Hey [Prénom]! On propose 1 500 € par semaine à ceux qui partagent nos jeux, t'es chaud ou pas ?\n\n"
    "Variante 4 :\n"
    "Salut [Prénom], petite question: on propose 1 500 €/semaine pour partager nos jeux, ça te dirait d'en être ?\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n\n"
    "🚀 IV/ LE CLOSING (Tunnel)\n\n"
    "Dès que l'influenceur donne une réponse positive, demande-lui immédiatement son WhatsApp "
    "ou son Telegram, puis envoie ses informations dans notre groupe sous ce format précis :\n\n"
    "USERNAME\n"
    "CONTACT WHATSAPP/TELEGRAM\n\n"
    f"❓ Problème ou question ? Contacte {CONTACT} sur Telegram."
)

def menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💼 Le Job & Paiements", callback_data="job")],
        [InlineKeyboardButton("📱 SETUP & Warmup", callback_data="setup")],
        [InlineKeyboardButton("💬 Outreach & DMs", callback_data="outreach")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Retour au Menu Principal", callback_data="menu")]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(MSG_WELCOME, reply_markup=menu_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(MSG_WELCOME, reply_markup=menu_keyboard())
    elif query.data == "job":
        await query.edit_message_text(MSG_JOB, reply_markup=back_keyboard())
    elif query.data == "setup":
        await query.edit_message_text(MSG_SETUP, reply_markup=back_keyboard())
    elif query.data == "outreach":
        await query.edit_message_text(MSG_OUTREACH, reply_markup=back_keyboard())


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    logger.info("AM Bot demarre...")
    app.run_polling()


if __name__ == "__main__":
    main()
