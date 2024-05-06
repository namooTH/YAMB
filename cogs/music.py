import wavelink
import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed
from wavelink import Queue

from time import strftime
from time import gmtime

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    group = app_commands.Group(name="music", description="music stuff")

    async def get_queue(self, guild):
        if not guild.id in self.bot.music_queue:
            self.bot.music_queue[guild.id] = Queue()
        return self.bot.music_queue[guild.id]

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload):
        await self.play_next_track(guild=payload.player.guild)

    @group.command(name="play", description="song name or the link")
    async def music(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer()
        if not interaction.guild.voice_client:
            await interaction.user.voice.channel.connect(cls=wavelink.Player)

        vc = interaction.guild.voice_client
        queue = await self.get_queue(guild=interaction.guild)

        try:
            tracks: wavelink.Search = await wavelink.Playable.search(search)
        except Exception as e:
            return await interaction.response.send_message(f'Something stupid has occured please try again:\n```{e}```')
        if not tracks:
            return await interaction.response.send_message(f'It was not possible to find the song: `{search}`')

        track: wavelink.Playable = tracks[0]
        track.extras = {"requester": interaction.user.name}
        vc.queue.put(track)

        self.music_channel = interaction.channel
        embed = Embed(title="🎵 Song added to the queue.", description=f'`{track.title} - {track.author}` was added to the queue.')
        await interaction.followup.send(embed=embed)
        if not vc.playing:
            await self.play_next_track(guild=interaction.guild)
#        else:
#            embed = Embed(title="🎵 Song added to the queue.", description=f'`{track.title} - {track.author}` was added to the queue.')
#            await interaction.followup.send(embed=embed)
        
    async def play_next_track(self, guild):
        vc = guild.voice_client
        queue = await self.get_queue(guild=guild)

        if not queue.is_empty:
            track = vc.queue.get()
            await vc.play(track)
            embed = Embed(title="🎵 playing now", description=f'`{track.title} - {track.author}` is playing now.')
            await self.music_channel.send(embed=embed)

    @group.command(name="stop", description="stop the everything")
    async def stop(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        await vc.stop()
        embed = Embed(title="⏹️ Music stopped", description="The music has been stopped.")
        await interaction.response.send_message(embed=embed)
        await vc.disconnect()

    @group.command(name="pause", description="pause everything")
    async def pause(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        await vc.pause(True)
        embed = Embed(title="⏸️ Music paused", description="The music has been paused")
        await interaction.response.send_message(embed=embed)

    @group.command(name="resume", description="pause everything")
    async def resume(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        await vc.pause(False)
        embed = Embed(title="▶️ Music Resumed", description="The music has been resumed.")
        await interaction.response.send_message(embed=embed)

    @group.command(name="skip", description="skip song")
    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        queue = await self.get_queue(guild=interaction.guild)

        if not queue.is_empty:
            await vc.stop()
            next_track = queue.pop()
            await vc.play(next_track)
            embed = Embed(title="⏭️ Song skipped", description=f'Playing the next song in the queue: `{next_track.title}`.')
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("There are no songs in the queue to skip")

    @group.command(name="queue", description="list queue")
    async def queue(self, interaction: discord.Interaction):
        queue = await self.get_queue(guild=interaction.guild)
        if not queue:
            embed = Embed(title="📜 Playlist", description="The queue is empty.")
            await interaction.response.send_message(embed=embed)
        else:
            queue_list = "\n".join([f"- {track.title}" for track in queue])
            embed = Embed(title="📜 Playlist", description=queue_list)
            await interaction.response.send_message(embed=embed)

    @group.command(name="current_playing", description="what is currently playing")
    async def current_playing(self, interaction: discord.Interaction):
        queue = await self.get_queue(guild=interaction.guild)
        vc = interaction.guild.voice_client

        progressbar_length = 50
        progressbar = ""
        currentprogress = int(vc.position / vc.current.length * progressbar_length)

        for i in range(progressbar_length):
            if i == currentprogress:
                progressbar += "▶"
                continue
            if i > currentprogress:
                progressbar += "-"
            else:
                progressbar += "="
        embed = Embed(title=f"# {vc.current.title}", color=discord.Color.from_rgb(237, 154, 225), description=f'### by {vc.current.author}\n{progressbar}\n- {strftime("%H:%M:%S", gmtime(vc.position / 1000))} - {strftime("%H:%M:%S", gmtime(vc.current.length / 1000))}')
        embed.add_field(name="Requested by:", value=f'`{vc.current.extras.requester}`', inline=True)
        if queue:
            embed.add_field(name="Next up:", value=f"`{queue[0].title} - {queue[0].author}`" , inline=True)
        embed.set_thumbnail(url=vc.current.artwork)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(music(bot))