from dataclasses import dataclass
from typing import Dict

from PyQt6.QtWidgets import QApplication
from dataclasses_json import dataclass_json
from flask import Flask, request, jsonify
from loguru import logger

from zerolan.ui.common.utils import get_center_point
from zerolan.ui.subtitle import QTSubtitle
from zerolan.ui.themes.modern import toast_theme
from zerolan.ui.toasts.base_toast import QtBaseToast
from zerolan.ui.toasts.progress_toast import QtProgressToast
from zerolan.ui.web.entities import ToastEntity, ProgressToastEntity, QtAppWrapper

flask_app = Flask(__name__)

logger_level_dict = {
    "info": logger.info,
    "warn": logger.warning,
    "error": logger.error,
}

toast_entities: Dict[str, QtAppWrapper] = dict()


def log(toast_entity: ToastEntity):
    logger_func = logger_level_dict.get(toast_entity.level, logger.info)
    logger_func(toast_entity.message)

@flask_app.route('/toast', methods=['POST'])
def show_toast():
    toast_entity: ToastEntity = ToastEntity.from_dict(request.json)  # type: ignore
    log(toast_entity)

    qt_app = QApplication([])


    toast = QtBaseToast(message=toast_entity.message,
                        duration=toast_entity.duration,
                        screen_center=get_center_point(qt_app),
                        theme=toast_theme.get(toast_entity.level, None))
    toast_entities[toast_entity.id] = QtAppWrapper(qt_app=qt_app, toast=toast)
    toast.show()
    qt_app.exec()
    qt_app.exit()

    return 'Toast shown', 200


@flask_app.route('/toast/progress', methods=['POST'])
def show_progress_toast():
    progress_toast_entity: ProgressToastEntity = ProgressToastEntity.from_dict(request.json)  # type: ignore
    log(progress_toast_entity)

    qt_app = QApplication([])
    toast = QtProgressToast(message=progress_toast_entity.message,
                            duration=progress_toast_entity.duration,
                            screen_center=get_center_point(qt_app),
                            theme=toast_theme.get(progress_toast_entity.level, None),
                            is_busy=progress_toast_entity.busy,
                            max_value=progress_toast_entity.max_value, )

    toast_entities[progress_toast_entity.id] = QtAppWrapper(qt_app=qt_app, toast=toast)
    toast.show()
    qt_app.exec()
    qt_app.exit()

    return 'Toast shown', 200


@flask_app.route('/toast/<toast_id>', methods=['PUT'])
def update_toast(toast_id):
    toast_entity = request.json

    wrapper = toast_entities.get(toast_id, None)
    if wrapper is None:
        return 'Toast not found', 404
    message = toast_entity.get('message', None)
    if message is not None:
        wrapper.toast.set_message(message=message)

    value = toast_entity.get('value', None)
    if value is not None:
        wrapper.toast.set_value(value=value)

    return 'Toast shown', 200


@flask_app.route('/toast/<toast_id>', methods=['DELETE'])
def close_toast(toast_id: str):
    wrapper = toast_entities.get(toast_id, None)
    if wrapper is None:
        return 'Toast not found', 404
    wrapper.toast.finish()
    toast_entities.pop(toast_id, None)
    return "Toast stopped", 200


@dataclass_json
@dataclass
class SubtitleEntity:
    id: str
    content: str
    duration: int


@flask_app.route('/subtitle', methods=['POST'])
def show_subtitle():
    subtitle_entity: SubtitleEntity = SubtitleEntity.from_dict(request.json)  # type: ignore
    qt_app = QApplication([])
    subtitle = QTSubtitle(content=subtitle_entity.content,
                          duration=subtitle_entity.duration,
                          screen_center=get_center_point(qt_app))
    subtitle.show()
    qt_app.exec()
    qt_app.exit()
    return "Subtitle shown", 200


@flask_app.route("/status", methods=['GET'])
def show_status():
    return jsonify({'status': 'ok'})


@flask_app.route("/stop", methods=['GET', "POST"])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('不在以 Werkzeug Server 运行')
    return jsonify({'status': 'shutdown'})


def start_ui_application():
    flask_app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    start_ui_application()
