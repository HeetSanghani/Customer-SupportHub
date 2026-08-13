import asyncio
import logging
from typing import Callable, Coroutine, Dict

logger = logging.getLogger(__name__)

class AIDebouncer:
    """
    Manages debouncing of AI generation tasks.
    If multiple messages arrive for the same ticket within the delay window,
    only one AI generation task will fire after the last message.
    """
    def __init__(self, delay_seconds: float = 4.0):
        self.delay_seconds = delay_seconds
        self._tasks: Dict[str, asyncio.Task] = {}
        
    def schedule(self, ticket_id: str, coro_func: Callable[[], Coroutine]) -> None:
        """
        Schedule a coroutine to run after delay_seconds.
        Cancels any previously scheduled task for the same ticket_id.
        """
        if ticket_id in self._tasks:
            logger.info("Debouncing AI generation for ticket %s (canceling previous)", ticket_id)
            self._tasks[ticket_id].cancel()
            
        async def delayed_execution():
            try:
                await asyncio.sleep(self.delay_seconds)
                logger.info("Debounce timer expired for ticket %s, executing AI generation", ticket_id)
                await coro_func()
            except asyncio.CancelledError:
                # Task was cancelled because a newer message arrived
                pass
            except Exception as e:
                logger.error("Error in delayed AI execution for ticket %s: %s", ticket_id, e, exc_info=True)
            finally:
                # Remove from dict if this exact task is still the active one
                if self._tasks.get(ticket_id) == task:
                    del self._tasks[ticket_id]
                    
        task = asyncio.create_task(delayed_execution())
        self._tasks[ticket_id] = task

# Global instance to be used across webhooks
ai_debouncer = AIDebouncer(delay_seconds=4.0)
