from typing import Any

import requests
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="the location need to check the weather")


class Weather(BaseTool):
    name = "weather"
    description = "Use for searching weather at a specific location"

    def __init__(self):
        super().__init__()

    def _run(self, location: str) -> dict[str, Any]:
        api_key = "SveZC8LEGmz5AARk4"
        url = f"https://api.seniverse.com/v3/weather/now.json?key={api_key}&location={location}&language=zh-Hans&unit=c"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                "temperature": data["results"][0]["now"]["temperature"],
                "description": data["results"][0]["now"]["text"],
            }
            return weather
        else:
            raise Exception(
                f"Failed to retrieve weather: {response.status_code}")

if __name__ == "__main__":
    weather_tool = Weather()
    weather_info = weather_tool.run("沈阳")
    print(weather_info)