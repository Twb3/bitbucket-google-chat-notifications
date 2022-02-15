import requests
from gchat import Api as gchatApi
from gchat import MessageCreator
import logging


logger = logging.getLogger("bbgc")


def handle_event(data: dict, request_args) -> dict:
    event_key = data["eventKey"]
    actor = data["actor"]["displayName"] + " (" + data["actor"]["emailAddress"] + ")"

    message = str()

    if event_key.startswith("pr:"):
        repo_name = data["pullRequest"]["toRef"]["repository"]["name"]
        pr_id = data["pullRequest"]["id"]
        pr_title = data["pullRequest"]["title"]
        pull_request_url = data["pullRequest"]["links"]["self"][0]["href"]

        logger.info("Handling %s for %s", event_key, repo_name)

        message_creator = MessageCreator()
        message_creator.add_text_paragraph_widget(
            "<b>" + repo_name + "</b>\n" + actor + " " + __translate_event_key(event_key)
        )

        if event_key.startswith("repo:comment:"):
            message_creator.add_text_paragraph_widget(
                "<b>Comment:</b> " + data["comment"]["text"]
            )

        message_creator.add_text_button_widget(
            button_text="#" + str(pr_id) + ": " + pr_title, button_url=pull_request_url)
        message = message_creator.create_message()

    if event_key.startswith("repo:"):
        repo_name = data["repository"]["name"]

        logger.info("Handling %s for %s", event_key, repo_name)

        message_creator = MessageCreator()
        message_creator.add_text_paragraph_widget(
            "<b>" + repo_name + "</b>\n" + actor + " " + __translate_event_key(event_key)
        )

        if event_key == "repo:refs_changed":
            message_creator.add_text_paragraph_widget(
                "<b>" + data["changes"][0]["ref"]["type"] + "</b>: " + data["changes"][0]["ref"]["displayId"] +
                " (" + data["changes"][0]["type"].lower() + ")"
            )

        if event_key.startswith("pr:comment:"):
            message_creator.add_text_paragraph_widget(
                "<b>Comment:</b> " + data["comment"]["text"]
            )

        message = message_creator.create_message()

    api = gchatApi(
        request_args.get('space'),
        request_args.get('key'),
        request_args.get('token'))
    return __handle_gchat_response(
        api.send_message(message), event_key
    )


def __handle_gchat_response(gchat_response: requests.models.Response, event_key: str) -> dict:
    if gchat_response.status_code == 200:
        return {
            "status": "ok",
            "eventKey": event_key
        }
    else:
        logger.error(
            "Failed to post message to google chat: %s",
            gchat_response.text)
        return {
            "status": "error",
            "message": "failed to post message to google chat",
            "eventKey": event_key
        }


def __translate_event_key(event_key: str) -> str:
    if event_key == "repo:refs_changed":
        return "pushed a commit(s)"
    if event_key == "repo:modified":
        return "updated a repo name"
    if event_key == "repo:fork":
        return "forked a repo"
    if event_key == "repo:comment:added":
        return "commented on a commit"
    if event_key == "repo:comment:edited":
        return "edited a comment on a commit"
    if event_key == "repo:comment:deleted":
        return "deleted a comment on a commit"
    if event_key == "mirror:repo_synchronized":
        return "Mirror finished synchronizing"
    if event_key == "pr:opened":
        return "opened a new pull request"
    if event_key == "pr:from_ref_updated":
        return "updated the source branch on a pull request"
    if event_key == "pr:modified":
        return "modified a pull request"
    if event_key == "pr:reviewer:updated":
        return "added reviewers to a pull request"
    if event_key == "pr:reviewer:approved":
        return "approved a pull request"
    if event_key == "pr:reviewer:unapproved":
        return "unapproved a pull request"
    if event_key == "pr:reviewer:needs_work":
        return "marked a pull requests as needs work"
    if event_key == "pr:merged":
        return "merged a pull request"
    if event_key == "pr:declined":
        return "declined a pull request"
    if event_key == "pr:deleted":
        return "deleted a pull request"
    if event_key == "pr:comment:added":
        return "added a comment to a pull request"
    if event_key == "pr:comment:edited":
        return "edited a comment on a pull request"
    if event_key == "pr:comment:deleted":
        return "deleted a comment on a pull request"
