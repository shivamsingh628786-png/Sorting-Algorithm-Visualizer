
import tkinter as tk
from tkinter import ttk
import random

root = tk.Tk()
root.title("Sorting Algorithm Visualizer")
root.geometry("900x650")

data = []
sorting = False

def draw_data(colors):
    canvas.delete("all")

    if not data:
        return

    bar_width = 800 / len(data)

    for i, value in enumerate(data):
        x1 = i * bar_width + 10
        y1 = 350 - value * 3
        x2 = (i + 1) * bar_width + 5

        canvas.create_rectangle(
            x1, y1, x2, 350,
            fill=colors[i]
        )

        canvas.create_text(
            (x1 + x2) / 2,
            y1 - 10,
            text=str(value),
            fill="black",
            font=("Arial", 9, "bold")
        )

def generate():
    global data

    if sorting:
        return

    data = [random.randint(10, 100) for _ in range(25)]
    draw_data(["blue"] * len(data))

    numbers_label.config(
        text="Generated Numbers: " +
        ", ".join(map(str, data))
    )
    status.config(text="Array Generated")

def visualize():
    colors = ["blue"] * len(data)
    draw_data(colors)

    root.update()
    yield

def bubble_sort():
    n = len(data)

    for i in range(n):
        for j in range(n - i - 1):
            colors = ["blue"] * n
            colors[j] = "red"
            colors[j + 1] = "yellow"
            draw_data(colors)
            yield

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_data(colors)
                yield

def selection_sort():
    n = len(data)

    for i in range(n):
        minimum = i

        for j in range(i + 1, n):
            colors = ["blue"] * n
            colors[minimum] = "red"
            colors[j] = "yellow"
            draw_data(colors)
            yield

            if data[j] < data[minimum]:
                minimum = j

        data[i], data[minimum] = data[minimum], data[i]
        yield

def insertion_sort():
    n = len(data)

    for i in range(1, n):
        key = data[i]
        j = i - 1

        while j >= 0:
            colors = ["blue"] * n
            colors[j] = "red"
            colors[j + 1] = "yellow"
            draw_data(colors)
            yield

            if data[j] <= key:
                break

            data[j + 1] = data[j]
            j -= 1
            yield

        data[j + 1] = key
        yield

def merge_sort():
    def merge(left, right):
        if right - left <= 1:
            return

        mid = (left + right) // 2

        yield from merge(left, mid)
        yield from merge(mid, right)

        a = data[left:mid]
        b = data[mid:right]

        i = j = 0
        k = left

        while i < len(a) and j < len(b):
            colors = ["blue"] * len(data)
            colors[k] = "yellow"
            draw_data(colors)
            yield

            if a[i] <= b[j]:
                data[k] = a[i]
                i += 1
            else:
                data[k] = b[j]
                j += 1

            k += 1
            yield

        while i < len(a):
            data[k] = a[i]
            i += 1
            k += 1
            yield

        while j < len(b):
            data[k] = b[j]
            j += 1
            k += 1
            yield

    yield from merge(0, len(data))

def quick_sort():
    def quick(low, high):
        if low >= high:
            return

        pivot = data[high]
        i = low - 1

        for j in range(low, high):
            colors = ["blue"] * len(data)
            colors[j] = "yellow"
            colors[high] = "red"
            draw_data(colors)
            yield

            if data[j] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                yield

        data[i + 1], data[high] = data[high], data[i + 1]
        p = i + 1
        yield

        yield from quick(low, p - 1)
        yield from quick(p + 1, high)

    yield from quick(0, len(data) - 1)

def start():
    global sorting

    if sorting or not data:
        return

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    sorting = True
    status.config(text="Sorting...")
    steps = algorithms[algorithm.get()]()

    def next_step():
        global sorting

        try:
            next(steps)
            root.after(speed.get(), next_step)
        except StopIteration:
            draw_data(["green"] * len(data))
            numbers_label.config(
        text="Sorted Numbers: " +
        ", ".join(map(str, data))
    )

            status.config(text="Sorting Completed!")
            sorting = False

    next_step()

tk.Label(
    root,
    text="Sorting Algorithm Visualizer",
    font=("Arial", 20, "bold")
).pack(pady=15)

frame = tk.Frame(root)
frame.pack(pady=10)

algorithm = ttk.Combobox(
    frame,
    values=[
        "Bubble Sort",
        "Selection Sort",
        "Insertion Sort",
        "Merge Sort",
        "Quick Sort"
    ],
    state="readonly"
)
algorithm.set("Bubble Sort")
algorithm.grid(row=0, column=0, padx=10)

tk.Button(
    frame,
    text="Generate Array",
    command=generate
).grid(row=0, column=1, padx=10)

tk.Button(
    frame,
    text="Start Sorting",
    command=start
).grid(row=0, column=2, padx=10)

speed = tk.Scale(
    root,
    from_=10,
    to=500,
    orient="horizontal",
    label="Speed Delay (ms)"
)
speed.set(50)
speed.pack()

canvas = tk.Canvas(
    root,
    width=820,
    height=370,
    bg="white"
)
canvas.pack(pady=10)

status = tk.Label(
    root,
    text="Ready",
    font=("Arial", 12)
)
status.pack()
numbers_label = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    wraplength=800
)
numbers_label.pack(pady=5)

generate()
root.mainloop()
