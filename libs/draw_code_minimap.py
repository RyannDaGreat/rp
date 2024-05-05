import sys


def draw_minimap(hscale: int, vscale: float, padding: int, code:str):
    assert hscale >= 0, hscale
    assert vscale >= 0, vscale
    assert padding >= 0, padding

    # We won't handle auto-importing this, as neither does black need to be...
    # pip_import("drawille", auto_yes=True)

    import drawille

    # Prevent Giant Outputs
    MIN_WIDTH = padding
    MAX_WIDTH = 1000
    MIN_HEIGHT = 1
    MAX_HEIGHT = 100000

    # Handle tabs as 4 spaces
    code = code.replace("\t", "    ")

    # Vertical Scaling
    lines = code.splitlines()
    num_lines = len(lines)
    num_lines = max(MIN_HEIGHT, round(num_lines * vscale))
    num_lines = min(num_lines, MAX_HEIGHT)
    lines = resize_list(lines, num_lines)

    # Horizontal Scaling
    if isinstance(hscale, int):
        lines = [line * hscale for line in lines]
    else:
        assert isinstance(hscale, float)
        lines = [line[: int(MAX_WIDTH / hscale) + 1] for line in lines]
        lines = [resize_list(line, round(len(line) * hscale)) for line in lines]
        lines = ["".join(line) for line in lines]
    lines = [line[:MAX_WIDTH] for line in lines]

    HEIGHT = len(lines)
    WIDTH = max(map(len, lines))
    WIDTH = max(MIN_WIDTH, WIDTH)

    canvas = drawille.Canvas()

    # Set the size
    canvas.set(0, 0)
    canvas.set(WIDTH - 1, HEIGHT - 1)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != " ":
                canvas.set(x, y)

    output = canvas.frame()
    output = output.splitlines()
    output = [x.ljust(MAX_WIDTH) for x in output]
    output = '\n'.join(output)

    print(output)
    # print(make_string_rectangular(output).replace(" ", fansi("·", "green")))


# INLINED FROM RP FOR FAST LOADING:


def resize_list(array: list, length: int):
    """
    This function stretches or compresses a list to a given length using nearest-neighbor interpolation.
    The last element of the input list is always included in the output list, regardless of the target length.

    Parameters:
        array (list): The input list to resize.
        length (int): The target length of the list.

    Assumptions:
        The function assumes that the target length is a non-negative integer.

    Returns:
        list: The resized list to the target length.

    Examples:
        >>> resize_list([0,1,2,3,4], 5)
        [0, 1, 2, 3, 4]
        # The target length is the length of the input array. No change.

        >>> resize_list([0,1,2,3,4,5,6,7,8,9], 5)
        [0, 2, 4, 6, 9]
        # Elements are skipped when resizing to a shorter length, but the last element is always included.

        >>> resize_list([1,2,3,4,5,6,7,8,9], 3)
        [1, 5, 9]

        >>> resize_list([1,2,3,4,5,6,7,8,9], 5)
        [1, 3, 5, 7, 9]

        >>> resize_list([0,1,2,3,4], 10)
        [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        # Elements are duplicated during resizing to a longer length.

        >>> resize_list([0,1,2,3,4], 1)
        [4]
        # Even when resizing to length 1, the last element is included.

        >>> resize_list(range(3000000000000000),4)
        [0, 1000000000000000, 1999999999999999, 2999999999999999]
        # Pro-tip: this ran in .00001 seconds! You can use it to get indices by passing in a range object

    """

    assert isinstance(
        length, int
    ), "Length must be an integer, but got %s instead" % repr(type(length))
    assert length >= 0, (
        "Length must be a non-negative integer, but got %i instead" % length
    )

    if len(array) > 1 and length > 1:
        step = (len(array) - 1) / (length - 1)
    else:
        step = 0  # default step size to 0 if array has only 1 element or target length is 1

    return [array[round(i * step)] for i in range(length)]


def text_file_to_string(file_path: str) -> str:
    "text_file_to_string(file_path) reads text file"

    try:
        return open(file_path).read()
    except UnicodeDecodeError:
        # UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 4781: ordinal not in range(128)
        return open(file_path, encoding="latin").read()


def usage():
    print("Usage: %s <hscale> <vscale> <padding> [file]" % sys.argv[0], file=sys.stderr)


def main():
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)

    hscale = float(sys.argv[1])
    vscale = float(sys.argv[2])
    padding = int(sys.argv[3])

    try:
        file = sys.argv[4]
        code = open(file).read()
    except Exception:
        code = sys.stdin.read()

    draw_minimap(hscale, vscale, padding, code)


if __name__ == "__main__":
    main()
