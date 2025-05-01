import discord
from discord.ext import commands
import requests
import csv
import io
import time
from dotenv import load_dotenv
import os
import re  # Import regex for Steam ID validation

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')

class SteamLibrary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name='fetchlibrary', description='Fetch Steam library metadata by Steam username or Steam ID')
    async def fetch_library(self, ctx, steam_input: str):
        """
        Fetch and process a user's Steam library metadata by their Steam username or Steam ID, including play times.
        """
        await ctx.defer()  # Defer the response as this might take time

        # Check if the input is a Steam ID (17-digit number)
        if re.fullmatch(r"\d{17}", steam_input):
            steam_id = steam_input
        else:
            # Resolve Steam username to Steam ID
            resolve_url = (
                f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
                f"?key={STEAM_API_KEY}&vanityurl={steam_input}"
            )
            try:
                resolve_response = requests.get(resolve_url)
                resolve_response.raise_for_status()
                resolve_data = resolve_response.json()

                if resolve_data["response"]["success"] != 1:
                    await ctx.respond(f"❗ Could not resolve Steam username: `{steam_input}`. Please check the username.")
                    return

                steam_id = resolve_data["response"]["steamid"]
            except Exception as e:
                await ctx.respond(f"❗ Error resolving Steam username: {str(e)}")
                return

        # Fetch owned games
        owned_games_url = (
            f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
            f"?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=1&include_played_free_games=1&format=json"
        )
        try:
            owned_games_response = requests.get(owned_games_url)
            owned_games_response.raise_for_status()
            owned_games = owned_games_response.json()
            games = owned_games["response"].get("games", [])

            if not games:
                await ctx.respond(f"❗ No games found in the Steam library for `{steam_input}`.")
                return

            # Prepare CSV data
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["AppID", "Name", "Genres", "Developer", "Publisher", "Short Description", "Metacritic Score", "Recommendations", "Playtime (Hours)"])

            for game in games:
                appid = game["appid"]
                name = game["name"]
                playtime_hours = round(game.get("playtime_forever", 0) / 60, 2)  # Convert playtime from minutes to hours

                # Fetch detailed metadata
                detail_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=en"
                try:
                    detail_response = requests.get(detail_url)
                    detail_response.raise_for_status()
                    data = detail_response.json()

                    if data[str(appid)]["success"]:
                        info = data[str(appid)]["data"]
                        genres = ", ".join(g["description"] for g in info.get("genres", []))
                        devs = ", ".join(info.get("developers", []))
                        pubs = ", ".join(info.get("publishers", []))
                        desc = info.get("short_description", "")
                        meta = info.get("metacritic", {}).get("score", "N/A")
                        recs = info.get("recommendations", {}).get("total", "N/A")

                        writer.writerow([appid, name, genres, devs, pubs, desc, meta, recs, playtime_hours])

                except Exception as e:
                    print(f"Error fetching data for {appid}: {e}")

                time.sleep(0.5)  # Avoid rate-limiting

            # Send the CSV file to the user
            csv_buffer.seek(0)
            discord_file = discord.File(fp=io.BytesIO(csv_buffer.getvalue().encode()), filename=f"{steam_input}_library_metadata.csv")
            await ctx.respond(f"✅ Here is the Steam library metadata for `{steam_input}` (including play times):", file=discord_file)

        except Exception as e:
            await ctx.respond(f"❗ Error fetching Steam library: {str(e)}")

def setup(bot):
    bot.add_cog(SteamLibrary(bot))