import discord
from discord.ext import commands
import pandas as pd
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Upload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_game_data = {}  # Dictionary to store uploaded data per user
        # self.recommender = GameRecommender('./Datasets/steam_data.csv')  # Load dataset

    @discord.slash_command(name='upload', description='Upload your Steam game library metadata')
    async def upload_file(self, ctx, file: discord.Attachment = None):
        """
        User uploads a CSV or JSON file containing their Steam game library metadata.
        """
        if not file:
            await ctx.respond("❗ Please attach a CSV or JSON file.")
            return
    
        attachment = file
        mime_type = attachment.content_type  # Discord gives this automatically
    
        allowed_types = ["text/csv", "application/json", "text/csv; charset=utf-8"]

        print(mime_type)
    
        if mime_type not in allowed_types:
            await ctx.respond(f"❗ Unsupported file type: {mime_type}. Only CSV or JSON are accepted.")
            return
    
        try:
            file_data = await attachment.read()
    
            if "text/csv" in mime_type:
                df = pd.read_csv(io.BytesIO(file_data))
            elif "application/json" in mime_type:
                df = pd.read_json(io.BytesIO(file_data))
    
            # Optional: Validate required columns exist
            required_columns = {"Name", "Short Description"}
            if not required_columns.issubset(set(df.columns)):
                await ctx.respond(f"❗ Your file must include the following columns: {', '.join(required_columns)}")
                return
    
            # Store user's uploaded data
            self.user_game_data[ctx.author.id] = df
    
            await ctx.respond(f"✅ File received and processed! {len(df)} games loaded.")
    
        except Exception as e:
            await ctx.respond(f"❗ Error processing file: {str(e)}")

    @discord.slash_command(name='checklibrary', description='Check your uploaded game library')
    async def check_library(self, ctx):
        """
        Command to provide basic statistics about the user's uploaded Steam library.
        """
        await ctx.defer()  # Defer the response to avoid timeout

        try:
            user_data = self.user_game_data.get(ctx.author.id)
            if user_data is not None:
                num_games = len(user_data)

                # Check if "Playtime (Hours)" exists
                if "Playtime (Hours)" in user_data.columns:
                    total_hours = user_data["Playtime (Hours)"].sum()
                    most_played_game = user_data.loc[user_data["Playtime (Hours)"].idxmax()]["Name"]
                    most_played_hours = user_data["Playtime (Hours)"].max()
                else:
                    total_hours = "N/A"
                    most_played_game = "N/A"
                    most_played_hours = "N/A"

                # Check if "Genres" exists
                if "Genres" in user_data.columns:
                    genre_counts = user_data["Genres"].str.split(", ").explode().value_counts()
                    top_genre = genre_counts.idxmax()
                    top_genre_count = genre_counts.max()
                else:
                    genre_counts = None
                    top_genre = "N/A"
                    top_genre_count = "N/A"

                # Build the response message
                response = (
                    f"📚 **Steam Library Stats**:\n"
                    f"- Total Games: {num_games}\n"
                    f"- Total Playtime: {total_hours} hours\n"
                    f"- Most Played Game: {most_played_game} ({most_played_hours} hours)\n"
                )

                if genre_counts is not None:
                    response += (
                        f"- Top Genre: {top_genre} ({top_genre_count} games)\n"
                        f"- Games Per Genre:\n"
                    )
                    for genre, count in genre_counts.items():
                        response += f"  - {genre}: {count} games\n"

                await ctx.respond(response)
            else:
                await ctx.respond("❗ You haven't uploaded a library yet!")
        except Exception as e:
            await ctx.respond(f"❗ An error occurred: {str(e)}")

def setup(bot):
    bot.add_cog(Upload(bot))