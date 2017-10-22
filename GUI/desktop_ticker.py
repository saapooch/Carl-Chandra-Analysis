from data_pull import RealTimeDataSession, HistoricDataSession
import tkinter as tk
import random

#FIXME

class Window(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.ticker = tk.Text(height=1, wrap= "none")
        self.ticker.pack(side="top", fill="x")

        self.ticker.tag_configure("up", foreground="green")
        self.ticker.tag_configure("down", foreground="red")
        self.ticker.tag_configure("even", foreground="black")
        r = RealTimeDataSession(portfolio = 'TVIX', sampling = 1, islive = True, max_time = 5,)
        text = r.pull_text()
        self.price = r.price_inquiry(text)
        self.data = r.portfolio
        self.after_idle(self.tick)

    def tick(self):
        # symbol = self.data.pop(0)
        # self.data.append(symbol)

        opening_price = 0
        if self.price[7] > opening_price:
            tag = 'up'
        elif self.price[7] < opening_price:
            tag = 'down'
        else:
            tag = 'even'
        # tag = {-1: "down", 0: "even", 1: "up"}[n]

        self.ticker.configure(state="normal")
        self.ticker.insert("end", " %s %s" % (self.data, self.price[7]), tag)
        self.ticker.see("end")
        self.ticker.configure(state="disabled")
        self.after(1000, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
