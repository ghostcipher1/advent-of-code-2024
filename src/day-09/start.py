from src.helpers.io import read_input


async def get_line():
    """
    Generates a line based on the input string.
    """
    input_data = await read_input("day-09")
    line = [
        [idx // 2] * int(digit) if idx % 2 == 0 else ["."] * int(digit)
        for idx, digit in enumerate(input_data)
    ]
    return [item for sublist in line for item in sublist if len(sublist) > 0]


async def part1():
    """
    Part 1 solution logic.
    """
    temp_line = await get_line()
    length = len(temp_line) - 1
    stop = length - sum(1 for i in temp_line if i == ".")
    dot_index = next((idx for idx, val in enumerate(temp_line) if val == "."), -1)

    while length:
        if length == stop:
            break
        if isinstance(temp_line[length], int):
            temp_line[dot_index], temp_line[length] = temp_line[length], "."
            dot_index = next((idx for idx, val in enumerate(temp_line) if val == "."), -1)
        length -= 1

    checksum = sum(i * int(val) for i, val in enumerate(temp_line) if isinstance(val, int))
    print(checksum)
    return checksum


async def part2():
    """
    Part 2 solution logic.
    """
    input_data = await read_input("day-09")
    files = [
        {"id": i // 2 if i % 2 == 0 else None, "size": int(size)}
        for i, size in enumerate(input_data)
    ]

    for i in range(len(files) - 1, 1, -1):
        if files[i]["id"] is not None:
            for j in range(i):
                left_file = files[j]
                if left_file["id"] is None:
                    right_file = files[i]
                    if left_file["size"] >= right_file["size"]:
                        files[i] = {"id": None, "size": right_file["size"]}
                        files.insert(j, right_file)
                        left_file["size"] -= right_file["size"]
                        break

    checksum = 0
    block_index = 0
    for block in files:
        if block["id"] is not None:
            for _ in range(block["size"]):
                checksum += block["id"] * block_index
                block_index += 1
        else:
            block_index += block["size"]

    print(checksum)
    return checksum


# For testing purposes
if __name__ == "__main__":
    import asyncio

    asyncio.run(part1())
    asyncio.run(part2())
