import discord
from discord.ext import commands
from discord.ext.commands import Command
from test_audio import convert_audio
from ai_reader import coqui_tts_model
from get_tibiawiki_data import get_page_sections, get_page_content, extract_section_by_anchor, extract_text, extract_images
from test_books import gather_data
from llm_pipeline import generate_story
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Automatically install and set up ChromeDriver
chromedriver_autoinstaller.install()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command(name="render")
async def render_html(ctx, url: str):
    """Render a webpage as an image and send it."""
    try:
        # Set up Chrome options
        options = Options()
        options.binary_location = "/usr/bin/google-chrome-stable"  # Adjust this if installed elsewhere
        options.headless = True  # Run Chrome in headless mode (no GUI)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--force-device-scale-factor=2")  # Zoom al 200%
        
        # Initialize ChromeDriver
        driver = webdriver.Chrome(options=options)

        # Open the webpage and take a screenshot
        driver.get(url)
        screenshot_path = "webpage_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        # Send the screenshot in Discord
        await ctx.send(file=discord.File(screenshot_path))

    except Exception as e:
        await ctx.send(f"Error rendering the page: {e}")

@bot.command(name="join")
async def join_channel(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("¡Me uní al canal de voz!")
    else:
        await ctx.send("No estás conectado a ningún canal de voz.")


@bot.command(name="leave")
async def leave_channel(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Salí del canal de voz.")
    else:
        await ctx.send("No estoy en ningún canal de voz.")


@bot.command(name="say")
async def say_text(ctx, *, texto: str):
    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.send("Primero usa !join para que me una a tu canal de voz.")
        return

    salida_coqui = "salida_coqui.wav"
    coqui_tts_model.tts_to_file(text=texto, file_path=salida_coqui)

    source = discord.FFmpegPCMAudio(salida_coqui)
    voice_client.play(source)

    await ctx.send(f"**Leyendo**: {texto}")

@bot.command(name="stop")
async def stop(ctx):
    # Check if the bot is in a voice channel
    if not ctx.voice_client:
        await ctx.send("I'm not currently connected to a voice channel.")
        return

    # Stop the currently playing audio
    ctx.voice_client.stop()
    await ctx.send("Playback stopped.")
        
@bot.command(name="quest")
async def quest(ctx, *, quest_name: str):
    global last_query
    global story
    global quest_name_saved
    
    # Fetch sections using the MediaWiki API
    sections = get_page_sections(quest_name)
    if sections:
        story = ""
        quest_name_saved = quest_name
        last_query = {"sections": sections, "page": quest_name}

        # List sections to the user
        response = f"Secciones de la quest **{quest_name}**:\n"
        for i, section in enumerate(sections, 1):  # Start numbering from 1
            response += f"{i}. {section['line']}\n"

        await ctx.send(response + "\nUsa `!1`, `!2`, etc., para seleccionar una sección.")

        # Dynamically create commands for each section
        for i, section in enumerate(sections, 1):
            create_dynamic_section_command(i, section)
    else:
        await ctx.send(f"No se encontraron secciones para la quest: {quest_name}")


def create_dynamic_section_command(section_number: int, section: dict):
    """
    Dynamically creates a command for a specific section.
    """

    async def section_command(ctx):
        global last_query
        global story
        
        # Ensure there is a recent query
        if not last_query["sections"]:
            await ctx.send("Primero usa el comando `!quest <nombre_de_la_quest>`.")
            return

        # Get the page content and the selected section's anchor
        page_content = get_page_content(last_query["page"])
        if not page_content:
            await ctx.send(f"No se pudo obtener el contenido completo de la página.")
            return

        # Extract the section content by anchor
        section_content = extract_section_by_anchor(page_content, section["anchor"])
        if not section_content:
            await ctx.send(f"No se pudo encontrar la sección '{section['line']}'.")
            return

        # Process the content
        text_content = extract_text(section_content)
        images = extract_images(section_content)

        # Construct the response
        # response = f"**{section['line']}**:\n\n{text_content[:2000]}"
        # if images:
        #     response_with_images = response + "\n\nImágenes:\n" + "\n".join(images)
        #     # Send the response to the text channel
        #     await ctx.send(response_with_images)
        # else:
        #     # Send the response to the text channel
        #     await ctx.send(response)

        quest_name, legend_text, wiki_scrapped, important_books = gather_data(quest_name_saved)
        index = section_number
        response = generate_story(quest_name, legend_text, wiki_scrapped, important_books, story, index)
        story = ""+response
        await ctx.send(response[:1900])

        # Check if the bot is connected to a voice channel
        voice_client = ctx.voice_client
        if not voice_client:
            await ctx.send("No estoy conectado a un canal de voz. Usa `!join` primero.")
            return

        # Read the content with Coqui TTS
        try:
            salida_coqui = "salida_coqui.wav"
            convert_audio(response, salida_coqui)
            source = discord.FFmpegPCMAudio(salida_coqui)
            voice_client.play(source)
        except Exception as e:
            await ctx.send(f"Error al reproducir el audio: {str(e)}")

    # Register the command dynamically
    bot.add_command(Command(section_command, name=str(section_number)))
    