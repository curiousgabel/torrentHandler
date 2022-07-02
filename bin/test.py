"""import magic

print("starting test")
print(magic.from_file("C:\\Users\\Mike\\Documents\\Furnace Rebate Confirmation.pdf"))
print("finished test")
"""


class FuncDecorator(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        print('Called {func} with args: {args}'.format(func=self.func.__name__,
                                                       args=args))
        new_args = list(args)
        new_args[0] += 1

        return self.func(*new_args)


@FuncDecorator
def test_func(x, y):
    return x, y


def ClassDecorator(sourceClass):
    class Wrapper:
        def __init__(self, *args):
            self.sourceClass = sourceClass(*args)

        def __getattr__(self, item):
            return getattr(self.sourceClass, item)

        def echo(self):
            print('decorator first', end=' ')
            self.sourceClass.echo()

    return Wrapper


@ClassDecorator
class DecoratedTest:
    prop = None

    def __init__(self, default_prop):
        self.prop = default_prop

    def echo(self):
        print(self.prop)

    def plainecho(self):
        print(self.prop)

if __name__ == '__main__':
    test = DecoratedTest("plain string")
    print("calling plain echo")
    test.plainecho()
    print("calling decorated echo")
    test.echo()
    print("calling prop directly")
    print(test.prop)

