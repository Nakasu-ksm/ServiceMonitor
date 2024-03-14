# 自动载入helper
import httpx


class Helper:
    def __init__(self):
        self.http = httpx.Client()

    def test_website(self, url):
        res = self.http.request("GET", url)
        if res.is_success:
            return True
        return False