import asyncio

from zerolan.ui.api.toasts import ProgressToast


async def main():
    with ProgressToast(message="Testing...", busy=False) as bar:
        for i in range(5):
            await asyncio.sleep(1)
            bar.set_message(message=f"{i + 1}", cur_value=i + 1)
        bar.set_message(message="Finished")
    await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
