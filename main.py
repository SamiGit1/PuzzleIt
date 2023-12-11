import discord
import time
from discord.ext import commands
import asyncio
import random
import json
import praw
from datetime import datetime
import requests
import datetime
from periodic_table_data import periodic_table_data


quotes = {}
name_values = {}
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')
  synced = await bot.tree.sync()
  print("SLASH CMDS synced:", len(synced), "commands")














games = {}

@bot.command(aliases=['pt'])
async def periodic(ctx, element_name_or_symbol_or_number: str):
    element = None
    for data in periodic_table_data:
        if data["name"].lower() == element_name_or_symbol_or_number.lower() or data["symbol"].lower() == element_name_or_symbol_or_number.lower() or str(data["number"]) == element_name_or_symbol_or_number:
            element = data
            break

    if element:
        

        embed = discord.Embed(title=f"Element: {element['name']} ({element['symbol']})", color=0x3498db)
        embed.set_thumbnail(url=element["image"]["url"]) 
        embed.add_field(name="Atomic Number", value=str(element["number"]), inline=True)
        embed.add_field(name="Electron Configuration", value=electron_config, inline=True)
        embed.add_field(name="Category", value=element["category"], inline=True)
        embed.add_field(name="Appearance", value=element["appearance"], inline=True)
        embed.add_field(name="Atomic Mass", value=str(element["atomic_mass"]), inline=True)
        embed.add_field(name="Boiling Point", value=str(element["boil"]), inline=True)
        embed.add_field(name="Melting Point", value=str(element["melt"]), inline=True)
        embed.add_field(name="Density", value=str(element["density"]), inline=True)
        embed.add_field(name="Molar Heat", value=str(element["molar_heat"]), inline=True)
        embed.add_field(name="Electronegativity", value=str(element["electronegativity_pauling"]), inline=True)
        embed.add_field(name="Electron Affinity", value=str(element["electron_affinity"]), inline=True)
        embed.add_field(name="Ionization Energies", value=', '.join(map(str, element["ionization_energies"])), inline=False)
        embed.set_image(url=element["bohr_model_image"])  
        embed.add_field(name="3D Model", value=element["bohr_model_3d"], inline=False)  
        embed.set_image(url=element["spectral_img"])  
        embed.set_footer(text="Source: " + element["source"])
        await ctx.send(embed=embed)
    else:
        await ctx.send("Element not found!")


@bot.tree.command(name="hello")
async def ping(ctx):
  await ctx.send(f'Ping **{round(bot.latency* 1000)}** ms')


@bot.command()
async def bored(ctx, activity=None):
    if activity is None:
        boreUrl = requests.get("http://www.boredapi.com/api/activity")
    else:
        boreUrl = requests.get(f"http://www.boredapi.com/api/activity?{activity}")

    boreData = boreUrl.json()
    dictActivity = boreData['activity']
    dictType = boreData['type']
    dictLink = boreData['link']
    dictParticipants = boreData['participants']
    dictPrice = boreData['price']
    dictAcc = boreData['accessibility']
    dictKey = boreData['key']

    boreEmbed = discord.Embed(
        title="Activity For Bored",
        description=f"**Activity**  = {dictActivity}\n**Type** = {dictType}\n**Participants** = {dictParticipants}\nLink = {dictLink}\nPrice = {dictPrice}, Accessibility = {dictAcc}\n**Key** = {dictKey}",
        color=discord.Color.random(),
    )
    boreEmbed.set_footer(text="You can set the type, participants, price, key, accessibility.")
    await ctx.send(embed=boreEmbed)




















@bot.command()
async def agify(ctx, pname):
  agifyUrl = f"https://api.agify.io?name={pname}"
  if isinstance(pname, str) == False:
    await ctx.send(
      "Please enter the name properly. Make sure there are no numbers.")
  else:
    agefile = requests.get(agifyUrl)
    agedata = agefile.json()
    age = agedata['age']

    age_embed = discord.Embed(
      title=f"Agify-- Find the age of a person, given their name only!",
      description=
      f"According to my very accurate sources, the age of **{pname}** should be **{age}**",
      color=discord.Color.random())
    await ctx.send(embed=age_embed)


@bot.command()
async def country(ctx, *, cname):
  cname = cname.replace(" ", "%20")

  cinfo = requests.get(
    f"https://restcountries.com/v3.1/name/{cname}?fullText=true")
  cdata = cinfo.json()

  if cinfo.status_code == 200 and cdata:
    country_data = cdata[
      0] 

    embed = discord.Embed(
      title=
      f"{country_data['name']['official']} ({country_data['name']['common']})",
      color=discord.Color.blue())

    embed.set_thumbnail(url=country_data['flags']['png'])
    embed.add_field(name="Capital",
                    value=country_data['capital'][0],
                    inline=True)

    if 'currencies' in country_data and isinstance(
        country_data['currencies'], list) and country_data['currencies']:
      currency = country_data['currencies'][0]
      currency_name = currency['name']
      currency_symbol = currency['symbol'] if 'symbol' in currency else ''
      embed.add_field(name="Currency",
                      value=f"{currency_name} ({currency_symbol})",
                      inline=True)

    if 'population' in country_data:
      embed.add_field(name="Population",
                      value=country_data['population'],
                      inline=True)

    if 'gini' in country_data:
      embed.add_field(name="Gini Index",
                      value=country_data['gini'],
                      inline=True)

    if 'area' in country_data:
      area = country_data['area']
      area_unit = country_data[
        'area_unit'] if 'area_unit' in country_data else 'square kilometers'
      embed.add_field(name="Area", value=f"{area} {area_unit}", inline=True)

    

    await ctx.send(embed=embed)
  else:
    await ctx.send(f"Failed to fetch information for {cname}.")


@bot.command()
async def picofday(ctx, date=None):
  if date:
    try:
      date = datetime.datetime.strptime(date, '%d-%m-%Y').date()
    except ValueError:
      await ctx.send("Invalid date format. Please use 'dd-mm-yyyy' format.")
      return
  else:
    date = datetime.date.today()

  api_key = 'LJJNXnIEYS5ZuoRVBYVndkA93H0DqS1gZFMNVZER'
  nasa_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
  moon_url = f'https://api.nasa.gov/planetary/earth/assets?lon=0&lat=0&date={date}&dim=0.1&api_key={api_key}'
  mars_url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date}&api_key={api_key}'

  try:
    
    apod_response = requests.get(nasa_url)
    apod_data = apod_response.json()
    apod_embed = discord.Embed(
      title=f"The Astronomy Picture of the Day for {date.strftime('%d-%m-%Y')}",
      color=0x000000)
    apod_embed.set_image(url=apod_data['url'])
    apod_embed.description = apod_data['explanation']
    await ctx.send(embed=apod_embed)

    moon_response = requests.get(moon_url)
    moon_data = moon_response.json()
    moon_embed = discord.Embed(title='Picture of the Moon', color=0x000000)
    moon_embed.set_image(url=moon_data['url'])
    await ctx.send(embed=moon_embed)


    mars_response = requests.get(mars_url)
    mars_data = mars_response.json()
    if mars_data['photos']:
      mars_embed = discord.Embed(title='Picture of Mars', color=0x000000)
      mars_embed.set_image(url=mars_data['photos'][0]['img_src'])
      await ctx.send(embed=mars_embed)
    else:
      await ctx.send('No Mars picture available for the given date.')

  except requests.exceptions.RequestException:
    await ctx.send('Error occurred while retrieving NASA data.')


@bot.event
async def on_member_join(member):
  guild = member.guild
  welcome_channel_id = 1073596557066252311

  welcome_channel = discord.utils.get(guild.text_channels,
                                      id=welcome_channel_id)

  if welcome_channel:
    message = f"◆︎Welcome {member.name} to {guild.name}! Enjoy your stay!"
    await welcome_channel.send(message)


def get_eightball_response():
  responses = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
    "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
    "My reply is no.", "My sources say no.", "Outlook not so good.",
    "Very doubtful."
  ]
  return random.choice(responses)


@bot.command(name='8ball')
async def eight_ball(ctx):
  response = get_eightball_response()

  embed = discord.Embed(title='8Ball🎱',
                        description=response,
                        color=discord.Color.blue())

  await ctx.send(embed=embed)


@bot.event
async def on_disconnect():
  save_name_values()


def load_name_values():
  try:
    with open("name_values.json", "r") as file:
      data = file.read()
      if data:
        name_values.update(json.loads(data))
  except (FileNotFoundError, json.JSONDecodeError):
    pass


def save_name_values():
  with open("name_values.json", "w") as file:
    json.dump(name_values, file)


load_name_values()


def fetch_pokemon_info(pokemon_name: str) -> dict:
  url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    return data
  else:
    return None


async def send_pokedex_embed(ctx: commands.Context, pokemon_name: str) -> None:
  pokemon_data = fetch_pokemon_info(pokemon_name)

  if pokemon_data:
    name = pokemon_data["name"].capitalize()
    sprite_url = pokemon_data["sprites"]["front_default"]
    types = [t["type"]["name"].capitalize() for t in pokemon_data["types"]]
    abilities = [
      a["ability"]["name"].capitalize() for a in pokemon_data["abilities"]
    ]
    stats = pokemon_data["stats"]
    base_experience = pokemon_data["base_experience"]

    embed = discord.Embed(title=f"{name} Pokédex Information",
                          color=random_color())
    embed.set_thumbnail(url=sprite_url)
    embed.add_field(name="Name", value=name, inline=True)
    embed.add_field(name="Type(s)", value=", ".join(types), inline=True)
    embed.add_field(name="Abilities", value=", ".join(abilities), inline=False)

    for stat in stats:
      stat_name = stat["stat"]["name"].capitalize()
      stat_value = stat["base_stat"]
      embed.add_field(name=stat_name, value=stat_value, inline=True)

    embed.add_field(name="Base Experience",
                    value=base_experience,
                    inline=False)

    await ctx.send(embed=embed)
  else:
    await ctx.send("Pokémon not found!")




@bot.command()
async def pokedex(ctx: commands.Context, *, pokemon_name: str) -> None:
  await send_pokedex_embed(ctx, pokemon_name)


@bot.command()
async def test(ctx, arg):
  await ctx.send(arg)


@bot.command()
async def rizz(ctx, arg=""):
  if arg:
    lowercase_arg = arg.lower()
    if lowercase_arg in name_values:
      value = name_values[lowercase_arg]
    else:
      value = random.randint(1, 100)
      name_values[lowercase_arg] = value
    save_name_values() 
    await ctx.send(f"{arg} has {value}% rizz")
  else:
    await ctx.send("You must provide a name next to your command.")


@bot.command()
async def printrizz(ctx):
  await ctx.send(name_values)


@bot.command()
async def randint(ctx, start:int, end:int):
  await ctx.send(f"A random number between the numbers {start} and {end} is {random.randint(start, end)}")

def load_quotes():
  try:
    with open('quotes.json', 'r') as f:
      return json.load(f)
  except FileNotFoundError:
    return []


def save_quotes(quotes):
  with open('quotes.json', 'w') as f:
    json.dump(quotes, f)


@bot.command()
async def add(ctx, *, quote):
  quotes = load_quotes()

  quotes.append(quote)

  save_quotes(quotes)

  await ctx.send(f'Added quote: {quote}')



@bot.event
async def on_message(message):
  if message.author.bot:
    return

  if message.content.lower() == '$unmute':
    role_name = 'SHUT'
    role = discord.utils.get(message.guild.roles, name=role_name)
    if role in message.author.roles:
      await message.author.remove_roles(role)
      await message.channel.send(f'{message.author.mention} has been unmuted!')
    else:
      await message.channel.send(
        f'{message.author.mention}, you are not muted.')

  await bot.process_commands(message)


@bot.command()
async def email(ctx, recipient: discord.User, selfname, *, message):
  await recipient.send(f"You received an email from {selfname}:\n{message}")
  sent_message = await ctx.send(f'Message sent to {recipient.name}!')

  time.sleep(1)
  await ctx.message.delete()
  await sent_message.delete()


@email.error
async def email_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(
      "Missing required arguments. Please use the following format: `$email <@recipient or give their id> <put any username for yourself here> <message>`."
    )


reddit = praw.Reddit(client_id='DGJ_9LTjpCQDJ8x-An9RZg',
                     client_secret='mpoe_u__gIsD3HV6LdXJs3jcEAPxPQ',
                     user_agent='discord bot that fetches memes')


@bot.command()
async def meme(ctx):
  subreddit = reddit.subreddit('anarchychess')
  memes = subreddit.random_rising(
    limit=5) 

  for submission in memes:
    if not submission.stickied and submission.url.endswith(
      ('.jpg', '.png',
       '.gif')):  
      embed = discord.Embed(
        title=submission.title,
        url=f'https://www.reddit.com{submission.permalink}',
        description='Collected from Reddit',
        color=discord.Color.blue())
      embed.set_image(url=submission.url)
      embed.set_footer(text='r/anarchychess')

      await ctx.send(embed=embed)
      break  


# Command to display a random quote from the JSON file
@bot.command()
async def wow(ctx):
  quotes = load_quotes()

  if quotes:
    quote = random.choice(quotes)
    await ctx.send(f' {quote}')
  else:
    await ctx.send('No quotes found.')


@bot.command()
async def nword(ctx):
  await ctx.send("ninja")


@bot.command()
async def sword(ctx):
  await ctx.send("samurai")


@bot.command()
async def printquote(ctx):
  await ctx.send(quotes)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided."):
  await member.kick(reason=reason)
  await ctx.send(f'{member.mention} has been kicked. \nReason: {reason}')


@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have permission to use this command.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided."):
  await member.ban(reason=reason)
  await ctx.send(f'{member.mention} has been banned. \nReason: {reason}')


@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have permission to use this command.")

 



@bot.command()
async def rating(ctx, username):
    try:
        url = f"https://api.chess.com/pub/player/{username}/stats"
        headers = {
            "User-Agent": "My Python Application. Contact me at email@example.com",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            player_data = response.json()

            blitz_rating = player_data['chess_blitz']['last']['rating']
            bullet_rating = player_data['chess_bullet']['last']['rating']
            rapid_rating = player_data['chess_rapid']['last']['rating']

            embed = discord.Embed(
                title=f"⭐ {username}'s Chess Stats",
                color=discord.Color.random()
            )
            embed.add_field(name="⚡ Blitz Rating", value=blitz_rating, inline=False)
            embed.add_field(name="🔫 Bullet Rating", value=bullet_rating, inline=False)
            embed.add_field(name="⌚ Rapid Rating", value=rapid_rating, inline=False)
            embed.set_footer(text="Requested By \n From Chess.com")

            await ctx.send(embed=embed)
        else:
            print(f"HTTP error occurred: {response.status_code} {response.text}")
            await ctx.send("Failed to retrieve data. Please try again later.")

    except Exception as e:
        error_message = "An unexpected error occurred. Please try again later."
        await ctx.send(error_message)
        print(f"Error: {str(e)}") 



@bot.command()
async def puzzle(ctx):
    try:
        url = "https://api.chess.com/pub/puzzle/random"
        headers = {
            "User-Agent": "My Python Application. Contact me at email@example.com"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        puzzle_data = response.json()

        title = puzzle_data["title"]
        puzzle_url = puzzle_data["url"]
        fen = puzzle_data["fen"]
        image = puzzle_data["image"]

        move_info = fen.split()  # Split FEN string
        current_player = "Black" if move_info[1] == "b" else "White"

        embed = discord.Embed(
            title=f"🧩 {title}",
            url=puzzle_url,
            color=discord.Color.random()
        )
        embed.add_field(name="FEN", value=fen, inline=False)
        embed.add_field(name="Current Move", value=f"{current_player} to move", inline=False)

        embed.set_image(url=image)
        embed.set_footer(text="Please note that puzzles take around 15 seconds to reset.\nTaken from chess.com.")

        await ctx.send(embed=embed)

    except Exception as e:
        error_message = "An unexpected error occurred. Please try again later."
        await ctx.send(error_message)
        print(f"Error: {str(e)}")




@bot.command(aliases=["val"])
async def valorant(ctx, agent):
   try:
    url = "https://valorant-api.com/v1/agents"
    headers = {
      "User-Agent": "My Python Application. Contact me at example@gmail.com"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    agent_data = response.json()
    agent_info = next((a for a in agent_data["data"] if a["displayName"].lower() == agent.lower()), None)

    if agent_info:
      name = agent_info["displayName"]
      description = agent_info["description"]
      image = agent_info["displayIcon"]
      abilities = agent_info["abilities"]

      embed = discord.Embed(
        title=f"🧩 {name}",
        description=description,
        color=discord.Color.random()
      )

      for ability in abilities:
        ability_name = ability["displayName"]
        ability_description = ability["description"]
        ability_image = ability["displayIcon"]
        embed.add_field(name=ability_name, value=ability_description, inline=False)
        embed.set_image(url=ability_image)

      embed.set_thumbnail(url=image)
      embed.set_footer(text="Taken from valorant-api.com")
      await ctx.send(embed=embed)
    else:
      await ctx.send(f"Agent '{agent}' not found.")

   except Exception as e:
    await ctx.send("An unexpected error occurred. Please try again later.")
    print(f"Error: {str(e)}")






@bot.tree.command(name="deez", description="Says hello to the user.")
async def deez(interaction: discord.Interaction):
   await interaction.response.send_message(content="Hello!")






@bot.command()
async def daily(ctx):
    try:
        url = "https://api.chess.com/pub/puzzle"
        headers = {
            "User-Agent": "My Python Application. Contact me at email@example.com",
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        puzzle_data = response.json()

        title = puzzle_data["title"]
        url = puzzle_data["url"]
        fen = puzzle_data["fen"]
        image = puzzle_data["image"]
        move_info = fen.split()  # Split FEN string
        current_player = "Black" if move_info[1] == "b" else "White"

      
        embed = discord.Embed(
            title=f"🧩 {title}",
            url=url,
            color=discord.Color.random()
        )
        embed.add_field(name="FEN", value=fen, inline=False)
        embed.add_field(name="Current Move", value=f"{current_player} to move", inline=False)
        embed.set_image(url=image)
        embed.set_footer(text="Chess.com Daily Puzzle")

        await ctx.send(embed=embed)

    except Exception as e:
        
        error_message = "An unexpected error occurred. Please try again later."
        await ctx.send(error_message)
        print(f"Error: {str(e)}")












@bot.command()
async def kanye(ctx):
    response = requests.get("https://api.kanye.rest/")
    if response.status_code == 200:
        quote = response.json()["quote"]

    

        embed = discord.Embed(title="Kanye West Quote", description=quote, color=discord.color(random.randint(0, 0xFFFFFF)))
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to fetch Kanye West quote.")










@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided."):

    role = discord.utils.get(ctx.guild.roles, name="SHUT")
    
    if role is not None:
       
        await member.add_roles(role)

       
        embed = discord.Embed(
            title="Member Muted",
            description=f"{member.mention} has been muted.",
            color=discord.Color.red()  # You can customize the color
        )
        embed.add_field(name="Reason", value=reason, inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("The 'SHUT' role does not exist. Please create the role and try again.")



@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason="No reason provided."):
    # Check if the role exists in the guild
    role = discord.utils.get(ctx.guild.roles, name="SHUT")
    
    if role is not None:
        
        await member.remove_roles(role)

        # Create an embed for the response
        embed = discord.Embed(
            title="Member Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.green() 
        )
        embed.add_field(name="Reason", value=reason, inline=False)

        # Send the embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("The person is not muted.")



@bot.command(aliases=["clear"])
async def purge(ctx, mnum: int):
  
    if ctx.author.guild_permissions.administrator:
       
        channel = ctx.channel

        
        deleted_messages = await channel.purge(limit=mnum)

        
        message = await ctx.send(f"Deleted {len(deleted_messages)} messages.")

        await asyncio.sleep(2)

       
        await message.delete()
    else:
       
        await ctx.send("You don't have permission to use this command.")

















bot.run(
  "MTEwNjI5MjMzNjQ5MDcyMTMzMA.GWcVKI.VlIrdumvBcAG0MkKNvk4f82HCJEF4ZQDZ1-6lo"
)
print("Working...")
