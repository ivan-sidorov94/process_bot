from aiogram.utils import executor
from bot import dp, check_process
       
if __name__ == "__main__":
    dp.loop.create_task(check_process(dp))
    executor.start_polling(dp, skip_updates=True)