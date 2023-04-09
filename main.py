from sanic import Sanic

from api import bp_api
from utils.config import config
from utils.log import run_logger

app = Sanic(__name__)
app.blueprint(bp_api)

if __name__ == "__main__":
    run_logger.info("启动服务...")
    app.run(host="0.0.0.0", port=config.port, single_process=True)
