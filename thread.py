import  threading, progressbar, random
class ThreadPool:
    def __init__(self, threadCount):
        self.__lock = lock = threading.Lock()
        self.__threadCount = threadCount

    def work(self, tasks, show):
        count = 0
        for task in tasks:
            self.__work(*task)
            count  = count + 1
            if show[count] == 0:
                with self.__lock:
                    self.__total = self.__total + count
                    self.__bar.update(self.__total + 1)
    def Start(self, work, tasks):
        length = len(tasks)
        self.__bar = progressbar.ProgressBar(maxval=length)
        show = [random.randint(0, 100) for i in range(length)]
        self.__threads = []
        self.__total = 0
        self.__work = work
        for threadId in range(self.__threadCount):
            data = [tasks[i] for i in range(length) if i % self.__threadCount == threadId]
            thread = threading.Thread(target=self.work, args=(data, show, ))
            self.__threads.append(thread)
            thread.start()
    def Join(self):
        for thread in self.__threads:
            thread.join()
        self.__bar.finish()