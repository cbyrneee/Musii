import click
import requests
from urllib.parse import urljoin

session = requests.Session()


def load_proxies():
    try:
        proxies_file = open("proxies.txt", "r")
        proxies_text = proxies_file.read().split()

        session.proxies = {}
        for proxy in proxies_text:
            session.proxies = {"http": proxy, "https": proxy}

        if session.proxies == {}:
            print("[!] Proxies file was empty, not using proxy.")
            return False

        return True
    except Exception as e:
        print("[!] Failed to read proxies.txt file, not using proxy.")
        return False


def perform_deezer_search(query, type="", noproxy=False):
    url = f"https://api.deezer.com/search/{type}"
    params = {"q": query}

    if noproxy or session.proxies == {}:
        response = requests.get(url, params=params)
    else:
        response = session.get(url, params=params)

    if response.status_code != 200:
        return None

    json = response.json()
    if json == None:
        return None

    data = json["data"]
    total = json["total"]

    if total == 0:
        return None

    if data == None:
        return None

    return data


@click.command()
@click.option("--count", default=1, help="Number of results to display")
@click.option("--type", default="", help="Method to use when searching (track, artist, album, etc)")
@click.option("--noproxy", is_flag=True, help="Use direct connection without proxy")
@click.argument("query", nargs=-1, required=True)
def main(count, type, noproxy, query):
    proxies_loaded = False
    if noproxy == False:
        proxies_loaded = load_proxies()

    string_query = ' '.join(query)

    print(
        f"[i] Searching for '{string_query}'{type == '' and ' ' or f' with type {type} '}and showing {count} result{count > 1 and 's' or ''}. {((not proxies_loaded) or noproxy) and '(not using proxy)' or '(using proxy)'}")

    results = perform_deezer_search(string_query, type, noproxy)
    if results == None:
        return print("[!] No results found")

    for result in results[:count]:
        print(
            f"[*] Result {results.index(result) + 1}: {result['title']} by {result['artist']['name']}: {result['link']}")


if __name__ == "__main__":
    main()
