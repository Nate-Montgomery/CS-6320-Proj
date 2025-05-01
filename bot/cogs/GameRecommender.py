import discord
from discord.ext import commands
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os

embeddings_file = 'Datasets/steam_embeddings.npy'

class GameRecommender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dataset = pd.read_csv('Datasets\\steam_data_cleaned.csv')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.dataset = self.dataset.loc[self.dataset['num_reviews'] > 10].reset_index(drop=True)

        # Precompute embeddings for all games
        self.dataset['combined_text'] = (
            self.dataset['name'] + " " +
            self.dataset['popu_tags'].fillna('') + " " +
            self.dataset['full_desc'].fillna('') + " " +
            self.dataset['sentiment'].fillna('') + " " +
            # self.dataset['num_reviews'].astype(str).fillna('') + " " +
            self.dataset['review_txt'].fillna('')
        ).fillna('')

        if os.path.exists(embeddings_file):
            self.embeddings = np.load(embeddings_file)
        else:
            self.embeddings = self.model.encode(self.dataset['combined_text'].tolist(), convert_to_tensor=True)
            np.save(embeddings_file, self.embeddings)

    @discord.slash_command(name='recommend', description='Get a game recommendation based on your library and preferences.')
    async def recommend_game(self, ctx: discord.ApplicationContext, prompt: str):
        await ctx.defer()

        try:
            # Encode the user prompt
            prompt_embedding = self.model.encode(prompt, convert_to_tensor=True)

            # Retrieve the user's library
            user_library = self.bot.get_cog('Upload').user_game_data.get(ctx.author.id, pd.DataFrame())

            if not user_library.empty:
                # Combine the embeddings of the user's library to create a "user profile embedding"
                user_library_games = self.dataset[self.dataset['name'].isin(user_library['Name'])]
                if not user_library_games.empty:
                    user_library_embeddings = self.embeddings[user_library_games.index]
                    user_profile_embedding = user_library_embeddings.mean(axis=0)
                    # user_profile_embedding = np.mean(user_library_embeddings, axis=0)

                    # Combine prompt embedding and user profile embedding
                    combined_embedding = (prompt_embedding + user_profile_embedding) / 2
                else:
                    combined_embedding = prompt_embedding
            else:
                combined_embedding = prompt_embedding

            # Compute cosine similarities
            similarities = np.dot(self.embeddings, combined_embedding).flatten()

            # Add similarity scores to the dataset
            self.dataset['similarity'] = similarities

            # Exclude games the user already owns
            if not user_library.empty:
                recommendations = self.dataset[~self.dataset['name'].isin(user_library['Name'])]
            else:
                recommendations = self.dataset

            # Sort and recommend
            recommendations = recommendations.sort_values(by=['similarity', 'num_reviews'], ascending=[False, False])

            if not recommendations.empty:
                top_game = recommendations.iloc[0]
                response = (
                    f"🎮 **Recommended Game:** [{top_game['name']}]({top_game['url']})\n"
                    f"📝 **Description:** {top_game['full_desc']}\n"
                    f"🏷️ **Genres:** {top_game['categories']}\n"
                    f"💯 **User Reviews:** {top_game['review_txt']}\n"
                    f"💲 **Price:** {top_game['price']}\n"
                )
            else:
                response = "❗ No suitable recommendations found. Try a different prompt!"

            await ctx.respond(response)
        except Exception as e:
            await ctx.respond(f"❗ An error occurred: {str(e)}")

def setup(bot):
    bot.add_cog(GameRecommender(bot))