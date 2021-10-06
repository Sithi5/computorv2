from tkinter import *
from src.expression_resolver import ExpressionResolver


# Creating frame for calculator
def iCalc(source, side):
    storeObj = Frame(source, borderwidth=4, bd=4, bg="#c94d00")
    storeObj.pack(side=side, expand=YES, fill=BOTH)
    return storeObj


# Creating Button
def button(source, side, text, command=None):
    storeObj = Button(source, text=text, command=command)
    storeObj.pack(side=side, expand=YES, fill=BOTH)
    return storeObj


class Application(Frame):
    def __init__(self, resolver: ExpressionResolver, master=None):
        self._resolver = resolver
        Frame.__init__(self)
        self.option_add("*Font", "arial 20 bold")
        self.pack(expand=YES, fill=BOTH)
        self.master.title("Calculator")  # type: ignore
        display = StringVar()
        Entry(self, relief=RIDGE, textvariable=display, justify="right", bd=30, bg="#c94d00").pack(
            side=TOP, expand=YES, fill=BOTH
        )

        for clearButton in ["C"]:
            erase = iCalc(self, TOP)
            for char in clearButton:
                button(erase, LEFT, char, lambda storeObj=display, q=char: storeObj.set(""))

        # Add fn(x) and = and ? buttons
        special_button = iCalc(self, TOP)
        button(
            special_button,
            LEFT,
            "f(x)",
            lambda storeObj=display, q="f(x)": storeObj.set(storeObj.get() + q),
        )
        button(
            special_button,
            LEFT,
            "=",
            lambda storeObj=display, q="=": storeObj.set(storeObj.get() + q),
        )
        button(
            special_button,
            LEFT,
            "?",
            lambda storeObj=display, q="?": storeObj.set(storeObj.get() + q),
        )
        for numButton in ("iX()^%", "789/", "456*", "123-", "0.+"):
            FunctionNum = iCalc(self, TOP)
            for char in numButton:
                button(
                    FunctionNum,
                    LEFT,
                    char,
                    lambda storeObj=display, q=char: storeObj.set(storeObj.get() + q),
                )

        EqualButton = iCalc(self, TOP)
        result_string = "Compute"
        btniEquals = button(EqualButton, LEFT, result_string)
        btniEquals.bind(
            "<ButtonRelease-1>", lambda e, s=self, storeObj=display: s.calc(storeObj), "+"
        )

    def calc(self, display):
        try:
            display.set(self._resolver.solve(display.get()))
        except:
            display.set("ERROR")


def main(argv=None):
    resolver = ExpressionResolver(
        verbose=False,
        force_calculator_verbose=False,
        output_graph=False,
    )
    root = Tk()
    app = Application(master=root, resolver=resolver)
    app.mainloop()


if __name__ == "__main__":
    main()
