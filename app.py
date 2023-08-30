import oci
import os
import interactions
from interactions import slash_command, SlashContext, OptionType, slash_option
from dotenv import load_dotenv
load_dotenv()

bot = interactions.Client(token=os.getenv("DISCORD_BOT_TOKEN"))


@slash_command(name="start", description="Start the server")
@slash_option(name="secret", description="server secret", required=True, opt_type=OptionType.STRING)
async def my_command_function(ctx: SlashContext, secret: str):
  if (secret == os.getenv("SERVER_SECRET")):
    start_instance()
    await ctx.send("It's starting up now.")
  else:
    await ctx.send("Incorrect server secret.")

def start_instance():
  config = oci.config.from_file()
  core_client = oci.core.ComputeClient(config)

  try:
    instance_action_response = core_client.instance_action(
      instance_id=os.getenv("ORACLE_INSTANCE_ID"),
      action="START"
    )
  except oci.exceptions.ServiceError as e:
    print(f"Error occurred while shutting down the instance: {e}")

  print(instance_action_response.data)

bot.start()