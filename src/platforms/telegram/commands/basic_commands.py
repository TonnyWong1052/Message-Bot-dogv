import time
import platform
import os
import logging
import random
from telethon import events
from telethon.errors.rpcerrorlist import FloodWaitError
from .base import CommandHandler
from ..commands.utils import MessageHelper
from services.unwire_fetch import fetch_unwire_news, fetch_unwire_recent

logger = logging.getLogger("telegram_basic_commands")

class BasicCommandHandler(CommandHandler):
    """
    Basic command handler class for simple Telegram commands
    """
    
    def __init__(self, client, llm_client=None):
        """
        Initialize basic command handler
        
        Args:
            client: Telegram client
            llm_client: LLM client instance (optional)
        """
        super().__init__(client, llm_client)
    
    async def register_handlers(self):
        """
        Register all basic command handlers
        """
        self.client.add_event_handler(
            self.ping_handler,
            events.NewMessage(pattern=r'^/ping$')
        )
        
        self.client.add_event_handler(
            self.hi_dog_handler,
            events.NewMessage(pattern=r'^/hi_dog$')
        )
        
        self.client.add_event_handler(
            self.test_handler,
            events.NewMessage(pattern=r'^/test$')
        )
        
        self.client.add_event_handler(
            self.env_handler,
            events.NewMessage(pattern=r'^/env$')
        )
        
        self.client.add_event_handler(
            self.dotenv_handler,
            events.NewMessage(pattern=r'^/\.env$')
        )
        
        # Modified pattern to support /unwire with optional date parameter
        self.client.add_event_handler(
            self.unwire_handler,
            events.NewMessage(pattern=r'^/unwire(?:\s+\d{4}-\d{2}-\d{2})?$')
        )
        
        logger.info("Basic command handlers registered")
    
    async def ping_handler(self, event):
        """Handle /ping command"""
        try:
            # Get current timestamp
            start_time = time.time()
            
            # Reply with initial message
            message = await event.reply("Pinging...")
            
            # Calculate latency
            latency = round((time.time() - start_time) * 1000, 2)
            
            # Determine service type and location
            service_type = "Local"
            location = "Unknown"
            
            # Check if running in Azure (you can add more detailed checks)
            if os.getenv('AZURE_DEPLOYMENT') or os.getenv('AZURE_WEBSITE_NAME'):
                service_type = "Azure"
            
            # Create compact response format
            response = f"{latency}ms\nService: {service_type}\nLocation: {location}"
            
            # Update message with response
            await message.edit(response)
        except FloodWaitError as e:
            await self.handle_flood_wait_error(event, e)
        except Exception as e:
            await self.handle_error(event, e)
    
    async def hi_dog_handler(self, event):
        """Handle /hi_dog command"""
        try:
            # Dog ASCII arts
            dog_arts = [
                """
⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡤⠞⠋⠉⠀⠀⠀⠀⠀⠀⠀⠉⠙⠳⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡆⠀⠀⠀⠀⠀⠀⠀⠀
⢠⠇⠀⢰⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡄⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀    Sit, Stay,'N Play
⢸⠀⠀⢸⠀⠀⢰⣶⡀⠀⠀⠀⢠⣶⡀⠀⠀⡇⠀⢸⠂⠀⠀⠀⠀⠀⠀⠀
⠈⢧⣀⢸⡄⠀⠀⠉⠀⠀⠀⠀⠀⠉⠀⠀⢠⡇⣠⡞⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠉⠙⣇⠀⠂⠀⠀⢶⣶⣶⠀⠄⠀⠀⣾⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠞⠓⠤⣤⣀⣀⣠⣤⠴⠚⠉⠑⠲⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⣀⣠⣀⣀⣠⣀⡀⠀⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠰⡇⠀⠈⠁⠀⠈⡧⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀⠀⢠⠖⡆
⠀⠀⠀⠀⢸⠀⠀⠑⢦⡀⠀⣠⠞⠁⠀⢸⠀⠀⠀⠀⠀⠀⠈⣷⠞⠋⢠⠇
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠙⡞⠁⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⢹⢀⡴⠋⠀
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⡞⠉⠀⠀⠀
⠀⠀⠀⠀⢸⡀⠀⠀⠀⢠⣧⠀⠀⠀⠀⣸⡀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠳⠦⠤⠴⠛⠈⠓⠤⠤⠞⠁⠉⠛⠒⠚⠋⠁⠀⠀⠀⠀⠀⠀
                """,
                """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⣄⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠶⠋⠉⠙⢿⣿⣿⣿⣄⠈⢻⣶⠤⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⠈⣿⠋⠉⠙⢧⡀⢿⡄⢸⣷⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣾⣿⣷⣄⠀⠀⠀⠀⠀⠀⣴⣶⣶⡄⢸⡇⢸⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡏⣉⢻⣿⠟⠋⠀⠀⠀⠀⠀⠀⠿⠒⠻⣧⢸⡇⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡇⢻⡀⠻⡄⠀⣶⣿⣷⠀⠀⠀⣀⡀⠀⠈⠻⣧⢻⣄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣷⠸⣷⣄⣹⣆⣿⠋⠁⠀⠠⣿⣿⣟⠀⠀⢀⡿⠿⠿⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣄⠀⠈⠉⠛⢷⢰⠆⠀⠀⠀⠛⣿⠗⣺⣿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⢻⣶⣄⣸⠦⠤⠤⠤⠾⠥⠚⠹⣿⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠻⣿⠋⠛⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⡄⠀⠀⠀⠀
⠀⣠⢖⣢⠀⢀⠀⠀⢀⣴⣿⠁⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣧⠀⠀⠀⠀
⣾⣿⠋⣠⣾⠛⠀⣴⡿⠛⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀
⠈⠁⣰⡿⠁⢀⣾⠟⠁⠀⢻⣷⡄⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⡘⢿⡆⠀⠀⠀
⠀⠀⣿⡇⠀⣼⠃⠀⠀⠀⠈⣿⣿⡄⠀⠀⠀⠀⠘⣿⠇⠀⠀⠀⣠⣧⠈⢷⠀⠀⠀
⠀⠀⣿⣇⢰⣿⠀⠀⠀⠀⠀⣿⣿⣿⡄⠀⠀⠀⠀⡟⠀⠀⠀⣠⣴⣿⠃⠀⠘⡆⠀⠀
⠀⠀⢹⣿⣾⣧⠀⠀⠀⠀⣸⣿⣿⣿⡇⠀⠀⠀⢹⣦⣴⣾⣿⢿⡿⠀⠀⠀⣧⠀⠀
⠀⠀⠈⢻⣿⣿⣄⣼⣿⣶⣿⣿⣿⣿⣷⠀⠀⢀⣸⣿⡿⠟⠁⢸⠇⠀⢤⡾⠿⣦⡀
⠀⠀⠀⠀⠙⢿⡟⠉⠉⠉⠁⠈⠻⡏⠀⠰⠶⠛⠋⢹⡄⠀⠀⠸⡄⢀⠀⢸⡔⣆⢳
⠀⠀⠀⠀⠀⠀⠹⠤⠼⠤⠼⠷⠞⢷⣀⡀⠀⢰⠀⣦⣷⠀⠀⠀⠉⠙⠒⠚⠳⠞⠋
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠉⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""",
                """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡴⣆⠀⠀⠀⠀⠀⣠⡀ ᶻ 𝗓 𐰁 .ᐟ ⣼⣿⡗⠀⠀⠀⠀
⠀⠀⠀⣠⠟⠀⠘⠷⠶⠶⠶⠾⠉⢳⡄⠀⠀⠀⠀⠀⣧⣿⠀⠀⠀⠀⠀
⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣤⣤⣤⣤⣤⣿⢿⣄⠀⠀⠀⠀
⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀⠙⣷⡴⠶⣦
⠀⠀⢱⡀⠀⠉⠉⠀⠀⠀⠀⠛⠃⠀⢠⡟⠀⠀⠀⢀⣀⣠⣤⠿⠞⠛⠋
⣠⠾⠋⠙⣶⣤⣤⣤⣤⣤⣀⣠⣤⣾⣿⠴⠶⠚⠋⠉⠁⠀⠀⠀⠀⠀⠀
⠛⠒⠛⠉⠉⠀⠀⠀⣴⠟⢃⡴⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""",
                """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣠⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⠟⠁⠀⠀⠀⠹⣿⣿⣿⣿⣿⠟⠁⠀⠀⠹⣿⣿⡿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⢼⣿⠀⢿⣿⣿⣿⣿⠀⣾⣷⠀⠀⢿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣷⡀⠀⠀⠈⠋⢀⣿⣿⣿⣿⣿⡀⠙⠋⠀⢀⣾⣿⣿⠀⠀⠀⠀⠀
⢀⣀⣀⣀⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣾⣿⣷⣦⣤⣴⣿⣿⣿⣿⣤⠤⢤⣤⡄
⠈⠉⠉⢉⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⡀⠀
⠐⠚⠋⠉⢀⣬⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣥⣀⡀⠈⠀⠈⠛
⠀⠀⠴⠚⠉⠀⠀⠀⠉⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠁⠀⠀⠀⠉⠛⠢⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀""",
                """
                             ＿＿
　　　　　🌸＞　　フ
　　　　　| 　_　 _ l
　 　　　／` ミ＿xノ
　　 　 /　　　 　 |
　　　 /　 ヽ　　 ﾉ
　 　 │　　|　|　|
　／￣|　　 |　|　|
　| (￣ヽ＿_ヽ_)__)
　＼二つ"""
            ]
            
            # Choose a random dog art
            dog_art = random.choice(dog_arts)
            
            await event.reply(f"Woof! Hello there! 🐶\n{dog_art}")
        except FloodWaitError as e:
            await self.handle_flood_wait_error(event, e)
        except Exception as e:
            await self.handle_error(event, e)
    
    async def test_handler(self, event):
        """Handle /test command"""
        try:
            await event.reply("Bot is running! This is a test response.")
        except FloodWaitError as e:
            await self.handle_flood_wait_error(event, e)
        except Exception as e:
            await self.handle_error(event, e)
    
    async def env_handler(self, event):
        """Handle /env command"""
        try:
            # Get environment information
            environment = os.getenv('ENVIRONMENT', 'Not set')
            
            # Format response
            response = f"Environment: {environment.upper()}\n\n"
            
            await event.reply(response)
        except FloodWaitError as e:
            await self.handle_flood_wait_error(event, e)
        except Exception as e:
            await self.handle_error(event, e)
    
    async def dotenv_handler(self, event):
        """Handle /.env command - calls the same handler as /env"""
        await self.env_handler(event)
    
    async def unwire_handler(self, event):
        """
        Handle /unwire command - Fetch news from Unwire.hk
        
        Usage:
        /unwire - Get today's news
        /unwire 2025-04-15 - Get news from specific date
        """
        try:
            # Get the command text and split it
            command_text = event.message.text.split()
            
            # If no date specified, get today's news
            if len(command_text) == 1:
                news_content = fetch_unwire_news()
            else:
                # Try to get news for specified date
                date_str = command_text[1]
                # Validate date format (YYYY-MM-DD)
                try:
                    from datetime import datetime
                    datetime.strptime(date_str, '%Y-%m-%d')
                    news_content = fetch_unwire_news(date=date_str)
                except ValueError:
                    error_msg = "Invalid date format. Please use YYYY-MM-DD format (e.g., 2025-04-19)."
                    await event.respond(error_msg)
                    return
            
            # Send the news content
            await event.respond(news_content)
            
        except Exception as e:
            logger.error(f"Error in unwire_handler: {e}")
            error_msg = "Sorry, I couldn't fetch the news. Please try again later."
            await event.respond(error_msg) 