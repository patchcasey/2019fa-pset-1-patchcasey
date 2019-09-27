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
    # #TODO - check if exists, file of that name
    # folder = os.listdir(os.path.dirname(file))
    # temp_name = next(tempfile._get_candidate_names())
    # print(tf.name)
    # if os.path.exists(tf.name):
    #     print('exists')


    tf = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file), suffix=suffix_parser(file))


    if as_file == True:
        try:
            yield tf
            tf.seek(0)
            tf.flush()
            os.fsync(tf.fileno())
            tf.close()
            shutil.copy(tf.name, file)
            os.remove(tf.name)
        except:
            yield tf
            tf.close()
            os.remove(tf.name)
            print('error')
    else:
        yield tf
        tempfile_name = tf.name
        tf.close()
        os.remove(tf.name)
        return tempfile_name

@contextmanager
def test():
    cwd = os.getcwd()
    fp = os.path.join(os.getcwd(), "abcd.txt")
    with atomic_write(fp,"w") as f:
        f.write(b"world!")

if __name__ == '__main__':
    test()