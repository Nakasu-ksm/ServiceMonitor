# 自动载入helper
import httpx


class Helper:
    def __init__(self):
        self.http = httpx.Client()

    def test_website(self, url, method: str = "GET"):
        """
        测试网站是否可以正常访问
        """
        try:
            res = self.http.request(method, url)
            if res.is_success:
                return True
            return False
        except:
            return False

    def get_result(self, url, method: str = "GET"):
        """
        获得网站返回结果
        """
        try:
            return self.http.request(method, url).content
        except:
            return None
