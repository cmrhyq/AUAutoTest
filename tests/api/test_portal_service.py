import json
import os.path
from typing import Dict

import allure
import pytest

from base.api.fixtures import api_cache
from base.api.services.portal_service import PanJiPortalService, PortalUserEntity, ClusterPlaneEntity
from core.allure.allure_helper import AllureHelper


@pytest.mark.api
@allure.feature("磐基门户服务API")
@allure.story("统一门户")
class TestPanjiPortalAPI:

    @pytest.fixture(scope="class")
    def portal_service(self, api_logger):
        """创建 Panji Portal 服务实例"""
        service = PanJiPortalService(logger=api_logger)
        yield service
        service.close()

    @allure.title("测试获取Token")
    @allure.description("验证能够成功获取Token数据")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_token(self, portal_service, api_env, api_cache, api_logger):
        with AllureHelper.step("发送 POST 请求获取Token"):
            panji_sign = PortalUserEntity(
                username=api_env.get("basic_auth_username"),
                password=api_env.get("basic_auth_password"),
                tenant_code=api_env.get("tenant_code")
            )
            sign_info = portal_service.get_token(panji_sign)

        with AllureHelper.step("验证响应数据"):
            assert isinstance(sign_info, Dict), "响应应该是字典类型"
            assert "data" in sign_info, "响应应包含Token"
            assert sign_info["code"] == 200, "响应Code应等于200"

        with AllureHelper.step("缓存Token供后续使用"):
            api_cache.set("token", sign_info["data"])
            api_logger.info(f"已经登陆并缓存Token: {sign_info['data']}")

        allure.attach(
            str(sign_info),
            name="登陆响应信息",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("测试获取一级域")
    @allure.description("验证能够成功获取一级域数据")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_first_field_info(self, portal_service, api_cache, api_logger):
        with AllureHelper.step("发送 GET 请求获取一级域"):
            first_field = portal_service.get_first_field_info()

        with AllureHelper.step("验证响应数据"):
            assert isinstance(first_field, Dict), "响应应该是字典类型"
            assert first_field["code"] == 0, "响应Code应等于0"

        with AllureHelper.step("缓存一级域id数据"):
            api_cache.set("firstFieldId", first_field["data"][0]["systemId"])
            api_logger.info(f"已缓存一级域Id: {first_field['data'][0]['systemId']}")

        allure.attach(
            str(first_field),
            name="一级域信息",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("测试获取二级域")
    @allure.description("验证能够成功获取二级域数据")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_second_field_info(self, portal_service, api_cache, api_logger):
        with AllureHelper.step("发送 GET 请求获取二级域"):
            second_field = portal_service.get_second_field_info()

        with AllureHelper.step("验证响应数据"):
            assert isinstance(second_field, Dict), "响应应该是字典类型"
            assert second_field["code"] == 0, "响应Code应等于0"

        with AllureHelper.step("缓存二级域id数据"):
            api_cache.set("secondFieldId", second_field["data"][0]["moduleId"])
            api_logger.info(f"已缓存二级域Id: {second_field['data'][0]['moduleId']}")

        allure.attach(
            str(second_field),
            name="二级域信息",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("测试新增集群平面单元")
    @allure.description("验证能够成功新增集群平面单元")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_cluster_plane(self, portal_service, api_env):
        with AllureHelper.step("发送 POST 请求新增平面集群"):
            cluster = ClusterPlaneEntity(
                prod_inst_name=api_env.get("prod_inst_name"),
            )
            cluster_info = portal_service.create_cluster_plane(cluster)

        with AllureHelper.step("验证响应数据"):
            assert isinstance(cluster_info, Dict), "响应应该是字典类型"
            assert cluster_info["code"] == 2000, "响应Code应等于200"

        allure.attach(
            str(cluster_info),
            name="新增集群的响应信息",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("测试查询集群平面单元")
    @allure.description("验证能够成功查询集群平面单元")
    @allure.severity(allure.severity_level.NORMAL)
    def test_query_cluster_plane(self, portal_service, api_env, api_cache, api_logger):
        with AllureHelper.step("发送 GET 请求查询集群平面单元"):
            cluster = ClusterPlaneEntity(
                prod_inst_name=api_env.get("prod_inst_name"),
            )
            cluster_info = portal_service.query_cluster_plane(cluster)

        with AllureHelper.step("验证响应数据"):
            assert isinstance(cluster_info, Dict), "响应应该是字典类型"
            assert cluster_info["code"] == 2000, "响应Code应等于200"

        with AllureHelper.step("缓存实例id数据"):
            api_cache.set("instanceId", cluster_info["data"]['list'][0]["instanceId"])
            api_logger.info(f"已缓存实例id: {cluster_info['data']['list'][0]['instanceId']}")

        allure.attach(
            str(cluster_info),
            name="查询集群平面响应信息",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("测试修改集群平面单元")
    @allure.description("验证能够成功修改集群平面单元")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_cluster_plane(self, portal_service, api_env, api_cache, api_logger):
        with AllureHelper.step("发送 PATCH 请求修改集群平面单元"):
            cluster = ClusterPlaneEntity(
                prod_inst_name=api_env.get("prod_inst_name"),
                instance_id=api_cache.get("instanceId")
            )
            cluster_info = portal_service.update_cluster_plane(cluster)

        with AllureHelper.step("验证响应数据"):
            assert isinstance(cluster_info, Dict), "响应应该是字典类型"
            assert cluster_info["code"] == 2000, "响应Code应等于200"

        allure.attach(
            str(cluster_info),
            name="修改后的集群平面响应信息",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.title("测试删除集群平面单元")
    @allure.description("验证能够成功删除集群平面单元")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_cluster_plane(self, portal_service, api_env, api_cache, api_logger):
        with AllureHelper.step("发送 DELETE 请求删除集群平面单元"):
            cluster = ClusterPlaneEntity(
                instance_id=api_cache.get("instanceId")
            )
            cluster_info = portal_service.delete_cluster_plane(cluster)

        with AllureHelper.step("验证响应数据"):
            assert isinstance(cluster_info, Dict), "响应应该是字典类型"
            assert cluster_info["code"] == 2000, "响应Code应等于200"

        allure.attach(
            str(cluster_info),
            name="删除集群平面响应信息",
            attachment_type=allure.attachment_type.JSON
        )