import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from uuid import uuid4

from aiogram import Router
from aiogram.types import CallbackQuery, BufferedInputFile
from matplotlib import pyplot as plt
from tabulate import tabulate

from database import get_activity_statistic
from filters.base_filters import UserExistsFilter
from lang.lang_based_provider import Lang, format_string, get_message
from lang_based_variable import ActivityStatistic, MessageKey

router = Router(name="user_activity_router")


@router.callback_query(ActivityStatistic.filter(), UserExistsFilter())
async def process_statistic(query: CallbackQuery, lang: Lang) -> None:
    statistic = list(await get_activity_statistic())
    img = await generate_plot_async(statistic)
    text_table = generate_text_table(list(reversed(statistic)))
    img_file = BufferedInputFile(file=img.read(), filename=f"{uuid4()}.png")
    await query.message.answer_photo(photo=img_file,
                                     caption=format_string(
                                         get_message(MessageKey.USER_ACTIVITY_STATISTIC, lang),
                                         min_date=str(statistic[-1][0]),
                                         max_date=str(statistic[0][0]),
                                         text_table=text_table)
                                     )


def generate_plot(data) -> BytesIO:
    # Unpack the data into two separate lists
    dates, counts = zip(*data)

    # Extract the first and last dates for title
    low_date = dates[0]
    max_date = dates[-1]

    # Create a new figure
    plt.figure(figsize=(10, 6))
    plt.bar(dates, counts, color='skyblue')

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('User Count')
    plt.title(f'User Activity ({low_date}, {max_date})')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot to a BytesIO object
    image_bytes = BytesIO()
    plt.savefig(image_bytes, format='png')
    image_bytes.seek(0)  # Rewind the BytesIO object to the beginning

    # Close the figure to release memory
    plt.close()

    return image_bytes


async def generate_plot_async(data) -> BytesIO:
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        image_data = await loop.run_in_executor(pool, generate_plot, data)
    return image_data


def generate_text_table(data) -> str:
    return tabulate(data[:7], headers=['date', 'user count'], tablefmt='grid')
