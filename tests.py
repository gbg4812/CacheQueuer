import contextlib
import io

outputstr = io.StringIO()

with contextlib.redirect_stdout(outputstr):
    print("hello world")

print("the output string value: " + outputstr.getvalue())