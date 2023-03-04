import matplotlib.pyplot as plt


def set_pie_chart(telegram_id):
    pass


def get_pie_chart(telegram_id):

    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')

    photo_path = f'static//{telegram_id}.png'
    plt.savefig(photo_path)

    return photo_path
