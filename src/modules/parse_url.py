import user_agents
import logging
import uuid
from traceback import format_exc


def parseUserAgent(user_agent):
    ua = user_agent
    ua = ''.join(ua)
    ua = user_agents.parse(ua)
    temp_obj = {
        "browser": ua.browser.family,
        "browser_version": ua.browser.version_string,
        "os": ua.os.family,
        "os_version": ua.os.version_string,
        "device": ua.device.family
    }
    return temp_obj


def parse_and_join(data, user_agents):
    try:
        ua_obj = parseUserAgent(user_agents)
        event_id = uuid.uuid4().hex
        data['event_id'] = event_id
        data.update(ua_obj)
        return [data], event_id
    except Exception as e:
        logging.error(e.args[0])
        logging.error(format_exc())
