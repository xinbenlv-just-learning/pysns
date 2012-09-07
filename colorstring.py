# Simple color print for python
def colorstring(msg, fg = "clear", bg = "clear", bold = False):
    header = "\033["
    if bold == True:
        header += "1;" 
    colored_msg = msg
    if fg == "gray":
            colored_msg = header + "30m" + colored_msg
    elif fg == "red":
            colored_msg = header + "31m" + colored_msg
    elif fg == "green":
            colored_msg = header + "32m" + colored_msg
    elif fg == "yellow":
            colored_msg = header + "33m" + colored_msg
    elif fg == "blue":
            colored_msg = header + "34m" + colored_msg
    elif fg == "magenta":
            colored_msg = header + "35m" + colored_msg
    elif fg == "cyan":
            colored_msg = header + "36m" + colored_msg
    elif fg == "white":
            colored_msg = header + "37m" + colored_msg
    elif fg == "crimson":
            colored_msg = header + "38m" + colored_msg

    if bg == "gray":
            colored_msg = header + "40m" + colored_msg
    elif bg == "red":
            colored_msg = header + "41m" + colored_msg
    elif bg == "green":
            colored_msg = header + "42m" + colored_msg
    elif bg == "yellow":
            colored_msg = header + "43m" + colored_msg
    elif bg == "blue":
            colored_msg = header + "44m" + colored_msg
    elif bg == "magenta":
            colored_msg = header + "45m" + colored_msg
    elif bg == "cyan":
            colored_msg = header + "46m" + colored_msg
    elif bg == "white":
            colored_msg = header + "47m" + colored_msg
    elif bg == "crimson":
            colored_msg = header + "48m" + colored_msg

    colored_msg = colored_msg + "\033[m"
    return colored_msg


# Examples
# print '\033[1;30mGray like Ghost\033[1;m'
# print '\033[1;31mRed like Radish\033[1;m'
# print '\033[1;32mGreen like Grass\033[1;m'
# print '\033[1;33mYellow like Yolk\033[1;m'
# print '\033[1;34mBlue like Blood\033[1;m'
# print '\033[1;35mMagenta like Mimosa\033[1;m'
# print '\033[1;36mCyan like Caribbean\033[1;m'
# print '\033[1;37mWhite like Whipped Cream\033[1;m'
# print '\033[1;38mCrimson like Chianti\033[1;m'
# print '\033[1;41mHighlighted Red like Radish\033[1;m'
# print '\033[1;42mHighlighted Green like Grass\033[1;m'
# print '\033[1;43mHighlighted Brown like Bear\033[1;m'
# print '\033[1;44mHighlighted Blue like Blood\033[1;m'
# print '\033[1;45mHighlighted Magenta like Mimosa\033[1;m'
# print '\033[1;46mHighlighted Cyan like Caribbean\033[1;m'
# print '\033[1;47mHighlighted Gray like Ghost\033[1;m'
# print '\033[1;48mHighlighted Crimson like Chianti\033[1;m'

