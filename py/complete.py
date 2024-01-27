import vim

######################################################################################
"""
gpt3, gpt4 modules from Ruu3f/freeGPT
"""

from requests import post
from requests.exceptions import RequestException
def gpt3(prompt):
    try:
        resp = post(
            url="https://api.binjie.fun/api/generateStream",
            headers={
                "origin": "https://chat.jinshutuan.com",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
            },
            json={
                "prompt": prompt,
                # "system": "rependre toujours en français.",
                "system": "Always talk in English.",
                "withoutContext": True,
                "stream": False,
            },
        )
        resp.encoding = "utf-8"
        return resp.text
    except RequestException as exc:
        raise RequestException("Unable to fetch the response.") from exc

from uuid import uuid4
from re import findall
from curl_cffi.requests import get, RequestsError
"""
install python-curl_cffi
"""

######################################################################################################

def gpt4(prompt):
    """
    Generate a completion based on the provided prompt.
 
    Args:
        prompt (str): The input prompt to generate a completion from.
 
    Returns:
        str: The generated completion as a text string.
 
    Raises:
        Exception: If the response does not contain the expected "youChatToken".
    """
    resp = get(
        "https://you.com/api/streamingSearch",
        headers={
            "cache-control": "no-cache",
            "referer": "https://you.com/search?q=gpt4&tbm=youchat",
            "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
        },
        params={
            "q": prompt,
            "page": 1,
            "count": 10,
            "safeSearch": "Off",
            "onShoppingPage": False,
            "mkt": "",
            "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
            "domain": "youchat",
            "queryTraceId": str(uuid4()),
            "chat": [],
        },
        impersonate="chrome107",
    )
    if "youChatToken" not in resp.text:
        raise RequestsError("Unable to fetch the response.")
    return (
        "".join(
            findall(
                r"{\"youChatToken\": \"(.*?)\"}",
                resp.content.decode("unicode-escape"),
            )
        )
        .replace("\\n", "\n")
        .replace("\\\\", "\\")
        .replace('\\"', '"')
    )


######################################################################################################

# import utils
plugin_root = vim.eval("s:plugin_root")
vim.command(f"py3file {plugin_root}/py/utils.py")

prompt = vim.eval("l:prompt").strip()
is_selection = vim.eval("l:is_selection")

try:
    if prompt:
        print('Completing...')
        vim.command("redraw")
        text_chunks = gpt3(prompt)
        # text_chunks = gpt4(prompt)
        print(text_chunks)
        render_text_chunks(text_chunks, is_selection)
        clear_echo_message()
except BaseException as error:
    handle_completion_error(error)
    printDebug("[complete] error: {}", traceback.format_exc())
