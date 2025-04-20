import time
import platform
import os
import logging
import random
import asyncio
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
        """Handle the /ping command"""
        # Create a unique task ID for this command execution
        task_id = f"ping_{event.id}_{int(time.time())}"
        
        # Create a task for command processing
        task = asyncio.create_task(self._process_ping(event))
        
        # Store the task in the bot's handlers dictionary with the unique task ID
        self.client.handlers[task_id] = task
        
        # Add task to active tasks set
        self.client.active_tasks.add(task)
        task.add_done_callback(self.client.active_tasks.discard)
        task.add_done_callback(lambda t: self.client.handlers.pop(task_id, None))
    
    async def _process_ping(self, event):
        """Process ping command asynchronously"""
        start_time = time.time()
        message = await event.respond("Pinging...")
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        # Get service information
        service = "Azure"
        location = "Unknown"
        
        # Try to get Azure region from environment
        try:
            # First try to get from environment variables
            if 'AZURE_REGION' in os.environ:
                location = os.environ['AZURE_REGION']
            elif 'AZURE_LOCATION' in os.environ:
                location = os.environ['AZURE_LOCATION']
            
            # If still unknown, try to get from Azure metadata service
            if location == "Unknown":
                import requests
                try:
                    # Azure Instance Metadata Service
                    response = requests.get(
                        'http://169.254.169.254/metadata/instance?api-version=2021-02-01',
                        headers={'Metadata': 'true'},
                        timeout=2
                    )
                    if response.status_code == 200:
                        metadata = response.json()
                        location = metadata.get('compute', {}).get('location', 'Unknown')
                except:
                    pass
            
            # If still unknown, try to get from system information
            if location == "Unknown":
                try:
                    import platform
                    if platform.system() == 'Linux':
                        with open('/etc/os-release', 'r') as f:
                            for line in f:
                                if line.startswith('PRETTY_NAME='):
                                    location = line.split('=')[1].strip().strip('"')
                                    break
                except:
                    pass
        except Exception as e:
            logger.error(f"Error getting location: {e}")
            pass
        
        # Format the response
        response = f"{latency}ms\nService: {service}\nLocation: {location}"
        
        # Edit the message with the response
        await message.edit(response)
    
    async def hi_dog_handler(self, event):
        """Handle /hi_dog command"""
        # Create a unique task ID for this command execution
        task_id = f"hi_dog_{event.id}_{int(time.time())}"
        
        # Create a task for command processing
        task = asyncio.create_task(self._process_hi_dog(event))
        
        # Store the task in the bot's handlers dictionary with the unique task ID
        self.client.handlers[task_id] = task
        
        # Add task to active tasks set
        self.client.active_tasks.add(task)
        task.add_done_callback(self.client.active_tasks.discard)
        task.add_done_callback(lambda t: self.client.handlers.pop(task_id, None))
    
    async def _process_hi_dog(self, event):
        """Process hi_dog command asynchronously"""
        try:
            # Dog ASCII arts
            dog_arts = [
                """
                /\  /\
            =( ´ •⁠ω• ⁠)=
            / ͡      ︵\
            (⁠人_____づ_づ
        """,
                """
                .·´¯`·.  ·´¯·.
        |
        |   |__     ╲  ╲ ╲
        |ロ |       ╲╲     /\~/\
        |ロ |        ╲ ╲  ( •ω • )
        |ロ |         ╲   ⊂     づ
        |ロ |          ╲ ╲     ⊃⊃╲
        |ロ |___        ╲| _ ╲|__
        """,
                """
        ╱|、
        (˚ˎ 。7  
        |、˜〵          
        じしˍ,)ノ
        """,
                """
         |\_/|                  
         | @ @   Woof! 
         |   <>              _  
         |  _/\------____ ((| |))
         |               `--' |   
        ____|_       ___|   |___.' 
        /_/_____/____/_______|
        """,
                """
         |\|\
        ..    \       .
        o--     \\    / @)
        v__///\\\\__/ @
        {           }
        {  } \\\{  }
        <_|      <_|
        """,
                """
        ⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢠⣤⡀⣾⣿⣿⠀⣤⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⢿⣿⡇⠘⠛⠁⢸⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠈⣉⣤⣾⣿⣿⡆⠉⣴⣶⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⣾⣿⣿⣿⣿⣿⣿⡀⠻⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠙⠛⠻⢿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠈⠙⠋⠁⠀⠀
        """,
                """
        (\_/)
        ( •,•)
        (")_(")
        """,
                """
        _██_
        ‹(•¿•)›
        ..(█)
        .../ I
        """
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
        # Create a unique task ID for this command execution
        task_id = f"test_{event.id}_{int(time.time())}"
        
        # Create a task for command processing
        task = asyncio.create_task(self._process_test(event))
        
        # Store the task in the bot's handlers dictionary with the unique task ID
        self.client.handlers[task_id] = task
        
        # Add task to active tasks set
        self.client.active_tasks.add(task)
        task.add_done_callback(self.client.active_tasks.discard)
        task.add_done_callback(lambda t: self.client.handlers.pop(task_id, None))
    
    async def _process_test(self, event):
        """Process test command asynchronously"""
        try:
            await event.reply("Bot is running! This is a test response.")
        except FloodWaitError as e:
            await self.handle_flood_wait_error(event, e)
        except Exception as e:
            await self.handle_error(event, e)
    
    async def env_handler(self, event):
        """Handle /env command"""
        # Create a unique task ID for this command execution
        task_id = f"env_{event.id}_{int(time.time())}"
        
        # Create a task for command processing
        task = asyncio.create_task(self._process_env(event))
        
        # Store the task in the bot's handlers dictionary with the unique task ID
        self.client.handlers[task_id] = task
        
        # Add task to active tasks set
        self.client.active_tasks.add(task)
        task.add_done_callback(self.client.active_tasks.discard)
        task.add_done_callback(lambda t: self.client.handlers.pop(task_id, None))
    
    async def _process_env(self, event):
        """Process env command asynchronously"""
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
        # Create a unique task ID for this command execution
        task_id = f"unwire_{event.id}_{int(time.time())}"
        
        # Create a task for command processing
        task = asyncio.create_task(self._process_unwire(event))
        
        # Store the task in the bot's handlers dictionary with the unique task ID
        self.client.handlers[task_id] = task
        
        # Add task to active tasks set
        self.client.active_tasks.add(task)
        task.add_done_callback(self.client.active_tasks.discard)
        task.add_done_callback(lambda t: self.client.handlers.pop(task_id, None))
    
    async def _process_unwire(self, event):
        """Process unwire command asynchronously"""
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