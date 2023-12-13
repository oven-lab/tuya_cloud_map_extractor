DOMAIN = "tuya_cloud_map_extractor"
PLATFORMS = ["camera"]

CONTENT_TYPE = "image/png"
DEFAULT_NAME = "Tuya Cloud Map Extractor"

CONF_SERVER = "server"
CONF_SERVER_CHINA = "https://openapi.tuyacn.com"
CONF_SERVER_WEST_AMERICA = "https://openapi.tuyaus.com"
CONF_SERVER_EAST_AMERICA = "https://openapi-ueaz.tuyaus.com"
CONF_SERVER_CENTRAL_EUROPE = "https://openapi.tuyaeu.com"
CONF_SERVER_WEST_EUROPE = "https://openapi-weaz.tuyaeu.com"
CONF_SERVER_INDIA = "https://openapi.tuyain.com"

CONF_COLORS = "color_conf"
CONF_BG_COLOR = "bg_color"
CONF_INSIDE_COLOR = "inside_color"
CONF_WALL_COLOR = "wall_color"
CONF_ROOM_COLORS = "room_colors"
CONF_ROOM_COLOR = "room_color_"
CONF_ROOM_NAME = "room_name_"

CONF_PATH = "path_enabled"
CONF_PATH_COLOR = "path_color"
CONF_LAST = "last"
CONF_ROTATE = "rotate"
CONF_FLIP_VERTICAL = "flip_vertical"
CONF_FLIP_HORIZONTAL = "flip_horizontal"

CONF_ROTATE_0 = 0
CONF_ROTATE__90 = -90
CONF_ROTATE_90 = 90
CONF_ROTATE_180 = 180

CONF_ROTATES = {
    CONF_ROTATE__90: "-90",
    CONF_ROTATE_0: "0",
    CONF_ROTATE_90: "90",
    CONF_ROTATE_180: "180"
}

DEFAULT_BG_COLOR = [44, 50, 64]
DEFAULT_WALL_COLOR = [255, 255, 255]
DEFAULT_ROOM_COLOR = [94, 93, 109]
DEFAULT_PATH_COLOR = [0, 255, 0]
