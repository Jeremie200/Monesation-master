import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes, ConversationHandler

# Configuration du bot
TOKEN = "8128880321:AAHV3D84FIvKHND8rta8qivAaL1j2P9ogcc"
ADMIN_USERNAME = "@Boostmasterann"
MOBILE_MONEY = "0022952181148"
PAYMENT_API_KEY = "API_KEY_newpayment"

# États de conversation
CHOOSING_PLATFORM, COLLECT_INFO, PAYMENT = range(3)

# Configuration du logger
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Menu principal
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("YouTube", callback_data="youtube")],
        [InlineKeyboardButton("TikTok", callback_data="tiktok")],
        [InlineKeyboardButton("Facebook", callback_data="facebook")],
        [InlineKeyboardButton("Instagram", callback_data="instagram")],
        [InlineKeyboardButton("Twitter", callback_data="twitter")]
    ]
    await update.message.reply_text(
        "Bienvenue sur Google Monetisation Master ! Choisissez une plateforme à monétiser :",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSING_PLATFORM

# Description des avantages selon plateforme
async def platform_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    platform = query.data
    context.user_data['platform'] = platform

    advantages = {
        "youtube": "**YouTube** : Gagnez jusqu’à 1000$/mois avec une chaîne monétisée professionnelle !",
        "tiktok": "**TikTok** : Devenez créateur à succès et générez des revenus avec vos vidéos virales !",
        "facebook": "**Facebook** : Activez la monétisation et gagnez de l’argent avec vos vidéos et publications !",
        "instagram": "**Instagram** : Boostez vos revenus avec les Reels et placements de produits !",
        "twitter": "**Twitter** : Gagnez avec des publications sponsorisées et vos abonnés !"
    }
    prix_usd = {"youtube": 100, "tiktok": 70, "facebook": 50, "instagram": 120, "twitter": 75}
    prix_cfa = {key: round(value * 610, 2) for key, value in prix_usd.items()}

    msg = f"{advantages[platform]}\n\nPrix : {prix_usd[platform]}$ ({prix_cfa[platform]} FCFA)"
    await query.edit_message_text(
        text=msg + "\n\nVeuillez maintenant envoyer les informations suivantes :\n\n- Nom\n- Prénom\n- Numéro de téléphone\n- Adresse email\n- Photo de profil\n- Lien (si existant)\n\nEnvoyez-les dans un seul message."
    )
    return COLLECT_INFO

# Réception des infos utilisateur
async def collect_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['infos'] = update.message.text
    platform = context.user_data['platform']
    prix_usd = {"youtube": 100, "tiktok": 70, "facebook": 50, "instagram": 120, "twitter": 75}
    prix_cfa = {key: round(value * 610, 2) for key, value in prix_usd.items()}

    await update.message.reply_text(
        f"Merci ! Le coût de création d’un compte {platform.upper()} monétisé est de {prix_usd[platform]}$ ({prix_cfa[platform]} FCFA).\n\nVeuillez effectuer le paiement via Mobile Money au numéro suivant :\n{MOBILE_MONEY}\n\nOu via notre système en ligne sécurisé. Cliquez ci-dessous pour payer.\n\nUne fois le paiement effectué, envoyez une capture d’écran ici."
    )
    return PAYMENT

# Confirmation après paiement
async def payment_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merci pour votre commande ! Votre compte est en cours de création. Vous recevrez les accès sous 24h.\n\nPour toute question, contactez : " + ADMIN_USERNAME
    )
    return ConversationHandler.END

# Commande annuler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Opération annulée. Revenez avec /start pour recommencer.")
    return ConversationHandler.END

# Démarrage de l’application
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_PLATFORM: [CallbackQueryHandler(platform_description)],
            COLLECT_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_info)],
            PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_received)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)

    print("Bot démarré...")
    app.run_polling()
