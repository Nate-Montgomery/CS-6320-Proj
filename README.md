# CS-6320-Proj

- **Class:** CS 6320
- **Name:** Nate Montgomery (NAM190002)
- **Team:** Individual Project

NLP Project for CS 6320

## Discord Bot Project

This project is a Discord bot built using the `py-cord` library. The bot provides game recommendations based on user preferences and their Steam library. It leverages NLP techniques and embeddings to generate personalized recommendations.

---

### Project Structure

```
CS-6320-Proj
├── bot
│   ├── __init__.py
│   ├── main.py
│   ├── cogs
│   │   ├── GameRecommender.py # Handles game recommendation logic
│   │   ├── SteamLibrary.py    # Fetches and processes user Steam library
│   │   ├── Upload.py          # Handles user-uploaded library metadata
│   │   └── SlashCommands.py   # Additional bot commands
├── Datasets
│   └── steam_data_cleaned.zip # Compressed cleaned dataset
├── Environment
│   └── environment.yaml       # Conda environment configuration
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── README.md                  # Project documentation
```

---

### Features

- **Game Recommendations**:
  - Provides personalized game recommendations based on user preferences and their Steam library.
  - Uses Sentence Transformers for semantic similarity and embeddings.
- **Steam Library Integration**:
  - Fetches and processes user Steam library metadata.
- **Custom Slash Commands**:
  - Includes commands for uploading libraries, fetching recommendations, and more.

---

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CS-6320-Proj
   ```

2. **Create and activate the Conda environment:**
   - Create the environment using the `environment.yaml` file:
     ```bash
     conda env create -f Environment/environment.yaml
     ```
   - Activate the environment:
     ```bash
     conda activate ProjectNLP
     ```

3. **Set up your environment variables:**
   - Create a `.env` file in the root directory and add your Discord bot token and Steam API key:
     ```properties
     DISCORD_TOKEN=your_bot_token_here
     STEAM_API_KEY=your_steam_api_key_here
     ```

4. **Run the bot:**
   ```bash
   python bot/main.py
   ```

---

### Usage

- **Commands**:
  - `/fetchlibrary [Steam ID/username]`: Fetch your Steam library metadata.
  - `/upload`: Upload your Steam library metadata manually.
  - `/recommend [prompt]`: Get a game recommendation based on your library and preferences.
  - `/checklibrary`: Check your uploaded library.

---

### Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.

