import httpx
import xmltodict
import logging
from typing import Tuple


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"


async def get_exchange_rate(currency_code: str) -> Tuple[float | None, str | None]:
    try:
        logger.debug(f"Requesting exchange rate for currency: {currency_code}")

        async with httpx.AsyncClient() as client:
            response = await client.get(CBR_URL)
            response.raise_for_status()
            xml_data = response.content.decode('windows-1251')
            logger.debug(f"XML data received: {xml_data[:200]}...")
            json_data = xmltodict.parse(xml_data)
            logger.debug(f"Converted JSON data: {json_data}")

        for valute in json_data["ValCurs"]["Valute"]:
            code = valute["CharCode"]
            if code.upper() == currency_code.upper():
                nominal = int(valute["Nominal"])
                value = float(valute["Value"].replace(",", "."))
                date = response.headers.get("Date")
                logger.debug(
                    f"Found rate: {value / nominal} RUB (Nominal: {nominal}, Value: {value})")
                return round(value / nominal, 4), date

        logger.warning(
            f"Currency code {currency_code} not found in response data.")
        return None, None
    except Exception as e:
        logger.error(
            f"Error while fetching exchange rate for {currency_code}: {e}")
        return None, None
