# TibiaLore 🧙‍♂️ a Tibia quest narrator

The purpose is to have a storytelling pipeline that transforms Tibia quests into immersive, voice-narrated experiences. It scrapes quest data from TibiaWiki, uses large language models to generate rich narratives, adds historical context from in-game books, and then narrates the story with background music via a Discord bot.

This project blends **fantasy RPG storytelling**, **machine learning**, and **voice synthesis** to breathe new life into Tibia quests. It provides context, motivation, and atmosphere to elevate the player’s experience.

## 🎯 Project Goals

- 🎮 Enhance the storytelling of Tibia quests.
- 🤖 Use LLMs (like LLaMA) to generate immersive quest narratives.
- 📚 Incorporate historical context from Tibia books.
- 🗣️ Synthesize the generated text into voice narration.
- 🎧 Add background music from the game for immersion.
- 💬 Let users interact via a Discord bot.

---

## 📌 Features

- ✅ **Quest Parser**: Scrapes TibiaWiki for quest data (legend, sections, and dialogue).
- ✅ **Book Analyzer**: Loads and ranks books relevant to the quest’s theme.
- ✅ **LLM Story Generator**: Generates story context for each quest section using LLaMA.
- ✅ **Text-to-Speech**: Converts story segments into narrated audio with optional background music.
- ✅ **Discord Integration**: Users interact through commands like `!quest`, `!1`, `!say`, etc.

## 🧪 Tech Stack

- 🐍 Python
- 🤗 [Transformers](https://huggingface.co/transformers/)
- 🦙 LLaMA (e.g. `meta-llama/Llama-3.2-1B`)
- 🗣️ [Coqui TTS](https://github.com/coqui-ai/TTS)
- 📄 [Tibia Fandom API](https://tibia.fandom.com/api.php)
- 💬 discord.py
- 🎵 pydub + ffmpeg

---

## 🚀 Usage

1. **Install dependencies**  
   Make sure you have `torch`, `transformers`, `discord.py`, `TTS`, `pydub`, and `nltk`.

2. **Run the bot**  
   Update your `bot.run("YOUR_TOKEN")` with a valid Discord token.

3. **Interact via Discord**
   - `!quest The Pits of Inferno Quest`: Lists quest sections.
   - `!1`, `!2`, etc.: Generates and narrates that section.
   - `!join` / `!leave`: Bot joins or leaves your voice channel.
   - `!say Hello adventurer!`: Speaks a custom line.
   - `!stop`: Stops the narration.
   - `!render <url>`: Renders a webpage screenshot and sends it.

4. **Audio Narration**  
   - Narrated text is slowed slightly.
   - Background music is randomly selected from a local folder (`./TibiaSoundtrack`).

## 📖 Example Flow

1. A user types `!quest The Pits of Inferno Quest`.
2. The bot fetches sections and asks the user to pick one.
3. Upon choosing `!1`, the bot:
   - Scrapes the section content
   - Finds relevant books
   - Builds a story using LLaMA
   - Generates audio and plays it with immersive music

---

## 🛠️ TODO / Future Improvements

- [ ] Improve historical context creation
- [ ] Allow full quest narration in a single flow
- [ ] Add multi-language support (Spanish, Portuguese, etc.)
- [ ] Improve background music selection by theme
- [ ] Add image rendering in Discord from TibiaWiki pages for quests
- [ ] Add web interface for quest selection and listening

---

## 🙌 Acknowledgements

- Tibia Fandom Wiki for quest and lore data
- HuggingFace for LLaMA and TTS support
- Coqui TTS for amazing voice synthesis
- Tibia community for inspiration 🐉

---

## 🧪 About This Project

This was a fun weekend project to explore storytelling, language models, and voice synthesis using Tibia quests. If you're interested in collaborating, extending it, or just curious about how it works — feel free to reach out! 😊
