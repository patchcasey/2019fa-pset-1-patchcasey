from contextlib import contextmanager
import tempfile
import os
import shutil

def suffix_parser(input):
    parts = []
    parts = input.split('.')
    return '.'+parts[1]

@contextmanager
def atomic_write(file, mode="w", as_file=True, *args, **kwargs):
    """Write a file atomically

    :param file: str or :class:`os.PathLike` target to write

    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string

    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """
    tf = tempfile.NamedTemporaryFile(delete=False, dir=os.getcwd(), suffix=suffix_parser(file))
    print(args)
    try:
        for x in args:
            tf.write(x.encode())
    except:
        tf.close()
        os.remove(tf.name)
    finally:
        tf.seek(0)
        print(tf.read())
        tf.flush()
        os.fsync(tf.fileno())
        tf.close()
    shutil.copy(tf.name, file)
    os.remove(tf.name)

    # if isinstance(file, str):
    #     yield tempfile.mkstemp(dir=os.getcwd())
    #         # print(filename)
    #     # yield open(file, "w+")
    #
    # elif isinstance(file, os.PathLike):
    #     decoded_file = os.fsdecode(file)
    #     #todo - all of the isinstance(file, str)...
    #
    # else:
    #     #TODO - raise warning here?
    #     print('Incompatible datatype')
    #     exit()

    # f = open("hello.txt","w+")
    # f.write("world!")
    # f.close()
    #
    # ffile = open("hello.txt", "r")
    # print(ffile.read())

@contextmanager
def test():
    with tempfile.TemporaryDirectory() as tmp:
        fp = os.path.join(tmp, "asdf.txt")

    with atomic_write(fp,"w") as f:
        f.write("world!")

if __name__ == '__main__':
    test()
    # atomic_write('test.txt','teststring')