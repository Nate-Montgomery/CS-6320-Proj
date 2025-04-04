# CS-6320-Proj

- **Class:** CS 6320
- **Name:** Nate Montgomery (NAM190002)
- **Team:** Myself

NLP Project for CS 6320

## Discord Bot Project

This project is a Discord bot built using the `discord.py` library. It serves as a template for creating a customizable bot with various features.

### Project Structure

```
discord-bot-project
├── bot
│   ├── __init__.py
│   ├── main.py
│   ├── cogs
│   │   └── example_cog.py
│   └── utils
│       └── helpers.py
├── requirements.txt
├── .env
└── README.md
```

### Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd discord-bot-project
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Set up your environment variables:**
   Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

### Usage

To run the bot, execute the following command:
```
python bot/main.py
```

### Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.

### License

This project is licensed under the MIT License. See the LICENSE file for details.