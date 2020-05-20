import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8889)
    print('Commands of the form: *echo* message, *calendar*, *stop*')
    while True:
        message = str(input('Enter the command: ')) + '\n'
        writer.write(message.encode())
        await writer.drain()
        data = await reader.readline()
        data = data.decode()
        print(f'{data}')
        if data.startswith('stop'):
            break
    print('Close the connection')
    writer.close()


if __name__ == '__main__':
    asyncio.run(tcp_echo_client())
