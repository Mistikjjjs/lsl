const puppeteer = require('puppeteer');
const { Telegraf } = require('telegraf');

// Reemplaza con tu token de Telegram
const BOT_TOKEN = '7878507254:AAGZ4i6ZPAnQKqBH4qAO2n-XCMU6Dl5E-Us';
const bot = new Telegraf(BOT_TOKEN);

// URL del chatbot
const CHATBOT_URL = 'https://onlinechatbot.ai/chatbots/sus-anime-girl/';

// Función para interactuar con el chatbot
const interactWithChatbot = async (userMessage) => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Navega al chatbot
    await page.goto(CHATBOT_URL, { waitUntil: 'networkidle2' });

    // Encuentra el campo de texto y escribe el mensaje
    await page.type('input[placeholder="Type your message..."]', userMessage, { delay: 100 });

    // Presiona "Enter" para enviar
    await page.keyboard.press('Enter');

    // Espera la respuesta
    await page.waitForSelector('.response-class'); // Cambia esto al selector correcto de la respuesta
    const response = await page.evaluate(() => {
        const element = document.querySelector('.response-class'); // Cambia esto al selector correcto de la respuesta
        return element ? element.innerText : 'No response found';
    });

    await browser.close();
    return response;
};

// Configura el bot para recibir mensajes
bot.on('text', async (ctx) => {
    const userMessage = ctx.message.text;

    try {
        // Obtén la respuesta del chatbot
        const chatbotResponse = await interactWithChatbot(userMessage);

        // Envía la respuesta al usuario en Telegram
        ctx.reply(chatbotResponse);
    } catch (error) {
        console.error('Error:', error);
        ctx.reply('Hubo un problema al interactuar con el chatbot. Inténtalo de nuevo.');
    }
});

// Inicia el bot
bot.launch();
console.log('Bot de Telegram iniciado...');
