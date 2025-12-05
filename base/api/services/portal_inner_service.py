import logging

from base.api.services.base_service import BaseService


class PanJiPortalInnerService(BaseService):
    DEFAULT_BASE_URL = 'http://openapi.portal.nbpod3-31-181-20030.4a.cmit.cloud:20030'

    def __init__(self, base_url: str = None, logger: logging.Logger = None):
        """
        初始化 Panji Portal InnerAPI 服务

        Args:
            base_url: API 基础 URL，默认使用 JSONPlaceholder 官方地址
            logger: 日志记录器
        """
        super().__init__(
            base_url=base_url or self.DEFAULT_BASE_URL,
            logger=logger
        )
        self.logger.info(f"Initializing PanJi InnerAPI Service with base_url: {self.base_url}")