import asyncio
import datetime
import unittest


class Test(unittest.TestCase):
    def test_command_echo(self):
        counter = 0
        list_input = ['echo Hello, Python!', 'echo Hello, World', 'echo very very very very long line']
        list_exp = ['Hello, Python!', 'Hello, World', 'very very very very long line']
        for _ in list_exp:
            _, data = command_echo(list_input[counter])
            assert data == list_exp[counter]
            counter += 1


def command_echo(data):
    command_echo_ = False
    if data.startswith('echo'):
        data = data.replace('echo ', '')
        command_echo_ = True
    return command_echo_, data


async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected the client{addr!r}")
    while True:
        data = await reader.readline()
        # print(data.decode())
        data = data.decode()
        if not data.startswith('echo'):
            if not data.startswith('calendar'):
                if not data.startswith('stop'):
                    info = str('Commands: *echo* message - returns the sent message,'
                               ' *calendar* - returns the current time in the '
                               'format dd.mm.YYYY HH:MM, *stop* - closes the server\n')
                    writer.write(info.encode())
                    writer.write(''.encode())
                    await writer.drain()
        command_echo_, data = command_echo(data)
        if command_echo_:
            writer.write(data.encode())
            await writer.drain()
        if data.startswith('calendar'):
            writer.write((datetime.datetime.today().strftime('%d.%m.%Y %H:%M') + '\n').encode())
            await writer.drain()
        if data.startswith('stop'):
            writer.write(data.encode())
            addr = writer.get_extra_info('peername')
            print(f"Disconnected the client{addr!r}")
            writer.close()
            break


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8889)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
