from blocks.base import *

def main():
    print('Program 1')
    Program(
        ForLoop('i', range(10), [
            Print(Literal('i is: ')),
            Print(Get('i')),
            Print(Literal('\n'))
        ])
    ).run()

    print('Program 2')
    Program([
        Print(Math('+', [Literal(2), Literal(3)])),
        Print(Literal('\n'))
    ]).run()

    print('Program 3')
    Program([
        Set('i', Literal(0)),
        Print(Literal('i is: ')),
        Print(Get('i')),
        Print(Literal('\n')),
        Set('i', Math('+', [Get('i'), Literal(1)])),
        Print(Literal('i is: ')),
        Print(Get('i')),
        Print(Literal('\n'))
    ]).run()

    print('Program 4')
    Program([
        Function('test', 'n', [
            Set('n', Math('+', [Get('n'), Literal(10)])),
            Return(Get('n'))
        ]),
        Print(Call('test', 3)),
        Print(Literal('\n'))
    ]).run()

    print('Program5')
    Program([
        Set('n', Literal(0)),
        WhileLoop(Compare('<', Get('n'), Literal(10)), [
            Print(Get('n')),
            Print(Literal('\n')),
            Set('n', Math('+', [Get('n'), Literal(2)]))
        ])
    ]).run()

if (__name__ == '__main__'):
    main()
