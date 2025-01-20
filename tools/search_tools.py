import json
import os
import requests

from langchain.tools import tool


class SearchTools():

    @tool("search the internet")
    def search_internet(query):
        """
        Useful to search the internet about a given topic nd return the results
        """
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'

        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if 'organic' not in response.json():
            return "sorry I couldn't find any results"

        else:
            results = response.json()['organic']
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append('\n'.join([
                        f"Title: {result['title']}", f"link: {result['link']}",
                        f"snippet: {result['snippet']}", "\n--------------"
                    ]))
                except KeyError:
                    next

            return '\n'.join(string)
