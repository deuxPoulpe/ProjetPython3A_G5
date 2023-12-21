import multiprocessing
import time

class API:
    def __init__(self):
        self.shared_data = multiprocessing.Manager().dict()
        self.process = None

    def start(self):
        self.process = multiprocessing.Process(target=self.run)
        self.process.start()

    def run(self):
        while True:
            # Exécutez votre boucle et stockez les variables dans self.shared_data
            self.shared_data['variable1'] = 42
            self.shared_data['variable2'] = 'Bonjour'
            time.sleep(1)

    def stop(self):
        if self.process is not None:
            self.process.terminate()
            self.process.join()

class DISPLAY:
    def __init__(self, api_instance):
        self.api = api_instance

    def start(self):
        while True:
            # Récupérez les variables depuis self.api.shared_data
            variable1 = self.api.shared_data.get('variable1', None)
            variable2 = self.api.shared_data.get('variable2', None)

            if variable1 is not None:
                print(f"Variable1: {variable1}")

            if variable2 is not None:
                print(f"Variable2: {variable2}")

            time.sleep(1)

if __name__ == '__main__':
    api = API()
    display = DISPLAY(api)

    api.start()
    display.start()
