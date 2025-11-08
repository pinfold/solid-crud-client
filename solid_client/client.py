import requests
from rdflib import Graph

class SolidPodClient:
    def __init__(self, pod_base_url, access_token):
        self.pod_base_url = pod_base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "text/turtle"
        }

    def _url(self, path):
        return f"{self.pod_base_url}/{path.lstrip('/')}"

    def read(self, path):
        url = self._url(path)
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            raise Exception(f"Failed to read: {r.status_code} {r.text}")

        g = Graph()
        g.parse(data=r.text, format="turtle")
        return g

    def create(self, path, turtle_data):
        url = self._url(path)
        headers = {**self.headers, "Content-Type": "text/turtle"}
        r = requests.put(url, headers=headers, data=turtle_data)
        if r.status_code not in (200, 201, 204):
            raise Exception(f"Failed to create: {r.status_code} {r.text}")
        return True

    def update(self, path, turtle_data):
        return self.create(path, turtle_data)

    def delete(self, path):
        url = self._url(path)
        r = requests.delete(url, headers=self.headers)
        if r.status_code not in (200, 204):
            raise Exception(f"Failed to delete: {r.status_code} {r.text}")
        return True
