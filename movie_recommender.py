import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import discord
from discord.ext import commands
import random

###############################################################################################################
#										RECOMMENDATION SYSTEMS
###############################################################################################################

##Step 1: Read CSV File

df = pd.read_csv("movie_dataset.csv")

##Step 2: Select Features

features = ['keywords','cast','genres','director']

##Step 3: Create a column in DF which combines all selected features

for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	try:	
		return row['keywords']+ " " + row['cast']+ " " + row['genres']+ " " + row['director']
	except:
		print("Error : ",row)

df["combined_features"] = df.apply(combine_features,axis=1)

##Step 4: Create count matrix from this new combined column

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

##Step 5: Compute the Cosine Similarity based on the count_matrix

cosine_sim = cosine_similarity(count_matrix)
movie_user_likes = "Avatar"

## Step 6: Get index of this movie from its title

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]


movie_index = get_index_from_title(movie_user_likes)
similar_movies = list(enumerate(cosine_sim[movie_index]))

## Step 7: Get a list of similar movies in descending order of similarity score

sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1],reverse=True)

## Step 8: Print titles of first 10 movies

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]
i=0
#print("Because you liked ", movie_user_likes , ", you should like these movies : \n")
for element in sorted_similar_movies:
	if i == 0:
		i+=1
		continue
		
	#print(get_title_from_index(element[0]))
	i+=1
	if i>10:
		break



########################################################################################################
# 												API / BOT
########################################################################################################
api_key = "f825c7230b434c69136a7516a6b98175"

import requests





bot = commands.Bot(command_prefix="?", description="Movie Chatbot")

@bot.event
async def on_ready():
	print("Ready !")


@bot.command()
async def hey(ctx):
	liste=["Hey welcome to my server !", "Hello buddy", "Hi, how can I help you ?", "Hello :D", "Heeellllooooo", "My name is Chatbot Movie"]
	await ctx.send(random.choice(liste))

@bot.command()
async def what(ctx):
	await ctx.send("Type ?movie **[movie]** to see an overview of a movie. 🎥")
	await ctx.send("Type ?recommend **[movie]** to see have some recommendations of movies. 🎬")
	await ctx.send("Type ?hey to discuss with me 👋")
	await ctx.send("Type ?creators to see who built me ! 👨‍💻")
	await ctx.send("Type ?hi to know how I feel 😄")

@bot.command()
async def creators(ctx):
	await ctx.send("I have been created by Bilal SELMI & RATSIMBAZAFY Lalaina :)")

@bot.command()
async def hi(ctx):
	liste=["I am really happy to see  you", "I'm glad to see you", "I enjoy your presence", "I feel like a bee in a honey pot !", "I LOVE MOVIES 🎥"]
	await ctx.send(random.choice(liste))


@bot.command()
async def recommend(ctx, texte):

	if(texte not in df["title"].to_list()):
		listesim=[]
		for row in df["title"]:
			sim = similar(texte,row)
			listesim.append(sim)
		if max(listesim) < 0.5:
			print(max(listesim))
			print("I do not know this movie")
		else:
			texte = df["title"][np.argmax(listesim)]
			await ctx.send("Did you mean " + texte + " ?")
			print(texte)
			
	try:
		movie_index = get_index_from_title(texte)
		similar_movies = list(enumerate(cosine_sim[movie_index]))
		sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1],reverse=True)
		await ctx.send("Because you liked "+ texte + ", you should like these movies : \n\n")
		i=0
		for element in sorted_similar_movies:
			if i == 0:
				i+=1
				continue
				
			await ctx.send(get_title_from_index(element[0]))
			i+=1
			if i>10:
				break
	except:
		await ctx.send("I do not know this movie.")


@bot.command()
async def movie(ctx,*texte):
	#texte = texte.replace(" ","+")
	print(texte)
	response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=f825c7230b434c69136a7516a6b98175&language=en-US&page=1&include_adult=false&query={texte}")
	print(f"https://api.themoviedb.org/3/search/movie?api_key=f825c7230b434c69136a7516a6b98175&language=en-US&page=1&include_adult=false&query={texte}")
	try:
		await ctx.send(response.json()['results'][0]['overview'])
		await ctx.send("\nIt was released in " + response.json()['results'][0]['release_date'])
		await ctx.send("https://www.themoviedb.org/t/p/w1280/"+ response.json()['results'][0]['poster_path'])
	except:
		await ctx.send("I don't know this movie, please write another one.")

bot.run("ODI1NDUwMzQzMTM1MTgyOTIw.YF-GiQ.GiLWzATbeYxcMe0f3GUHOBhwCx0")

