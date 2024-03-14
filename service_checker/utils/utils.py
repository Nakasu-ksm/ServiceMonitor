from service_checker import Checker


class Core():
    @staticmethod
    def get_status():
        check = Checker()
        return check._get_data()
